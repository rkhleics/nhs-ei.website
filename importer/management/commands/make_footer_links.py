from cms.pages.models import ComponentsPage
import sys
from django.core.management.base import BaseCommand
from wagtail.core.models import Page
from cms.core.models import CoreSettings, UpperFooterLinks, LowerFooterLinks
from importer.websites import STAGING


class Command(BaseCommand):
    help = "Creates the footer links"

    def handle(self, *args, **options):
        settings = CoreSettings.objects.all().first()

        # first delete them all
        upper = UpperFooterLinks.objects.all().delete()
        lower = LowerFooterLinks.objects.all().delete()

        home_page = Page.objects.filter(title="Home")[0]
        all_pages = Page.objects.all()

        about_us = None
        contact_us = None
        complaints = None
        jobs = None
        transparency_legal = STAGING + "transparency-and-legal/"
        statistics = "https://www.england.nhs.uk/statistics"

        terms_and_conditions = None
        accessibility = None
        commentpolicy = None
        privacypolicy = None

        for page in all_pages:
            if page.get_url() == "/about/":
                about_us = page

            if page.get_url() == "/contact-us/":
                contact_us = page

            # if page.get_url() == '/complaint/':
            #     complaints = page

            if page.get_url() == "/about/working-for/":
                jobs = page

            # if page.get_url() == '/transparency-and-legal/':
            #     transparency_legal = page

            if page.get_url() == "/terms-and-conditions/":
                terms_and_conditions = page

            if page.get_url() == "/accessibility/":
                accessibility = page

            if page.get_url() == "/comment-policy/":
                commentpolicy = page

            if page.get_url() == "/privacy-policy/":
                privacypolicy = page

        upper_footer_links = [
            {
                "text": "About us",
                "page": about_us,
                "external_url": "",
                "setting": settings,
            },
            {
                "text": "Contact us",
                "page": contact_us,
                "external_url": "",
                "setting": settings,
            },
            # {
            #     'text': 'Complaints', 'page': complaints, 'external_url': '', 'setting': settings
            # },
            {"text": "Jobs", "page": jobs, "external_url": "", "setting": settings},
            {
                "text": "Transparency and legal",
                "page": None,
                "external_url": transparency_legal,
                "setting": settings,
            },
            {
                "text": "Statistics",
                "page": None,
                "external_url": statistics,
                "setting": settings,
            },
        ]

        for link in upper_footer_links:
            link = UpperFooterLinks(
                text=link["text"],
                page=link["page"],
                external_url=link["external_url"],
                setting=link["setting"],
            )
            link.save()

        lower_footer_links = [
            {
                "text": "Terms and conditions",
                "page": terms_and_conditions,
                "external_url": "",
                "setting": settings,
            },
            {
                "text": "Accessibility statement",
                "page": accessibility,
                "external_url": "",
                "setting": settings,
            },
            {
                "text": "Social media and content moderation",
                "page": commentpolicy,
                "external_url": "",
                "setting": settings,
            },
            {
                "text": "Privacy and cookies",
                "page": privacypolicy,
                "external_url": "",
                "setting": settings,
            },
            {
                "text": "Open Government Licence v3.0",
                "page": home_page,
                "external_url": "",
                "setting": settings,
            },
        ]

        for link in lower_footer_links:
            link = LowerFooterLinks(
                text=link["text"],
                page=link["page"],
                external_url=link["external_url"],
                setting=link["setting"],
            )
            link.save()

        sys.stdout.write("Footer Links Created\n")


""" footer menu upper """

# about us

# contact us

# statistics

# patentent involvement

# system guideance and process

# jobs

# transparency and legal

# complaints

""" footer menu lower """

# Terms and conditions

# Accessibility statement

# Social media and content moderation

# Privacy and cookies
