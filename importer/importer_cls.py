import ast
from cms.blogs.models import Blog
from cms.pages.models import BasePage, ComponentsPage, LandingPage
from cms.posts.models import Post
from cms.atlascasestudies.models import AtlasCaseStudy
from cms.publications.models import Publication
import random
import sys
from io import BytesIO
import logging

import dateutil.parser
import requests
from django.core.files import File
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils.timezone import make_aware
from importer.richtextbuilder import RichTextBuilder
from requests.api import head, post
from wagtail.core.models import Collection, Page
from wagtail.documents.models import Document
from wagtail.images.models import Image
from .httpcache import session

logger = logging.getLogger("importer")


class Importer:

    # should_delete = False # True to remove all existing records form the model
    sleep_between_fetches = 0  # seconds, use it in parse_results()

    def fetch_url(self, url):
        sys.stdout.write("\n⌛️ fetching API url {}\n".format(url))
        r = requests.get(url).json()
        self.count = r.get("count")
        self.next = r.get("next")
        self.previous = r.get("previous")
        self.results = r.get("results")
        return True

    def get_count(self):
        return self.count

    def get_next_url(self):
        return self.next

    def get_previous_url(self):
        return self.previous

    def get_results(self):
        return self.results

    def parse_results(self):
        # best to add a sleep between fetches time.sleep(self.sleep_between_fetches)
        raise NotImplementedError

    def empty_table(self):
        # its an optional argument when running the importer [-d]
        raise NotImplementedError


class ComponentsBuilder:
    def __init__(self, data, url_map=None, page=None):

        # a temporary fix to rewrite absolute urls
        # in the block types that ultimatley will have a page chooser etc
        self.url_map = url_map
        self.page = page

        self.data = data
        self.component_keys = [
            "a_to_z_index_component",
            "article_component",
            "in_this_section_component",
            "priorities_component",
            "recent_posts_component",
            "promos_component",
            "topic_section_component",
        ]
        self.layouts = []
        if not isinstance(self.data, list):
            print("data is not a list")
            print(self.data)
            # good to go as each item represents a layout
        # print(self.layouts)

    def make_blocks(self):
        block = None

        for layout in self.data:  # for each acf_fc_layout for a page
            block = self.get_block_type(layout)
        if block:
            self.layouts.append(block)
        # print(self.layouts)
        return self.layouts

    def get_block_type(self, layout):
        if layout["acf_fc_layout"] == "a_to_z_index_component":
            print("found a to z section")

        if layout["acf_fc_layout"] == "topic_section_component":
            # this page: https://www.england.nhs.uk/about/
            topic_section_component = self.build_topic_section_component(layout)
            # print(topic_section_component)
            if topic_section_component:
                self.layouts.append(topic_section_component)

        if layout["acf_fc_layout"] == "priorities_component":
            # this can return a list, needs to be flattened
            priorities_component = self.build_priorities_component(layout)
            if priorities_component and isinstance(priorities_component, list):
                for item in priorities_component:
                    self.layouts.append(item)
            elif (
                priorities_component
            ):  # can get nothing back used in wordpress but nothing added
                self.layouts.append(priorities_component)

        if layout["acf_fc_layout"] == "in_this_section_component":
            in_this_section_component = self.build_in_this_section_component(layout)
            if in_this_section_component and isinstance(
                in_this_section_component, list
            ):
                for item in in_this_section_component:
                    self.layouts.append(item)
            elif (
                in_this_section_component
            ):  # can get nothing back used in wordpress but nothing added
                self.layouts.append(in_this_section_component)

        if layout["acf_fc_layout"] == "recent_posts_component":
            # self.layouts.append(self.build_recent_posts_component(layout))
            recent_posts_component = self.build_recent_posts_component(layout)
            if recent_posts_component:
                self.layouts.append(recent_posts_component)

        if layout["acf_fc_layout"] == "promos_component":
            promos_component = self.build_promos_component(layout)
            if promos_component:
                self.layouts.append(promos_component)

        if layout["acf_fc_layout"] == "article_component":
            article_component = self.build_article_component(layout)
            if article_component:
                self.layouts.append(article_component)

    def build_article_component(self, layout):

        if layout["article_image"]:
            image_url = layout["article_image"]["url"]
        else:
            image_url = ""

        data = {
            "image": image_url,
            "image_alignment": layout["article_image_alignment"],
            "title": strip_tags(layout["article_title"]),
            "content": layout["article_content"],
            "url": layout["article_url"],
        }
        """
        {
            'type': 'panel',
            'value': {
                'label': 'optional label',
                'body': 'required body'
            }
        }
        """
        block = {  # uses the panel block
            "type": "panel",
            "value": {
                "label": strip_tags(data["title"]),
                # this is the default, might want to change it...
                "heding_level": "3",
                # after it's been parsed for links
                "body": self.fix_anchor_button_class(data["content"]),
            },
        }
        return block

    def build_promos_component(self, layout):
        # using promo group block
        promos = layout["promo_component"]
        if len(promos) > 2:
            columns = "one-third"
        else:
            columns = "one-half"
        """
        {'type': 'promo_group',
         'value': {
             'column': 'one-third',
             'size': 'small',
             'heading_level': 3,
             'promos': [
                 {
                     'url': 'http://wwww.test.com',
                     'heading': 'Heading',
                     'description': 'Descrtipion',
                     'content_image': 1,  # image id
                     'alt_text': ''
                 },
                 {
                     'repeats': 'repeats',
                 }
             ]

         }}
         """
        block_group = {
            "type": "promo_group",
            "value": {
                "column": columns,
                "size": "small",
                "heading_level": 3,
                "promos": [],
            },
        }

        # print(content)
        if promos:
            for promo in promos:
                has_image = promo["promo_image"]
                content_image_id = None
                content_image_alt = None
                page_path = self.get_page_path(promo["promo_url"])
                # if has_image:
                #     # found_image = self.fetch_image_id(promo['promo_image']['title'])
                #     found_image = self.fetch_image_id(
                #         self.variate_name())  # just for testing
                #     if found_image:
                #         content_image_id = found_image.id
                #         content_image_alt = promo['promo_image']['title']
                #     else:
                #         content_image_id = None
                #         content_image_alt = None
                # sometime they are there but have not content at all and get rendered empty
                if promo["promo_title"] or promo["promo_content"]:
                    block_promo = {
                        "url": page_path,
                        "heading": strip_tags(promo["promo_title"]),
                        "description": strip_tags(promo["promo_content"]),
                        "content_image": content_image_id,  # need to make it work in wagtail
                        "alt_text": content_image_alt,
                    }
                    block_group["value"]["promos"].append(block_promo)
            return block_group

    def build_recent_posts_component(self, layout):
        block_group = {
            "type": "recent_posts",
            "value": {
                "title": layout["section_title"],
                "type": ["post", "blog"],
                "num_posts": 3,
                "see_all": layout["show_see_all"],
            },
        }

        return block_group

    def build_priorities_component(self, layout):
        # the expander component
        """
        {'type': 'expander',
         'value': {
             'title': '',
             'body': [
                 'type': 'action_link'
                 'value': {
                     'text': '',
                    'external_url': '',
                    'new_window': ''
                 }
             ]
         }}
        """
        # print(layout)
        priorities = layout["our_priorities"]

        if layout["priorities_section_title"]:
            block_group = {
                "type": "expander",
                "value": {"title": layout["priorities_section_title"], "body": []},
            }
            if priorities:
                for priority in priorities:
                    page_path = self.get_page_path(priority["priority_url"])
                    obj = {
                        "type": "action_link",
                        "value": {
                            "text": strip_tags(priority["priority_title"]),
                            "external_url": page_path,
                            "new_window": False,
                        },
                    }

                    block_group["value"]["body"].append(obj)
                return block_group
        else:
            # just the action links
            links = []
            if priorities:
                for priority in priorities:
                    page_path = self.get_page_path(priority["priority_url"])
                    obj = {
                        "type": "action_link",
                        "value": {
                            "text": strip_tags(priority["priority_title"]),
                            "external_url": page_path,
                            "new_window": False,
                        },
                    }

                    links.append(obj)
            return links

    def build_in_this_section_component(self, layout):
        # the expander component
        """
        {'type': 'expander',
         'value': {
             'title': '',
             'body': [
                 'type': 'action_link'
                 'value': {
                     'text': '',
                    'external_url': '',
                    'new_window': ''
                 }
             ]
         }}
        """
        # print(layout)
        action_links = layout["in_this_section_topics"]

        if action_links:
            if layout["in_this_section_title"]:
                block_group = {
                    "type": "expander",
                    "value": {
                        "title": strip_tags(layout["in_this_section_title"]),
                        "body": [],
                    },
                }

                for link in action_links:
                    page_path = self.get_page_path(link["in_this_section_link_url"])
                    action_link = {
                        "type": "action_link",
                        "value": {
                            "text": strip_tags(link["in_this_section_link_title"]),
                            "external_url": page_path,
                            "new_window": False,
                        },
                    }

                    block_group["value"]["body"].append(action_link)
                return block_group
            else:
                links = []
                for link in action_links:
                    page_path = self.get_page_path(link["in_this_section_link_url"])
                    action_link = {
                        "type": "action_link",
                        "value": {
                            "text": strip_tags(link["in_this_section_link_title"]),
                            "external_url": page_path,
                            "new_window": False,
                        },
                    }

                    links.append(action_link)
                return links
        else:
            return None

    def build_topic_section_component(self, layout):
        # using promo group block
        sections = layout["in_this_section"]
        if len(sections) > 2:
            columns = "one-third"
        else:
            columns = "one-half"
        """
        {'type': 'promo_group',
         'value': {
             'column': 'one-third',
             'size': 'small',
             'heading_level': 3,
             'promos': [
                 {
                     'url': 'http://wwww.test.com',
                     'heading': 'Heading',
                     'description': 'Descrtipion',
                     'content_image': 1,  # image id
                     'alt_text': ''
                 },
                 {
                     'repeats': 'repeats',
                 }
             ]

         }}
         """
        block_group = {
            "type": "promo_group",
            "value": {
                "column": columns,
                "size": "small",
                "heading_level": 3,
                "promos": [],
            },
        }

        # print(content)
        if sections:
            for section in sections:
                # has_image = section['promo_image']
                # if has_image:
                #     url = section['promo_image']['url']
                #     alt = section['promo_image']['alt']
                # else:
                #     url = ''
                #     alt = ''
                # if section['topic_url'] != '': # some topic urls are blank
                page_path = self.get_page_path(section["topic_url"])
                block_promo = {
                    "url": page_path,
                    "heading": strip_tags(section["topic_title"]),
                    "description": strip_tags(section["topic_content"]),
                    # need to make it work in wagtail, topic blocks never have an image
                    "content_image": None,
                    "alt_text": "",
                }
                # print(block_promo)
                block_group["value"]["promos"].append(block_promo)
            return block_group

    def fix_anchor_button_class(self, content):
        content_fixed = content.replace("wpc-button", "")
        content_fixed = content_fixed.replace(
            "nhs-aqua-blue", "nhsuk-button nhsuk-button--secondary"
        )

        return content_fixed

    def fetch_image_id(self, title):
        try:
            return Image.objects.get(title=title)
        except Image.DoesNotExist:
            return None

    def variate_name(self):
        names = ["Wide", "Tall"]
        r = random.choice([True, False])
        if r:
            return names[0]
        else:
            return names[1]

    # temp for getting absolute url page path
    def get_page_path(self, url):
        if url:
            path_list = url.split("/")  # a list of path segments
            # first is always '' so lets remove it
            del path_list[0]
            if not path_list[0]:  # this one can go too
                del path_list[0]
            if not path_list[-1]:  # this one can go too
                del path_list[-1]
            if path_list[0] == "www.england.nhs.uk":
                del path_list[0]

            page_path = "/" + "/".join(path_list) + "/"  # a string of the path
            if page_path in self.url_map:
                page = Page.objects.get(id=self.url_map[page_path]["id"])
                page_path = page.get_full_url()
            if "http://coding.nickmoreton.co.uk/" in page_path:
                logger.warn("nickmoreton.co.uk url found: %s", url)
                page_path = page_path.replace(
                    "http://coding.nickmoreton.co.uk/",
                    "http://coding.nickmoreton.co.uk:8000/",
                )
            return page_path


class DocumentsBuilder:
    def __init__(self, publication_page, document):
        self.document = document
        self.publication = publication_page
        # self.collection = None
        # the indiators from wordpress aren't nice so map them to better titles
        self.sources = {
            "publications": "NHS England & Improvement",
            "publications-aac": "Accelerated Access Collaborative",
            "publications-commissioning": "Commissioning",
            "publications-coronavirus": "Corovavirus",
            "publications-greenernhs": "Greener NHS",
            "publications-improvement-hub": "Improvement Hub",
            "publications-non-executive-opportunities": "Non-executive opportunities",
            "publications-rightcare": "Right Care",
        }

        # print(self.document)

        try:
            self.collection = Collection.objects.get(
                name=self.sources[publication_page.source]
            )
            # collection exists
        except Collection.DoesNotExist:
            # make the collection
            collection_root = Collection.get_first_root_node()
            self.collection = collection_root.add_child(
                name=self.sources[publication_page.source]
            )

    def make_documents(self):

        if self.document["type_of_publication"] == "heading":
            return self.create_heading(self.document["heading_text"])

        elif self.document["type_of_publication"] == "document":
            document = self.document["document"]
            if document:
                # lets get the file here, saves cluttering the block builder
                response = session.get(document["url"])
                if response:
                    media_file = File(
                        BytesIO(response.content), name=document["filename"]
                    )
                    file = Document(
                        title=document["title"],
                        file=media_file,
                        collection=self.collection,
                    )
                    file.save()
                    file.created_at = make_aware(
                        dateutil.parser.parse(document["date"])
                    )
                    file.save()
                    return self.create_document_type(file, document, self.document)
                else:
                    logger.warn(
                        "make_document_list_error: %s (%s)",
                        self.publication,
                        self.publication.id,
                    )

        elif self.document["type_of_publication"] == "documentlink":
            # pass
            # document = self.data['document']
            return self.create_link_type(self.document)

        elif self.document["type_of_publication"] == "audiovideo":
            # pass
            # document = self.data['document']
            return self.create_embed_type(self.document)

        elif self.document["type_of_publication"] == "freetext":
            return self.create_free_text(self.document)

        # return self.stream_value

        """
        'heading',
        'document',
        'documentlink',
        'audiovideo',
        'freetext',
        """

    def create_heading(self, heading):
        block = {
            "type": "named_anchor",
            "value": {
                "heading": heading,
                "anchor_id": slugify(heading),
            },
        }

        return block

    def create_document_type(self, file, document, container):
        block = {
            "type": "document",
            "value": {
                "title": container["title"],
                "document": file.id,
                # 'type': 'pdf',
                # 'num_pages': '2',
                # 'file_size': '1000',
            },
        }

        return block

    def create_link_type(self, document):
        return {
            "type": "document_link",
            "value": {
                "title": document["title"],
                "external_url": document["link_url"],
                "page": "1234",
                "summary": document["snapshot"],
            },
        }

    def create_embed_type(self, document):
        return {
            "type": "document_embed",
            "value": {"title": document["title"], "html": document["audio_or_video"]},
        }

    def create_free_text(self, document):
        return {"type": "free_text", "value": document["free_text"]}
