import sys
import time

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from nhsei_wagtail.pages.models import BasePage, ComponentsPage


"""" WE NO LONGER NEED TO RUN THIS """


class Command(BaseCommand):
    """
    the purpose of this module is to fix pages slugs and only fix sub sites plus others
    defind later on such as moving them into the new hierarchy.
    there's lots of pages still at the top level that should be at a lower level
    """
    help = 'Fixes page slugs subsite and more'

    def handle(self, *args, **options):
        """ 
        we need to loop through every base page model and get the original slug
        updated to be the same as the slug in SCRAPY but only for slugs represented below in SOURCES
        changing a parent page must update the path for child pages too
        """

        # they look strange but are what comes over from wordpress API
        # im giessing there are redirects in place to make this work
        SOURCES = {
            'sample-page': 'aac',
            'home-2': 'commissioning',
            'nhs-england-and-nhs-improvement-corona-virus': 'coronavirus',
            'greener-nhs': 'greenernhs',
            'improvement-knowledge-hub': 'improvement-hub',
            'tbc': 'non-executive-opportunities',
            'nhs-rightcare': 'rightcare',
        }
        # for BasePage models
        pages = BasePage.objects.all().order_by('-depth')

        for page in pages:
            first_published = page.first_published_at
            last_published = page.last_published_at
            latest_revision_created = page.latest_revision_created_at

            if page.slug in SOURCES.keys():
                # print(SOURCES[page.wp_slug])
                sys.stdout.write('\n✅ {} is fixed'.format(SOURCES[page.wp_slug]))
                slug = SOURCES[page.wp_slug]
                page.slug = slug
                """
                running save_revision() as it seems like a good idea to not break page paths
                just to be safe...
                try to keep revision dates to match whats in wordpress as our
                revisions reset that at the save()
                """
                try:
                    rev = page.save_revision()
                    page.first_published_at = first_published
                    page.last_published_at = last_published
                    page.latest_revision_created_at = latest_revision_created
                    # probably not the best way to do this but need to update the dates on the page record
                    # to keep in sync with wordpress at the import stage
                    # futher imports will collect new data and new dates.
                    page.save()
                    rev.publish()
                except ValidationError:
                    print('⚠️ {} slug cannot be updated!!!'.format(page))
                    time.sleep(2)

        # for ComponentsPage models
        # pages = ComponentsPage.objects.all().order_by('-depth')

        # for page in pages:
        #     first_published = page.first_published_at
        #     last_published = page.last_published_at
        #     latest_revision_created = page.latest_revision_created_at

        #     if page.slug in SOURCES.keys():
        #         # print(SOURCES[page.wp_slug])
        #         sys.stdout.write('\n✅ {} is fixed'.format(SOURCES[page.wp_slug]))
        #         slug = SOURCES[page.wp_slug]
        #         page.slug = slug
        #         """
        #         running save_revision() as it seems like a good idea to not break page paths
        #         just to be safe...
        #         try to keep revision dates to match whats in wordpress as our
        #         revisions reset that at the save()
        #         """
        #         try:
        #             rev = page.save_revision()
        #             page.first_published_at = first_published
        #             page.last_published_at = last_published
        #             page.latest_revision_created_at = latest_revision_created
        #             # probably not the best way to do this but need to update the dates on the page record
        #             # to keep in sync with wordpress at the import stage
        #             # futher imports will collect new data and new dates.
        #             page.save()
        #             rev.publish()
        #         except ValidationError:
        #             print('⚠️ {} slug cannot be updated!!!'.format(page))
        #             time.sleep(2)

        sys.stdout.write('\n✅ Done\n')
