from cms.atlascasestudies.models import AtlasCaseStudy
from cms.blogs.models import Blog
from cms.categories.models import (
    Category,
    CategorySubSite,
    PublicationType,
    PublicationTypeSubSite,
    Region,
    Setting,
)
from cms.posts.models import Post
from cms.publications.models import Publication
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    PermissionHelper,
    modeladmin_register,
)

"""CATEGORIES"""


class CategorySubSitePermissionHelper(PermissionHelper):
    def user_can_delete_obj(self, user, obj):
        categories = Category.objects.filter(sub_site=obj)
        if not categories:
            return True


class CategorySubSiteAdmin(ModelAdmin):
    model = CategorySubSite
    search_fields = ("title",)
    menu_icon = "tag"

    # to prevent deletion of a category subsite if it has any categories belonging to it
    permission_helper_class = CategorySubSitePermissionHelper

    panels = [
        FieldPanel("title"),
        FieldPanel("source"),
        # eventually hidden
    ]


class CategoryPermissionHelper(PermissionHelper):
    def user_can_delete_obj(self, user, obj):
        posts = Post.objects.filter(post_category_relationship__category=obj)
        blogs = Blog.objects.filter(blog_category_relationship__category=obj)
        publications = Publication.objects.filter(
            publication_category_relationship__category=obj
        )
        if not posts and not blogs and not publications:
            return True


class CategoriesAdmin(ModelAdmin):
    model = Category
    search_fields = ("name",)
    list_display = ("name", "sub_site", "get_category_usage")
    menu_icon = "folder-open-inverse"
    list_filter = ("sub_site",)

    # to prevent deletion of a category if it's in use
    permission_helper_class = CategoryPermissionHelper

    panels = [
        FieldPanel("sub_site"),
        FieldPanel("name"),
        # eventually hidden
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("wp_id"),
        FieldPanel("source"),
    ]

    def get_category_usage(self, obj):
        posts = Post.objects.filter(post_category_relationship__category=obj)
        blogs = Blog.objects.filter(blog_category_relationship__category=obj)
        # posts_count, blogs_count = Category.get_category_usage()
        return "Posts {} | Blogs {}".format(posts.count(), blogs.count())

    get_category_usage.short_description = "Usage"


# modeladmin_register(CategoriesAdmin)

"""PUBLICATION TYPES"""


class PublicationTypeSubSitePermissionHelper(PermissionHelper):
    def user_can_delete_obj(self, user, obj):
        publication_types = PublicationType.objects.filter(sub_site=obj)
        if not publication_types:
            return True


class PublicationTypeSubSiteAdmin(ModelAdmin):
    model = PublicationTypeSubSite
    search_fields = ("title",)
    menu_icon = "tag"

    # to prevent deletion of a publication type subsite if it has any publication types belonging to it
    permission_helper_class = PublicationTypeSubSitePermissionHelper

    panels = [
        FieldPanel("title"),
        FieldPanel("source"),
        # eventually hidden
    ]


class PublicationTypePermissionHelper(PermissionHelper):
    def user_can_delete_obj(self, user, obj):
        publication_types = Publication.objects.filter(
            publication_publication_type_relationship__publication_type=obj
        )
        if not publication_types:
            return True


class PublicationTypeAdmin(ModelAdmin):
    model = PublicationType
    search_fields = ("name",)
    list_display = ("name", "sub_site", "get_publication_type_usage")
    # list_display = ('name', 'sub_site')
    menu_icon = "folder-open-inverse"
    list_filter = ("sub_site",)

    # to prevent deletion of a publiction type if it's in use
    permission_helper_class = PublicationTypePermissionHelper

    panels = [
        FieldPanel("sub_site"),
        FieldPanel("name"),
        # eventually hidden
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("wp_id"),
        FieldPanel("source"),
    ]

    def get_publication_type_usage(self, obj):
        publications = Publication.objects.filter(
            publication_publication_type_relationship__publication_type=obj
        )
        # blogs = Blog.objects.filter(blog_category_relationship__category=obj)
        # posts_count, blogs_count = Category.get_category_usage()
        return "Publications {}".format(publications.count())

    get_publication_type_usage.short_description = "Usage"


"""SETTINGS"""


class SettingPermissionHelper(PermissionHelper):
    def user_can_delete_obj(self, user, obj):
        atlas_case_studies = AtlasCaseStudy.objects.filter(
            atlas_case_study_setting_relationship__setting=obj
        )
        if not atlas_case_studies:
            return True


class SettingAdmin(ModelAdmin):
    model = Setting
    search_fields = ("name",)
    list_display = ("name", "get_setting_usage")
    menu_icon = "folder-open-inverse"
    # list_filter = ('sub_site', )

    # to prevent deletion of a category if it's in use
    permission_helper_class = SettingPermissionHelper

    panels = [
        # FieldPanel('sub_site'),
        FieldPanel("name"),
        # eventually hidden
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("wp_id"),
        # FieldPanel('source'),
    ]

    def get_setting_usage(self, obj):
        atlas_case_studies = AtlasCaseStudy.objects.filter(
            atlas_case_study_setting_relationship__setting=obj
        )
        # blogs = Blog.objects.filter(blog_category_relationship__category=obj)
        # posts_count, blogs_count = Category.get_category_usage()
        return "Atlas Case Studies {}".format(atlas_case_studies.count())

    get_setting_usage.short_description = "Usage"


"""REGIONS"""


class RegionPermissionHelper(PermissionHelper):
    def user_can_delete_obj(self, user, obj):
        regions = Region.objects.filter(
            atlas_case_study_region_relationship__region=obj
        )
        if not regions:
            return True


class RegionAdmin(ModelAdmin):
    model = Region
    search_fields = ("name",)
    list_display = ("name", "get_region_usage")
    menu_icon = "folder-open-inverse"
    # list_filter = ('sub_site', )

    # to prevent deletion of a category if it's in use
    # permission_helper_class = RegionPermissionHelper

    panels = [
        # FieldPanel('sub_site'),
        FieldPanel("name"),
        # eventually hidden
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("wp_id"),
        # FieldPanel('source'),
    ]

    def get_region_usage(self, obj):
        atlas_case_studies = AtlasCaseStudy.objects.filter(
            atlas_case_study_region_relationship__region=obj
        )
        # blogs = Blog.objects.filter(blog_category_relationship__category=obj)
        # posts_count, blogs_count = Category.get_category_usage()
        return "Atlas Case Studies {}".format(atlas_case_studies.count())

    get_region_usage.short_description = "Usage"


class CategoriesAdminGroup(ModelAdminGroup):
    menu_label = "Classification"
    menu_icon = "folder-open-1"
    items = (
        CategoriesAdmin,
        CategorySubSiteAdmin,
        PublicationTypeAdmin,
        PublicationTypeSubSiteAdmin,
        SettingAdmin,
        RegionAdmin,
    )


modeladmin_register(CategoriesAdminGroup)
