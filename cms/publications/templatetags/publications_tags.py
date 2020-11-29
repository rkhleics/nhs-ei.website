from django import template
from cms.publications.models import PublicationIndexPage

register = template.Library()

@register.simple_tag
def get_lastest_publications_columns(num):
    return [
        PublicationIndexPage.get_latest_publications(num)[:3],
        PublicationIndexPage.get_latest_publications(num)[3:]
    ]