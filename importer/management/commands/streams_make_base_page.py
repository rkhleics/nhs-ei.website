import ast
from io import BytesIO
import json
from os import link
import re
import sys
from sys import path
from typing import ItemsView
from bs4 import BeautifulSoup
from django.core.files.base import File
import requests
from html import unescape


from django.core.management import call_command
from django.core.management.base import BaseCommand
from wagtail.core.models import Collection
from wagtail.documents.models import Document
from wagtail.images.models import Image
from cms.pages.models import BasePage, ComponentsPage, LandingPage
from cms.posts.models import Post
from cms.blogs.models import Blog
from cms.publications.models import Publication
from cms.atlascasestudies.models import AtlasCaseStudy
from importer.richtextbuilder import RichTextBuilder

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

"""
http://coding.nickmoreton.co.uk:8000/rightcare/products/ccg-data-packs/long-term-conditions-packs/
example of the expander group, demostrates block with a list of items as well as a title
body = json.dumps([{
            'type': 'expander_group',
            'value': {
                'expanders': [
                    {'title': 'asdfasf', 'body': [ # title is expander text or summary from wordpress
                        {'type': 'richtext', 'value': '<p>asdfsadfa</p>'} # value is details form wordpress
                    ]
                    },
                    {'title': 'asdfasdfa', 'body': [
                        {'type': 'richtext', 'value': '<p>asdfasdfasdfsa</p>'}
                    ]
                    },
                    {'title': 'asdfasdfafasdf asd', 'body': [
                        {'type': 'richtext', 'value': '<p>asdf dfs asdfa</p>'}
                    ]
                    }
                ]
            },
        }])
example of a panel block
body = json.dumps([{
            'type': 'panel',
            'value': {
                'label': 'my label',
                'body': '1234'
            }
        }])

"""


class Command(BaseCommand):
    help = "stream fields in base pages for expander blocks"

    def __init__(self):
        # we need to loop though all the page models to generate and cache a list of
        # page url_paths to page.id to use in page chooser blocks and richtext fields.
        # seemed to be an efficient way to make the list (12,000+ pages) and use it over
        # and over later on

        models = [
            BasePage,
            # ComponentsPage,
            # Blog,
            # Post,
            # AtlasCaseStudy,
            # Publication,
            # LandingPage
        ]

        url_ids = {}  # cached

        for model in models:
            pages = model.objects.all()
            for page in pages:
                url_ids[page.url] = page.id

        self.urls = url_ids
        self.block_builder = RichTextBuilder(
            self.urls
        )  # passing the url_ids along to the RichTextBuilder
        # print(self.urls)
        # sys.exit()

    def handle(self, *args, **options):
        pages = BasePage.objects.all()
        # loop though each page look for the content_fields with default_template_hidden_text_blocks
        for page in pages:
            # keep the dates as when imported
            # if page.title == 'Join the NHS COVID-19 vaccine team':
            first_published_at = page.first_published_at
            last_published_at = page.last_published_at
            latest_revision_created_at = page.latest_revision_created_at

            body = []  # the stream field
            # get this to make a stream field
            raw_content = page.raw_content

            print("⚙️ {} parsed".format(page.title))
            # deal first with wysiwyg from wordpress
            if raw_content:
                raw_content_block = self.make_panel_block(raw_content)
                body.append(raw_content_block)

            # then add any content fields if a field block has been used
            if page.content_fields:
                content_fields = ast.literal_eval(page.content_fields)
                for field in content_fields:
                    keys = field.keys()
                    for key in keys:
                        if key == "default_template_hidden_text_blocks":
                            print(page)
                            if len(ast.literal_eval(page.content_field_blocks)) > 0:
                                content_blocks = self.make_expander_group_block(
                                    ast.literal_eval(page.content_field_blocks), page
                                )
                                body.append(content_blocks)

                page.body = json.dumps(body)

                # dealing with unicode in title
                page.title = unescape(page.title)

                rev = page.save_revision()
                page.first_published_at = first_published_at
                page.last_published_at = last_published_at
                page.latest_revision_created_at = latest_revision_created_at
                page.save()
                rev.publish()

    def make_expander_group_block(self, content, page):
        """
        {
            'type': 'expander_group',
            'value': {
                'expanders': [
                    {'title': 'asdfasf', 'body': [
                        {'type': 'richtext', 'value': '<p>asdfsadfa</p>'}
                    ]
                    },
                    {'title': 'asdfasdfa', 'body': [
                        {'type': 'richtext', 'value': '<p>asdfasdfasdfsa</p>'}
                    ]
                    },
                    {'title': 'asdfasdfafasdf asd', 'body': [
                        {'type': 'richtext', 'value': '<p>asdf dfs asdfa</p>'}
                    ]
                    }
                ]
            },
        }
        """

        # block_title = {}

        print(page)
        block_group = {
            "type": "expander_group",
            "value": {"expanders": []},
        }
        for field in content:
            # pass
            # a title needed if present field['title']
            for item in field["items"]:
                self.block_builder.extract_links(item["detail"], page)
                item_detail = item["detail"]
                for link in self.block_builder.change_links:
                    item_detail = item_detail.replace(str(link[0]), str(link[1]))
                block_item = {
                    "title": item["summary"],
                    "body": [{"type": "richtext", "value": item_detail}],
                }
                block_group["value"]["expanders"].append(block_item)

        return block_group

    def make_panel_block(self, content):
        """
        {
            'type': 'panel',
            'value': {
                'label': 'optional label',
                'body': 'required body'
            }
        }
        """
        # rich_text = self.block_builder.extract_links(content)
        self.block_builder.extract_links(content)
        content = content
        for link in self.block_builder.change_links:
            content = content.replace(str(link[0]), str(link[1]))
        block = {
            "type": "panel",
            "value": {
                "label": "",
                # this is the default, might want to change it...
                "heding_level": "3",
                # after it's been parsed for links
                "body": content,
            },
        }

        return block


# def convert_inline_links(content):
#     # BS4 to get a handle on all the anchor links

#     content_base = content
#     soup = BeautifulSoup(content, features="html5lib")

#     links = soup.find_all('a', href=re.compile(
#         r"^https://www.england.nhs.uk/"))

#     for link in links:
#         # print(link)
#         old_url = link['href']
#         separator = '/'
#         old_path = '/home/' + separator.join(old_url.split('/')[3:])

#         try:
#             page = BasePage.objects.get(url_path=old_path)
#             page_id = page.id

#             new_link = '<a id="{}" linktype="page">{}</a>'.format(
#                 page_id, link.text)
#             # print(link, new_link)
#             content_base.replace(str(link), new_link)
#         except BasePage.DoesNotExist:
#             print(link)
#     # print(content_base)

#     # print(content_base)
#     # sys.exit()

#     return content_base

#     # for i in range(0, len(links)):
#     #     document = None
#     #     file = None
#     #     link_url = links[i]['href']  # the link url
#     #     if link_url.endswith('.pdf'):
#     #         file_title = link_url.split('/')[-1]
#     #         file = link_url
#     #         document = get_and_save_media('Documents', file, file_title)
#     #     elif link_url.endswith('.xlsx'):
#     #         file_title = link_url.split('/')[-1]
#     #         file = link_url
#     #         document = get_and_save_media('Sheets', file, file_title)

#     #     if document:
#     #         content = replace_anchor_link(content, document, file)


# def extract_content_inline_links(content):
#     """parse each link to the neccessary details so we can reconstruct in blocks
#     along with .pdf, docs, xlsx files"""

#     # content = '<ul><li><u><a href="https://www.england.nhs.uk/rightcare/wp-content/uploads/sites/40/2016/08/cfv-barking-and-dagenham-ltc.pdf" class="pdf-link">Barking and Dagenham CCG</a></u></li><li><u><a href="https://www.england.nhs.uk/rightcare/wp-content/uploads/sites/40/2016/08/cfv-barnet-ltc.pdf" class="pdf-link">Barnet CCG</a></u></li><li><a href="https://www.england.nhs.uk/rightcare/wp-content/uploads/sites/40/2017/02/data-used-ltc-2016.xlsx" class="xls-link">Data used in the 2016 Long term conditions packs and tools</a></li></ul>'

#     # try:
#     #     collection = Collection.objects.get(
#     #         name='Documents',
#     #     )
#     # except Collection.DoesNotExist:
#     #     root_collection = Collection.get_first_root_node()
#     #     collection = root_collection.add_child(
#     #         name='Documents',
#     #     )

#     # try:
#     #     collection = Collection.objects.get(
#     #         name='Sheets',
#     #     )
#     # except Collection.DoesNotExist:
#     #     root_collection = Collection.get_first_root_node()
#     #     collection = root_collection.add_child(
#     #         name='Sheets',
#     #     )

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
