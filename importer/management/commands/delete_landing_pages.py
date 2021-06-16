import sys
import time

from django.core.management import call_command
from django.core.management.base import BaseCommand
from cms.pages.models import LandingPage


class Command(BaseCommand):
    help = "Deletes base pages (bulk action)"

    def handle(self, *args, **options):
        # depth order to start at deepest pages, seems sensible
        pages = LandingPage.objects.all().order_by("-depth")

        if not pages:
            sys.stdout.write("✅ Landing Pages is empty\n")
        else:
            pages_length = pages.count()

            sys.stdout.write(
                "Landing Pages to delete: {} this can take a while to complete\n".format(
                    pages_length
                )
            )

            for page in pages:
                page.delete()
                sys.stdout.write("-")

            sys.stdout.write("\n✅ Landing Pages is now empty\n")
