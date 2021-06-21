import ast
import json
import re
from html import unescape
from io import BytesIO
from os import link
import sys
from django.utils.html import strip_tags
import logging

import requests
from bs4 import BeautifulSoup
from django.core.files.base import File
from django.core.management import call_command
from django.core.management.base import BaseCommand
from cms.pages.models import BasePage, ComponentsPage, LandingPage
from importer.importer_cls import ComponentsBuilder
from wagtail.core.models import Collection
from wagtail.documents.models import Document
from wagtail.images.models import Image

logger = logging.getLogger("importer")
logger.critical(
    "Entered parse_stream_fields_landing_pages: here be TODO dragons stacked nine high."
)

"""TODO TODO TODO TODO TODO TODO TODO TODO TODO """

# https://www.caktusgroup.com/blog/2019/09/12/wagtail-data-migrations/

# <a id="3" linktype="page">link</a> link to a page
# <a id="1" linktype="document">link</a> link to a doc
# <a href="mailto:nick@nick.com">link</a> email link
# <a href="tel:01212">0121</a> phone link
# tables show ok but disapear after any save in the admin

# Super big note:
# after the pages are all imported plus all other content we need to move page content into blocks
# everything is a stream field, has to be that way for imported pages, possibly posts and blogs too...
# LINKS during this parsing and rich text fields need to be altered to consider internal liks to page types
# need to find the page link id for the stream field anchor
# DOWNLOADS and docs, and anythiong else that pops up
# need to get and upload documents
# IMAGES they too need to be uploaded to image manager and linked accordingly, well set everything to left align for now
########

"""TODO TODO TODO TODO TODO TODO TODO TODO TODO """


class Command(BaseCommand):
    help = "parsing stream fields component pages"

    def handle(self, *args, **options):
        pages = LandingPage.objects.all()
        component_types = []  # just for dev to check we have them all
        """
        [
            'promo_component', # parse
            'article_component', # parse
            'two_columns_section', # parse
            'topic_section_component', # parse
            'breadcrumbs', ###
            'visit_nhsuk_infobar', 
            'priorities_component'
        """
        # loop though each page look for the content_fields with default_template_hidden_text_blocks
        for page in pages:
            # keep the dates as when imported
            first_published_at = page.first_published_at
            last_published_at = page.last_published_at
            latest_revision_created_at = page.latest_revision_created_at

            body = []  # the stream field
            # get this to make a stream field
            # raw_content = page.raw_content

            # if page.title == 'Email bulletins':
            #     print(page.component_fields)

            # print('{} parsed'.format(page.title))
            # deal first with wysiwyg from wordpress
            # if raw_content:
            #     raw_content_block = self.make_panel_block(raw_content)
            #     body.append(raw_content_block)

            # then add any content fields if a field block has been used

            if page.content_fields:
                print(page, page.id)
                components = ast.literal_eval(page.content_fields)[0]
                builder = ComponentsBuilder(ast.literal_eval(components))
                blocks = builder.make_blocks()
                body = blocks

            # page.body = json.dumps(body)

            # # dealing with unicode in title
            # page.title = unescape(page.title)

            # rev = page.save_revision()
            # page.first_published_at = first_published_at
            # page.last_published_at = last_published_at
            # page.latest_revision_created_at = latest_revision_created_at
            # page.save()
            # rev.publish()

            # if page.title == 'About us':
            #     sys.exit()


# def parse_html_for_links(self, content):
#     return content


# def extract_content_inline_links(content):
#     """parse each link to the neccessary details so we can reconstruct in blocks
#     along with .pdf, docs, xlsx files"""

#     content = '<ul><li><u><a href="https://www.england.nhs.uk/rightcare/wp-content/uploads/sites/40/2016/08/cfv-barking-and-dagenham-ltc.pdf" class="pdf-link">Barking and Dagenham CCG</a></u></li><li><u><a href="https://www.england.nhs.uk/rightcare/wp-content/uploads/sites/40/2016/08/cfv-barnet-ltc.pdf" class="pdf-link">Barnet CCG</a></u></li><li><a href="https://www.england.nhs.uk/rightcare/wp-content/uploads/sites/40/2017/02/data-used-ltc-2016.xlsx" class="xls-link">Data used in the 2016 Long term conditions packs and tools</a></li></ul>'

#     try:
#         collection = Collection.objects.get(
#             name='Documents',
#         )
#     except Collection.DoesNotExist:
#         root_collection = Collection.get_first_root_node()
#         collection = root_collection.add_child(
#             name='Documents',
#         )

#     try:
#         collection = Collection.objects.get(
#             name='Sheets',
#         )
#     except Collection.DoesNotExist:
#         root_collection = Collection.get_first_root_node()
#         collection = root_collection.add_child(
#             name='Sheets',
#         )

#     # BS4 to get a handle on all the anchor links
#     soup = BeautifulSoup(content, features="html5lib")
#     links = soup.find_all('a', href=re.compile(
#         r"^https://www.england.nhs.uk/"))

#     for i in range(0, len(links)):
#         document = None
#         file = None
#         link_url = links[i]['href']  # the link url
#         if link_url.endswith('.pdf'):
#             file_title = link_url.split('/')[-1]
#             file = link_url
#             document = get_and_save_media('Documents', file, file_title)
#         elif link_url.endswith('.xlsx'):
#             file_title = link_url.split('/')[-1]
#             file = link_url
#             document = get_and_save_media('Sheets', file, file_title)

#         if document:
#             content = replace_anchor_link(content, document, file)

#     # return content


# def replace_anchor_link(html_content, document, url):
#     content = html_content
#     print(url)
#     print(content)
#     content.replace(url, '1234')
#     print(content)
#     # regex = re.compile(r'<a\s+href\s*=\s*"([^"]+).*')
#     # [re.sub(regex, r"\1", string) for string in content]
#     return content


# def get_and_save_media(file_type, file_url, file_title):
#     # download the file contents in binary format
#     r = requests.get(file_url, stream=True)
#     # open method to open a file and write the contents of the response
#     # with open(file_url, "wb") as f:
#     file_path = BytesIO()
#     file_path.write(r.content)
#     file_path.write(r.content)
#     # f.write(r.content)

#     document = None

#     if file_type == 'Documents':
#         collection = Collection.objects.get(name=file_type)
#         document = Document.objects.create(
#             collection=collection,
#             title=file_title
#         )
#         document.file.save('my title', File(file_path))
#     elif file_type == 'Sheets':
#         collection = Collection.objects.get(name=file_type)
#         document = Document.objects.create(
#             collection=collection,
#             title=file_title
#         )
#         document.file.save('my title', File(file_path))

#     return document


# def clean_string(string):
#     s = string.replace('\n', '')
#     s = s.replace('\t', '')
#     clean = s.strip()
#     return clean
