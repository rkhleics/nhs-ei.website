import sys
import time

from django.core.management import call_command
from cms.categories.models import Region

from .importer_cls import Importer


# the indiators from wordpress aren't nice so map them to better titles
# SOURCES = {
#     'categories': 'NHS England & Improvement',
#     'categories-aac': 'Accelerated Access Collaborative',
#     'categories-commissioning': 'Commissioning',
#     'categories-coronavirus': 'Corovavirus',
#     'categories-greenernhs': 'Greener NHS',
#     'categories-improvement-hub': 'Improvement Hub',
#     'categories-non-executive-opportunities': 'Non-executive opportunities',
#     'categories-rightcare': 'Right Care',
# }


class RegionsImporter(Importer):
    def __init__(self):
        regions = Region.objects.all()
        # category_sub_sites = CategorySubSite.objects.all()
        if regions:
            sys.stdout.write("⚠️  Run delete_regions before running this command\n")
            sys.exit()

    def parse_results(self):
        regions = self.results
        for r in regions:
            # if the subsite parent for this category does not exits make it once
            # try:
            #     category_sub_site = CategorySubSite.objects.get(source=r.get('source'))
            # except CategorySubSite.DoesNotExist:
            #     title = SOURCES.get(r.get('source'))
            #     sys.stdout.write('.')
            #     category_sub_site = CategorySubSite(
            #         title = title,
            #         source = r.get('source')
            #     )
            #     category_sub_site.save()

            region = Region(
                name=r.get("name"),
                slug=r.get("slug"),
                description=r.get("description"),
                wp_id=r.get("wp_id"),
                # source = r.get('source'),
                # sub_site = category_sub_site
            )
            region.save()
            sys.stdout.write(".")

        if self.next:
            time.sleep(self.sleep_between_fetches)
            self.fetch_url(self.next)
            self.parse_results()
        return Region.objects.count(), self.count
