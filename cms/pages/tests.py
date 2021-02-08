from bs4 import BeautifulSoup
from django.test import TestCase


class TestComponentsPage(TestCase):

    # or load whichever file you piped it to
    fixtures = ['fixtures/testdata.json']

    def test_first_heading(self):
        response = self.client.get('/component-page/')
        soup = BeautifulSoup(response.content, 'html.parser')

        heading = soup.select_one('main h1')

        self.assertEqual(heading.text, 'Component Page')

    def test_recent_panel(self):
        response = self.client.get('/component-page/')
        soup = BeautifulSoup(response.content, 'html.parser')

        panel = soup.select_one('main .nhsuk-panel-with-label')

        heading = panel.select_one('h3')
        self.assertEqual(heading.text, 'Recent Posts')

        # first list is the left side on desktop
        first_list = panel.find_all('ol')[0]
        first_list_item_1_link = first_list.select_one(
            'li:nth-child(1) article h2 a')

        self.assertEqual(
            first_list_item_1_link['href'], '/post-index-page/post-two/')
        self.assertEqual(first_list_item_1_link.text.strip(), 'Post Two')

        first_list_item_1_label = first_list.select_one(
            'li:nth-child(1) article span:nth-of-type(1)')
        self.assertEqual(first_list_item_1_label.text.strip(), 'News')

        first_list_item_1_date = first_list.select_one(
            'li:nth-child(1) article span:nth-of-type(2) time')
        self.assertGreater(len(first_list_item_1_date.text.split()), 0)

        first_list_item_2_link = first_list.select_one(
            'li:nth-child(2) article h2 a')

        self.assertEqual(
            first_list_item_2_link['href'], '/post-index-page/post-one/')
        self.assertEqual(first_list_item_2_link.text.strip(), 'Post One')

        first_list_item_2_label = first_list.select_one(
            'li:nth-child(2) article span:nth-of-type(1)')
        self.assertEqual(first_list_item_2_label.text.strip(), 'News')

        first_list_item_2_date = first_list.select_one(
            'li:nth-child(2) article span:nth-of-type(2) time')
        self.assertGreater(len(first_list_item_2_date.text.split()), 0)

        # second list is the right side on desktop
        second_list = panel.find_all('ol')[1]
        second_list_item_1_link = second_list.select_one(
            'li:nth-child(1) article h2 a')

        self.assertEqual(
            second_list_item_1_link['href'], '/blog-index-page/blog-post-two/')
        self.assertEqual(second_list_item_1_link.text.strip(), 'Blog Post Two')

        second_list_item_1_label = second_list.select_one(
            'li:nth-child(1) article span:nth-of-type(1)')
        self.assertEqual(second_list_item_1_label.text.strip(), 'Blog')

        second_list_item_1_date = second_list.select_one(
            'li:nth-child(1) article span:nth-of-type(2) time')
        self.assertGreater(len(second_list_item_1_date.text.split()), 0)

        second_list_item_2_link = second_list.select_one(
            'li:nth-child(2) article h2 a')

        self.assertEqual(
            second_list_item_2_link['href'], '/blog-index-page/blog-post-one/')
        self.assertEqual(second_list_item_2_link.text.strip(), 'Blog Post One')

        second_list_item_2_label = second_list.select_one(
            'li:nth-child(2) article span:nth-of-type(1)')
        self.assertEqual(second_list_item_2_label.text.strip(), 'Blog')

        second_list_item_2_date = second_list.select_one(
            'li:nth-child(2) article span:nth-of-type(2) time')
        self.assertGreater(len(second_list_item_2_date.text.split()), 0)
