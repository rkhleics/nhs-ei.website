from urllib.parse import urlparse
from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from cms.core.blocks import CoreBlocks


class BasePage(Page):
    # parent_page_types = ['home.HomePage'] # not sure about this yet
    # these fields are meta data we dont display but helps content publishers
    md_owner = models.TextField("Owner", blank=True)
    md_description = models.TextField("Description", blank=True)
    md_gateway_ref = models.TextField("Gateway Ref", blank=True)
    md_pcc_reference = models.TextField("PCC Reference", blank=True)

    """
    title already in the Page class
    slug already in the Page class
    """

    # we may not need this???
    excerpt = models.TextField(blank=True)
    # going to need to parse the html here to extract the text
    # body = RichTextField(blank=True)
    body = StreamField(CoreBlocks, blank=True)

    """ coming across form wordpress need to keep for now"""
    wp_id = models.IntegerField(null=True)
    parent = models.IntegerField(blank=True, null=True)
    source = models.CharField(null=True, max_length=100)
    wp_template = models.CharField(null=True, max_length=100, blank=True)
    wp_slug = models.TextField(null=True)
    real_parent = models.IntegerField(null=True, blank=True)
    wp_link = models.TextField(null=True, blank=True)
    raw_content = models.TextField(null=True, blank=True)
    model_fields = models.TextField(null=True, blank=True)
    content_fields = models.TextField(null=True, blank=True)
    content_field_blocks = models.TextField(null=True, blank=True)
    component_fields = models.TextField(null=True, blank=True)

    author = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        # StreamFieldPanel('body2'),
        StreamFieldPanel("body"),
        FieldPanel("excerpt"),
        MultiFieldPanel(
            [
                FieldPanel("md_owner"),
                FieldPanel("md_description"),
                FieldPanel("md_gateway_ref"),
                FieldPanel("md_pcc_reference"),
            ],
            heading="Meta Data",
            classname="collapsed collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("wp_id"),
                FieldPanel("author"),
                FieldPanel("parent"),
                FieldPanel("source"),
                FieldPanel("wp_template"),
                FieldPanel("wp_slug"),
                FieldPanel("real_parent"),
                FieldPanel("wp_link"),
                FieldPanel("model_fields"),
                FieldPanel("raw_content"),
                FieldPanel("content_fields"),
                FieldPanel("content_field_blocks"),
                FieldPanel("component_fields"),
            ],
            heading="wordpress data we dont need in the end",
            classname="collapsed collapsible",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["children"] = self.get_children()
        return context

    def get_wp_api_link(self):
        wp_source = self.source.replace("pages-", "")
        wp_id = self.wp_id
        if wp_source != "pages":
            api_url = "https://www.england.nhs.uk/{}/wp-json/wp/v2/pages/{}".format(
                wp_source, wp_id
            )
        else:
            api_url = "https://www.england.nhs.uk/wp-json/wp/v2/pages/{}".format(wp_id)
        return api_url

    def get_wp_live_link(self):
        self_url_path = self.url
        live_url_path = urlparse(self.wp_link).path
        live_url = "https://www.england.nhs.uk{}".format(live_url_path)
        print(self_url_path)
        print(live_url_path)
        return live_url

    @property
    def next_sibling(self):
        return self.get_next_siblings().live().first()

    @property
    def prev_sibling(self):
        return self.get_prev_siblings().live().first()


class LandingPage(Page):
    """
    a temporary holding page for wordpress pages of template=page-landing.php, page-blog-landing.php
    """

    # parent_page_types = ['home.HomePage'] # not sure about this yet
    # these fields are meta data we dont display but helps content publishers
    md_owner = models.TextField("Owner", blank=True)
    md_description = models.TextField("Description", blank=True)
    md_gateway_ref = models.TextField("Gateway Ref", blank=True)
    md_pcc_reference = models.TextField("PCC Reference", blank=True)

    # we may not need this???
    excerpt = models.TextField(blank=True)
    # going to need to parse the html here to extract the text
    # body = RichTextField(blank=True)
    body = StreamField(CoreBlocks, blank=True)

    """ coming across form wordpress need to keep for now"""
    wp_id = models.IntegerField(null=True)
    parent = models.IntegerField(blank=True, null=True)
    source = models.CharField(null=True, max_length=100)
    wp_template = models.CharField(null=True, max_length=100, blank=True)
    wp_slug = models.TextField(null=True)
    real_parent = models.IntegerField(null=True, blank=True)
    wp_link = models.TextField(null=True, blank=True)
    raw_content = models.TextField(null=True, blank=True)
    model_fields = models.TextField(null=True, blank=True)
    content_fields = models.TextField(null=True, blank=True)
    content_field_blocks = models.TextField(null=True, blank=True)
    component_fields = models.TextField(null=True, blank=True)

    author = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        # StreamFieldPanel('body2'),
        StreamFieldPanel("body"),
        FieldPanel("excerpt"),
        MultiFieldPanel(
            [
                FieldPanel("md_owner"),
                FieldPanel("md_description"),
                FieldPanel("md_gateway_ref"),
                FieldPanel("md_pcc_reference"),
            ],
            heading="Meta Data",
            classname="collapsed collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("wp_id"),
                FieldPanel("author"),
                FieldPanel("parent"),
                FieldPanel("source"),
                FieldPanel("wp_template"),
                FieldPanel("wp_slug"),
                FieldPanel("real_parent"),
                FieldPanel("wp_link"),
                FieldPanel("model_fields"),
                FieldPanel("content_fields"),
                FieldPanel("content_field_blocks"),
                FieldPanel("component_fields"),
            ],
            heading="wordpress data we dont need in the end",
            classname="collapsed collapsible",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["children"] = self.get_children()
        return context

    @property
    def next_sibling(self):
        return self.get_next_siblings().live().first()

    @property
    def prev_sibling(self):
        return self.get_prev_siblings().live().first()


class ComponentsPage(Page):
    """
    a page for wordpress pages of template=page-comonents.php
    """

    # parent_page_types = ['home.HomePage'] # not sure about this yet
    # these fields are meta data we dont display but helps content publishers
    md_owner = models.TextField("Owner", blank=True)
    md_description = models.TextField("Description", blank=True)
    md_gateway_ref = models.TextField("Gateway Ref", blank=True)
    md_pcc_reference = models.TextField("PCC Reference", blank=True)

    """
    title already in the Page class
    slug already in the Page class
    """

    # we may not need this???
    excerpt = models.TextField(blank=True)
    # going to need to parse the html here to extract the text
    # body = RichTextField(blank=True)
    body = StreamField(CoreBlocks, blank=True)

    """ coming across form wordpress need to keep for now"""
    wp_id = models.IntegerField(null=True)
    parent = models.IntegerField(blank=True, null=True)
    source = models.CharField(null=True, max_length=100)
    wp_template = models.CharField(null=True, max_length=100, blank=True)
    wp_slug = models.TextField(null=True)
    real_parent = models.IntegerField(null=True, blank=True)
    wp_link = models.TextField(null=True, blank=True)
    raw_content = models.TextField(null=True, blank=True)
    model_fields = models.TextField(null=True, blank=True)
    content_fields = models.TextField(null=True, blank=True)
    content_field_blocks = models.TextField(null=True, blank=True)
    component_fields = models.TextField(null=True, blank=True)

    author = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        # StreamFieldPanel('body2'),
        StreamFieldPanel("body"),
        FieldPanel("excerpt"),
        MultiFieldPanel(
            [
                FieldPanel("md_owner"),
                FieldPanel("md_description"),
                FieldPanel("md_gateway_ref"),
                FieldPanel("md_pcc_reference"),
            ],
            heading="Meta Data",
            classname="collapsed collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("wp_id"),
                FieldPanel("author"),
                FieldPanel("parent"),
                FieldPanel("source"),
                FieldPanel("wp_template"),
                FieldPanel("wp_slug"),
                FieldPanel("real_parent"),
                FieldPanel("wp_link"),
                FieldPanel("model_fields"),
                FieldPanel("content_fields"),
                FieldPanel("content_field_blocks"),
                FieldPanel("component_fields"),
            ],
            heading="wordpress data we dont need in the end",
            classname="collapsed collapsible",
        ),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["children"] = self.get_children()
        return context

    @property
    def next_sibling(self):
        return self.get_next_siblings().live().first()

    @property
    def prev_sibling(self):
        return self.get_prev_siblings().live().first()


class HoldingPage(Page):
    """
    a temporary holding page for wordpress pages that so far are left as immediate children of the home page
    """

    parent_page_types = ["home.HomePage"]
    subpage_types = ["pages.BasePage"]
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["children"] = self.get_children()
        return context
