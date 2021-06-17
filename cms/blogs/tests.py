from bs4 import BeautifulSoup
from cms.blogs.models import BlogIndexPage
from django.test import TestCase


class TestBlogIndexPage(TestCase):

    # or load whichever file you piped it to
    fixtures = ["fixtures/testdata.json"]

    """below was changed"""

    def test_first_heading(self):
        response = self.client.get("/blog-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.select_one("main h1")

        self.assertEqual(heading.text, "Blog Index Page")

    def test_first_paragrpah(self):
        response = self.client.get("/blog-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.select_one("main p")

        self.assertEqual(heading.text, "Blog Index Content")

    def test_blog_list(self):
        response = self.client.get("/blog-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        blog_newest = soup.select_one(
            "main .nhsuk-width-container:nth-child(3) .nhsuk-panel:nth-of-type(1)"
        )

        # heading
        self.assertEqual(blog_newest.select_one("h2").text.strip(), "Blog Post Two")
        self.assertEqual(
            blog_newest.select_one("h2 a")["href"], "/blog-index-page/blog-post-two/"
        )

        # paragraph
        self.assertGreater(
            len(blog_newest.select_one("div.nhsuk-u-margin-bottom-3").text.strip()), 0
        )

        # dates
        self.assertIn(
            blog_newest.select_one("p.nhsuk-body-s").text.strip()[:23],
            "Published:  04 Feb 2021 -",
        )

        # topics
        self.assertEqual(
            blog_newest.select_one("p.nhsuk-body-s a:nth-of-type(1)").text.strip(),
            "Category Two",
        )
        self.assertEqual(
            blog_newest.select_one("p.nhsuk-body-s a:nth-of-type(1)")["href"],
            "?category=2",
        )

        blog_oldest = soup.select_one(
            "main .nhsuk-width-container:nth-child(3) .nhsuk-panel:nth-of-type(2)"
        )

        # heading
        self.assertEqual(blog_oldest.select_one("h2").text.strip(), "Blog Post One")
        self.assertEqual(
            blog_oldest.select_one("h2 a")["href"], "/blog-index-page/blog-post-one/"
        )

        # paragraph
        self.assertGreater(
            len(blog_oldest.select_one("div.nhsuk-u-margin-bottom-3").text.strip()), 0
        )

        # dates
        self.assertIn(
            blog_oldest.select_one("p.nhsuk-body-s").text.strip()[:23],
            "Published:  04 Feb 2021 -",
        )

        # topics
        self.assertEqual(
            blog_oldest.select_one("p.nhsuk-body-s a:nth-of-type(1)").text.strip(),
            "Category One",
        )
        self.assertEqual(
            blog_oldest.select_one("p.nhsuk-body-s a:nth-of-type(1)")["href"],
            "?category=1",
        )

    def test_get_latest_blogs(self):
        index_page = BlogIndexPage.objects.get(slug="blog-index-page")
        latest = index_page.get_latest_blogs(2)
        self.assertEqual(latest.count(), 2)

    def test_get_context(self):
        response = self.client.get("/blog-index-page/")
        context = response.context

        self.assertEqual(context["title"], "Blog Index Page")
        self.assertEqual(len(context["blogs"]), 2)
        self.assertEqual(len(context["categories"]), 2)


class TestBlog(TestCase):

    # or load whichever file you piped it to
    fixtures = ["fixtures/testdata.json"]

    # theres a couple of pages worth testing

    def test_oldest_blog(self):
        # this page is using a PDF document link
        response = self.client.get("/blog-index-page/blog-post-one/")
        soup = BeautifulSoup(response.content, "html.parser")

        # page title
        title = soup.select_one("main h1").text.strip()
        self.assertEqual(title, "Blog Post One")

        # page content just the first p tag
        content = soup.select_one("main p").text.strip()
        self.assertEqual(content, "Blog Post Content")

        # review date
        # better to test these actual date objects as unittest I think, one for later
        date_container = soup.select_one("main .nhsuk-review-date")
        self.assertIn(date_container.text.strip()[:20], "Published: 04 Feb 2021")

        # # taxonomy links
        category_1 = soup.select_one("main a:nth-of-type(1)")
        self.assertEqual(category_1["href"], "/blog-index-page/?category=1")
        self.assertEqual(category_1.text.strip(), "Category One")

    def test_newest_blog(self):
        # this page is using a PDF document link
        response = self.client.get("/blog-index-page/blog-post-two/")
        soup = BeautifulSoup(response.content, "html.parser")

        # page title
        title = soup.select_one("main h1").text.strip()
        self.assertEqual(title, "Blog Post Two")

        # page content just the first p tag
        content = soup.select_one("main p").text.strip()
        self.assertEqual(content, "Blog Post Two")

        # review date
        # better to test these actual date objects as unittest I think, one for later
        date_container = soup.select_one("main .nhsuk-review-date")
        self.assertIn(date_container.text.strip()[:20], "Published: 04 Feb 2021")

        # # taxonomy links
        category_1 = soup.select_one("main a:nth-of-type(1)")
        self.assertEqual(category_1["href"], "/blog-index-page/?category=2")
        self.assertEqual(category_1.text.strip(), "Category Two")
