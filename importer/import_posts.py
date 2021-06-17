import json
import sys
import time
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from django.core.management import call_command
from django.utils.html import strip_tags
from cms.categories.models import Category, CategorySubSite
from cms.pages.models import BasePage
from cms.posts.models import Post, PostCategoryRelationship, PostIndexPage
from wagtail.core.models import Page

from .importer_cls import Importer

# so we can match the subsite categories for the post index page
POST_SOURCES_TO_CATEGORY_SOURCES = {
    "posts": "categories",
    "posts-aac": "categories-aac",
    "posts-commissioning": "categories-commissioning",
    "posts-coronavirus": "categories-coronavirus",
    "posts-greenernhs": "categories-greenernhs",
    "posts-improvement-hub": "categories-improvement-hub",
    "posts-non-executive-opportunities": "categories-non-executive-opportunities",
    "posts-rightcare": "categories-rightcare",
}

# so we can a post to a sub site and build out sub site post index pages
POST_SOURCES = {
    "posts": "NHS England & Improvement",
    "posts-aac": "Accelerated Access Collaborative",
    "posts-commissioning": "Commissioning",
    "posts-coronavirus": "Corovavirus",
    "posts-greenernhs": "Greener NHS",
    "posts-improvement-hub": "Improvement Hub",
    "posts-non-executive-opportunities": "Non-executive opportunities",
    "posts-rightcare": "Right Care",
}


class PostsImporter(Importer):
    def __init__(self):
        posts = Post.objects.all()
        if posts:
            sys.stdout.write("⚠️  Run delete_posts before running this command\n")
            sys.exit()

    def parse_results(self):
        # make a posts index page for the whole site, only one to exist, call is News ...
        posts = self.results
        home_page = Page.objects.filter(title="Home")[0]

        for post in posts:
            # we need a sub_site_category for the news index page
            try:
                sub_site_category = CategorySubSite.objects.get(
                    source=POST_SOURCES_TO_CATEGORY_SOURCES[post.get("source")]
                )
            except CategorySubSite.DoesNotExist:
                sys.exit("\n😲Cannot continue... did you import the categories first?")

            # lets make a news index page if not already in place
            try:
                # we need a pretty unique name here as some imported page have the title as News
                # a parent for all news item index pages
                news_index_page = BasePage.objects.get(title="News Items Base")
            except Page.DoesNotExist:
                news_index_page = BasePage(
                    title="News Items Base",
                    body="theres a place here for some text",
                    show_in_menus=True,
                    slug="news-items-base",
                    wp_slug="auto-generated-news-index",
                    wp_id=0,
                    source="auto-generated-news-index",
                )
                home_page.add_child(instance=news_index_page)
                revision = news_index_page.save_revision()
                revision.publish()
                sys.stdout.write(".")

            try:
                sub_site_news_index_page = PostIndexPage.objects.get(
                    title=POST_SOURCES[post.get("source")]
                )
            except PostIndexPage.DoesNotExist:
                sub_site_news_index_page = PostIndexPage(
                    title=POST_SOURCES[post.get("source")],
                    body="",
                    show_in_menus=True,
                    sub_site_categories=sub_site_category,
                )
                news_index_page.add_child(instance=sub_site_news_index_page)
                rev = sub_site_news_index_page.save_revision()
                rev.publish()
                sys.stdout.write(".")

            # lets make the posts for each sub site, we're in a loop for each post here
            first_published_at = post.get("date")
            last_published_at = post.get("modified")
            latest_revision_created_at = post.get("modified")

            obj = Post(
                title=post.get("title"),
                # excerpt = post.get('excerpt'),
                # dont preset the slug coming from wordpress some are too long
                body=post.get("content"),
                show_in_menus=True,
                wp_id=post.get("wp_id"),
                author=post.get("author"),
                source=post.get("source"),
                wp_slug=post.get("slug"),
                wp_link=post.get("link"),
            )
            sub_site_news_index_page.add_child(instance=obj)
            rev = obj.save_revision()  # this needs to run here
            rev.publish()

            obj.first_published_at = first_published_at
            obj.last_published_at = last_published_at
            obj.latest_revision_created_at = latest_revision_created_at
            obj.save()
            rev.publish()
            sys.stdout.write(".")

            # add the categories as related many to many, found this needs to be after the save above
            if not not post.get("categories"):  # some categories are blank
                cats = post.get("categories").split(" ")  # list of category wp_id's
                categories = Category.objects.filter(
                    sub_site=sub_site_category, wp_id__in=cats
                )
                for cat in categories:
                    rel = PostCategoryRelationship.objects.create(
                        post=obj, category=cat
                    )
                sys.stdout.write(".")

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Post.objects.count(), self.count


class PostsParser(Importer):
    def __init__(self):
        self.tables = []
        posts = Post.objects.all()
        if not posts:
            sys.stdout.write("⚠️  Import posts before running this command\n")
            sys.exit()

    def parse_results(self):
        """
        url_path examples
        BY ID
        a_page = Page.objects.get(id='3075')
        print(a_page.url_path)
        /home/news-items-base/non-executive-opportunities/nottingham-and-nottinghamshire-integrated-care-system-ics-independent-chair/
        BY URL PATH
        a_page = Page.objects.get(url_path='/home/news-items-base/non-executive-opportunities/nottingham-and-nottinghamshire-integrated-care-system-ics-independent-chair/')
        print(a_page.id)
        SO ALL URL PATHS HAVE /home/ to start
        """

        # turns out that tables exist in the content
        # which I think is pasted in from external generator
        # it's only on a few posts but need to parse them too

        # lets find out whats in there other than anchor links

        posts = self.results

        # a_page = Page.objects.filter(title='Home')[0]
        # a_page = Page.objects.get(id='3075')
        # print(a_page.url_path)
        # a_page = Page.objects.get(url_path='/home/news-items-base/non-executive-opportunities/nottingham-and-nottinghamshire-integrated-care-system-ics-independent-chair/')
        # print(a_page.id)

        for post in posts:

            #     if post.get('post_custom_inline_links'):
            #         # get from scrapy as a list
            #         inline_anchor_links = [x for x in post.get(
            #             'post_custom_inline_links') if x.get('media') == False]

            # get the page object we are dealing with
            post_page = Post.objects.get(wp_id=post.get("wp_id"))

            # and so get the latest revision
            post_page_live_revision = post_page.get_latest_revision()

            # and get the body content_json
            body_json = json.loads(post_page_live_revision.content_json)

            soup = BeautifulSoup(body_json.get("body"), features="html5lib")

            has_table = soup.find_all("table")
            print(has_table)
            for table in has_table:
                cells = InlineTable(table).parse_table()
                self.tables.append(cells)
            print(self.tables)

            # print(self.tables)
            #         # find the anchor links

            #         print(body_json)

            # id = None

            # for anchor_link in inline_anchor_links:
            #     # loop through anchor links form scrapy
            #     url_path = '/home' + \
            #         urlparse(anchor_link.get('link_url')).path
            #     try:
            #         # try to get the wagtail page to link to
            #         page_target = Page.objects.get(url_path=url_path)
            #         id = page_target.id
            #     except Page.DoesNotExist:
            #         sys.stdout('NO PAGE EXISTS!!!')
            #         sys.exit()

            #     if id:
            #         # now aletr the link in body_json
            #         anchor_soup = soup.findAll('a')
            #         for anchor in anchor_soup:
            #             anchor_href = anchor['href']
            #             if anchor_link.get('link_url') == anchor_href:
            #                 # <a linktype="page" id="3">Contact us</a>
            #                 # here we are not making target="_blank" or rel="noopener noreferrer" as they are same site
            #                 # new_anchor = '<a linktype="page" id="{}">{}</a>'.format(id, strip_tags(anchor.contents[0]))
            #                 new_anchor = soup.new_tag(
            #                     'a', attrs={'id': 2, 'linktype': 'page', 'href':''})
            #                 print(new_anchor)
            #                 anchor.replaceWith(new_anchor)
            #                 # a = anchor.extract()
            #                 # a.previousSibling = new_anchor
            #         # print(soup)
            sys.exit()

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Post.objects.count(), self.count

    def get_anchor_link_to_page(page, link_text):
        # <a linktype="page" id="3">Contact us</a>
        return None


class InlineTable:
    def __init__(self, table_html=""):
        self.table_html = table_html
        self.table_cells = []

    def parse_table(self):
        output_rows = []
        for table_row in self.table_html.findAll("tr"):
            columns = table_row.findAll("td", "th")
            output_row = []
            for column in columns:
                output_row.append(column.text)
            output_rows.append(output_row)
        self.table_cells = output_rows
        return self.table_cells
