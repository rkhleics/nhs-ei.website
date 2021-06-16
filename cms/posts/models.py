from cms.blogs.models import BlogIndexPage
from cms.categories.models import Category, CategorySubSite
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.fields.related import ForeignKey
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class FilteredInlinePanel(InlinePanel):
    def on_model_bound(self):
        # print(self.model)
        super().on_model_bound()

    def on_form_bound(self):
        # post_index_page_sub_site = PostIndexPage.objects.get(id=self.instance.get_parent().id).sub_site_categories
        # categories = Category.objects.filter(sub_site=post_index_page_sub_site)
        # print(categories)
        # print(self.categories)
        # print(self.model.queryset)
        # choices = self.model.get_category_inline_field_choices(self.model)
        # choices = None
        # self.form.fields['postcategoryrelationship'].queryset = categories
        # self.form.fields['postcategoryrelationship'].empty_label = None
        super().on_form_bound()


class PostIndexPage(Page):
    # title already in the Page class
    # slug already in the Page class
    subpage_types = ["posts.Post"]
    body = RichTextField(blank=True)

    # so we can filter available categories based on the sub site as well as the
    sub_site_categories = models.ForeignKey(
        CategorySubSite,
        on_delete=models.PROTECT,
        related_name="category_sub_site",
        null=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("sub_site_categories"),
        FieldPanel("body"),
    ]

    def get_latest_posts(num):
        return Post.objects.all().order_by("-first_published_at")[:num]

    def get_context(self, request, *args, **kwargs):
        post_ordering = "-first_published_at"
        context = super().get_context(request, *args, **kwargs)
        # sub_site_categories = Category.objects.filter(
        #     sub_site=self.sub_site_categories.id)

        if request.GET.get("category"):
            context["chosen_category_id"] = int(request.GET.get("category"))
            posts = (
                Post.objects.child_of(self)
                .live()
                .order_by(post_ordering)
                .filter(
                    post_category_relationship__category=request.GET.get("category")
                )
            )
        else:
            posts = Post.objects.child_of(self).live().order_by(post_ordering)

        paginator = Paginator(posts, 16)

        try:
            items = paginator.page(request.GET.get("page"))
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context["posts"] = items
        context["categories"] = Category.objects.filter(
            sub_site=self.sub_site_categories.id
        )

        return context


class PostCategoryRelationship(models.Model):
    post = ParentalKey(
        "posts.Post",
        related_name="post_category_relationship",
    )
    category = ForeignKey(
        "categories.Category",
        related_name="+",
        on_delete=models.CASCADE,
    )


class Post(Page):

    parent_page_types = ["posts.PostIndexPage"]
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

    content_panels = Page.content_panels + [
        InlinePanel("post_category_relationship", label="Categories"),
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

    # def get_category_inline_field_choices(self):
    #     # need to limit the category inline panel choices to
    #     # categories belonging to the parent page sub_site_categories
    #     parent = PostIndexPage.objects.parent_of(self.id)
    #     # print(parent)
    #     # print(parent)
    #     # parent_sub_site = parent.sub_site_categories

    #     return Category.objects.filter(sub_site=self.get_parent().sub_site)
