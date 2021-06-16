import sys
import time
import ast
from django.core.validators import slug_re
from django.utils.crypto import get_random_string
from django.core.management import call_command
from django.utils.html import strip_tags
from cms.pages.models import BasePage
from wagtail.core.models import Page
from importer.utils import URLParser

from .importer_cls import Importer


class PagesImporter(Importer):
    def __init__(self):
        # uniqufy urls to start with so we can deal with altering them later
        # all pages initially come in at the top level under home page
        # so urls can get changed to keep them unique (Wagtail action)
        self.random_strings = []
        pages = BasePage.objects.all()
        if pages:
            sys.stdout.write("⚠️  Run delete_pages before running this command\n")
            sys.exit()

    def parse_results(self):

        home_page = Page.objects.filter(title="Home")[0]
        pages = self.results  # this is json result set

        for page in pages:

            first_published_at = page.get("date")
            last_published_at = page.get("modified")
            latest_revision_created_at = page.get("modified")

            """ 
            Process: We need to import the pages at the top level under the home page as we don't know the 
            page sitemap structure until all pages have been imported.
            
            Problem: using the wordpress slugs here means wagtail wrangles them to be unique at the top level
            
            Solution: we need to be able to fix these slugs later on still run into slugs we are again
            duplicating so lets set our own unique slug here so we can change back later without
            issue.
            """
            # these are fields that are meta data to be saved
            model_fields = {
                "owner": "",
                "description": "",
                "gateway_ref": "",
                "pcc_reference": "",
            }
            for item in page.get("model_fields"):
                for k, v in item.items():
                    model_fields[k] = v

            slug = URLParser(page.get("link")).find_slug()
            # sometimes there's external links with params so fall back to the slug fomr wordpress
            if not slug_re.match(slug):
                slug = page.get("slug")

            obj = BasePage(
                title=page.get("title"),
                slug=self.unique_slug(slug),
                excerpt=strip_tags(page.get("excerpt")),
                raw_content=page.get("content"),
                show_in_menus=True,
                author=page.get("author"),
                md_owner=model_fields["owner"],
                md_description=model_fields["description"],
                md_gateway_ref=model_fields["gateway_ref"],
                md_pcc_reference=model_fields["pcc_reference"],
                # start wordpress fields we can delete later
                wp_id=page.get("wp_id"),
                parent=page.get("parent"),
                source=page.get("source"),
                wp_template=page.get("template"),
                wp_slug=page.get("slug"),
                real_parent=page.get("real_parent") or 0,
                wp_link=page.get("link"),
                model_fields=page.get("model_fields"),
                content_fields=page.get("content_fields"),
                content_field_blocks=page.get("content_fields_blocks"),
                component_fields=page.get("component_fields"),
            )

            home_page.add_child(instance=obj)
            rev = obj.save_revision()  # this needs to run here

            obj.first_published_at = first_published_at
            obj.last_published_at = last_published_at
            obj.latest_revision_created_at = latest_revision_created_at
            # probably not the best way to do this but need to update the dates on the page record.
            obj.save()
            rev.publish()
            sys.stdout.write(".")

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return BasePage.objects.live().descendant_of(home_page).count(), self.count

    def unique_slug(self, slug):
        # 8 characters, only digits.
        random_string = get_random_string(8, "0123456789")
        if not random_string in self.random_strings:
            self.random_strings.append(random_string)
            return str(slug) + "----" + str(random_string)
        else:
            self.unique_slug(slug)
