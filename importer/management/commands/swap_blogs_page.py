import time
import sys

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.core.validators import slug_re
from django.utils.html import strip_tags
from cms.pages.models import BasePage, ComponentsPage, LandingPage
from importer.utils import URLParser
from cms.blogs.models import BlogIndexPage


class Command(BaseCommand):
    help = "Swap blogs page"

    def __init__(self):
        # uniqufy urls to start with so we can deal with altering them later
        # all pages initially come in at the top level under home page
        # so urls can get changed to keep them unique (Wagtail action)
        self.random_strings = []

    def handle(self, *args, **options):
        """
        Process: We need to change the blogs landing page from a Components Page here to a Landing Page type

        Landing pages: have a different layout better catered for with a separate page type
        """

        # its title here it 'Blogs' its slug is 'blogs' and it's a component page type
        # there should only be one...
        blog_landing_page = ComponentsPage.objects.get(
            wp_template="page-blog-landing.php"
        )
        # first create the new Components Pages

        # make a new page and place it under the same parent page
        first_published_at = blog_landing_page.first_published_at
        last_published_at = blog_landing_page.last_published_at
        latest_revision_created_at = blog_landing_page.latest_revision_created_at

        slug = URLParser(blog_landing_page.wp_link).find_slug()

        # sometimes there's external links with params so fall back to the slug fomr wordpress
        if not slug_re.match(slug):
            slug = blog_landing_page.slug

        # the body field is left blank for now
        obj = LandingPage(
            title=blog_landing_page.title,
            slug=self.unique_slug(slug),
            excerpt=strip_tags(blog_landing_page.excerpt),
            # raw_content=blog_landing_page.content,
            show_in_menus=True,
            author=blog_landing_page.author,
            md_owner=blog_landing_page.md_owner,
            md_description=blog_landing_page.md_description,
            md_gateway_ref=blog_landing_page.md_gateway_ref,
            md_pcc_reference=blog_landing_page.md_pcc_reference,
            # start wordpress fields we can delete later
            wp_id=blog_landing_page.wp_id,
            parent=blog_landing_page.parent,
            source=blog_landing_page.source,
            wp_template=blog_landing_page.wp_template,
            wp_slug=blog_landing_page.wp_slug,
            real_parent=blog_landing_page.real_parent,
            wp_link=blog_landing_page.wp_link,
            model_fields=blog_landing_page.model_fields,
            content_fields=blog_landing_page.content_fields,
            content_field_blocks=blog_landing_page.content_field_blocks,
            component_fields=blog_landing_page.component_fields,
        )
        blog_landing_page.get_parent().add_child(instance=obj)

        rev = obj.save_revision()  # this needs to run here

        obj.first_published_at = first_published_at
        obj.last_published_at = last_published_at
        obj.latest_revision_created_at = latest_revision_created_at

        obj.save()
        rev.publish()

        blogs_page = LandingPage.objects.get(wp_template="page-blog-landing.php")
        print("Moving all blog posts to new parent page, Takes a while...")

        # find base page with that wp_id and source so we can move it's children
        old_blog_index_base_page = BlogIndexPage.objects.get(slug="blog")
        # blog_pages = old_blog_index_base_page.get_children()

        # for blog in blog_pages:
        old_blog_index_base_page.move(blogs_page, pos="last-child")

        # delete the old blog-items-index now dont need it
        blog_landing_page.delete()

        # rename the slug for the new blogs page now we deleted the old one
        blogs_page.slug = "blogs"
        rev = blogs_page.save_revision()
        blogs_page.save()
        rev.publish()
        sys.stdout.write("\n✅  Blogs Page Now Set Up\n")

    def unique_slug(self, slug):
        # 8 characters, only digits.
        random_string = get_random_string(8, "0123456789")
        if not random_string in self.random_strings:
            self.random_strings.append(random_string)
            return str(slug) + "----" + str(random_string)
        else:
            self.unique_slug(slug)
