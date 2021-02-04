from bs4 import BeautifulSoup
from django.http import response
from django.test import TestCase


class TestHomePage(TestCase):

    fixtures = ['testdata.json']  # or load whichever file you piped it to

    def test_home_page_hero(self):
        '''get a response from a page'''
        # this in effect does a get on the home page '/'
        # the response obj has many keys but we are after the content (body)
        response = self.client.get('/')

        # make a bs4 obj to work with and pass it the content
        soup = BeautifulSoup(response.content, 'html.parser')

        # TODO how do we include a text image for this as a fixture, added manually for now

        '''select what you are looking for'''
        # example style attr: background-image: url('/media/images/homepage-hero-image.original.width-1000.jpg');
        # we ant to confirm it starts with `background-image`
        hero_section = soup.select_one('section.nhsuk-hero')
        # split the style attr on `:` to a list and use the first item from the list
        background_image = hero_section['style'].split(':')[0]

        # do the test
        '''https://docs.djangoproject.com/en/3.1/topics/testing/tools/#assertions to see all assertions'''
        self.assertEqual(background_image, 'background-image')
