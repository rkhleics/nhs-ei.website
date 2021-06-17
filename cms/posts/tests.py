from bs4 import BeautifulSoup
from django.test import TestCase


class TestPostIndexPage(TestCase):

    # or load whichever file you piped it to
    fixtures = ["fixtures/testdata.json"]

    """below was changed"""

    def test_first_heading(self):
        response = self.client.get("/post-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.select_one("main h1")

        self.assertEqual(heading.text, "Post Index Page")

    def test_first_paragrpah(self):
        response = self.client.get("/post-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.select_one("main p")

        self.assertEqual(heading.text, "Post index page content")

    def test_post_list(self):
        response = self.client.get("/post-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        post_newest = soup.select_one(
            "main .nhsuk-width-container:nth-child(3) .nhsuk-panel:nth-of-type(1)"
        )

        # heading
        self.assertEqual(post_newest.select_one("h2").text.strip(), "Post Two")
        self.assertEqual(
            post_newest.select_one("h2 a")["href"], "/post-index-page/post-two/"
        )

        # paragraph
        self.assertGreater(
            len(post_newest.select_one("div.nhsuk-u-margin-bottom-3").text.strip()), 0
        )

        # dates
        self.assertIn(
            post_newest.select_one("p.nhsuk-body-s").text.strip()[:23],
            "Published:  04 Feb 2021 -",
        )

        # topics
        self.assertEqual(
            post_newest.select_one("p.nhsuk-body-s a:nth-of-type(1)").text.strip(),
            "Category One",
        )
        self.assertEqual(
            post_newest.select_one("p.nhsuk-body-s a:nth-of-type(1)")["href"],
            "?category=1",
        )

        post_oldest = soup.select_one(
            "main .nhsuk-width-container:nth-child(3) .nhsuk-panel:nth-of-type(2)"
        )

        # heading
        self.assertEqual(post_oldest.select_one("h2").text.strip(), "Post One")
        self.assertEqual(
            post_oldest.select_one("h2 a")["href"], "/post-index-page/post-one/"
        )

        # paragraph
        self.assertGreater(
            len(post_oldest.select_one("div.nhsuk-u-margin-bottom-3").text.strip()), 0
        )

        # dates
        self.assertIn(
            post_oldest.select_one("p.nhsuk-body-s").text.strip()[:23],
            "Published:  04 Feb 2021 -",
        )

        # topics
        self.assertEqual(
            post_oldest.select_one("p.nhsuk-body-s a:nth-of-type(1)").text.strip(),
            "Category One",
        )
        self.assertEqual(
            post_oldest.select_one("p.nhsuk-body-s a:nth-of-type(1)")["href"],
            "?category=1",
        )


class TestPost(TestCase):

    # or load whichever file you piped it to
    fixtures = ["fixtures/testdata.json"]

    # theres a couple of pages worth testing

    def test_oldest_post(self):
        # this page is using a PDF document link
        response = self.client.get("/post-index-page/post-one/")
        soup = BeautifulSoup(response.content, "html.parser")

        # page title
        title = soup.select_one("main h1").text.strip()
        self.assertEqual(title, "Post One")

        # page content just the first p tag
        content = soup.select_one("main p").text.strip()
        self.assertEqual(content, "Post one content")

        # review date
        # better to test these actual date objects as unittest I think, one for later
        date_container = soup.select_one("main .nhsuk-review-date")
        self.assertIn(date_container.text.strip()[:20], "Published: 04 Feb 2021")

        # taxonomy links
        category_1 = soup.select_one("main a:nth-of-type(1)")
        self.assertEqual(category_1["href"], "/post-index-page/?category=1")
        self.assertEqual(category_1.text.strip(), "Category One")

    def test_newest_blog(self):
        # this page is using a PDF document link
        response = self.client.get("/post-index-page/post-two/")
        soup = BeautifulSoup(response.content, "html.parser")

        # page title
        title = soup.select_one("main h1").text.strip()
        self.assertEqual(title, "Post Two")

        # page content just the first p tag
        content = soup.select_one("main p").text.strip()
        self.assertEqual(content, "Post one content")  # fixture has this content 🙄

        # review date
        # better to test these actual date objects as unittest I think, one for later
        date_container = soup.select_one("main .nhsuk-review-date")
        self.assertIn(date_container.text.strip()[:20], "Published: 04 Feb 2021")

        # taxonomy links
        category_1 = soup.select_one("main a:nth-of-type(1)")
        self.assertEqual(category_1["href"], "/post-index-page/?category=1")
        self.assertEqual(category_1.text.strip(), "Category One")
