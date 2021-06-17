from django.template.defaultfilters import default, filesizeformat
from wagtail.core.blocks import (
    StructBlock,
    RawHTMLBlock,
    CharBlock,
    StreamBlock,
    ListBlock,
)
from wagtail.core.blocks.field_block import (
    BooleanBlock,
    ChoiceBlock,
    DecimalBlock,
    IntegerBlock,
    MultipleChoiceBlock,
    PageChooserBlock,
    RichTextBlock,
    URLBlock,
)
from wagtail.documents.blocks import DocumentChooserBlock

from wagtailnhsukfrontend.blocks import (
    ActionLinkBlock,
    CareCardBlock,
    DetailsBlock,
    DoBlock,
    DontBlock,
    ExpanderBlock,
    ExpanderGroupBlock,
    FlattenValueContext,
    GreyPanelBlock,
    InsetTextBlock,
    ImageBlock,
    PanelBlock,
    PanelListBlock,
    WarningCalloutBlock,
    PromoBlock,
    PromoGroupBlock,
    SummaryListBlock,
)

from cms.posts.models import Post
from cms.blogs.models import Blog

RICHTEXT_FEATURES_ALL = [
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "bold",
    "italic",
    "ol",
    "ul",
    "hr",
    "link",
    "document-link",
    "image",
    "embed",
    "code",
    "superscript",
    "subscript",
    "strikethrough",
    "blockquote",
]


class RecentPostsBlock(FlattenValueContext, StructBlock):
    title = CharBlock()
    type = MultipleChoiceBlock(
        choices=(
            ("post", "Post"),
            ("blog", "Blog"),
        ),
        default=["post", "blog"],
    )
    num_posts = IntegerBlock(default=6, help_text="How many of each type")
    see_all_posts = BooleanBlock(default=True)
    see_all_blogs = BooleanBlock(default=True)

    class Meta:
        icon = "pick"
        template = "blocks/recent_posts_block.html"
        help_text = "Show a recent posts/blogs panel. Choose post and/or blog and categories to filter by."

    def get_context(self, value, parent_context):
        context = super().get_context(value, parent_context=parent_context)
        num_of_each = int(value.get("num_posts"))
        posts = Post.objects.all().order_by("-first_published_at")[:num_of_each]
        blogs = Blog.objects.all().order_by("-first_published_at")[:num_of_each]
        post_types = value.get("type")
        qs = {
            "posts": [],
            "blogs": [],
        }
        if "post" in post_types:
            for post in posts:
                qs["posts"].append({"record": post, "tag": "News"}),

        if "blog" in post_types:
            for blog in blogs:
                qs["blogs"].append({"record": blog, "tag": "Blog"})

        context["queryset"] = qs

        # for post_type in post_types:

        # if len(post_types) == 1:
        #     pass
        # elif len(post_types) == 2:
        #     pass
        return context


class JumpMenuBlock(StructBlock):
    # this block renders a list of indivual anchor links as a jump menu
    # used in conjunction with the Named Anchor block
    menu = ListBlock(StructBlock([("title", CharBlock()), ("menu_id", CharBlock())]))

    class Meta:
        icon = "order-down"
        template = "blocks/jump_menu_block.html"
        help_text = 'Add a list of named anchors that correspond to the Named achors below e.g. "document-name"'


class NamedAnchorBlock(StructBlock):
    # this block is to render a named anchor for the jump menu
    # you can also add the heading if required
    anchor_id = CharBlock()
    heading = CharBlock(required=False)

    class Meta:
        icon = "placeholder"
        template = "blocks/named_anchor_block.html"
        help_text = 'Add a named place holder to jump to e.g. "document-name" with an optional heading'


class DocumentBlock(StructBlock):
    title = RichTextBlock(required=False)
    document = DocumentChooserBlock()
    summary = RichTextBlock(required=False)

    class Meta:
        icon = "doc"
        template = "blocks/document_block.html"
        help_text = "Choose or upload a document"

    def get_context(self, value, parent_context):
        context = super().get_context(value, parent_context)
        context["file_ext"] = value["document"].file_extension
        context["file_size"] = filesizeformat(value["document"].get_file_size())

        return context


class DocumentLinkBlock(StructBlock):
    title = RichTextBlock(required=False)
    external_url = URLBlock(required=False)
    page = PageChooserBlock(required=False)
    summary = RichTextBlock(required=False)

    class Meta:
        icon = "doc"
        template = "blocks/document_link_block.html"
        help_text = "Choose or upload a document"


class DocumentEmbedBlock(StructBlock):
    title = RichTextBlock(required=False)
    html = RawHTMLBlock()

    class Meta:
        icon = "doc"
        template = "blocks/document_embed_block.html"
        help_text = "Choose or upload a document"


class DocumentGroupBlock(StreamBlock):
    document = DocumentBlock()
    document_link = DocumentLinkBlock()
    document_embed = DocumentEmbedBlock()
    free_text = RichTextBlock()

    class Meta:
        icon = "placeholder"
        help_text = "Add any number of related documents"
        template = "blocks/document_group_block.html"


class CoreBlocks(StreamBlock):
    action_link = ActionLinkBlock(group="Base")
    care_card = CareCardBlock(group="Base")
    details = DetailsBlock(group="Base")
    do_list = DoBlock(group="Base")
    dont_list = DontBlock(group="Base")
    expander = ExpanderBlock(group="Base")
    expander_group = ExpanderGroupBlock(group="Base")
    inset_text = InsetTextBlock(group="Base")
    image = ImageBlock(group="Base")
    panel = PanelBlock(group="Base")
    panel_list = PanelListBlock(group="Base")
    # panel_with_image = PanelBlockWithImage(group='Base')
    grey_panel = GreyPanelBlock(group="Base")
    warning_callout = WarningCalloutBlock(group="Base")
    summary_list = SummaryListBlock(group="Base")
    promo = PromoBlock(group="Base")
    promo_group = PromoGroupBlock(group="Base")

    recent_posts = RecentPostsBlock(group="Custom")
    text = RichTextBlock(
        group="Custom",
        help_text="""
            Use this block to add formatted text into a page e.g. 
            paragraph with heading and/or links and images
        """,
        template="blocks/text_block.html",
        features=RICHTEXT_FEATURES_ALL,
    )
    html = RawHTMLBlock(
        group="custom",
        help_text="""
            Use this block to add raw html
        """,
        template="blocks/html_block.html",
    )


class PublicationsBlocks(StreamBlock):
    # document = DocumentBlock(group='Custom')
    # document_link = DocumentLinkBlock(group='Custom')
    # document_embed = DocumentEmbedBlock(group='Custom')
    document_group = DocumentGroupBlock(group="Custom")
    jump_menu = JumpMenuBlock(group="Custom")
    named_anchor = NamedAnchorBlock(group="Custom")


class LinkListBlock(StructBlock):
    footer_links = ListBlock(
        StructBlock(
            [
                ("text", CharBlock()),
                ("page", PageChooserBlock()),
                ("external_link", URLBlock()),
            ]
        )
    )


class FooterBlocks(StreamBlock):
    footer_links = LinkListBlock(group="Custom")
