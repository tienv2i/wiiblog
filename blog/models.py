from datetime import datetime
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.models import Page
from wagtailmetadata.models import MetadataPageMixin
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField, RichTextField
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from modelcluster.tags import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtailmarkdown.fields import MarkdownField
from wagtailmarkdown.blocks import MarkdownBlock
from wagtail.search import index
from wagtail.snippets.models import register_snippet

# Create your models here.
class BlogIndexPage(RoutablePageMixin, Page):
    intro = MarkdownField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(BlogIndexPage, self).get_context(request, *args, **kwargs)
        all_posts = self.get_posts()
        paginator = Paginator(all_posts, 10)  # Hiển thị 2 bài viết mỗi trang
        page = request.GET.get('page')
        try:
            posts = paginator.get_page(page)
        except PageNotAnInteger:
            posts = paginator.get_page(1)
        except EmptyPage:
            posts = paginator.get_page(paginator.num_pages)
        context['blog_page'] = self
        context['posts'] = posts
        return context
    
    def get_posts(self):
        return BlogPostPage.objects.descendant_of(self).live().order_by('-post_date')
    
    @route(r'^tag/(?P<tag>[-\w]+)$')
    def post_by_tag(self, request, tag, *arg, **kwargs):
        self.page_type = "tag"
        self.posts = self.get_posts().filter(tag__slug = tag)
        return self.render(request)

    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return self.render(request)
    


class BlogPostPage(MetadataPageMixin, Page):
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_date = models.DateTimeField(default = datetime.now())
    tags = ClusterTaggableManager(through='blog.BlogPageTag', blank=True)
    intro = RichTextField(blank = True) 
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname='title')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('markdown', MarkdownBlock(icon="code")),
    ], use_json_field=True, blank = True)

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        InlinePanel('categories', label='Categories'),
        FieldPanel('tags'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    settings_panels = Page.settings_panels + [
        FieldPanel('post_date'),
    ]

class BlogSinglePage(Page):
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    post_date = models.DateTimeField(default = datetime.now())
    intro = RichTextField(blank = True) 
    body = StreamField([
        ('h1', blocks.CharBlock(form_classname='title')),
        ('h2', blocks.CharBlock(form_classname='title')),
        ('h3', blocks.CharBlock(form_classname='title')),
        ('h4', blocks.CharBlock(form_classname='title')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('markdown', MarkdownBlock(icon="code"))
    ], use_json_field=True, blank = True)

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    settings_panels = Page.settings_panels + [
        FieldPanel('post_date'),
    ]

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'

class BlogPageCategory(models.Model):
    page = ParentalKey('blog.BlogPostPage', on_delete=models.CASCADE, related_name='categories')
    blog_category = models.ForeignKey(
        'blog.BlogCategory', 
        on_delete=models.CASCADE,
        related_name='post_pages'
    )
    panels = [
        FieldPanel('blog_category'),
    ]
    class Meta:
        unique_together = ('page', 'blog_category')

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'blog.BlogPostPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True