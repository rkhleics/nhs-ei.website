import requests
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
    def __init__(self):
        collection_root = Collection.get_first_root_node()
        try:
            collection = Collection.objects.get(name='Temporary Images')
            # so delete the images and collection
            images = Image.objects.filter(collection=collection)
            for image in images:
                image.delete()
            
            collection.delete()

        except Collection.DoesNotExist:
            pass

        # image_tall = ('https://unsplash.com/photos/A-11N8ItHZo/download?force=true')
        # image_tall_content = urllib.request.urlopen(image_tall).read()
        # self.tall_image = Image.open(io.BytesIO(image_tall_content))
        # image_wide = ('https://unsplash.com/photos/twukN12EN7c/download?force=true')
        # image_wide_content = urllib.request.urlopen(image_wide).read()
        # self.wide_image = Image.open(io.BytesIO(image_wide_content))

    def handle(self, *args, **options):
        collection_root = Collection.get_first_root_node()
        collection = collection_root.add_child(name='Temporary Images')
    
        tall = requests.get('https://unsplash.com/photos/A-11N8ItHZo/download?force=true')
        image_file = ImageFile(BytesIO(tall.content), name='tall.jpg')

        tall_image = Image(title='Tall', file=image_file, collection=collection)
        tall_image.save()

        wide = requests.get('https://unsplash.com/photos/twukN12EN7c/download?force=true')
        image_file = ImageFile(BytesIO(wide.content), name='wide.jpg')

        wide_image = Image(title='Wide', file=image_file, collection=collection)
        wide_image.save()

        home_page = HomePage.objects.filter(title='Home')[0]

        our_nhs_people_page = Page.objects.get(slug='ournhspeople') # so this needs to run after the make_top_pages

        home_page.body = """
            <h3><a id="{}" linktype="page">We are the NHS: People Plan for 2020/21</a></h3>
            
            <p>Our NHS is made up of 1.3 million people who care for the people of this country with skill, compassion and dedication.
            This plan sets out what the people of the NHS can expect – from their leaders and from each other – for the rest of 2020
            and into 2021.</p>

            <p>It sets out actions to support transformation across the whole NHS. It focuses on how we must all continue to look after
            each other and foster a culture of inclusion and belonging, as well as action to grow our workforce, train our people,
            and work together differently to deliver patient care.</p>
            """.format(our_nhs_people_page.id)

        home_page.body_image = wide_image

        np = BasePage.objects.child_of(home_page).filter(slug='news')[0]
        home_page.all_news_page = np
        home_page.all_news_title = 'Latest news'
        home_page.all_news_sub_title = ''

        home_page.all_publications_page = BasePage.objects.child_of(home_page).filter(slug='publication')[0]
        home_page.all_publications_title = 'Latest in publications'
        home_page.all_publications_sub_title = ''

        # print(home_page.__dict__)

        rev = home_page.save_revision()
        home_page.save()
        rev.publish()