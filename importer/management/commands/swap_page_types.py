import time
import sys

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.core.validators import slug_re
from django.utils.html import strip_tags
from cms.pages.models import BasePage, ComponentsPage
from importer.utils import URLParser
from cms.blogs.models import BlogIndexPage


class Command(BaseCommand):
    help = "Swap page types"

    def __init__(self):
        # uniqufy urls to start with so we can deal with altering them later
        # all pages initially come in at the top level under home page
        # so urls can get changed to keep them unique (Wagtail action)
        self.random_strings = []

    def handle(self, *args, **options):
        """
        Process: We need to change some pages from a base page to another page type
        based on it's page type from wordpress

        Component pages: have a different layout better catered for with a separate page type
        """

        base_pages = BasePage.objects.filter(
            wp_template="page-components.php"
        ) | BasePage.objects.filter(wp_template="page-blog-landing.php")
        # first create the new Components Pages

        for page in base_pages:

            # print(page)
            # make a new page and place it under the same parent page
            first_published_at = page.first_published_at
            last_published_at = page.last_published_at
            latest_revision_created_at = page.latest_revision_created_at
            # print('{}'.format(page.title))

            slug = URLParser(page.wp_link).find_slug()
            # sometimes there's external links with params so fall back to the slug fomr wordpress
            if not slug_re.match(slug):
                slug = page.slug

            # the body field is left blank for now
            obj = ComponentsPage(
                title=page.title,
                slug=self.unique_slug(slug),
                excerpt=strip_tags(page.excerpt),
                # raw_content=page.content,
                show_in_menus=True,
                author=page.author,
                md_owner=page.md_owner,
                md_description=page.md_description,
                md_gateway_ref=page.md_gateway_ref,
                md_pcc_reference=page.md_pcc_reference,
                # start wordpress fields we can delete later
                wp_id=page.wp_id,
                parent=page.parent,
                source=page.source,
                wp_template=page.wp_template,
                wp_slug=page.wp_slug,
                real_parent=page.real_parent,
                wp_link=page.wp_link,
                model_fields=page.model_fields,
                content_fields=page.content_fields,
                content_field_blocks=page.content_field_blocks,
                component_fields=page.component_fields,
            )

            page.get_parent().add_child(instance=obj)

            rev = obj.save_revision()  # this needs to run here

            obj.first_published_at = first_published_at
            obj.last_published_at = last_published_at
            obj.latest_revision_created_at = latest_revision_created_at

            obj.save()
            rev.publish()

        components_pages = ComponentsPage.objects.all()

        for component_page in components_pages:
            # print(component_page.id)
            wp_id = component_page.wp_id
            source = component_page.source
            # find base page with that wp_id and source so we can move it's children
            old_base_page = BasePage.objects.get(source=source, wp_id=wp_id)
            children = old_base_page.get_children()

            for child in children:
                child.move(component_page, pos="last-child")
            old_base_page.delete()

        # sys.exit()

        # new_blogs_page = ComponentsPage.objects.filter(title='Blogs', wp_template='page-blog-landing.php')
        # blog_items_base = BlogIndexPage.objects.get(slug='blog-items-base')
        # children = blog_items_base.get_children()

        # for child in children:
        #     child.move(new_blogs_page, pos='last-child')
        # blog_items_base.delete()

    def unique_slug(self, slug):
        # 8 characters, only digits.
        random_string = get_random_string(8, "0123456789")
        if not random_string in self.random_strings:
            self.random_strings.append(random_string)
            return str(slug) + "----" + str(random_string)
        else:
            self.unique_slug(slug)
