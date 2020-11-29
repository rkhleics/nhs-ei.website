import os
import sys
import csv
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from nhsei_wagtail.importer.ancestry import Ancestry
from nhsei_wagtail.pages.models import BasePage
from .block_parse_experiment_data import DATA_1, DATA_2, DATA_ALL
from nhsei_wagtail.importer.importer_cls import ComponentsBuilder


class Command(BaseCommand):

    help = 'Moves pages into position indicated by the parent field (the wordpress page id)'

    def handle(self, *args, **options):
        d1 = DATA_1
        d2 = DATA_2
        dall = DATA_ALL
        # datahome = DATA_HOME_PAGE

        blocks = []

        builder = ComponentsBuilder(dall)
        blocks = builder.make_blocks()

        print(json.dumps(blocks, indent=2))