from cms.pages.models import ComponentsPage, BasePage, LandingPage
from urllib.parse import urlparse
from django.db import models

from cms.core.blocks import CoreBlocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel


class HomePage(Page):
    max_num = 1
    body = RichTextField(blank=True)
    body_image = models.ForeignKey(
        'wagtailimages.Image',
        related_name='+',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    all_news_page = models.ForeignKey(
        'wagtailcore.Page',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+',
    )
    all_news_title = models.CharField(max_length=100, blank=True)
    all_news_sub_title = RichTextField(blank=True)
    all_publications_page = models.ForeignKey(
        'wagtailcore.Page',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+'
    )
    all_publications_title = models.CharField(max_length=100, blank=True)
    all_publications_sub_title = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('body'),
            ImageChooserPanel('body_image'),
        ], heading='Main Body'),
        MultiFieldPanel([
            PageChooserPanel('all_news_page'),
            FieldPanel('all_news_title'),
            FieldPanel('all_news_sub_title'),
        ], heading='Latest News'),
        MultiFieldPanel([
            PageChooserPanel('all_publications_page'),
            FieldPanel('all_publications_title'),
            FieldPanel('all_publications_sub_title'),
        ], heading='Latest Publications'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['component_pages'] =  ComponentsPage.objects.child_of(self)
        context['base_pages'] =  BasePage.objects.child_of(self)
        context['landing_pages'] =  LandingPage.objects.child_of(self)
        return context

    # @property
    # def next_sibling(self):
    #     return self.get_next_siblings().live().first()

    # @property
    # def prev_sibling(self):
    #     return self.get_prev_siblings().live().first()