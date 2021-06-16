import sys
import time

from django.core.management import call_command
from django.core.management.base import BaseCommand
from cms.core.models import CoreSettings


class Command(BaseCommand):
    help = "Deletes regions (bulk action)"

    def handle(self, *args, **options):
        # depth order to start at deepest pages, seems sensible
        settings = CoreSettings.objects.all().first()

        if not settings:
            sys.stdout.write("✅ Core Settings is empty\n")
        else:
            settings_length = 1

            sys.stdout.write(
                "Core Settings to delete: {} this can take a while to complete\n".format(
                    settings_length
                )
            )

            settings.delete()
            sys.stdout.write("-")

            sys.stdout.write("\n✅ Core Settings is now empty\n")
