import json
from io import BytesIO

from cms.home.models import HomePage
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from wagtail.core.models import Collection
from wagtail.images.models import Image
from importer.webpages import STAGING


class Command(BaseCommand):
    help = "Creates the home page content"

    def handle(self, *args, **options):
        collection_root = Collection.get_first_root_node()
        try:
            collection = Collection.objects.get(name="Temporary Images")
        except Collection.DoesNotExist:
            collection = collection_root.add_child(name="Temporary Images")

        try:
            image = Image.objects.get(title="Hero Image")
        except Image.DoesNotExist:
            path = "importer/bin/homepage-hero-image.jpg"
            load_image = open(path, "rb").read()
            image_file = ImageFile(BytesIO(load_image), name="homepage-hero-image.jpg")
            image = Image(title="Hero Image", file=image_file, collection=collection)
            image.save()

        home_page = HomePage.objects.filter(title="Home")[0]

        """ home page body is a streamfield. make a dict for the promo_group block
        if a decision is made to alter the home page this will need to be updated"""

        home_page_stream_field = [
            {
                "type": "promo_group",
                "value": {
                    "column": "one-half",
                    "size": "",
                    "heading_level": "3",
                    "promos": [
                        {
                            "url": STAGING + "publication/nhs-england-improvement/",
                            "heading": "Latest publications",
                            "description": "See our most recent publications and search for documents in our publications library",
                            "content_image": None,
                            "alt_text": "",
                        },
                        {
                            "url": STAGING + "news/nhs-england-improvement/",
                            "heading": "News",
                            "description": "Our headline announcements",
                            "content_image": None,
                            "alt_text": "",
                        },
                        {
                            "url": STAGING + "gp/",
                            "heading": "General Practice",
                            "description": "Supporting GPs and GP-led services across our local communities ",
                            "content_image": None,
                            "alt_text": "",
                        },
                        {
                            "url": STAGING + "diabetes/",
                            "heading": "Diabetes",
                            "description": "Improving outcomes for people with diabetes",
                            "content_image": None,
                            "alt_text": "",
                        },
                    ],
                },
            },
            {
                "type": "warning_callout",
                "value": {
                    "title": "Are you looking for health advice?",
                    "heading_level": "3",
                    "body": '<p><a href="https://www.nhs.uk/">Find advice on health conditions, symptoms, healthy living, medicines and how to get help.</a></p>',
                },
            },
        ]

        home_page.body = json.dumps(home_page_stream_field)

        home_page.hero_heading = "Supporting the NHS"
        home_page.hero_text = "to improve people’s care"
        home_page.hero_image = image

        rev = home_page.save_revision()
        home_page.save()
        rev.publish()
