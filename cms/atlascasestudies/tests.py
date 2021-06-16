from bs4 import BeautifulSoup
from cms.atlascasestudies.models import AtlasCaseStudyIndexPage
from django.test import TestCase


class TestAtlasCaseStudyIndexPage(TestCase):

    # or load whichever file you piped it to
    fixtures = ["fixtures/testdata.json"]

    def test_first_heading(self):
        response = self.client.get("/atlas-case-studies-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.select_one("main h1")

        self.assertEqual(heading.text, "Atlas Case Studies Index Page")

    def test_first_paragrpah(self):
        response = self.client.get("/atlas-case-studies-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.select_one("main p")

        self.assertEqual(heading.text, "Atlas case studies Index Page")

    def test_side_bar(self):
        # in the test data we have 2 of each of settings, regions and topics
        # check that all show up in a-z order and link to correct url
        response = self.client.get("/atlas-case-studies-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        setting_1 = soup.select_one('main a[href="?setting=1"]')
        setting_2 = soup.select_one('main a[href="?setting=2"]')

        self.assertEqual(setting_1.text, "Setting One")
        self.assertEqual(setting_1["href"], "?setting=1")
        self.assertEqual(setting_2.text, "Setting Two")
        self.assertEqual(setting_2["href"], "?setting=2")

        region_1 = soup.select_one('main a[href="?region=1"]')
        region_2 = soup.select_one('main a[href="?region=2"]')

        self.assertEqual(region_1.text, "Region One")
        self.assertEqual(region_1["href"], "?region=1")
        self.assertEqual(region_2.text, "Region Two")
        self.assertEqual(region_2["href"], "?region=2")

        # careful because topics are actually categories!
        topic_1 = soup.select_one('main a[href="?category=1"]')
        topic_2 = soup.select_one('main a[href="?category=2"]')

        self.assertEqual(topic_1.text, "Category One")
        self.assertEqual(topic_1["href"], "?category=1")
        self.assertEqual(topic_2.text, "Category Two")
        self.assertEqual(topic_2["href"], "?category=2")

    def test_case_study_list(self):
        response = self.client.get("/atlas-case-studies-index-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        case_list = soup.select_one(
            "main .nhsuk-width-container:nth-child(3) .nhsuk-panel"
        )

        # heading
        self.assertEqual(
            case_list.select_one("h2").text.strip(), "Atlas Case Study One"
        )
        self.assertEqual(
            case_list.select_one("h2 a")["href"],
            "/atlas-case-studies-index-page/atlas-case-study-one/",
        )

        # paragraph
        self.assertEqual(
            case_list.select_one("div.nhsuk-u-margin-bottom-3").text.strip(),
            "Atlas case study one content",
        )

        # dates
        self.assertIn(
            case_list.select_one("p.nhsuk-body-s").text.strip()[:30],
            "Published:  04 February 2021 -",
        )

        # links
        self.assertEqual(
            case_list.select_one("p.nhsuk-body-s a:nth-of-type(1)").text.strip(),
            "Category One",
        )
        self.assertEqual(
            case_list.select_one("p.nhsuk-body-s a:nth-of-type(1)")["href"],
            "?category=1",
        )

        self.assertEqual(
            case_list.select_one("p.nhsuk-body-s a:nth-of-type(2)").text.strip(),
            "Setting One",
        )
        self.assertEqual(
            case_list.select_one("p.nhsuk-body-s a:nth-of-type(2)")["href"],
            "?setting=1",
        )

        self.assertEqual(
            case_list.select_one("p.nhsuk-body-s a:nth-of-type(3)").text.strip(),
            "Region One",
        )
        self.assertEqual(
            case_list.select_one("p.nhsuk-body-s a:nth-of-type(3)")["href"], "?region=1"
        )

    def test_get_latest_atlas_case_studies(self):
        index_page = AtlasCaseStudyIndexPage.objects.get(
            slug="atlas-case-studies-index-page"
        )
        latest = index_page.get_latest_atlas_case_studies(1)
        self.assertEqual(latest.count(), 1)

    def test_get_context(self):
        response = self.client.get("/atlas-case-studies-index-page/")
        context = response.context

        self.assertEqual(context["title"], "Atlas Case Studies Index Page")
        self.assertEqual(len(context["atlas_case_studies"]), 1)
        self.assertEqual(len(context["categories"]), 2)
        self.assertEqual(len(context["setting"]), 2)
        self.assertEqual(len(context["regions"]), 2)


class TestAtlasCaseStudy(TestCase):

    # or load whichever file you piped it to
    fixtures = ["fixtures/testdata.json"]

    def test_page_title(self):
        response = self.client.get(
            "/atlas-case-studies-index-page/atlas-case-study-one/"
        )
        soup = BeautifulSoup(response.content, "html.parser")

        # page title
        title = soup.select_one("main h1").text.strip()
        self.assertEqual(title, "Atlas Case Study One")

    def test_page_content(self):
        response = self.client.get(
            "/atlas-case-studies-index-page/atlas-case-study-one/"
        )
        soup = BeautifulSoup(response.content, "html.parser")

        # page content
        content = soup.select_one("main p").text.strip()
        self.assertEqual(content, "Atlas case study one content")

    def test_taxonomy_link(self):
        response = self.client.get(
            "/atlas-case-studies-index-page/atlas-case-study-one/"
        )
        soup = BeautifulSoup(response.content, "html.parser")

        # taxonomy links
        topic_1 = soup.select_one("main a:nth-of-type(1)")
        self.assertEqual(topic_1["href"], "/atlas-case-studies-index-page/?category=1")
        self.assertEqual(topic_1.text.strip(), "Category One")

        setting_1 = soup.select_one("main a:nth-of-type(2)")
        self.assertEqual(setting_1["href"], "/atlas-case-studies-index-page/?setting=1")
        self.assertEqual(setting_1.text.strip(), "Setting One")

        region_1 = soup.select_one("main a:nth-of-type(3)")
        self.assertEqual(region_1["href"], "/atlas-case-studies-index-page/?region=1")
        self.assertEqual(region_1.text.strip(), "Region One")
