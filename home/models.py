from django.http import HttpResponseRedirect
from django.db import models
from wagtail.core.models import Page


class HomePage(Page):
    def serve(self, request):
        # Redirect to blog index page
        return HttpResponseRedirect('/blog/')

        # only do this if you're using urls.py and namespaces
        # return HttpResponseRedirect(reverse('blog:index'))