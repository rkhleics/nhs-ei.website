from bs4 import BeautifulSoup
from django.http import response
from django.test import TestCase


class TestHomePage(TestCase):

    fixtures = ["fixtures/testdata.json"]  # or load whichever file you piped it to

    def test_home_page_hero(self):
        """get a response from a page"""
        # this in effect does a get on the home page '/'
        # the response obj has many keys but we are after the content (body)
        response = self.client.get("/")

        # make a bs4 obj to work with and pass it the content
        soup = BeautifulSoup(response.content, "html.parser")

        # TODO how do we include a text image for this as a fixture, added manually for now

        """select what you are looking for"""
        # example style attr: background-image: url('/media/images/homepage-hero-image.original.width-1000.jpg');
        # we ant to confirm it starts with `background-image`
        hero_section = soup.select_one("section.nhsuk-hero")
        # split the style attr on `:` to a list and use the first item from the list
        background_image = hero_section["style"].split(":")[0]

        hero_header = hero_section.find("h1", "nhsuk-u-margin-bottom-3")
        hero_content = hero_section.find("p", "nhsuk-body-l")

        # do the test
        """https://docs.djangoproject.com/en/3.1/topics/testing/tools/#assertions to see all assertions"""
        self.assertEqual(background_image, "background-image")
        self.assertEqual(hero_header.string, "Hero Heading")
        self.assertEqual(hero_content.string, "Hero text content")

    def test_home_page_header(self):
        response = self.client.get("/")
        soup = BeautifulSoup(response.content, "html.parser")

        header = soup.find("header", "nhsuk-header nhsuk-header--organisation")
        header_link = header.find("a", "nhsuk-header__link")
        self.assertEqual(
            header_link["aria-label"], "NHS England and Improvement homepage"
        )

    def test_home_page_navigtion(self):
        response = self.client.get("/")
        soup = BeautifulSoup(response.content, "html.parser")

        navigation = soup.find("nav", "mega_nav")
        navigation_links = navigation.select_one("ul.menu-bar").find_all("li")
        # Check the first navigation item is a list item with the text 'Publications'
        self.assertEqual(navigation_links[0].name, "li")
        self.assertEqual(navigation_links[0].find("a").string.strip(), "Publications")

    def test_home_page_alert_banner(self):
        response = self.client.get("/")
        soup = BeautifulSoup(response.content, "html.parser")

        alert_banner = soup.select_one("div.nhsuk-global-alert")
        alert_title = alert_banner.find("h2")
        alert_link = alert_banner.find("p").find("a")

        self.assertEqual(alert_title.string, "Alert Banner Title")
        self.assertEqual(alert_link.string, "Alert banner link")

    def test_home_page_promos(self):
        response = self.client.get("/")
        soup = BeautifulSoup(response.content, "html.parser")

        # Check there are two promos
        promos = soup.find_all("div", "nhsuk-promo")
        self.assertEqual(len(promos), 2)

        # promo1 contains a header and text
        promo1 = promos[0]
        promo1_header = promo1.find("h3", "nhsuk-promo__heading")
        self.assertEqual(promo1_header.string, "Promo One Heading")

        # promo2 contains a header, text and an image with scr containing 'homepage-hero-image'
        promo2 = promos[1]
        promo2_header = promo2.find("h3", "nhsuk-promo__heading")
        self.assertEqual(promo2_header.string, "Promo Two Heading")
        promo2_image = promo2.find("img", "nhsuk-promo__img")
        self.assertTrue(
            "homepage-hero-image" in promo2_image["src"],
            f"src was {promo2_image['src']} which doesn't contain homepage-hero-image",
        )

    def test_home_page_callout(self):
        response = self.client.get("/")
        soup = BeautifulSoup(response.content, "html.parser")

        # Check there is a callout block
        callout = soup.select_one("div.nhsuk-warning-callout")
        callout_header = callout.find("h3", "nhsuk-warning-callout__label")
        self.assertEqual(callout_header.string, "Callout title?")
        callout_content = callout.find("p")
        self.assertEqual(callout_content.string, "Callout content")
        callout_link = callout.find("a")
        self.assertEqual(callout_link.string, "Callout Link")

    def test_home_page_footer(self):
        response = self.client.get("/")
        soup = BeautifulSoup(response.content, "html.parser")

        footer = soup.select_one("div.nhsuk-footer")
        footer_links = footer.find("ul", "nhsie-footer-menu")
        self.assertEqual(len(footer_links.find_all("li")), 2)

        link1 = footer_links.find_all("li")[0].find("a", "nhsuk-footer__list-item-link")
        link2 = footer_links.find_all("li")[1].find("a", "nhsuk-footer__list-item-link")

        self.assertEqual(link1.string, "Link Internal")
        self.assertTrue("/" in link1["href"])
        self.assertEqual(link2.string, "Link External")
        self.assertEqual("http://www.example.com" in link2["href"], True)
