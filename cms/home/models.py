from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
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
    pass


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
