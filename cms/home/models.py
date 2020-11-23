from cms.pages.models import ComponentsPage
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtailnhsukfrontend.blocks import (ActionLinkBlock, CareCardBlock,
                                         DetailsBlock, DoBlock, DontBlock,
                                         ExpanderBlock, ExpanderGroupBlock,
                                         GreyPanelBlock, ImageBlock,
                                         InsetTextBlock, PanelBlock,
                                         PanelListBlock, PromoBlock,
                                         PromoGroupBlock, SummaryListBlock,
                                         WarningCalloutBlock)
from wagtailnhsukfrontend.mixins import HeroMixin, ReviewDateMixin


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['component_pages'] =  ComponentsPage.objects.live().descendant_of(HomePage.objects.get(id=self.id))
        return context

    @property
    def next_sibling(self):
        return self.get_next_siblings().live().first()

    @property
    def prev_sibling(self):
        return self.get_prev_siblings().live().first()


class DemoPage(HeroMixin, ReviewDateMixin, Page):
    body = StreamField(
        [
            ("action_link", ActionLinkBlock()),
            ("care_card", CareCardBlock()),
            ("details", DetailsBlock()),
            ("do", DoBlock()),
            ("dont", DontBlock()),
            ("expander", ExpanderBlock()),
            ("expander_group", ExpanderGroupBlock()),
            ("grey_panel", GreyPanelBlock()),
            ("image", ImageBlock()),
            ("inset_text", InsetTextBlock()),
            ("panel", PanelBlock()),
            ("panel_list", PanelListBlock()),
            ("promo", PromoBlock()),
            ("promo_group", PromoGroupBlock()),
            ("summary_list", SummaryListBlock()),
            ("warning_callout", WarningCalloutBlock()),
        ]
    )

    content_panels = (
        Page.content_panels
        + HeroMixin.content_panels
        + [
            StreamFieldPanel("body"),
        ]
    )

    settings_panels = Page.settings_panels + ReviewDateMixin.settings_panels
