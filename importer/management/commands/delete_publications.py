import sys

from django.core.management.base import BaseCommand
from cms.pages.models import BasePage
from cms.publications.models import Publication, PublicationIndexPage


class Command(BaseCommand):
    help = "Deletes publications (bulk action)"

    def handle(self, *args, **options):
        """delete indiviual publications, start at the deepest level"""
        publications = Publication.objects.all().order_by("-depth")
        if not publications:
            sys.stdout.write("✅ Publications is empty\n")
        else:
            publications_length = publications.count()

            sys.stdout.write("Publications to delete: {}\n".format(publications_length))

            for publication in publications:
                publication.delete()
                sys.stdout.write("-")

            # delete sub site post index pages
            publication_indexes = PublicationIndexPage.objects.all().order_by("-depth")
            publication_indexes_length = publication_indexes.count()

            sys.stdout.write(
                "\n⌛️ Publications index pages to delete: {} may take a while\n".format(
                    publication_indexes_length
                )
            )

            for publication_index in publication_indexes:
                publication_index.delete()
                publication_indexes_length -= 1

            # delete the top level news index page
            try:
                publication_index = BasePage.objects.get(title="Publication Items Base")
                publication_index.delete()
            except BasePage.DoesNotExist:
                pass

            sys.stdout.write("\n")

            sys.stdout.write("✅ Complete\n")
