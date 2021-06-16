import sys
import time

from django.core.management.base import BaseCommand
from cms.categories.models import (
    Category,
    CategorySubSite,
    PublicationType,
    PublicationTypeSubSite,
)
from cms.posts.models import Post
from cms.blogs.models import Blog
from cms.publications.models import Publication


class Command(BaseCommand):
    help = "Deletes publicaton types (bulk action)"

    def handle(self, *args, **options):
        """remove publciation types first"""
        publications = Publication.objects.all()
        if publications:
            sys.stdout.write(
                "⚠️ Please delete publications before running this commend\n"
            )
            sys.exit()

        publication_types = PublicationType.objects.all()
        if not publication_types.count():
            sys.stdout.write("✅ Publication Types is empty\n")
        else:

            publication_types_length = len(publication_types)

            sys.stdout.write(
                "Publication Types to delete: {}\n".format(publication_types_length)
            )

            for publication_type in publication_types:
                sys.stdout.write("-")
                publication_type.delete()
                publication_types_length -= 1

                # time.sleep(.3)

            sys.stdout.write("\n")

            """ remove category sub sites last """
            publication_type_sub_sites = PublicationTypeSubSite.objects.all()
            publication_type_sub_sites_length = len(publication_type_sub_sites)

            sys.stdout.write(
                "Publication Type Sub Sites to delete: {}\n".format(
                    publication_type_sub_sites_length
                )
            )

            for publicaiton_type_sub_site in publication_type_sub_sites:
                sys.stdout.write("-")
                publicaiton_type_sub_site.delete()
                publication_type_sub_sites_length -= 1

                # time.sleep(.3)

            sys.stdout.write("\n")

            sys.stdout.write("✅ Complete\n")
