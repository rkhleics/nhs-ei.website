import sys
import time

from django.core.management.base import BaseCommand
from cms.pages.models import BasePage
from cms.posts.models import Post, PostIndexPage


class Command(BaseCommand):
    help = "Deletes posts (bulk action)"

    def handle(self, *args, **options):
        """delete indiviual posts, start at the deepest level"""
        posts = Post.objects.all().order_by("-depth")
        if not posts:
            sys.stdout.write("✅ Posts is empty\n")
        else:
            posts_length = posts.count()

            sys.stdout.write("Posts to delete: {}\n".format(posts_length))

            for post in posts:
                post.delete()
                sys.stdout.write("-")

            # delete sub site post index pages
            post_indexes = PostIndexPage.objects.all().order_by("-depth")
            post_indexes_length = post_indexes.count()

            sys.stdout.write(
                "\n⌛️ Post index pages to delete: {} may take a while\n".format(
                    post_indexes_length
                )
            )

            for post_index in post_indexes:
                post_index.delete()
                post_indexes_length -= 1

            # delete the top level news index page
            try:
                post_index = BasePage.objects.get(title="News Items Base")
                post_index.delete()
            except BasePage.DoesNotExist:
                pass

            sys.stdout.write("\n")

            sys.stdout.write("✅ Complete\n")
