from django.core.management.base import BaseCommand

# from nhsei_wagtail.tags.models import Tag
from django.core.management import call_command
import time


# class Command(BaseCommand):
#     help = 'Deletes categories (bulk action)'

#     def handle(self, *args, **options):
#         # depth order to start at deepest pages
#         tags = Tag.objects.all()
#         tags_length = len(tags)
#         print('Tags to delete:{} This will take some time to run...'.format(tags_length))
#         for tag in tags:
#             print('{} {}'.format(tags_length, tag))
#             tag.delete()
#             tags_length -= 1
