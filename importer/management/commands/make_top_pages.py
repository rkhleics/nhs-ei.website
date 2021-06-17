import requests
import sys
from cms.home.models import HomePage
from django.core.management.base import BaseCommand
from cms.pages.models import BasePage, ComponentsPage, LandingPage
from wagtail.core.models import Collection, Page
from django.core.files.images import ImageFile
from wagtail.images.models import Image
from io import BytesIO
import json


class Command(BaseCommand):
    help = "Creates the home page content"

    def handle(self, *args, **options):

        home_page = HomePage.objects.filter(title="Home")[0]

        ############## main menu #############

        """ PUBLICATIONS """

        # already exists url is 'publication' so update the page
        # TEMP: This is the publciations top level page. On the right are the sub sites
        publications = BasePage.objects.get(slug="publication")
        first_published_at = publications.first_published_at
        last_published_at = publications.last_published_at
        latest_revision_created_at = publications.latest_revision_created_at

        # making a new block as body is empty
        block = [
            {
                "type": "panel",
                "value": {
                    "label": "",
                    # this is the default, might want to change it...
                    "heding_level": "3",
                    # after it's been parsed for links
                    "body": "<p>This is the publciations top level page. On the right are the sub sites</p>",
                },
            }
        ]

        publications.body = json.dumps(block)

        rev = publications.save_revision()  # this needs to run here

        publications.first_published_at = first_published_at
        publications.last_published_at = last_published_at
        publications.latest_revision_created_at = latest_revision_created_at

        publications.save()
        rev.publish()

        """ OUR WORK """

        # existing url is 'ourwork' so update the page
        # INTRO: Learn more about our latest initiatives and what we’re doing for cancer, primary care, mental health, diabetes and other key areas of the NHS.
        our_work = ComponentsPage.objects.get(slug="ourwork")
        first_published_at = our_work.first_published_at
        last_published_at = our_work.last_published_at
        latest_revision_created_at = our_work.latest_revision_created_at

        # updating the exiting blocks
        blocks = our_work.body.__dict__
        blocks["stream_data"][0]["value"][
            "body"
        ] = "<p>Learn more about our latest initiatives and what we’re doing for cancer, primary care, mental health, diabetes and other key areas of the NHS.</p>"

        our_work.body = json.dumps(blocks["stream_data"])

        rev = our_work.save_revision()
        our_work.first_published_at = first_published_at
        our_work.last_published_at = last_published_at
        our_work.latest_revision_created_at = latest_revision_created_at
        our_work.save()
        rev.publish()

        """ OUR PEOPLE """
        # new page at url 'ourpeople' there's page to move below this
        # INTRO: Supporting our people is a priority. We want to make sure you’re well looked after, so that you can care for others. Learn about access to health and wellbeing support, the NHS pension plan, and find the latest guidance for recruitment.

        our_people = LandingPage(
            title="Our People",
            wp_id=-10,
            source="none",
            wp_slug="none",
        )

        # making a new block as body is empty
        block = [
            {
                "type": "panel",
                "value": {
                    "label": "",
                    # this is the default, might want to change it...
                    "heding_level": "3",
                    # after it's been parsed for links
                    "body": "<p>Supporting our people is a priority. We want to make sure you’re well looked after, so that you can care for others. Learn about access to health and wellbeing support, the NHS pension plan, and find the latest guidance for recruitment.</p>",
                },
            }
        ]

        our_people.body = json.dumps(block)

        home_page.add_child(instance=our_people)

        rev = our_people.save_revision()
        our_people.save()
        rev.publish()

        """ IMPOROVEMENT """
        # new page at url 'improvement' there's pages to move below this
        # INTRO: We want to promote a culture of ongoing learning and improvement within the NHS. We aim to do this by encouraging shared learning, and through initiatives such as RightCare, the Insights Platform and Model Hospital.
        improvement = LandingPage(
            title="Improvement",
            wp_id=-10,
            source="none",
            wp_slug="none",
        )

        # making a new block as body is empty
        block = [
            {
                "type": "panel",
                "value": {
                    "label": "",
                    # this is the default, might want to change it...
                    "heding_level": "3",
                    # after it's been parsed for links
                    "body": "<p>We want to promote a culture of ongoing learning and improvement within the NHS. We aim to do this by encouraging shared learning, and through initiatives such as RightCare, the Insights Platform and Model Hospital.</p>",
                },
            }
        ]

        improvement.body = json.dumps(block)

        home_page.add_child(instance=improvement)

        rev = improvement.save_revision()
        improvement.save()
        rev.publish()

        """ Transparency and legal """

        """ Mental health """
