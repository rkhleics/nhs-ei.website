# import sys
# import time
# from os import write
# from sys import stdout

# from django.utils.html import strip_tags
# from nhsei_wagtail.pages.models import BasePage
# from wagtail.core.models import Page

# from .importer_cls import Importer


# class PagesTopImporter(Importer):
#     def __init__(self, should_delete):
#         if should_delete:
#             sys.stdout.write('Emptying Table ...')
#             # seems this is too many to do in one go with SQLITE, postgres might be OK
#             # but lets keep it sane, there must be lots going on in Wagtail
#             pages = TopPage.objects.all()
#             for page in pages:
#                 sys.stdout.write('{} deleted \n'.format(page))
#                 page.delete()

#     def parse_results(self):
#         # make a blog index page to use for now ...
#         home_page = Page.objects.filter(
#             title='Home')[0]  # should always exists 😲
#         # try:
#         #     home_page = Page.objects.filter(title='Home')[0]
#         #     if not home_page:
#         #         # get the root page. might need further work here
#         #         home_page = Page.objects.filter(title='Home')[0]
#         #         blog_index_page = BlogIndexPage(
#         #             title='Blogs',
#         #             body='A small amout of body text, this content needs to be part of the import process',
#         #             show_in_menus=True,
#         #             slug='blogs'
#         #         )
#         #         home_page.add_child(instance=blog_index_page)
#         #         rev = blog_index_page.save_revision()
#         #         rev.publish()
#         #         # blog_index_page.save()

#         # except Page.DoesNotExist:
#         #     sys.stdout.write('A wagtail page does not exist')

#         pages = self.results  # this is json result set
#         for page in pages:
#             first_published_at = page.get('date')
#             last_published_at = page.get('modified')
#             latest_revision_created_at = page.get('modified')

#             obj = TopPage(
#                 title=page.get('title'),
#                 excerpt=strip_tags(page.get('excerpt')),  # removing html tags
#                 body=page.get('content'),
#                 show_in_menus=True,
#                 wp_id=page.get('wp_id'),
#                 author=page.get('author'),
#                 parent=page.get('parent'),
#                 source = page.get('source')
#             )
#             home_page.add_child(instance=obj)
#             rev = obj.save_revision()  # this needs to run here

#             # update the page and add the categories if available
#             # try:
#             #     cats = blog.get('categories').split(' ')
#             #     for c in cats:
#             #         category = Category.objects.get(wp_id=c)
#             #         obj.categories.add(category)
#             #         rev = obj.save_revision()
#             #         rev.publish()
#             # except:
#             #     pass

#             obj.first_published_at = first_published_at
#             obj.last_published_at = last_published_at
#             obj.latest_revision_created_at = latest_revision_created_at
#             # probably not the best way to do this but need to update the dates on the page record.
#             obj.save()
#             rev.publish()

#         if self.next:
#             time.sleep(self.sleep_between_fetches)
#             self.fetch_url(self.next)
#             self.parse_results()
#         return TopPage.objects.live().descendant_of(home_page).count(), self.count
