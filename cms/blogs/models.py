from urllib.parse import urlparse

from cms.categories.models import Category, CategorySubSite
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, ParentalManyToManyField


class BlogIndexPage(Page):
    # title already in the Page class
    # slug already in the Page class
    subpage_types = ["blogs.Blog"]
    body = RichTextField(blank=True)

    # so we can filter available categories based on the sub site as well as the
    sub_site_categories = models.ForeignKey(
        CategorySubSite,
        on_delete=models.PROTECT,
        related_name="category_blog_site",
        null=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("sub_site_categories"),
        FieldPanel("body"),
    ]

    def get_latest_blogs(self, num):
        return Blog.objects.all().order_by("-first_published_at")[:num]

    def get_context(self, request, *args, **kwargs):
        blog_ordering = "-first_published_at"
        context = super().get_context(request, *args, **kwargs)

        if request.GET.get("category"):
            context["chosen_category_id"] = int(request.GET.get("category"))
            blogs = (
                Blog.objects.live()
                .order_by(blog_ordering)
                .filter(
                    blog_category_relationship__category=request.GET.get("category")
                )
            )
        else:
            blogs = Blog.objects.live().order_by(blog_ordering)

        paginator = Paginator(blogs, 16)

        try:
            items = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context["blogs"] = items
        # context['categories'] = Category.objects.all()

        # an experiment to get only categories that are used by blogs
        blog_pages_ids = [x.id for x in Blog.objects.all()]
        # print(blog_pages_ids)
        # print(Category.objects.filter(blog_categories__in=blog_pages_ids))
        # context['categories'] = Category.objects.filter(blog_categories__in=blog_pages_ids)
        context["categories"] = Category.objects.filter(
            sub_site=self.sub_site_categories.id
        )
        return context


class BlogCategoryRelationship(models.Model):
    blog = ParentalKey(
        "blogs.Blog",
        related_name="blog_category_relationship",
    )
    category = models.ForeignKey(
        "categories.Category",
        related_name="+",
        on_delete=models.CASCADE,
    )


class Blog(Page):
    parent_page_types = ["blogs.BlogIndexPage"]
    """
    title already in the Page class
    slug already in the Page class
    going to need to parse the html here to extract the text
    """

    # going to need to parse the html here to extract the text
    body = RichTextField(blank=True)

    """ coming across form wordpress need to keep for now"""
    wp_id = models.PositiveIntegerField(null=True)
    source = models.CharField(null=True, max_length=100)
    wp_slug = models.TextField(null=True, blank=True)
    wp_link = models.TextField(null=True, blank=True)

    """i think we can do away with this field
    and use the text from body to create the exceprt"""
    # excerpt = RichTextField(blank=True)

    author = models.CharField(max_length=255, blank=True)
    # categories = ParentalManyToManyField(
    #     'categories.Category',
    #     blank=True,
    #     related_name='blog_categories',
    #     help_text='use cmd/ctrl click to select multiple categories',
    # )

    content_panels = Page.content_panels + [
        InlinePanel("blog_category_relationship", label="Categories"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                FieldPanel("wp_id"),
                FieldPanel("author"),
                FieldPanel("source"),
                FieldPanel("wp_slug"),
                FieldPanel("wp_link"),
            ],
            heading="wordpress data we dont need in the end",
            classname="collapsed collapsible",
        ),
    ]

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

    # def get_wp_live_link(self):
    #     self_url_path = self.url
    #     live_url_path = urlparse(self.wp_link).path
    #     live_url = 'https://www.england.nhs.uk{}'.format(live_url_path)
    #     print(self_url_path)
    #     print(live_url_path)
    #     return live_url
