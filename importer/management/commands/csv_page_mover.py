import csv
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    """
    the purpose of this module is to move pages undr the correct parent according to worpress.
    """

    help = "Moves pages into position indicated by the parent field (the wordpress page id)"

    def handle(self, *args, **options):
        IMPORTER_PATH = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        csv_path = os.path.join(IMPORTER_PATH, "bin/moves.csv")
        # print(csv_path)
        # csv_file = Path('../../bin/moves.csv')
        input_file = csv.DictReader(open(csv_path), fieldnames=["from", "to"])
        for row in input_file:
            print(row["from"])
            # page_to_move = BasePage.objects.get(wp_link=row['to'])
            # page_to_receive = BasePage.objects.get(wp_link=row['to'])
            # print(page_to_move)
        # print(input_file)
        # keys = input_file.keys()
        # for key in keys:
        #     print(key)
        # pages = BasePage.objects.exclude(title='News Items Base')

        # if not pages:
        #     sys.stdout.write(
        #         '⚠️  Run `runimport pages` before running this command\n')
        #     sys.exit()

        # for page in pages:
        #     sys.stdout.write('\n⌛️ {} is moving'.format(page))

        #     parent_id = Ancestry(page).get_parent()
        #     if parent_id:
        #         parent = BasePage.objects.get(id=parent_id)
        #         page.move(parent, pos='last-child')
        #         sys.stdout.write('\n✅ {} done'.format(page))

        # sys.stdout.write('\n✅  All pages moved\n')
