from django import template
from cms.posts.models import PostIndexPage

register = template.Library()


@register.simple_tag
def get_lastest_posts(num):
    return PostIndexPage.get_latest_posts(num)


@register.simple_tag
def get_lastest_posts_columns(num):
    return [
        PostIndexPage.get_latest_posts(num)[:2],
        PostIndexPage.get_latest_posts(num)[2:],
    ]
