import sys
import time

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from nhsei_wagtail.pages.models import ComponentsPage


class Command(BaseCommand):
    """
    the purpose of this module is to fix the commissioning page slug that gets set to home-2 from wordpress.
    """
    help = 'Fixes commissioning page slug'

    def handle(self, *args, **options):

        page = ComponentsPage.objects.get(slug='home-2')

        # for page in pages:
            # if page.slug not in FIX_SLUGS_IGNORE:
        first_published = page.first_published_at
        last_published = page.last_published_at
        latest_revision_created = page.latest_revision_created_at

        # source = page.source
        # slug = 'commissioning'
        page.slug = 'commissioning'
        sys.stdout.write('\n⚙️ {} SLUG updated'.format(page))

        # """
        # running save_revision() as it seems like a good idea to not break page paths
        # just to be safe...
        # try to keep revision dates to match whats in wordpress as our
        # revisions reset that at the save()
        # """
        # try:
        rev = page.save_revision()
        page.first_published_at = first_published
        page.last_published_at = last_published
        page.latest_revision_created_at = latest_revision_created
        page.save()
        rev.publish()
        # except ValidationError:
        #     print(
        #         '⚠️ {} slug cannot be updated... we should log theses problems!!!'.format(page))
        #     time.sleep(2)

        # sys.stdout.write('\n✅  All slugs fixed\n')
