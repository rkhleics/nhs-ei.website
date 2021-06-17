import sys

from django.core.management.base import BaseCommand

from cms.core.models import CoreSettings


class Command(BaseCommand):
    help = "Creates the alert banner"

    def handle(self, *args, **options):
        settings = CoreSettings.objects.all().first()
        # delete first
        settings.alert_banner = ""
        settings.is_visible = False
        settings.save()

        settings.alert_banner = """
            <h2>Coronavirus (COVID-19)</h2>
            <p><a href="/coronavirus">
            Our advice for clinicians on the coronavirus is here.</a><br />
            If you are a member of the public looking for health advice, go to the 
            <a href="https://www.nhs.uk/conditions/coronavirus-covid-19/">NHS website</a>. 
            And if you are looking for the latest travel information, and advice about the government response to the outbreak, go to the 
            <a href="https://www.gov.uk/coronavirus">gov.uk website</a>.</p>
        """
        settings.is_visible = True
        settings.save()

        sys.stdout.write("Alert Banner Created\n")
