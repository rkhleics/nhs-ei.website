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
from django.core.files.images import ImageFile
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
# <a href="#myanchorlink">anchor link</a> anchor link is normal but need to remove before #
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
example of the expander group, demostrates block with a list of items
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

example of table
https://www.england.nhs.uk/ig/ig-resources/
"""


TEST_DATA_SET_PAGE_TITLES = [
    "Always Events",
    "Coronavirus guidance for clinicians and NHS managers",
]


class Command(BaseCommand):
    help = "parsing stream fields"

    def __init__(self):
        models = [
            BasePage,
            ComponentsPage,
            Blog,
            Post,
            AtlasCaseStudy,
            Publication,
            LandingPage,
        ]

        self.url_map = {}  # cached

        for model in models:
            pages = model.objects.all()
            for page in pages:
                self.url_map[page.url] = {
                    "id": page.id,
                    "slug": page.slug,
                    "title": page.title,
                }

        self.block_builder = RichTextBuilder(self.url_map)

        with open("importer/log/forms_found.txt", "w") as the_file:
            the_file.write("a list of forms found during import\n")

    def add_arguments(self, parser):
        parser.add_argument(
            "mode", type=str, help="Run as development with reduced recordsets"
        )

    def handle(self, *args, **options):
        pages = []
        if options["mode"] == "dev":
            """# dev get a small set of pages"""
            base_parent = BasePage.objects.get(wp_id=159085, source="pages")
            print("Starting from: {}".format(base_parent.title))
            components_parent = ComponentsPage.objects.get(
                wp_id=5, source="pages-coronavirus"
            )  # /coronavirus/
            base_pages = BasePage.objects.descendant_of(base_parent, inclusive=True)
            base_pages_under_components_page = BasePage.objects.descendant_of(
                components_parent, inclusive=True
            )
            pages = []
            for page in base_pages:
                pages.append(page)
            for page in base_pages_under_components_page:
                pages.append(page)

        if options["mode"] == "prod":
            """get all the pages"""
            pages = BasePage.objects.all()
        # pages_count = pages.count()
        # loop though each page look for the content_fields with default_template_hidden_text_blocks
        # counter = pages_count
        for page in pages:
            sys.stdout.write("⌛️ {} processing...\n".format(page))
            # keep the dates as when imported
            # if page.title == 'Join the NHS COVID-19 vaccine team':
            first_published_at = page.first_published_at
            last_published_at = page.last_published_at
            latest_revision_created_at = page.latest_revision_created_at

            body = []  # the stream field
            # get this to make a stream field
            raw_content = page.raw_content

            # print('⚙️  {}'.format(page.title))
            # deal first with wysiwyg from wordpress
            # """ cant deal with forms, needs investigating """
            # no_forms = True
            if raw_content and "<form action=" in raw_content:
                with open("importer/log/forms_found.txt", "a") as the_file:
                    the_file.write("{} | {} | {}\n".format(page, page.id, page.wp_link))
            #     no_forms = False
            # if raw_content and no_forms:
            if raw_content:
                # line breaks mess up bs4 parsing, we dont need them anyway :)
                raw_content = raw_content.replace("\n", "")
                raw_content_block = self.make_text_block(raw_content, page)

                for row in raw_content_block:
                    body.append(row)

            # then add any content fields if a field block has been used
            # AFAIK these are always after the body
            if page.content_fields:
                content_fields = ast.literal_eval(page.content_fields)
                for field in content_fields:
                    keys = field.keys()
                    for key in keys:
                        if (
                            key == "default_template_hidden_text_blocks"
                            and field["default_template_hidden_text_blocks"] != "False"
                        ):
                            # if len(page.content_fields) > 0:
                            content_fields = self.make_expander_group_block(
                                page.content_fields, page
                            )
                            for field in content_fields:
                                body.append(field)

                            # body.append(content_blocks)

            # print(body)
            # sys.exit()
            page.body = json.dumps(body)

            # dealing with unicode in title
            page.title = unescape(page.title)

            rev = page.save_revision()
            page.first_published_at = first_published_at
            page.last_published_at = last_published_at
            page.latest_revision_created_at = latest_revision_created_at
            page.save()
            rev.publish()

            sys.stdout.write("✅ {} done\n".format(page))

            # counter -=1
            # print(counter)

            # if page.id == 1420:
            #     print(body)

    def make_text_block(self, content, page):
        # here need to see whats in there and pull out specials like tables and so on
        # into their own block type
        # so far TABLE https://service-manual.nhs.uk/design-system/components/table

        block_group = self.find_content_types_to_make_blocks(
            content, page
        )  # all the elements pulled out as we find them

        return block_group

    def find_content_types_to_make_blocks(self, content, page):

        TAGS_TO_BLOCKS = ["table", "iframe"]

        REMOVE_ATTRIBUTES = [
            "lang",
            "language",
            "onmouseover",
            "onmouseout",
            "script",
            "style",
            "font",
            "dir",
            "face",
            "size",
            "color",
            "style",
            "class",
            "width",
            "height",
            "hspace",
            "border",
            "valign",
            "align",
            "background",
            "bgcolor",
            "text",
            "link",
            "vlink",
            "alink",
            "cellpadding",
            "cellspacing",
        ]

        soup = BeautifulSoup(content, "lxml", exclude_encodings=True)

        iframes = soup.find_all("iframe")

        # '[document]' means leave it alone
        IFRAME_POSSIBLE_PARENTS = ["p", "div", "span"]

        for iframe in iframes:
            parent = iframe.previous_element
            if parent.name in IFRAME_POSSIBLE_PARENTS:
                # print(parent)
                parent.replaceWith(iframe)

        for attribute in REMOVE_ATTRIBUTES:
            for tag in soup.find_all(attrs={attribute: True}):
                del tag[attribute]

        soup = soup.find("body").findChildren(recursive=False)

        blocks = []
        block_value = ""
        counter = 0

        for tag in soup:

            counter += 1

            """
            the process here loops though each soup tag to discover the block type to use
            there's a table and iframe block to deal with if they exist
            """

            # print(tag.name)
            if not tag.name in TAGS_TO_BLOCKS:

                images = tag.find_all("img")

                # img.replaceWith(new_image)
                # it's a simple text field so concat all text
                # self.block_builder.extract_img(str(tag), page)
                self.block_builder.extract_links(str(tag), page)
                linked_html = str(tag)
                for link in self.block_builder.change_links:
                    linked_html = linked_html.replace(str(link[0]), str(link[1]))

                # replace any img elements with str.replace, problem uploading image
                # as cant get correct src so missing images are marked and logged
                for img in images:
                    img_string = str(img)
                    src = (
                        "original_images/" + img.get("src").split("/")[-1]
                    )  # need the last part
                    alt = img.get("alt")
                    new_image = None
                    try:
                        image = Image.objects.get(file=src)
                        new_image = self.block_builder.make_image_embed(
                            image.id, alt, "fullwidth"
                        )
                        linked_html = linked_html.replace(img_string, new_image)
                    except Image.DoesNotExist:
                        # print('missing image')
                        with open(
                            "importer/log/media_document_not_found.txt", "a"
                        ) as the_file:
                            the_file.write(
                                "{} | {} | {}\n".format(img["src"], page, page.id)
                            )
                    if not new_image:
                        linked_html = (
                            linked_html + '<h3 style="color:red">missing image</h3>'
                        )
                block_value += linked_html

            if tag.name == "table":

                if len(block_value) > 0:
                    blocks.append({"type": "text", "value": block_value})
                    block_value = ""
                blocks.append({"type": "html", "value": str(tag)})

            if tag.name == "iframe":

                if len(block_value) > 0:
                    blocks.append({"type": "text", "value": block_value})
                    block_value = ""
                blocks.append(
                    {
                        "type": "html",
                        "value": '<div class="core-custom"><div class="responsive-iframe">{}</div></div>'.format(
                            str(tag)
                        ),
                    }
                )

            if counter == len(soup) and len(block_value) > 0:
                # when we reach the end and somehing is in the
                # block_value just output and clear

                blocks.append({"type": "text", "value": block_value})
                block_value = ""

        return blocks

    def make_expander_group_block(self, content, page):
        content = ast.literal_eval(content)
        title = content[0]["default_template_hidden_text_section_title"]
        expander_list = content[1]  # (a list of expanders)
        expanders = ast.literal_eval(
            expander_list["default_template_hidden_text_blocks"]
        )

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

        block_title = {"type": "text", "value": ""}

        block_group = {
            "type": "expander_group",
            "value": {"expanders": []},
        }

        for expander in expanders:
            summary = expander["default_template_hidden_text_summary"]
            details = expander["default_template_hidden_text_details"]

            # for item in field['items']:
            item_detail = details
            self.block_builder.extract_links(details, page)
            for link in self.block_builder.change_links:
                item_detail = item_detail.replace(str(link[0]), str(link[1]))
            block_item = {
                "title": summary,
                "body": [{"type": "richtext", "value": item_detail}],
            }
            block_group["value"]["expanders"].append(block_item)

        if title:
            block_title["value"] = "<h3>{}</h3>".format(title)
            return [block_title, block_group]
        else:
            return [block_group]

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
