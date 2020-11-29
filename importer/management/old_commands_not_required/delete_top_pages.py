from django.core.management.base import BaseCommand
# from nhsei_wagtail.pages.models import TopPage
from django.core.management import call_command
import time


# class Command(BaseCommand):
#     help = 'Deletes top pages (bulk action)'

#     def handle(self, *args, **options):
#         # depth order to start at deepest pages
#         pages = TopPage.objects.all().order_by('depth')
#         pages_length = len(pages)
#         print('Top Pages to delete:{} This will take some time to run...'.format(len(pages)))
#         for page in pages:
#             print('{} {}'.format(pages_length, page))
#             page.delete()
#             pages_length -= 1