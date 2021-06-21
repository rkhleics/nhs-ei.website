import sys
import time
import ast
import os
from io import BytesIO
from pathlib import Path
import logging

import requests
from django.core.files import File
from django.core.files.images import ImageFile
from wagtail.core.models import Collection
from wagtail.documents.models import Document
from wagtail.images.models import Image

from .importer_cls import Importer
from .httpcache import session

logger = logging.getLogger("importer")

# the indiators from wordpress aren't nice so map them to better titles
SOURCES = {
    "media": "NHS England & Improvement",
    "media-aac": "Accelerated Access Collaborative",
    "media-commissioning": "Commissioning",
    "media-coronavirus": "Corovavirus",
    "media-greenernhs": "Greener NHS",
    "media-improvement-hub": "Improvement Hub",
    "media-non-executive-opportunities": "Non-executive opportunities",
    "media-rightcare": "Right Care",
}


class MediaFilesImporter(Importer):
    def __init__(self):
        images = Image.objects.all()
        documents = Document.objects.all()
        if images or documents:
            sys.stdout.write("⚠️  Run delete_media_files before running this command\n")
            sys.exit()
        else:
            # keep it tidy remove collections first always
            for key in SOURCES.keys():
                try:
                    collection = Collection.objects.filter(name=SOURCES[key])
                    for c in collection:
                        c.delete()
                        sys.stdout.write("-")
                except Collection.DoesNotExist:
                    pass
            # make collections based on sources
            collection_root = Collection.get_first_root_node()
            for key in SOURCES.keys():
                collection_root.add_child(name=SOURCES[key])

    def parse_results(self):
        media_files = self.results

        for r in media_files:
            sub_site = r.get("source")
            collection_name = SOURCES[sub_site]
            collection = Collection.objects.get(name=collection_name)
            source_url = r.get("source_url")
            media_type = r.get("media_type")
            media_name = source_url.split("/")[-1]
            response = session.get(source_url)
            title = r.get("title")  # if the title id blank it causes an error
            if not title:
                logger.warn("No title was available for %s, %s", source_url, r)
                title = "No title was available"
            if response:

                if media_type == "file":  # save to documents

                    media_file = File(BytesIO(response.content), name=media_name)
                    file = Document(title=title, file=media_file, collection=collection)
                    file.save()
                    file.created_at = r.get("date")
                    file.save()

                elif media_type == "image":  # save to images

                    image_file = ImageFile(BytesIO(response.content), name=media_name)
                    image = Image(title=title, file=image_file, collection=collection)
                    image.save()
                    image.created_at = r.get("date")
                    image.save()

            else:
                logger.warn(
                    "Got no response and no file has been saved: %s, %s", source_url, r
                )

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Document.objects.count() + Image.objects.count(), 0
