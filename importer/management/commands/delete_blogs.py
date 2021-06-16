import sys

from django.core.management.base import BaseCommand
from cms.blogs.models import Blog, BlogIndexPage


class Command(BaseCommand):
    help = "Deletes blogs (bulk action)"

    def handle(self, *args, **options):
        # depth order to start at deepest pages, seems sensible
        blogs = Blog.objects.all().order_by("-depth")
        if not blogs:
            sys.stdout.write("✅ Blogs is empty\n")
        else:
            blogs_length = blogs.count()

            sys.stdout.write("\n⌛️ Blogs to delete: {}\n".format(blogs_length))

            for blog in blogs:
                blog.delete()
                sys.stdout.write("-")

            blog_indexes = BlogIndexPage.objects.all().order_by("-depth")
            blog_indexes_length = blog_indexes.count()

            sys.stdout.write(
                "\n⌛️ Blog index pages to delete: {} may take a while\n".format(
                    blog_indexes_length
                )
            )

            for blog_index in blog_indexes:
                blog_index.delete()
                blogs_length -= 1

            sys.stdout.write("\n")

            sys.stdout.write("✅ Complete\n")
