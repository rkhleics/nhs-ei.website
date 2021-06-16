import ast
import json
import sys

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

        with open("importer/log/make_documents_list_errors.txt", "w") as the_file:
            the_file.write("make documents list missing media url\n")

    def handle(self, *args, **options):

        """now not deleteing docuemnts they need to be found instead"""
        # documents = Document.objects.all()
        # if documents:
        #     sys.stdout.write(
        #         '⚠️  Deleteing the documents\n')
        #     docs = Document.objects.all().delete()

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
                        # self.block_builder.extract_links(row[k])
                        # item_detail = row[k]
                        # for link in self.block_builder.change_links:
                        #     item_detail = item_detail.replace(
                        #         str(link[0]), str(link[1]))
                        # introduction = item_detail
                        introduction = row[k]

                    if k == "documents":
                        # some docs have no document !!!! whaaaat wp_id 1115
                        docs = ast.literal_eval(row[k]) or []

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
"""
"introduction": "<p>This document sets out principles to support the remote monitoring, using pulse oximetry, of patients with confirmed or possible COVID-19.</p>\n<p><a href=\"https://www.england.nhs.uk/publication/pulse-oximetry-to-detect-early-deterioration-of-patients-with-covid-19-in-primary-and-community-care-settings-annex-2-covid-19-diary-translated-versions/\">Translated versions of Annex 2: COVID-19 diary</a> are available.</p>\n"
"table_of_contents": "False"
"documents": [
{
    'type_of_publication': 'document', 
    'document': {
        'ID': 164774, 
        'id': 164774, 
        'title': 'BW304 - NHS flu vaccination programme in Flu Vaccination Expedite Uptake Letter 13 November 2020', 
        'filename': 'BW304-NHS-flu-vaccination-programme-in-Flu-Vaccination-Expedite-Uptake-Letter-13-November-2020.pdf', 
        'filesize': 121755, 
        'url': 'https://www.england.nhs.uk/wp-content/uploads/2020/09/BW304-NHS-flu-vaccination-programme-in-Flu-Vaccination-Expedite-Uptake-Letter-13-November-2020.pdf', 
        'link': 'https://www.england.nhs.uk/publication/vaccine-ordering-for-2020-21-influenza-season-letters-2/bw304-nhs-flu-vaccination-programme-in-flu-vaccination-expedite-uptake-letter-13-november-2020/', 
        'alt': '', 
        'author': '2121', 
        'description': '', 
        'caption': '', 
        'name': 'bw304-nhs-flu-vaccination-programme-in-flu-vaccination-expedite-uptake-letter-13-november-2020', 
        'status': 'inherit', 
        'uploaded_to': 162413, 
        'date': '2020-11-13 16:42:55', 
        'modified': '2020-11-13 16:42:59', 
        'menu_order': 0, 
        'mime_type': 'application/pdf', 
        'type': 'application', 
        'subtype': 'pdf', 
        'icon': 'https://www.england.nhs.uk/wp-includes/images/media/document.png'
    }, 
    'audio_or_video': '', 
    'link_url': '', 
    'heading_text': '', 
    'free_text': '', 
    'title': 'Expediting the flu vaccination for healthcare workers - 13 November 2020', 
    'publication_type': {
        'term_id': 2574, 
        'name': 'Letter', 
        'slug': 'letter', 
        'term_group': 0, 
        'term_taxonomy_id': 2600, 
        'taxonomy': 'publication-type', 
        'description': '', 
        'parent': 0, 
        'count': 126, 
        'filter': 'raw'
    }, 
    'snapshot': '<p>This letter is co-signed by:</p>\\n<ul>\\n<li>NHS National Medical Director, Professor Stephen Powis</li>\\n<li>National Director for Emergency and Elective Care, Pauline Philip DBE</li>\\n</ul>\\n', 
    'number_of_pages': '2', 
    'length_of_file': None, 
    'thumbnail': False, 
    'icon': 'pdf'
}, {
    type_of_publication: "heading",
    document: false,
    audio_or_video: "",
    link_url: "",
    heading_text: "NHS provider directory",
    free_text: "",
    title: "",
    publication_type: {
        term_id: 3584,
        name: "Regulatory",
        slug: "regulatory",
        term_group: 0,
        term_taxonomy_id: 3610,
        taxonomy: "publication-type",
        description: "",
        parent: 0,
        count: 233,
        filter: "raw"
    },
    snapshot: "",
    number_of_pages: "",
    length_of_file: null,
    thumbnail: false,
    icon: ""
},{
    type_of_publication: "documentlink",
    document: false,
    audio_or_video: "",
    link_url: "https://www.england.nhs.uk/publication/nhs-provider-directory/",
    heading_text: "",
    free_text: "",
    title: "NHS provider directory",
    publication_type: {
        term_id: 3584,
        name: "Regulatory",
        slug: "regulatory",
        term_group: 0,
        term_taxonomy_id: 3610,
        taxonomy: "publication-type",
        description: "",
        parent: 0,
        count: 233,
        filter: "raw"
    },
    snapshot: "<p>A list of all NHS trusts and NHS foundation trusts with regulatory action, corporate publications and contact details.</p> ",
    number_of_pages: "",
    length_of_file: null,
    thumbnail: false,
    icon: ""
},{
    type_of_publication: "freetext",
    document: false,
    audio_or_video: "",
    link_url: "",
    heading_text: "",
    free_text: "<p><strong>For NHS trust and NHS foundation trust regulatory action, see the <a href="https://improvement.nhs.uk/about-us/corporate-publications/publications/nhs-provider-directory/">NHS provider directory</a>.</strong></p> ",
    title: "",
    publication_type: {
        term_id: 3584,
        name: "Regulatory",
        slug: "regulatory",
        term_group: 0,
        term_taxonomy_id: 3610,
        taxonomy: "publication-type",
        description: "",
        parent: 0,
        count: 233,
        filter: "raw"
    },
    snapshot: "",
    number_of_pages: "",
    length_of_file: null,
    thumbnail: false,
    icon: ""
}]"
"""


"""
https://www.england.nhs.uk/publication/nhs-provider-directory-and-registers-of-licensed-healthcare-providers/
"documents": "[
    {'type_of_publication': 'heading', 
        'document': False, 'audio_or_video': '', 'link_url': '', 'heading_text': 'NHS provider directory', 'free_text': '', 'title': '', 'publication_type': {'term_id': 3584, 'name': 'Regulatory', 'slug': 'regulatory', 'term_group': 0, 'term_taxonomy_id': 3610, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 233, 'filter': 'raw'}, 'snapshot': '', 'number_of_pages': '', 'length_of_file': None, 'thumbnail': False, 'icon': ''}, 

    {'type_of_publication': 'documentlink', 
        'document': False, 'audio_or_video': '', 'link_url': 'https://www.england.nhs.uk/publication/nhs-provider-directory/', 'heading_text': '', 'free_text': '', 'title': 'NHS provider directory', 'publication_type': {'term_id': 3584, 'name': 'Regulatory', 'slug': 'regulatory', 'term_group': 0, 'term_taxonomy_id': 3610, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 233, 'filter': 'raw'}, 'snapshot': '<p>A list of all NHS trusts and NHS foundation trusts with regulatory action, corporate publications and contact details.</p>\\n', 'number_of_pages': '', 'length_of_file': None, 'thumbnail': False, 'icon': ''}, 

    {'type_of_publication': 'heading', 
        'document': False, 'audio_or_video': '', 'link_url': '', 'heading_text': 'Registers of licensed healthcare providers', 'free_text': '', 'title': '', 'publication_type': {'term_id': 3584, 'name': 'Regulatory', 'slug': 'regulatory', 'term_group': 0, 'term_taxonomy_id': 3610, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 233, 'filter': 'raw'}, 'snapshot': '', 'number_of_pages': '', 'length_of_file': None, 'thumbnail': False, 'icon': ''}, 

    {'type_of_publication': 'document', 
        'document': {
            'ID': 148365, 'id': 148365, 'title': 'Public_Registry_FT_directory_190403', 'filename': 'Public_Registry_FT_directory_190403.xls', 'filesize': 53069, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2019/04/Public_Registry_FT_directory_190403.xls', 'link': 'https://www.england.nhs.uk/publication/nhs-provider-directory-and-registers-of-licensed-healthcare-providers/public_registry_ft_directory_190403/', 'alt': '', 'author': '1849', 'description': '', 'caption': '', 'name': 'public_registry_ft_directory_190403', 'status': 'inherit', 'uploaded_to': 144645, 'date': '2019-10-25 10:27:37', 'modified': '2019-10-25 10:27:49', 'menu_order': 0, 'mime_type': 'application/vnd.ms-excel', 'type': 'application', 'subtype': 'vnd.ms-excel', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/spreadsheet.png'}, 'audio_or_video': '', 'link_url': '', 'heading_text': '', 'free_text': '', 'title': 'NHS Foundation Trusts', 'publication_type': {'term_id': 3584, 'name': 'Regulatory', 'slug': 'regulatory', 'term_group': 0, 'term_taxonomy_id': 3610, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 233, 'filter': 'raw'}, 'snapshot': '', 'number_of_pages': '', 'length_of_file': None, 'thumbnail': False, 'icon': 'xls'}, 

    {'type_of_publication': 'document', 
        'document': {
            'ID': 164856, 'id': 164856, 'title': 'independent-provider-public-register-171120', 'filename': 'independent-provider-public-register-171120.csv', 'filesize': 44244, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2019/04/independent-provider-public-register-171120.csv', 'link': 'https://www.england.nhs.uk/publication/nhs-provider-directory-and-registers-of-licensed-healthcare-providers/independent-provider-public-register-171120/', 'alt': '', 'author': '2121', 'description': '', 'caption': '', 'name': 'independent-provider-public-register-171120', 'status': 'inherit', 'uploaded_to': 144645, 'date': '2020-11-17 18:03:23', 'modified': '2020-11-17 18:03:53', 'menu_order': 0, 'mime_type': 'text/csv', 'type': 'text', 'subtype': 'csv', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/text.png'}, 'audio_or_video': '', 'link_url': '', 'heading_text': '', 'free_text': '', 'title': 'Independent providers', 'publication_type': {'term_id': 3584, 'name': 'Regulatory', 'slug': 'regulatory', 'term_group': 0, 'term_taxonomy_id': 3610, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 233, 'filter': 'raw'}, 'snapshot': '', 'number_of_pages': '', 'length_of_file': None, 'thumbnail': False, 'icon': 'csv'}, 

    {'type_of_publication': 'document', 
        'document': {
            'ID': 148367, 'id': 148367, 'title': 'PublicRegister_NHS_controlled_providers_240619', 'filename': 'PublicRegister_NHS_controlled_providers_240619.xls', 'filesize': 1110, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2019/04/PublicRegister_NHS_controlled_providers_240619.xls', 'link': 'https://www.england.nhs.uk/publication/nhs-provider-directory-and-registers-of-licensed-healthcare-providers/publicregister_nhs_controlled_providers_240619/', 'alt': '', 'author': '1849', 'description': '', 'caption': '', 'name': 'publicregister_nhs_controlled_providers_240619', 'status': 'inherit', 'uploaded_to': 144645, 'date': '2019-10-25 10:27:40', 'modified': '2019-10-25 10:27:53', 'menu_order': 0, 'mime_type': 'application/vnd.ms-excel', 'type': 'application', 'subtype': 'vnd.ms-excel', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/spreadsheet.png'}, 'audio_or_video': '', 'link_url': '', 'heading_text': '', 'free_text': '', 'title': 'NHS-controlled providers', 'publication_type': {'term_id': 3584, 'name': 'Regulatory', 'slug': 'regulatory', 'term_group': 0, 'term_taxonomy_id': 3610, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 233, 'filter': 'raw'}, 'snapshot': '', 'number_of_pages': '', 'length_of_file': None, 'thumbnail': False, 'icon': 'xls'}, 

    {'type_of_publication': 'heading', 
        'document': False, 'audio_or_video': '', 'link_url': '', 'heading_text': 'Regulatory action', 'free_text': '', 'title': '', 'publication_type': {'term_id': 3584, 'name': 'Regulatory', 'slug': 'regulatory', 'term_group': 0, 'term_taxonomy_id': 3610, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 233, 'filter': 'raw'}, 'snapshot': '', 'number_of_pages': '', 'length_of_file': None, 'thumbnail': False, 'icon': ''}, 

    {'type_of_publication': 'documentlink', 
        'document': False, 'audio_or_video': '', 'link_url': 'https://improvement.nhs.uk/about-us/corporate-publications/publications/regulatory-action-licensed-independent-healthcare-providers/', 'heading_text': '', 'free_text': '', 'title': 'Licensed independent healthcare providers', 'publication_type': {'term_id': 3584, 'name': 'Regulatory', 'slug': 'regulatory', 'term_group': 0, 'term_taxonomy_id': 3610, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 233, 'filter': 'raw'}, 'snapshot': '<p>Information on regulatory action we&#8217;ve taken against licensed independent healthcare providers.</p>\\n', 'number_of_pages': '', 'length_of_file': None, 'thumbnail': False, 'icon': ''}, 

    {'type_of_publication': 'freetext', 
        'document': False, 'audio_or_video': '', 'link_url': '', 'heading_text': '', 'free_text': '<p><strong>For NHS trust and NHS foundation trust regulatory action, see the\\xa0<a href=\"https://improvement.nhs.uk/about-us/corporate-publications/publications/nhs-provider-directory/\">NHS provider directory</a>.</strong></p>\\n', 'title': '', 'publication_type': {'term_id': 3584, 'name': 'Regulatory', 'slug': 'regulatory', 'term_group': 0, 'term_taxonomy_id': 3610, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 233, 'filter': 'raw'}, 'snapshot': '', 'number_of_pages': '', 'length_of_file': None, 'thumbnail': False, 'icon': ''}]"

https://www.england.nhs.uk/publication/nhs-standard-contract-2020-21-awareness-raising-audio-presentations/
"documents": "[
    {'type_of_publication': 'audiovideo', 
        'document': False, 'audio_or_video': '<p><iframe width=\"500\" height=\"281\" src=\"//www.youtube.com/embed/iYn6es5X1EI?rel=0\" frameborder=\"0\" allowfullscreen></iframe></p>\\n', 'link_url': '', 'heading_text': '', 'free_text': '', 'title': 'Presentation 1 – Introduction to the Contract', 'publication_type': {'term_id': 2573, 'name': 'Guidance', 'slug': 'guidance', 'term_group': 0, 'term_taxonomy_id': 2599, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 1553, 'filter': 'raw'}, 'snapshot': '<p>The audio presentation is subtitled, and the entire <a href=\"https://www.england.nhs.uk/publication/draft-nhs-standard-contract-2020-21-audio-presentations-transcript/\">transcript is available download</a>.</p>\\n', 'number_of_pages': '', 'length_of_file': '00:30:45', 'thumbnail': False, 'icon': ''}, {'type_of_publication': 'document', 'document': {'ID': 153174, 'id': 153174, 'title': '2021-Contract-audio-presentation-1', 'filename': '2021-Contract-audio-presentation-1.pdf', 'filesize': 237289, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2020/01/2021-Contract-audio-presentation-1.pdf', 'link': 'https://www.england.nhs.uk/publication/draft-nhs-standard-contract-2020-21-presentation-1/2021-contract-audio-presentation-1/', 'alt': '', 'author': '1849', 'description': '', 'caption': '', 'name': '2021-contract-audio-presentation-1', 'status': 'inherit', 'uploaded_to': 153171, 'date': '2020-01-24 11:32:54', 'modified': '2020-01-24 11:33:07', 'menu_order': 0, 'mime_type': 'application/pdf', 'type': 'application', 'subtype': 'pdf', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/document.png'}, 'audio_or_video': '', 'link_url': '', 'heading_text': '', 'free_text': '', 'title': 'Draft NHS Standard Contract 2020/21: Audio presentation 1 - Introduction to the Contract', 'publication_type': {'term_id': 2573, 'name': 'Guidance', 'slug': 'guidance', 'term_group': 0, 'term_taxonomy_id': 2599, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 1553, 'filter': 'raw'}, 'snapshot': '', 'number_of_pages': '21', 'length_of_file': None, 'thumbnail': False, 'icon': 'pdf'}, {'type_of_publication': 'audiovideo', 'document': False, 'audio_or_video': '<p><iframe width=\"500\" height=\"281\" src=\"//www.youtube.com/embed/w4s2cDT6_YA?rel=0\" frameborder=\"0\" allowfullscreen></iframe></p>\\n', 'link_url': '', 'heading_text': '', 'free_text': '', 'title': 'Presentation 2 - Local system collaboration and integration', 'publication_type': {'term_id': 2573, 'name': 'Guidance', 'slug': 'guidance', 'term_group': 0, 'term_taxonomy_id': 2599, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 1553, 'filter': 'raw'}, 'snapshot': '<p>The audio presentation is subtitled, and the entire <a href=\"https://www.england.nhs.uk/publication/draft-nhs-standard-contract-2020-21-audio-presentations-transcript/\">transcript is available download</a>.</p>\\n', 'number_of_pages': '', 'length_of_file': '00:18:06', 'thumbnail': False, 'icon': ''}, {'type_of_publication': 'document', 'document': {'ID': 153175, 'id': 153175, 'title': '2021-Contract-audio-presentation-2', 'filename': '2021-Contract-audio-presentation-2.pdf', 'filesize': 182089, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2020/01/2021-Contract-audio-presentation-2.pdf', 'link': 'https://www.england.nhs.uk/publication/draft-nhs-standard-contract-2020-21-presentation-1/2021-contract-audio-presentation-2/', 'alt': '', 'author': '1849', 'description': '', 'caption': '', 'name': '2021-contract-audio-presentation-2', 'status': 'inherit', 'uploaded_to': 153171, 'date': '2020-01-24 11:32:54', 'modified': '2020-01-24 11:33:08', 'menu_order': 0, 'mime_type': 'application/pdf', 'type': 'application', 'subtype': 'pdf', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/document.png'}, 'audio_or_video': '', 'link_url': '', 'heading_text': '', 'free_text': '', 'title': 'Draft NHS Standard Contract 2020/21: Audio presentation 2 - Local system collaboration and integration', 'publication_type': {'term_id': 2573, 'name': 'Guidance', 'slug': 'guidance', 'term_group': 0, 'term_taxonomy_id': 2599, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 1553, 'filter': 'raw'}, 'snapshot': '', 'number_of_pages': '19', 'length_of_file': None, 'thumbnail': False, 'icon': 'pdf'}, {'type_of_publication': 'audiovideo', 'document': False, 'audio_or_video': '<p><iframe width=\"500\" height=\"281\" src=\"//www.youtube.com/embed/5Een1KGNhLs?rel=0\" frameborder=\"0\" allowfullscreen></iframe></p>\\n', 'link_url': '', 'heading_text': '', 'free_text': '', 'title': 'Presentation 3 - New national policy initiatives included in the draft Contract for 2020/21', 'publication_type': {'term_id': 2573, 'name': 'Guidance', 'slug': 'guidance', 'term_group': 0, 'term_taxonomy_id': 2599, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 1553, 'filter': 'raw'}, 'snapshot': '<p>The audio presentation is subtitled, and the entire <a href=\"https://www.england.nhs.uk/publication/draft-nhs-standard-contract-2020-21-audio-presentations-transcript/\">transcript is available to download</a>.</p>\\n', 'number_of_pages': '', 'length_of_file': '00:39:24', 'thumbnail': False, 'icon': ''}, {'type_of_publication': 'document', 'document': {'ID': 153176, 'id': 153176, 'title': '2021-Contract-audio-presentation-3', 'filename': '2021-Contract-audio-presentation-3.pdf', 'filesize': 279406, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2020/01/2021-Contract-audio-presentation-3.pdf', 'link': 'https://www.england.nhs.uk/publication/draft-nhs-standard-contract-2020-21-presentation-1/2021-contract-audio-presentation-3/', 'alt': '', 'author': '1849', 'description': '', 'caption': '', 'name': '2021-contract-audio-presentation-3', 'status': 'inherit', 'uploaded_to': 153171, 'date': '2020-01-24 11:32:55', 'modified': '2020-01-24 11:33:10', 'menu_order': 0, 'mime_type': 'application/pdf', 'type': 'application', 'subtype': 'pdf', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/document.png'}, 'audio_or_video': '', 'link_url': '', 'heading_text': '', 'free_text': '', 'title': 'Draft NHS Standard Contract 2020/21: Audio presentation 3 - New national policy initiatives included in the draft Contract for 2020/21', 'publication_type': {'term_id': 2573, 'name': 'Guidance', 'slug': 'guidance', 'term_group': 0, 'term_taxonomy_id': 2599, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 1553, 'filter': 'raw'}, 'snapshot': '', 'number_of_pages': '27', 'length_of_file': None, 'thumbnail': False, 'icon': 'pdf'}, {'type_of_publication': 'audiovideo', 'document': False, 'audio_or_video': '<p><iframe width=\"500\" height=\"281\" src=\"//www.youtube.com/embed/6BYTV6FGp5U?rel=0\" frameborder=\"0\" allowfullscreen></iframe></p>\\n', 'link_url': '', 'heading_text': '', 'free_text': '', 'title': 'Presentation 4 - Changes affecting national standards and NHS \"business rules\" for 2020/21', 'publication_type': {'term_id': 2573, 'name': 'Guidance', 'slug': 'guidance', 'term_group': 0, 'term_taxonomy_id': 2599, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 1553, 'filter': 'raw'}, 'snapshot': '<p>The audio presentation is subtitled, and the entire <a href=\"https://www.england.nhs.uk/publication/draft-nhs-standard-contract-2020-21-audio-presentations-transcript/\">transcript is available to download</a>.</p>\\n', 'number_of_pages': '', 'length_of_file': '00:24:31', 'thumbnail': False, 'icon': ''}, {'type_of_publication': 'document', 'document': {'ID': 153177, 'id': 153177, 'title': '2021-Contract-audio-presentation-4', 'filename': '2021-Contract-audio-presentation-4.pdf', 'filesize': 172554, 'url': 'https://www.england.nhs.uk/wp-content/uploads/2020/01/2021-Contract-audio-presentation-4.pdf', 'link': 'https://www.england.nhs.uk/publication/draft-nhs-standard-contract-2020-21-presentation-1/2021-contract-audio-presentation-4/', 'alt': '', 'author': '1849', 'description': '', 'caption': '', 'name': '2021-contract-audio-presentation-4', 'status': 'inherit', 'uploaded_to': 153171, 'date': '2020-01-24 11:32:56', 'modified': '2020-01-24 11:33:13', 'menu_order': 0, 'mime_type': 'application/pdf', 'type': 'application', 'subtype': 'pdf', 'icon': 'https://www.england.nhs.uk/wp-includes/images/media/document.png'}, 'audio_or_video': '', 'link_url': '', 'heading_text': '', 'free_text': '', 'title': 'Draft NHS Standard Contract 2020/21: Audio presentation 4 - Changes affecting national standards and NHS \"business rules\" for 2020/21', 'publication_type': {'term_id': 2573, 'name': 'Guidance', 'slug': 'guidance', 'term_group': 0, 'term_taxonomy_id': 2599, 'taxonomy': 'publication-type', 'description': '', 'parent': 0, 'count': 1553, 'filter': 'raw'}, 'snapshot': '', 'number_of_pages': '16', 'length_of_file': None, 'thumbnail': False, 'icon': 'pdf'}]"
"""
