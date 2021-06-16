from bs4 import BeautifulSoup
from django.test import TestCase


class TestComponentsPage(TestCase):

    # or load whichever file you piped it to
    fixtures = ["fixtures/testdata.json"]

    def test_first_heading(self):
        response = self.client.get("/component-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        heading = soup.select_one("main h1")

        self.assertEqual(heading.text, "Component Page")

    def test_recent_panel(self):
        response = self.client.get("/component-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        panel = soup.select_one("main .nhsuk-panel-with-label")

        heading = panel.select_one("h3")
        self.assertEqual(heading.text, "Recent Posts")

        # first list is the left side on desktop
        first_list = panel.find_all("ol")[0]
        first_list_item_1_link = first_list.select_one("li:nth-child(1) article h2 a")

        self.assertEqual(first_list_item_1_link["href"], "/post-index-page/post-two/")
        self.assertEqual(first_list_item_1_link.text.strip(), "Post Two")

        first_list_item_1_label = first_list.select_one(
            "li:nth-child(1) article span:nth-of-type(1)"
        )
        self.assertEqual(first_list_item_1_label.text.strip(), "News")

        first_list_item_1_date = first_list.select_one(
            "li:nth-child(1) article span:nth-of-type(2) time"
        )
        self.assertGreater(len(first_list_item_1_date.text.split()), 0)

        first_list_item_2_link = first_list.select_one("li:nth-child(2) article h2 a")

        self.assertEqual(first_list_item_2_link["href"], "/post-index-page/post-one/")
        self.assertEqual(first_list_item_2_link.text.strip(), "Post One")

        first_list_item_2_label = first_list.select_one(
            "li:nth-child(2) article span:nth-of-type(1)"
        )
        self.assertEqual(first_list_item_2_label.text.strip(), "News")

        first_list_item_2_date = first_list.select_one(
            "li:nth-child(2) article span:nth-of-type(2) time"
        )
        self.assertGreater(len(first_list_item_2_date.text.split()), 0)

        # second list is the right side on desktop
        second_list = panel.find_all("ol")[1]
        second_list_item_1_link = second_list.select_one("li:nth-child(1) article h2 a")

        self.assertEqual(
            second_list_item_1_link["href"], "/blog-index-page/blog-post-two/"
        )
        self.assertEqual(second_list_item_1_link.text.strip(), "Blog Post Two")

        second_list_item_1_label = second_list.select_one(
            "li:nth-child(1) article span:nth-of-type(1)"
        )
        self.assertEqual(second_list_item_1_label.text.strip(), "Blog")

        second_list_item_1_date = second_list.select_one(
            "li:nth-child(1) article span:nth-of-type(2) time"
        )
        self.assertGreater(len(second_list_item_1_date.text.split()), 0)

        second_list_item_2_link = second_list.select_one("li:nth-child(2) article h2 a")

        self.assertEqual(
            second_list_item_2_link["href"], "/blog-index-page/blog-post-one/"
        )
        self.assertEqual(second_list_item_2_link.text.strip(), "Blog Post One")

        second_list_item_2_label = second_list.select_one(
            "li:nth-child(2) article span:nth-of-type(1)"
        )
        self.assertEqual(second_list_item_2_label.text.strip(), "Blog")

        second_list_item_2_date = second_list.select_one(
            "li:nth-child(2) article span:nth-of-type(2) time"
        )
        self.assertGreater(len(second_list_item_2_date.text.split()), 0)

    def test_all_common_blocks(self):
        response = self.client.get("/base-page/")
        soup = BeautifulSoup(response.content, "html.parser")

        # Action links
        action_links = soup.find_all("div", "nhsuk-action-link")
        self.assertEqual(len(action_links), 3)
        self.assertEqual(
            action_links[0].find("span", "nhsuk-action-link__text").string,
            "Example Link",
        )
        self.assertEqual(
            action_links[1].find("span", "nhsuk-action-link__text").string,
            "Example Link New Window",
        )
        self.assertEqual(
            action_links[1].find("a", "nhsuk-action-link__link")["target"], "_blank"
        )
        self.assertEqual(
            action_links[2].find("span", "nhsuk-action-link__text").string,
            "Example expander group block action link, opens a new window",
        )
        self.assertEqual(
            action_links[2].find("a", "nhsuk-action-link__link")["target"], "_blank"
        )

        # Do don't list
        do_dont_lists = soup.find_all("div", "nhsuk-do-dont-list")
        self.assertEqual(len(do_dont_lists), 2)

        do_list = do_dont_lists[0]
        dont_list = do_dont_lists[1]

        self.assertEqual(len(do_list.find("ul", "nhsuk-list").find_all("li")), 2)
        self.assertEqual(len(dont_list.find("ul", "nhsuk-list").find_all("li")), 2)

        self.assertTrue("nhsuk-list--tick" in do_list.find("ul", "nhsuk-list")["class"])
        self.assertTrue(
            "nhsuk-list--cross" in dont_list.find("ul", "nhsuk-list")["class"]
        )

        # Inset text
        inset_text_block = soup.find("div", "nhsuk-inset-text")
        self.assertEqual(inset_text_block.find("p").string, "Inset text block")

        # Image block
        image_block = soup.find("figure", "nhsuk-image")
        self.assertTrue(image_block.find("img", "nhsuk-image__img"))
        self.assertTrue(image_block.find("figcaption", "nhsuk-image__caption"))
        self.assertEqual(
            image_block.find("figcaption", "nhsuk-image__caption").string.strip(),
            "Image block",
        )

        # Panel blocks
        panel_with_label = soup.find("div", "nhsuk-panel-with-label")
        self.assertTrue(panel_with_label.find("h3", "nhsuk-panel-with-label__label"))
        self.assertEqual(
            panel_with_label.find("h3", "nhsuk-panel-with-label__label").string,
            "Panel block",
        )

        panel_group = soup.find("div", "nhsuk-panel-group")
        self.assertEqual(len(panel_group.find_all("div", "nhsuk-panel-group__item")), 2)

        panel_grey = soup.find("div", "nhsuk-panel--grey")
        self.assertEqual(panel_grey.find("h3").string, "Grey panel block")
        self.assertEqual(panel_grey.find("p").string, "Grey panel block content")

        # Warning
        warning_callout = soup.find("div", "nhsuk-warning-callout")
        self.assertEqual(
            warning_callout.find("h3", "nhsuk-warning-callout__label").string,
            "Warning callout block",
        )
        self.assertEqual(
            warning_callout.find("p").string, "Warning callout block content"
        )
