from django import template
from cms.blogs.models import BlogIndexPage

register = template.Library()


@register.simple_tag
def get_lastest_blogs(num):
    return BlogIndexPage.get_latest_blogs(num)
