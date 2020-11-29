import ast
from io import BytesIO
import json
from os import link
import re
import sys
from sys import path
from bs4 import BeautifulSoup
from django.core.files.base import File
import requests
from html import unescape


from django.core.management import call_command
from django.core.management.base import BaseCommand
from wagtail.core.models import Collection
from wagtail.documents.models import Document
from wagtail.images.models import Image
from nhsei_wagtail.pages.models import BasePage

class Command(BaseCommand):
    help = 'parsing stream fields'

    def handle(self, *args, **options):
        page = BasePage.objects.get(url_path='/home/approved-costing-guidance/')
        c = self.convert_inline_links(page.raw_content)

    def convert_inline_links(self, content):
        # BS4 to get a handle on all the anchor links

        soup = BeautifulSoup(content, features="html5lib")

        links = soup.find_all('a', href=re.compile(
            r"^https://www.england.nhs.uk/"))

        change_links = []

        for link in links:

            old_url = link['href']
            separator = '/'
            old_path = '/home/' + separator.join(old_url.split('/')[3:])

            try:
                page = BasePage.objects.get(url_path=old_path)
                page_id = page.id
                
                old_link = str(link)
                new_link = '<a id="{}" linktype="page">{}</a>'.format(page_id, link.text)
                change_links.append([old_link,  new_link])
                # content_base = content.replace('financial year', '')
            except BasePage.DoesNotExist:
                # print('not found ' + old_path)
                pass
        
        # print(content_base.replace('<a href="#why-is-costing-important">Why is costing important?</a>','REPLCED'))
        # print(content_base)

        # for link in change_links:
        #     content_base.replace()
        
        for link in change_links:
            print(link[0])
            print(link[1])
            content = content.replace(link[0], link[1])

        print(content)
            

        return change_links