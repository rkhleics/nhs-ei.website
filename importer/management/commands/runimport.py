from importer.import_media_files import MediaFilesImporter
import sys
import time

from django.core.management import call_command
from django.core.management.base import BaseCommand
from importer.import_atlas_case_studies import AtlasCaseStudiesImporter
from importer.import_blogs import BlogsImporter
from importer.import_categories import CategoriesImporter
from importer.import_pages import PagesImporter
from importer.import_posts import PostsImporter, PostsParser
from importer.import_publication_types import PublicationTypesImporter
from importer.import_publications import PublicationsImporter
from importer.import_regions import RegionsImporter
from importer.import_settings import SettingsImporter

from importer.websites import SCRAPY


def get_api_url(app):
    if app == "categories":
        return SCRAPY + "api/categories/"
    if app == "publication_types":
        return SCRAPY + "api/publication_types/"
    if app == "settings":
        return SCRAPY + "api/settings/"
    if app == "regions":
        return SCRAPY + "api/regions/"
    if app == "tags":
        return SCRAPY + "api/tags/"
    if app == "pages":
        return SCRAPY + "api/pages/"
    if app == "posts":
        return SCRAPY + "api/posts/"
    if app == "publications":
        return SCRAPY + "api/publications/"
    if app == "atlas_case_studies":
        return SCRAPY + "api/atlas_case_studies/"
    if app == "blogs":
        return SCRAPY + "api/blogs/"
    if app == "media":
        return SCRAPY + "api/media_files"


"""
./manage.py runimport app
"""


class Command(BaseCommand):
    help = "Imports an apps records from the API. \
        available apps: categories, publication_types, settings, regions, pages, posts, blogs, publications, atlascasestudies"

    def add_arguments(self, parser):
        parser.add_argument("app", type=str, help="The APP to import")

    def handle(self, *args, **options):

        # the magic happens here e.g. getting initial api url then looping through items
        # and parsing the results. There's no other models involved except the one for each app
        # might we want to log it?

        # categories
        if options["app"] == "categories":  # categories
            self.stdout.write("⌛️ Initialising Categories Import \n")
            import_categories(get_api_url("categories"))

        if options["app"] == "publication_types":  # publications types
            self.stdout.write("⌛️ Initialising Publication Types Import \n")
            import_publication_types(get_api_url("publication_types"))

        if options["app"] == "settings":  # settings
            self.stdout.write("⌛️ Initialising Settings Import \n")
            import_settings(get_api_url("settings"))

        if options["app"] == "regions":  # regions
            self.stdout.write("⌛️ Initialising Regions Import \n")
            import_regions(get_api_url("regions"))

        if options["app"] == "posts":  # posts
            self.stdout.write("⌛️ Initialising Posts Import \n")
            import_posts(get_api_url("posts"))

        if options["app"] == "publications":  # publications
            self.stdout.write("⌛️ Initialising Publications Import \n")
            import_publications(get_api_url("publications"))

        if options["app"] == "atlas_case_studies":  # atlas case studies
            self.stdout.write("⌛️ Initialising Atlas Case Studies Import \n")
            import_atlas_case_studies(get_api_url("atlas_case_studies"))

        if options["app"] == "pages":  # pages
            self.stdout.write("⌛️ Initialising Pages Import \n")
            import_pages(get_api_url("pages"))

        if options["app"] == "blogs":  # blogs
            self.stdout.write("⌛️ Initialising Blogs Import \n")
            import_blogs(get_api_url("blogs"))

        if options["app"] == "media":  # media
            self.stdout.write("⌛️ Initialising Media Files Import \n")
            import_media_files(get_api_url("media"))

        if options["app"] == "all":
            # the whole lot in specific order
            # BEFORE ALL OTHERS as related keys exists
            # import_media_files(get_api_url('media'))
            import_categories(get_api_url("categories"))
            import_publication_types(get_api_url("publication_types"))
            import_settings(get_api_url("settings"))
            import_regions(get_api_url("regions"))
            # END BEFORE ALL OTHERS
            # pages needs to run here because later commands
            # create pages that prevent this script from running
            import_pages(get_api_url("pages"))
            import_posts(get_api_url("posts"))
            import_blogs(get_api_url("blogs"))
            import_publications(get_api_url("publications"))
            import_atlas_case_studies(get_api_url("atlas_case_studies"))

        if options["app"] == "build":
            call_command("page_mover")
            call_command("fix_slugs")
            call_command("swap_page_types")
            call_command("fix_component_page_slugs")
            call_command("fix_landing_page_slugs")
            call_command("swap_blogs_page")

        # this needs to run before 'fixes' because links go to images and files
        # as well as pages and also 'documents' needs the files
        if options["app"] == "mediafiles":
            # there's nothing more than a long process here
            # that collescts every media file form wordpress
            # and stores them in collection related to the subsite
            # names they come from. They are linked up in later scripts.
            import_media_files(get_api_url("media"))

        if options["app"] == "fixes":
            # some of the existing pages here get initial content
            # coming over form word press and when some page
            # types are changed that content comes with them
            # it's added to and adjusted in later scripts
            call_command("parse_stream_fields", "prod")
            call_command(
                "parse_stream_fields_component_pages", "prod"
            )  # here we have url issue

        if options["app"] == "makes":
            # TODO python manage.py parse_stream_fields_landing_pages  we need the blog autors may be do other stuff here first???
            call_command("make_top_pages")
            call_command("make_alert_banner")
            call_command("make_home_page")
            call_command("make_footer_links")

        if options["app"] == "documents":
            call_command("make_documents_list")

            """ other commands to add in
            # make any other pages we need
            # here we have url issue
            make documents 
             # this needs to be last ones so pages are all in place
            make footer links
            """

            """
            python manage.py page_mover
            python manage.py fix_slugs
            python manage.py fix_slugs_sub_sites
            python manage.py swap_page_types
            python manage.py fix_component_page_slugs
            python manage.py fix_landing_page_slugs
            python manage.py swap_blogs_page
            python manage.py parse_stream_fields
            python manage.py parse_stream_fields_component_pages
            TODO python manage.py parse_stream_fields_landing_pages  we need the blog autors may be do other stuff here first???
            python manage.py make_alert_banner
            python manage.py make_home_page
            """

        # if options['app'] == 'parse_posts_body':
        #     parse_posts_body(get_api_url('posts'))


# def run_build_commands():
#     call_command('page_mover')
#     call_command('fix_slugs')
#     call_command('fix_slugs_sub_sites')
#     call_command('swap_page_types')
#     call_command('fix_component_page_slugs')
#     call_command('fix_landing_page_slugs')
#     call_command('swap_blogs_page')
#     call_command('parse_stream_fields')
#     call_command('parse_stream_fields_component_pages') # here we have url issue
#     # TODO python manage.py parse_stream_fields_landing_pages  we need the blog autors may be do other stuff here first???
#     call_command('make_alert_banner')
#     call_command('make_home_page')
#     """ other commands to add in
#     make documents # here we have url issue
#     """

# def parse_posts_body(url):
#     if not url:
#         raise Exception('url error')
#     posts_parser = PostsParser()
#     fetch = posts_parser.fetch_url(url)
#     completed_count = 0
#     api_count = 0
#     if fetch:
#         completed_count, api_count = posts_parser.parse_results()

# a final check to report actual imports to be done vs records in the table
# if api_count == completed_count:
#     sys.stdout.write(
#         '\n✅ {} Posts imported'.format(completed_count))
# elif api_count > completed_count:
#     sys.stdout.write(
#         '\n😲 SOMETHING IS WRONG the record count is lower then the available records')
# elif api_count < completed_count:
#     sys.stdout.write(
#         '\n😲 SOMETHING IS WRONG the record count is higher then the available records (did you forget the delete option?)')

# sys.stdout.write('\n')


def import_media_files(url):
    if not url:
        raise Exception("url error")
    media_files_importer = MediaFilesImporter()
    fetch = media_files_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = media_files_importer.parse_results()

    sys.stdout.write("\n✅ Media Files imported")
    # a final check to report actual imports to be done vs records in the table
    # if api_count == completed_count:
    #     sys.stdout.write(
    #         '\n✅ {} Media Files imported'.format(completed_count))
    # elif api_count > completed_count:
    #     sys.stdout.write(
    #         '\n😲 SOMETHING IS WRONG the record count is lower then the available records')
    # elif api_count < completed_count:
    #     sys.stdout.write(
    #         '\n😲 SOMETHING IS WRONG the record count is higher then the available records (did you forget the delete option?)')

    sys.stdout.write("\n")


def import_categories(url):
    if not url:
        raise Exception("url error")
    categories_importer = CategoriesImporter()
    fetch = categories_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = categories_importer.parse_results()

    # a final check to report actual imports to be done vs records in the table
    if api_count == completed_count:
        sys.stdout.write("\n✅ {} Categories imported".format(completed_count))
    elif api_count > completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is lower then the available records"
        )
    elif api_count < completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is higher then the available records (did you forget the delete option?)"
        )

    sys.stdout.write("\n")


def import_publication_types(url):
    if not url:
        raise Exception("url error")
    publication_types_importer = PublicationTypesImporter()
    fetch = publication_types_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = publication_types_importer.parse_results()

    # a final check to report actual imports to be done vs records in the table
    if api_count == completed_count:
        sys.stdout.write("\n✅ {} Publication Types imported".format(completed_count))
    elif api_count > completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is lower then the available records"
        )
    elif api_count < completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is higher then the available records (did you forget the delete option?)"
        )

    sys.stdout.write("\n")


def import_atlas_case_studies(url):
    if not url:
        raise Exception("url error")
    atlas_case_studies_importer = AtlasCaseStudiesImporter()
    fetch = atlas_case_studies_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = atlas_case_studies_importer.parse_results()

    # a final check to report actual imports to be done vs records in the table
    if api_count == completed_count:
        sys.stdout.write("\n✅ {} Atals Case Studies imported".format(completed_count))
    elif api_count > completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is lower then the available records"
        )
    elif api_count < completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is higher then the available records (did you forget the delete option?)"
        )

    sys.stdout.write("\n")


def import_settings(url):
    if not url:
        raise Exception("url error")
    settings_importer = SettingsImporter()
    fetch = settings_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = settings_importer.parse_results()

    # a final check to report actual imports to be done vs records in the table
    if api_count == completed_count:
        sys.stdout.write("\n✅ {} Settings imported".format(completed_count))
    elif api_count > completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is lower then the available records"
        )
    elif api_count < completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is higher then the available records (did you forget the delete option?)"
        )

    sys.stdout.write("\n")


def import_regions(url):
    if not url:
        raise Exception("url error")
    regions_importer = RegionsImporter()
    fetch = regions_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = regions_importer.parse_results()

    # a final check to report actual imports to be done vs records in the table
    if api_count == completed_count:
        sys.stdout.write("\n✅ {} Regions imported".format(completed_count))
    elif api_count > completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is lower then the available records"
        )
    elif api_count < completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is higher then the available records (did you forget the delete option?)"
        )

    sys.stdout.write("\n")


def import_posts(url):
    if not url:
        raise Exception("url error")
    posts_importer = PostsImporter()
    fetch = posts_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = posts_importer.parse_results()

    # a final check to report actual imports to be done vs records in the table
    if api_count == completed_count:
        sys.stdout.write("\n✅ {} Posts imported".format(completed_count))
    elif api_count > completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is lower then the available records"
        )
    elif api_count < completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is higher then the available records (did you forget the delete option?)"
        )

    sys.stdout.write("\n")


def import_publications(url):
    if not url:
        raise Exception("url error")
    publications_importer = PublicationsImporter()
    fetch = publications_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = publications_importer.parse_results()

    # a final check to report actual imports to be done vs records in the table
    if api_count == completed_count:
        sys.stdout.write("\n✅ {} Publications imported".format(completed_count))
    elif api_count > completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is lower then the available records"
        )
    elif api_count < completed_count:
        sys.stdout.write(
            "\n😲 SOMETHING IS WRONG the record count is higher then the available records (did you forget the delete option?)"
        )

    sys.stdout.write("\n")


def import_blogs(url):
    if not url:
        raise Exception("url error")
    blogs_importer = BlogsImporter()
    fetch = blogs_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = blogs_importer.parse_results()

    # a final check to report actual imports to be done vs records in the table
    if api_count == completed_count:
        sys.stdout.write("EXCELLENT ✅ the record count matches the available records\n")
    elif api_count > completed_count:
        sys.stdout.write(
            "SOMETHING IS WRONG 😲 the record count is lower then the available records\n"
        )
    elif api_count < completed_count:
        sys.stdout.write(
            "SOMETHING IS WRONG 😲 the record count is higher then the available records (did you forget the delete option?)\n"
        )

    sys.stdout.write("{} Blogs are now imported :) \n".format(completed_count))


def import_pages(url):
    if not url:
        raise Exception("url error")
    pages_all_importer = PagesImporter()
    fetch = pages_all_importer.fetch_url(url)
    completed_count = 0
    api_count = 0
    if fetch:
        completed_count, api_count = pages_all_importer.parse_results()

    # a final check to report actual imports to be done vs records in the table
    if api_count == completed_count:
        sys.stdout.write("EXCELLENT ✅ the record count matches the available records\n")
    elif api_count > completed_count:
        sys.stdout.write(
            "SOMETHING IS WRONG 😲 the record count is lower then the available records\n"
        )
    elif api_count < completed_count:
        sys.stdout.write(
            "SOMETHING IS WRONG 😲 the record count is higher then the available records (did you forget the delete option?)\n"
        )

    sys.stdout.write("{} Pages are now imported :) \n".format(completed_count))
