from urllib.parse import urlparse

from cms.categories.models import (
    Category,
    CategorySubSite,
    PublicationType,
    PublicationTypeSubSite,
)
from cms.core.blocks import PublicationsBlocks
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.fields.related import ForeignKey
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page


class PublicationIndexPage(Page):
    # title already in the Page class
    # slug already in the Page class
    subpage_types = ["publications.Publication"]
    body = RichTextField(blank=True)

    # so we can filter available categories based on the sub site as well as the
    sub_site_publication_types = models.ForeignKey(
        PublicationTypeSubSite,
        on_delete=models.PROTECT,
        related_name="publication_type_sub_site",
        null=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("sub_site_publication_types"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Publications Index Page"
        verbose_name_plural = "Publications Index Pages"

    def get_latest_publications(num):
        return Publication.objects.all().order_by("-first_published_at")[:num]

    def get_context(self, request, *args, **kwargs):
        """
        publications can have one or more categories (topics) or publications (publiciation_type)
        at the moment you can only choose one or the other? I think thats best to avoid lots of empty
        result sets but we will need a decision made on that.
        """
        publication_ordering = "-first_published_at"
        if request.GET.get("order"):
            publication_ordering = request.GET.get("order")
        context = super().get_context(request, *args, **kwargs)
        # sub_site_categories = Category.objects.filter(
        #     sub_site=self.sub_site_categories.id)

        if request.GET.get("publication_type"):
            context["publication_type_id"] = int(request.GET.get("publication_type"))
            publications = (
                Publication.objects.child_of(self)
                .live()
                .order_by(publication_ordering)
                .filter(
                    publication_publication_type_relationship__publication_type=request.GET.get(
                        "publication_type"
                    )
                )
            )
        # elif request.GET.get("category"):
        #     context["category_id"] = int(request.GET.get("category"))
        #     publications = (
        #         Publication.objects.child_of(self)
        #         .live()
        #         .order_by(publication_ordering)
        #         .filter(
        #             publication_category_relationship__category=request.GET.get(
        #                 "category"
        #             )
        #         )
        #     )
        else:
            publications = (
                Publication.objects.child_of(self).live().order_by(publication_ordering)
            )

        paginator = Paginator(publications, 16)

        try:
            items = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context["publications"] = items
        context["publication_types"] = PublicationType.objects.filter(
            sub_site=self.sub_site_publication_types
        )

        if self.sub_site_publication_types.source == "publication_types":
            sub_site_source = "categories"
        else:
            sub_site_source = self.sub_site_publication_types.source.replace(
                "publication_types-", "categories-"
            )

        category_subsite = CategorySubSite.objects.get(source=sub_site_source)
        context["categories"] = Category.objects.filter(sub_site=category_subsite.id)
        context["order"] = publication_ordering

        return context

    def get_wp_api_link(self):
        wp_source = self.source.replace("pages-", "")
        wp_id = self.wp_id
        if wp_source != "pages":
            api_url = "https://www.england.nhs.uk/{}/wp-json/wp/v2/documents/{}".format(
                wp_source, wp_id
            )
        else:
            api_url = "https://www.england.nhs.uk/wp-json/wp/v2/documents/{}".format(
                wp_id
            )
        return api_url

    def get_wp_live_link(self):
        self_url_path = self.url
        live_url_path = urlparse(self.wp_link).path
        live_url = "https://www.england.nhs.uk{}".format(live_url_path)
        print(self_url_path)
        print(live_url_path)
        return live_url


class PublicationPublicationTypeRelationship(models.Model):
    publication = ParentalKey(
        "publications.Publication",
        related_name="publication_publication_type_relationship",
    )
    publication_type = ForeignKey(
        "categories.PublicationType",
        related_name="+",
        on_delete=models.CASCADE,
    )


class PublicationCategoryRelationship(models.Model):
    publication = ParentalKey(
        "publications.Publication",
        related_name="publication_category_relationship",
    )
    category = ForeignKey(
        "categories.Category",
        related_name="+",
        on_delete=models.CASCADE,
    )


class Publication(Page):

    parent_page_types = ["publications.PublicationIndexPage"]
    """
    title already in the Page class
    slug already in the Page class
    going to need to parse the html here to extract the text
    """

    # going to need to parse the html here to extract the text
    body = RichTextField(blank=True)
    documents = StreamField(PublicationsBlocks, blank=True)

    """ coming across form wordpress need to keep for now"""
    wp_id = models.PositiveIntegerField(null=True)
    source = models.CharField(null=True, max_length=100)
    wp_slug = models.TextField(null=True, blank=True)
    wp_link = models.TextField(null=True, blank=True)
    component_fields = models.TextField(null=True, blank=True)

    """i think we can do away with this field
    and use the text from body to create the exceprt"""
    # excerpt = RichTextField(blank=True)

    author = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        InlinePanel(
            "publication_publication_type_relationship", label="Publication Types"
        ),
        InlinePanel("publication_category_relationship", label="Publication Topics"),
        FieldPanel("body"),
        StreamFieldPanel("documents"),
        MultiFieldPanel(
            [
                FieldPanel("wp_id"),
                FieldPanel("author"),
                FieldPanel("source"),
                FieldPanel("wp_slug"),
                FieldPanel("wp_link"),
                FieldPanel("component_fields"),
            ],
            heading="wordpress data we dont need in the end",
            classname="collapsed collapsible",
        ),
    ]

    def get_wp_api_link(self):
        wp_source = self.source.replace("pages-", "")
        wp_id = self.wp_id
        if wp_source != "pages":
            api_url = "https://www.england.nhs.uk/{}/wp-json/wp/v2/documents/{}".format(
                wp_source, wp_id
            )
        else:
            api_url = "https://www.england.nhs.uk/wp-json/wp/v2/documents/{}".format(
                wp_id
            )
        return api_url

    def get_wp_live_link(self):
        self_url_path = self.url
        live_url_path = urlparse(self.wp_link).path
        live_url = "https://www.england.nhs.uk{}".format(live_url_path)
        print(self_url_path)
        print(live_url_path)
        return live_url
