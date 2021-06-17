import sys
import time

from django.core.management import call_command
from django.core.management.base import BaseCommand
from cms.categories.models import Setting


class Command(BaseCommand):
    help = "Deletes settings (bulk action)"

    def handle(self, *args, **options):
        # depth order to start at deepest pages, seems sensible
        settings = Setting.objects.all()

        if not settings:
            sys.stdout.write("✅ Settings is empty\n")
        else:
            settings_length = settings.count()

            sys.stdout.write(
                "Settings to delete: {} this can take a while to complete\n".format(
                    settings_length
                )
            )

            for setting in settings:
                setting.delete()
                sys.stdout.write("-")

            sys.stdout.write("\n✅ Settings is now empty\n")
