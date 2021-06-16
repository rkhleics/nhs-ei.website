from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Deletes base pages (bulk action)"

    def handle(self, *args, **options):
        call_command("delete_blogs")
        call_command("delete_posts")
        call_command("delete_atlas_case_studies")
        call_command("delete_publications")
        call_command("delete_pages")
        call_command("delete_components_pages")
        call_command("delete_landing_pages")
        call_command("delete_categories")
        call_command("delete_publication_types")
        call_command("delete_regions")
        call_command("delete_settings")
        call_command("delete_media_files")
