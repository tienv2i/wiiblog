from wagtail.models import Site
from .models import BlogIndexPage, BlogCategory, Tag


def blog_page(request):
    wagtail_site = Site.find_for_request(request)
    context = {
        'blog_page': BlogIndexPage.objects.in_site(wagtail_site).first(),
        'blog_categories': BlogCategory.objects.all(),
        'blog_tags': Tag.objects.all()
    }
    return context