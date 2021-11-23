from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.expressions import F
from django.db.models.fields import Field, proxy, related
from modelcluster.models import ClusterableModel
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from taggit.models import Tag as TaggitTag, TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

# Create your models here.

class BlogPage(Page):
   description = models.CharField(max_length=255, blank=True)
   content_panels = Page.content_panels + [
       FieldPanel('description', classname='full')
   ]

class PostPage(Page):
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
        related_name = '+'
    )

    tags = ClusterTaggableManager(through='blog.PostPageTag', blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('feed_image'),
        InlinePanel('categories', label = 'Category'),
        FieldPanel('tags')
    ]

class PostPageBlogCategory(models.Model):
    page = ParentalKey(
        'blog.PostPage',
        on_delete = models.CASCADE,
        related_name = 'categories'
    )
    blog_category = models.ForeignKey(
        'blog.BlogCategory',
        on_delete = models.CASCADE,
        related_name = "post_pages"
    )
    panels = [
        SnippetChooserPanel('blog_category'),
    ]
    class Meta:
        unique_together = ('page', 'blog_category')

class PostPageTag(TaggedItemBase):
    content_object = ParentalKey('PostPage', related_name = 'post_tags')

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy: True
