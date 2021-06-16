import sys
import time

from cms.blogs.models import Blog, BlogIndexPage, BlogCategoryRelationship
from cms.categories.models import Category, CategorySubSite
from wagtail.core.models import Page
from django.core.management import call_command

from .importer_cls import Importer

# blogs are not from a subsite so rewrite the source blogs to posts
# they use the same categories
POST_SOURCES_TO_CATEGORY_SOURCES = {
    "blogs": "categories",
    # 'posts-aac': 'categories-aac',
    # 'posts-commissioning': 'categories-commissioning',
    # 'posts-coronavirus': 'categories-coronavirus',
    # 'posts-greenernhs': 'categories-greenernhs',
    # 'posts-improvement-hub': 'categories-improvement-hub',
    # 'posts-non-executive-opportunities': 'categories-non-executive-opportunities',
    # 'posts-rightcare': 'categories-rightcare',
}

# so we can a post to a sub site and build out sub site post index pages
POST_SOURCES = {
    "blogs": "NHS England & Improvement",
    # 'posts-aac': 'Accelerated Access Collaborative',
    # 'posts-commissioning': 'Commissioning',
    # 'posts-coronavirus': 'Corovavirus',
    # 'posts-greenernhs': 'Greener NHS',
    # 'posts-improvement-hub': 'Improvement Hub',
    # 'posts-non-executive-opportunities': 'Non-executive opportunities',
    # 'posts-rightcare': 'Right Care',
}


class BlogsImporter(Importer):
    def __init__(self):
        blogs = Blog.objects.all()
        if blogs:
            sys.stdout.write("⚠️  Run delete_blogs before running this command\n")
            sys.exit()

    def parse_results(self):
        # make a blog index page to use for now ...
        blog_index_page = None
        home_page = Page.objects.filter(title="Home")[0]

        try:
            blog_index_page = BlogIndexPage.objects.get(title="Blog Items Base")
        except Page.DoesNotExist:
            sub_site_category = CategorySubSite.objects.get(title=POST_SOURCES["blogs"])
            blog_index_page = BlogIndexPage(
                title="Blog Items Base",
                body="theres a place here for some text",
                show_in_menus=True,
                slug="blog-items-base",
                sub_site_categories=sub_site_category,
            )
            home_page.add_child(instance=blog_index_page)
            rev = blog_index_page.save_revision()
            rev.publish()
            sys.stdout.write(".")

        blogs = self.results  # this is json result set
        for blog in blogs:
            sub_site_category = CategorySubSite.objects.get(
                source=POST_SOURCES_TO_CATEGORY_SOURCES[blog.get("source")]
            )
            first_published_at = blog.get("date")
            last_published_at = blog.get("modified")
            latest_revision_created_at = blog.get("modified")

            obj = Blog(
                title=blog.get("title"),
                # excerpt = post.get('excerpt'),
                # dont preset the slug coming from wordpress some are too long
                body=blog.get("content"),
                show_in_menus=True,
                wp_id=blog.get("wp_id"),
                author=blog.get("author"),
                source=blog.get("source"),
                wp_slug=blog.get("slug"),
                wp_link=blog.get("link"),
            )
            blog_index_page.add_child(instance=obj)
            rev = obj.save_revision()  # this needs to run here

            obj.first_published_at = first_published_at
            obj.last_published_at = last_published_at
            obj.latest_revision_created_at = latest_revision_created_at
            # probably not the best way to do this but need to update the dates on the page record.
            obj.save()
            rev.publish()

            # add the categories as related many to many, found this needs to be after the save above
            if not not blog.get("categories"):  # some categories are blank
                cats = blog.get("categories").split(" ")  # list of category wp_id's
                categories = Category.objects.filter(
                    sub_site=sub_site_category, wp_id__in=cats
                )
                for cat in categories:
                    rel = BlogCategoryRelationship.objects.create(
                        blog=obj, category=cat
                    )
                sys.stdout.write(".")

            sys.stdout.write(".")

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Blog.objects.count(), self.count
