import ast
import json
import sys
import logging

from cms.atlascasestudies.models import AtlasCaseStudy
from cms.blogs.models import Blog
from cms.pages.models import BasePage, ComponentsPage, LandingPage
from cms.posts.models import Post
from cms.publications.models import Publication
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from importer.importer_cls import DocumentsBuilder
from importer.richtextbuilder import RichTextBuilder
from wagtail.documents.models import Document

logger = logging.getLogger("importer")

DOCUMENT_TYPES = [
    "heading",
    "document",
    "documentlink",
    "audiovideo",
    "freetext",
]


class Command(BaseCommand):
    help = "Creates the documents for each publication page"

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
        url_ids = {}  # cached

        for model in models:
            pages = model.objects.all()
            for page in pages:
                url_ids[page.url] = page.id

        self.urls = url_ids
        self.block_builder = RichTextBuilder(self.urls)

    def handle(self, *args, **options):

        """now not deleteing docuemnts they need to be found instead"""
        publications = Publication.objects.all()

        for publication in publications:
            sys.stdout.write("\n⌛️ {} processing...".format(publication))
            component_fields = ast.literal_eval(publication.component_fields)
            introduction = ""
            docs = []
            document_list = []
            for row in component_fields:
                items = row.items()
                for k, v in items:
                    if k == "introduction":
                        introduction = row[k]

                    if k == "documents":
                        # some docs have no document !!!! whaaaat wp_id 1115
                        docs = ast.literal_eval(row[k]) or []
                        if not docs:
                            logger.warn("No document in doc %s", publication)

            for document in docs:
                if document and document["type_of_publication"] in DOCUMENT_TYPES:
                    documents_builder = DocumentsBuilder(publication, document)
                    item = documents_builder.make_documents()
                    if item:
                        document_list.append(item)
                else:
                    print("document type not found")
                    sys.exit()

            # make the jump menu after by looking for headings in final document_list[]

            jump_menu_links = []

            for document in document_list:
                if document["type"] == "named_anchor":
                    jump_menu_links.append(document)

            jump_menu = {"type": "jump_menu", "value": {"menu": []}}

            for item in jump_menu_links:
                jump_menu["value"]["menu"].append(
                    {
                        "title": item["value"]["heading"],
                        "menu_id": slugify(item["value"]["heading"]),
                    }
                )

            new_stream_value = []

            mapped_type_postitions = []

            docs = []

            for i in range(0, len(document_list)):
                if document_list[i]["type"] == "named_anchor":
                    mapped_type_postitions.append("anchor")

                elif document_list[i]["type"] != "named_anchor":
                    mapped_type_postitions.append("doc")

                last_item = mapped_type_postitions[-1]

                if last_item != "anchor":
                    # append to docs and remove last
                    del mapped_type_postitions[-1]

                    docs.append("doc")

                elif last_item == "anchor" and len(docs):
                    del mapped_type_postitions[-1]
                    mapped_type_postitions.append(docs)
                    mapped_type_postitions.append("anchor")
                    docs = []

                if i == len(document_list) - 1:
                    mapped_type_postitions.append(docs)
                    docs = []

            if len(mapped_type_postitions) == 1:
                mapped_type_postitions = mapped_type_postitions[0]

            """ 
            mapped_type_positions becomes this 
            
            ['anchor', ['doc'], 'anchor', ['doc', 'doc', 'doc'], 'anchor', ['doc', 'doc']] 
            https://www.england.nhs.uk/publication/torbay-and-south-devon-nhs-foundation-trust/ wp_id=146041
            may be problem as very different layout
            """

            block_group = {"type": "document_group", "value": []}

            if not "anchor" in mapped_type_postitions:

                for i in range(0, len(mapped_type_postitions)):
                    block_group["value"].append(document_list[i])
                new_stream_value.append(block_group)

            else:
                pos = 0  # some items are list but need to keep track to get document_list index
                docs = []
                for item in mapped_type_postitions:

                    if isinstance(item, list):  # deal with docs
                        block_group = {"type": "document_group", "value": []}

                        for doc in item:
                            block_group["value"].append(document_list[pos])
                            pos += 1
                        new_stream_value.append(block_group)

                    else:  # deal with anchor dont forget it's always len 1

                        new_stream_value.append(document_list[pos])
                        pos += 1

            if jump_menu["value"]["menu"]:
                new_stream_value.insert(0, jump_menu)

            publication.body = introduction
            publication.documents = json.dumps(new_stream_value)
            rev = publication.save_revision()
            publication.first_published_at = publication.first_published_at
            publication.last_published_at = publication.last_published_at
            publication.latest_revision_created_at = (
                publication.latest_revision_created_at
            )
            publication.save()
            rev.publish()
            sys.stdout.write("\n✅ {} processing...".format(publication))


"""
exmaple URL https://www.england.nhs.uk/wp-json/wp/v2/documents/144645
type_of_publication can be 
document
audiovideo
documentlink
heading
freetext
"""
