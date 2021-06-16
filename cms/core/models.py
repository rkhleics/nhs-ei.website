from django.db import models
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
)
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import RichTextField
from wagtail.core.models import ClusterableModel, Orderable, ParentalKey


@register_setting
class CoreSettings(BaseSetting, ClusterableModel):
    alert_banner = RichTextField()
    is_visible = models.BooleanField(default=False, blank=True)

    header_extra = models.TextField(blank=True, null=True)
    footer_extra = models.TextField(blank=True, null=True)

    panels = [
        MultiFieldPanel(
            [FieldPanel("alert_banner"), FieldPanel("is_visible")],
            heading="Alert Banner",
        ),
        MultiFieldPanel(
            [
                FieldPanel("header_extra"),
                FieldPanel("footer_extra"),
            ],
            heading="Extra header and footer code",
            help_text="You can add valid html code snippets here such as analytics code or other scripts",
        ),
        MultiFieldPanel(
            [InlinePanel("upper_footer_links")],
            heading="Upper Footer Links",
            help_text="NOTE: if you choose a page as a link it will overide the external link",
        ),
        MultiFieldPanel(
            [InlinePanel("lower_footer_links")],
            heading="Lower Footer Links",
            help_text="NOTE: if you choose a page as a link it will overide the external link",
        ),
    ]


class UpperFooterLinks(Orderable):
    setting = ParentalKey(
        CoreSettings,
        related_name="upper_footer_links",
    )
    text = models.CharField(max_length=100)
    page = models.ForeignKey(
        "wagtailcore.Page",
        related_name="+",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    external_url = models.URLField(blank=True)

    panels = [
        FieldPanel("text"),
        PageChooserPanel("page"),
        FieldPanel("external_url"),
    ]


class LowerFooterLinks(Orderable):
    setting = ParentalKey(
        CoreSettings,
        related_name="lower_footer_links",
    )
    text = models.CharField(max_length=100)
    page = models.ForeignKey(
        "wagtailcore.Page",
        related_name="+",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    external_url = models.URLField(blank=True)

    panels = [
        FieldPanel("text"),
        PageChooserPanel("page"),
        FieldPanel("external_url"),
    ]
