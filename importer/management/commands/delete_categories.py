import sys
import time

from django.core.management.base import BaseCommand
from cms.categories.models import Category, CategorySubSite
from cms.posts.models import Post
from cms.blogs.models import Blog


class Command(BaseCommand):
    help = "Deletes categories (bulk action)"

    def handle(self, *args, **options):
        """remove categories first"""
        posts = Post.objects.all()
        blogs = Blog.objects.all()
        if posts or blogs:
            sys.stdout.write(
                "⚠️ Please delete posts and blogs before running this commend\n"
            )
            sys.exit()

        categories = Category.objects.all()
        if not categories.count():
            sys.stdout.write("✅ Categories is empty\n")
        else:

            categories_length = len(categories)

            sys.stdout.write("Categories to delete: {}\n".format(categories_length))

            for category in categories:
                sys.stdout.write("-")
                category.delete()
                categories_length -= 1

                # time.sleep(.3)

            sys.stdout.write("\n")

            """ remove category sub sites last """
            category_sub_sites = CategorySubSite.objects.all()
            category_sub_sites_length = len(category_sub_sites)

            sys.stdout.write(
                "Categories Sub Sites to delete: {}\n".format(category_sub_sites_length)
            )

            for category_sub_site in category_sub_sites:
                sys.stdout.write("-")
                category_sub_site.delete()
                category_sub_sites_length -= 1

                # time.sleep(.3)

            sys.stdout.write("\n")

            sys.stdout.write("✅ Complete\n")
