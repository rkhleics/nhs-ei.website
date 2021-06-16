import sys
import time

from django.core.management import call_command
from django.core.management.base import BaseCommand
from cms.categories.models import Region


class Command(BaseCommand):
    help = "Deletes regions (bulk action)"

    def handle(self, *args, **options):
        # depth order to start at deepest pages, seems sensible
        regions = Region.objects.all()

        if not regions:
            sys.stdout.write("✅ Regions is empty\n")
        else:
            regions_length = regions.count()

            sys.stdout.write(
                "Regions to delete: {} this can take a while to complete\n".format(
                    regions_length
                )
            )

            for region in regions:
                region.delete()
                sys.stdout.write("-")

            sys.stdout.write("\n✅ Regions is now empty\n")
