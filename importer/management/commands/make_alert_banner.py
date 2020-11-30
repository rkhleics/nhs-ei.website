
import sys

from django.core.management.base import BaseCommand

from cms.core.models import CoreSettings


class Command(BaseCommand):
    help = 'Creates the alert banner'
    
    def handle(self, *args, **options):
        settings = CoreSettings.objects.all().first()
        # delete first
        settings.alert_banner = ''
        settings.is_visible = False
        settings.save()

        settings.alert_banner = """
            <h2>Coronavirus (COVID-19)</h2>
            <p><a href="https://www.nhs.uk/conditions/coronavirus-covid-19/">Get the latest advice about coronavirus</a></p>
        """
        settings.is_visible = True
        settings.save()

        sys.stdout.write('Alert Banner Created\n')