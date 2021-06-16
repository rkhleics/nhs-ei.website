import sys

from django.core.management.base import BaseCommand
from cms.blogs.models import BlogIndexPage
from cms.pages.models import BasePage
from cms.atlascasestudies.models import AtlasCaseStudyIndexPage
from wagtail.core.models import Page


class Command(BaseCommand):
    """
    the purpose of this module is to fix pages slugs.
    during the first import they get incremented by wagtail to make the slugs unique
    once moved into place by movepages.py they can be corrected to the slug
    in SCRAPY
    """

    help = "Fixes page slugs for some landing pages"

    def handle(self, *args, **options):

        home_page = Page.objects.filter(title="Home")[0]

        """some edge case pages"""
        # change blog-items-base slug to
        try:
            blog_items_base = BlogIndexPage.objects.get(slug="blog-items-base")

            first_published = blog_items_base.first_published_at
            last_published = blog_items_base.last_published_at
            latest_revision_created = blog_items_base.latest_revision_created_at

            blog_items_base.slug = "blog"
            blog_items_base.title = "Blogs"

            rev = blog_items_base.save_revision()
            blog_items_base.first_published_at = first_published
            blog_items_base.last_published_at = last_published
            blog_items_base.latest_revision_created_at = latest_revision_created
            blog_items_base.save()
            rev.publish()
        except BlogIndexPage.DoesNotExist:
            sys.stdout.write("\n✅  Blog Index Slug Already Changed\n")

        # change news-items-base slug to
        try:
            news_items_base = BasePage.objects.get(slug="news-items-base")

            delete_old_page = BasePage.objects.child_of(home_page).filter(slug="news")
            delete_old_page.delete()

            first_published = news_items_base.first_published_at
            last_published = news_items_base.last_published_at
            latest_revision_created = news_items_base.latest_revision_created_at

            news_items_base.slug = "news"
            news_items_base.title = "News"

            rev = news_items_base.save_revision()
            news_items_base.first_published_at = first_published
            news_items_base.last_published_at = last_published
            news_items_base.latest_revision_created_at = latest_revision_created
            news_items_base.save()
            rev.publish()
        except BasePage.DoesNotExist:
            sys.stdout.write("\n✅  News Index Slug Already Changed\n")

        # change publication-items-base slug to
        try:
            publication_items_base = BasePage.objects.get(slug="publication-items-base")

            # delete_old_page = BasePage.objects.child_of(home_page).filter(slug='news')
            # delete_old_page.delete()

            first_published = publication_items_base.first_published_at
            last_published = publication_items_base.last_published_at
            latest_revision_created = publication_items_base.latest_revision_created_at

            publication_items_base.slug = "publication"
            publication_items_base.title = "Publications"

            rev = publication_items_base.save_revision()
            publication_items_base.first_published_at = first_published
            publication_items_base.last_published_at = last_published
            publication_items_base.latest_revision_created_at = latest_revision_created
            publication_items_base.save()
            rev.publish()
        except BasePage.DoesNotExist:
            sys.stdout.write("\n✅  News Index Slug Already Changed\n")

        # change atlas-case-study-items-base slug to
        try:
            atlas_case_study_items_base = AtlasCaseStudyIndexPage.objects.get(
                slug="atlas-case-study-items-base"
            )

            first_published = atlas_case_study_items_base.first_published_at
            last_published = atlas_case_study_items_base.last_published_at
            latest_revision_created = (
                atlas_case_study_items_base.latest_revision_created_at
            )

            atlas_case_study_items_base.slug = "atlas_case_study"
            atlas_case_study_items_base.title = "Atlas Case Studies"

            rev = atlas_case_study_items_base.save_revision()
            atlas_case_study_items_base.first_published_at = first_published
            atlas_case_study_items_base.last_published_at = last_published
            atlas_case_study_items_base.latest_revision_created_at = (
                latest_revision_created
            )
            atlas_case_study_items_base.save()
            rev.publish()
        except BasePage.DoesNotExist:
            sys.stdout.write("\n✅  Atlas Case Studies Index Slug Already Changed\n")

        sys.stdout.write("\n✅  All slugs fixed\n")
