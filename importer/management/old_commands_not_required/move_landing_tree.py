import sys
from django.core.management import call_command
from django.core.management.base import BaseCommand
from nhsei_wagtail.pages.models import BasePage, LandingPage
from wagtail.core.models import Page


class Command(BaseCommand):
    """
    the purpose of this module is to move the pages into the correct tree position indicated by
    the wp_id.parent field that comes over from Wordpress. This is focused on the wordpress landing pages.
    we need to identify where the pages should really live perahps by csv update?
    """
    help = 'Moves pages into position under a temporary holding page'

    def handle(self, *args, **options):
        """ 
        sadly the wordpress ids are not unique because of the sub domains setup
        im guessing each subdomain or subsite has it's own database.
        need to try the the pages in the same source first so we move into the right place
        assuming an id in the sames source takes preference
        """

        ignore_theses_pages_by_slug = [
            'atnhs'
        ]

        pages = BasePage.objects.filter(wp_template='page-landing.php').order_by('-depth')

        print('Total Pages: {}'.format(pages.count()))

        counter = 1

        for page in pages:  # loop away
            # lets check for mulitple parents been available by wp_id
            print(counter) #so we know it's running
            move_to = None
            # has_multiple_parents = BasePage.objects.filter(wp_id=page.parent)
            # # print(has_multiple_parents)
            # if len(has_multiple_parents) > 1:
            #     # here we need to move to filtering the posible parents to the subsite
            #     # print('has multiple parents...')
            #     possible_parents = BasePage.objects.filter(
            #         source=page.source, wp_id=page.parent)
            #     if len(possible_parents) == 1:
            #         # print('can move this page inside subsite...')
            #         # but some pages have a parent of 0 when they do have a parent
            #         if page.real_parent != -1 and page.real_parent > 0:
            #             # use real_parent property in place of parent
            #             move_to = BasePage.objects.filter(
            #                 source=page.source, wp_id=page.real_parent)
            #         elif page.parent > 0:
            #             # use parent property as it's good
            #             move_to = BasePage.objects.filter(
            #                 source=page.source, wp_id=page.parent)
            #     else:
            #         print('possible parents error here, HOW SO!!!')
            #         break  # need to stop here as something serious is happening
            # elif page.parent != 0:
            #     # print('can move this page')
            #     move_to = BasePage.objects.filter(
            #         source=page.source, wp_id=page.parent)
            # elif page.parent == 0 and page.real_parent == 0 and page.source == 'pages':
            #     # here we are dealing with current top level pages that have no parent
            #     # some are components/landing pages so well add these below one of two
            #     # special page types. ComponentsPage or LandingPage
            #     # let amake these pages if they don't exist
            #     # THEY ARE ALL IN THE ROOT OF THE SITE source=pages
            #     print('!!!!!!!!!!!!!!!!!!!!!!')
            #     if page.wp_template == 'page-landing.php':
            #         # make a temporary parent if not exists
            try:
                landing_index_page = LandingPage.objects.first()
                if not landing_index_page:
                    home_page = Page.objects.filter(title='Home')[0]
                    landing_index_page = LandingPage(
                        title='Landing Page For wordpress Landing Pages',
                        body='The children of this page are all derived form word press landing pages where template=page-landing.php',
                        show_in_menus=True,
                        slug='landing-pages'
                    )
                    home_page.add_child(instance=landing_index_page)
                    rev = landing_index_page.save_revision()
                    rev.publish()
                # now make the move to
                move_to = Page.objects.filter(title='Landing Page For wordpress Landing Pages')
            except Page.DoesNotExist:
                sys.stdout.write('A wagtail page does not exist')


            #     elif page.wp_template == 'page-components.php':
            #         # make a temporary parent if not exists
            #         try:
            #             components_index_page = ComponentsPage.objects.first()
            #             if not components_index_page:
            #                 home_page = Page.objects.filter(title='Home')[0]
            #                 components_index_page = ComponentsPage(
            #                     title='Landing Page For wordpress Components Pages',
            #                     body='The children of this page are all derived form word press components pages where template=page-components.php',
            #                     show_in_menus=True,
            #                     slug='components-pages'
            #                 )
            #                 home_page.add_child(instance=components_index_page)
            #                 rev = components_index_page.save_revision()
            #                 rev.publish()
            #             # now make the move to
            #             move_to = Page.objects.filter(title='Landing Page For wordpress Components Pages')
            #         except Page.DoesNotExist:
            #             sys.stdout.write('A wagtail page does not exist')


            #     elif page.template == '':
            #         # maybe we can manually map these page to somewhere by csv?
            #         pass

            # else:
            #     print('This page cannot be moved {}'.format(page))
            #     break

            if not move_to and page.slug in ignore_theses_pages_by_slug:
                print('Move to page error {}'.format(page))
                # break
            elif move_to and len(move_to) == 1:
                page.move(move_to.first(), pos='last-child')

            # time.sleep(.05)
            counter += 1

    #     SOURCES = [
    #         # 'pages',
    #         # 'pages-aac',
    #         # 'pages-commissioning',
    #         # 'pages-coronavirus',
    #         # 'pages-greenernhs',
    #         # 'pages-improvement-hub',
    #         # 'pages-non-executive-opportunities',
    #         # 'pages-rightcare',
    #     ]

    #     # loop though the sources of subsites and deal with all base pages for each source
    #     # assuming a top page can only have children from the same source

    #     for source in SOURCES:
    #         # a reminder all the pages have equal depth till we move them :)

    #         print('Source: {}'.format(source))

    #         # Faux Parents
    #         pages_to_move = BasePage.objects.filter(source=source).exclude(real_parent=-1).exclude(parent__gt=0)
    #         for page in pages_to_move:
    #             print(page)
    #             has_valid_parent = BasePage.objects.filter(wp_id=page.real_parent)
    #             if has_valid_parent:
    #                 page.move(has_valid_parent.first(), pos='last-child')

    #         print(pages_to_move.count())

    #         # print('Has Faux Parent')
    #         # for page in BasePage.objects.filter(source=source, real_parent__gt=0, parent=0):
    #         #     # a faux parent had 0 as parent before but needs a parent page
    #         #     # print(page.real_parent)
    #         #     # parent = None
    #         #     # try:
    #         #     parent = BasePage.objects.filter(source=source, wp_id=page.real_parent).first()
    #         #     # except ObjectDoesNotExist:
    #         #         # parent = None
    #         #     if parent:
    #         #         page.move(parent, pos='last-child')
    #         #     else:
    #         #         print('A problem occured for {} ID:{} WP_ID:{}'.format(page, page.id, page.wp_id))

    #         # print('Natural Parent')
    #         # for page in BasePage.objects.filter(source=source, real_parent=0, parent__gt=0):
    #         #     # a natural already has a parent indicated so use that
    #         #     # print(page.id)
    #         #     # parent = None
    #         #     # try:
    #         #     parent = BasePage.objects.filter(source=source, wp_id=page.parent)
    #         #     # except ObjectDoesNotExist:
    #         #         # parent = None
    #         #     if parent.count() == 1:
    #         #         print(page.wp_id, parent.first().wp_id)
    #         #         page.move(parent.first(), pos='last-child')
    #         #     else:
    #         #         print('A problem occured for {} ID:{} WP_ID:{}'.format(page, page.id, page.wp_id))

    #         # print('Done...')

    # @staticmethod
    # def move_page(page, source):

    #     # print('{}       {}      {}'.format(page.parent, page.real_parent, page.title))

    #     # p = BasePage.objects.get(wp_id=page.parent)
    #     # r = BasePage.objects.get(wp_id=page.real_parent)

    #     if page.real_parent == -1:  # leave this in place for later
    #         print('Skipping Parent:{} ID:{} Title:{}'.format(
    #             page.parent, page.id, page))
    #     elif page.real_parent == 0 and page.parent > 0:  # move this page to its naturall parent
    #         print('Moving Parent:{} ID:{}'.format(page.parent, page.id))
    #         page.move(BasePage.objects.get(source=source,
    #                                        wp_id=page.parent), pos='last-child')
    #     elif page.parent == 0 and page.real_parent > 0:  # move this page to the alternate parent
    #         print('Moving Real Parent:{} ID:{}'.format(
    #             page.real_parent, page.id))
    #         page.move(BasePage.objects.get(source=source,
    #                                        wp_id=page.real_parent), pos='last-child')

    #     # if page.real_parent == -1: # leave this in place for later
    #     #     print('Skipping Parent:{} ID:{} Title:{}'.format(page.parent, page.id, page))
    #     # elif page.real_parent == 0 or page.real_page == '': # move this page to its naturall parent
    #     #     print('Moving Parent:{} ID:{}'.format(page.parent, page.id))
    #     #     page.move(BasePage.objects.get(source=source, wp_id=page.parent), pos='last-child')
    #     # else: # move this page to the alternate parent
    #     #     print('Moving Real Parent:{} ID:{}'.format(page.real_parent, page.id))
    #     #     page.move(BasePage.objects.get(source=source, wp_id=page.real_parent), pos='last-child')

    #     # if page.real_parent == 0:
    #     #     # we have all we need to do the move
    #         # move_to = BasePage.objects.get(source=source, wp_id=page.parent)
    #     #     # print('{} -> {}'.format(page, move_to))
    #     # elif page.real_parent > 0:
    #     #     # we need to move the page to a different parent (real_parent whcih is the wp_id)
    #     #     move_to = BasePage.objects.get(
    #     #         source=source, wp_id=page.real_parent)

    #     # if move_to:
    #     #     pass
    #         # page.move(move_to, pos='last-child')

    #         # print('{} -> {}'.format(page, move_to))

    #         # print(page.real_parent)
    #         # try:
    #         #     move_me = base_pages.get(source=source, wp_id=page.parent)
    #         #     if move_me.real_parent:
    #         #         # if source_pages:
    #         #         print('{} -> {}'.format(page, move_me))
    #         #         # page.move(source_pages[0], pos='last-child')
    #         # except BasePage.DoesNotExist:
    #         #     print('Not Found')

    #         # class Command(BaseCommand):
    #         #     """
    #         #     the purpose of this module is to move the pages into the correct tree position indicated by
    #         #     the wp_id.parent field that comes over from Wordpress. It's the best option we have just now.
    #         #     In the future there's going to need to be some adjusments Im sure but moveing a smaller amount
    #         #     of pages might be OK to do manually.
    #         #     """
    #         #     help = 'Moves pages into position indicated by the parent field (the wordpress page id)'

    #         #     def handle(self, *args, **options):
    #         #         # all_pages = Page.objects.all()

    #         #         # checkout the top pages all have parent=0 and not blank
    #         #         top_pages_check = [
    #         #             parent for parent in TopPage.objects.filter(parent__gt=0)]

    #         #         if top_pages_check:  # the check is for empty as success
    #         #             print('There are some top pages that have a parent ID not equal to 0')
    #         #         else:
    #         #             print('HAPPY! top pages check out OK')

    #         #         # checkout the child pages all have parent!=0
    #         #         child_pages_check = [
    #         #             child for child in BasePage.objects.filter(parent__lte=0)]

    #         #         if child_pages_check:  # the check is for empty as success
    #         #             print('There are some child pages that have no parent ID')
    #         #         else:
    #         #             print('HAPPY! child pages check out OK')

    #         #         print('moving on ...')

    #         #         """
    #         #         sadly the wordpress ids are not unique because of the sub domains setup
    #         #         im guessing each subdomain or subsite has it's own database.
    #         #         need to try the the pages in the same source first so we move into the right place
    #         #         assuming an id in the sames source takes preference
    #         #         might work better if reversed, then we're dealing with smaller sets to start with
    #         #         we'll see :)
    #         #         """

    #         #         SOURCES = [
    #         #             'pages',
    #         #             'pages-aac',
    #         #             'pages-commissioning',
    #         #             'pages-coronavirus',
    #         #             'pages-greenernhs',
    #         #             'pages-improvement-hub',
    #         #             'pages-non-executive-opportunities',
    #         #             'pages-rightcare',
    #         #         ]

    #         #         # loop though the sources and deal with all top and base pages for each source
    #         #         # assuming a top page can only have children from the same source
    #         #         # print('Top Pages No Filter: {} Base Pages No Filter: {}'.format(top_pages_parent_is_0.count(), child_pages_parent_not_0.count()))
    #         #         for source in SOURCES:
    #         #             # a reminder all the pages have equal depth till we move them :)
    #         #             base_pages = BasePage.objects.all()
    #         #             top_pages = TopPage.objects.all() # becuse a parent might be the top page

    #         #             print('Source: {}'.format(source))
    #         #             # top_pages.filter(source=source)
    #         #             print('Top Pages: {}'.format(top_pages.count()))
    #         #             # base_pages.filter(source=source)
    #         #             print('Base Pages: {}'.format(base_pages.count()))

    #         #             # can only move base_pages but can be moved to a top page

    #         #             for page in base_pages:
    #         #                 # may be dont need source here?
    #         #                 page_is_top = top_pages.filter(
    #         #                     wp_id=page.parent).first()
    #         #                 page_is_base = base_pages.filter(
    #         #                     wp_id=page.parent).first()

    #         #                 if not page_is_top:
    #         #                     # sanity check
    #         #                     if page_is_base:
    #         #                         # self.move_page(
    #         #                         #     page_is_base, base_pages, top_pages, source)
    #         #                         self.move_page(
    #         #                             page_is_base, base_pages, top_pages, source)
    #         #                     else:
    #         #                         print('error {}'.format(page_is_base))
    #         #                         print(page_is_top, page_is_base)
    #         #                 else:
    #         #                     print('was a top page already, leave it ...')

    #         #     def move_page(self, page, base_pages, top_pages, source):

    #         #         # parent_id = page.parent
    #         #         move_to_is_top = top_pages.filter(
    #         #             wp_id=page.parent, source=source).first()
    #         #         move_to_is_base = base_pages.filter(
    #         #             wp_id=page.parent, source=source).first()
    #         #         if not move_to_is_top and not move_to_is_base:  # it's not form the same source
    #         #             # redo the queries without source as no page was found
    #         #             # the parnet source is outide the page source
    #         #             move_to_is_top = top_pages.filter(
    #         #                 wp_id=page.parent).first()
    #         #             move_to_is_base = base_pages.filter(
    #         #                 wp_id=page.parent).first()

    #         #         # sanity check
    #         #         if not move_to_is_top and move_to_is_base: # we can go ahead
    #         #             print('moving page {} to '.format(move_to_is_base))
    #         #             page.move(move_to_is_base, pos='last-child')
    #         #         elif not move_to_is_base and move_to_is_top: #or we can go ahead
    #         #             print('moving page {} to {}'.format(page, move_to_is_top))
    #         #             page.move(move_to_is_top, pos='last-child')
    #         #         else:
    #         #             print('!!!!!!!!!!!!!!!!!!! somthing is not right, leave it ...')
