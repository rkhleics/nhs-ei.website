import sys
import time

from django.core.management import call_command

# from nhsei_wagtail.tags.models import Tag

# from .importer_cls import Importer


# class TagsImporter(Importer):
#     def __init__(self, should_delete):
#         if should_delete:
#             sys.stdout.write('Emptying categories ...\n')
#             call_command('delete_tags')

#     def parse_results(self):
#         tags = self.results
#         for r in tags:
#             tag = Tag(
#                 name=r.get('name'),
#                 slug=r.get('slug'),
#                 description=r.get('description'),
#                 wp_id=r.get('wp_id'),
#                 source = r.get('source')
#             )
#             tag.save()
#         if self.next:
#             time.sleep(self.sleep_between_fetches)
#             self.fetch_url(self.next)
#             self.parse_results()
#         return Tag.objects.count(), self.count
