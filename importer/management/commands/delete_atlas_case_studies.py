import sys
import time

from django.core.management.base import BaseCommand
from cms.pages.models import BasePage
from cms.atlascasestudies.models import AtlasCaseStudy, AtlasCaseStudyIndexPage


class Command(BaseCommand):
    help = "Deletes atlas case studies (bulk action)"

    def handle(self, *args, **options):
        """delete indiviual case studies, start at the deepest level"""
        atlas_case_studies = AtlasCaseStudy.objects.all().order_by("-depth")

        if not atlas_case_studies:
            sys.stdout.write("✅ Atlas Case Studies is empty\n")

        atlas_case_studies_length = atlas_case_studies.count()

        sys.stdout.write(
            "Atlas Case Studies to delete: {}\n".format(atlas_case_studies_length)
        )

        for atlas_case_study in atlas_case_studies:
            atlas_case_study.delete()
            sys.stdout.write("-")

        # delete the top level news index page
        try:
            atlas_case_study_index = AtlasCaseStudyIndexPage.objects.get(
                title="Atlas Case Studies"
            )
            atlas_case_study_index.delete()
        except AtlasCaseStudyIndexPage.DoesNotExist:
            pass

        sys.stdout.write("\n")

        sys.stdout.write("✅ Complete\n")
