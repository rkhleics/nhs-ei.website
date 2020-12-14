import requests
import json
import sys
from cms.home.models import HomePage
from django.core.management.base import BaseCommand
from cms.pages.models import BasePage
from wagtail.core.models import Collection, Page
from django.core.files.images import ImageFile
from wagtail.images.models import Image
from io import BytesIO


class Command(BaseCommand):
    help = 'Creates the home page content'
    # def __init__(self):
    #     collection_root = Collection.get_first_root_node()
    #     try:
    #         collection = Collection.objects.get(name='Temporary Images')
    #         # so delete the images and collection
    #         images = Image.objects.filter(collection=collection)
    #         for image in images:
    #             image.delete()
            
    #         collection.delete()

    #     except Collection.DoesNotExist:
    #         pass

        # image_tall = ('https://unsplash.com/photos/A-11N8ItHZo/download?force=true')
        # image_tall_content = urllib.request.urlopen(image_tall).read()
        # self.tall_image = Image.open(io.BytesIO(image_tall_content))
        # image_wide = ('https://unsplash.com/photos/twukN12EN7c/download?force=true')
        # image_wide_content = urllib.request.urlopen(image_wide).read()
        # self.wide_image = Image.open(io.BytesIO(image_wide_content))

    def handle(self, *args, **options):
        collection_root = Collection.get_first_root_node()
        try:
            collection = Collection.objects.get(name='Temporary Images')
        except Collection.DoesNotExist:
            collection = collection_root.add_child(name='Temporary Images')

        try:
            image = Image.objects.get(title='Hero Image')
        except Image.DoesNotExist:
            hero_image_remote = requests.get('https://assets.nhs.uk/nhsuk-cms/images/IS_0818_homepage_hero_3_913783962.width-1000.jpg')
            image_file = ImageFile(BytesIO(hero_image_remote.content), name='hero.jpg')
            image = Image(title='Hero Image', file=image_file, collection=collection)
            image.save()
    
        # tall = requests.get('https://unsplash.com/photos/A-11N8ItHZo/download?force=true')
        # image_file = ImageFile(BytesIO(tall.content), name='tall.jpg')

        # tall_image = Image(title='Tall', file=image_file, collection=collection)
        # tall_image.save()

        # wide = requests.get('https://unsplash.com/photos/twukN12EN7c/download?force=true')
        # image_file = ImageFile(BytesIO(wide.content), name='wide.jpg')

        # wide_image = Image(title='Wide', file=image_file, collection=collection)
        # wide_image.save()

        home_page = HomePage.objects.filter(title='Home')[0]

        # our_nhs_people_page = Page.objects.get(slug='ournhspeople') # so this needs to run after the make_top_pages

        """
        {'type': 'promo_group',
         'value': {
             'column': 'one-third',
             'size': 'small',
             'heading_level': 3,
             'promos': [
                 {
                     'url': 'http://wwww.test.com',
                     'heading': 'Heading',
                     'description': 'Descrtipion',
                     'content_image': 1,  # image id
                     'alt_text': ''
                 },
                 {
                     'repeats': 'repeats',
                 }
             ]

         }}
         """

        home_page_stream_field = [
            {
                'type': 'promo_group',
                'value': {
                    'column': 'one-half',
                    'size': '',
                    'heading_level': '3',
                    'promos': [
                        {
                            'url': 'https://staging.nhsei.rkh.co.uk/publication/nhs-england-improvement/',
                            'heading': 'Latest publications',
                            'description': 'Short description to inform users goes here',
                            'content_image': None,
                            'alt_text': ''
                        },
                        {
                            'url': 'https://staging.nhsei.rkh.co.uk/news/nhs-england-improvement/',
                            'heading': 'Latest news',
                            'description': 'Short description to inform users goes here',
                            'content_image': None,
                            'alt_text': ''
                        },
                        {
                            'url': 'https://staging.nhsei.rkh.co.uk/ourwork/',
                            'heading': 'Key topical issue',
                            'description': 'Short description to inform users goes here',
                            'content_image': None,
                            'alt_text': ''
                        },
                        {
                            'url': 'https://staging.nhsei.rkh.co.uk/publication/coronavirus/',
                            'heading': 'Special topical issue',
                            'description': 'Short description to inform users goes here',
                            'content_image': None,
                            'alt_text': ''
                        },
                    ]
                }
            },
            {
                'type': 'warning_callout',
                'value': {
                    'title': 'Are you looking for health advice?',
                    'heading_level': '3',
                    'body': '<p><a href="https://www.nhs.uk/">Find advice on health conditions, symptoms, healthy living, medicines and how to get help.</a></p>',
                }
            },
        ]

        home_page.body = json.dumps(home_page_stream_field)

        home_page.hero_heading = 'Supporting the NHS'
        home_page.hero_text = 'to improve peoples care'
        home_page.hero_image = image

        rev = home_page.save_revision()
        home_page.save()
        rev.publish()