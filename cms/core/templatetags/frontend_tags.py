from django import template
from wagtail.core.models import Page
from cms.core.models import UpperFooterLinks, LowerFooterLinks

register = template.Library()


@register.inclusion_tag('tags/breadcrumb.html', takes_context=True)
def breadcrumb(context):
    """
    Generates an array of pages which are passed to the breadcrumb template.
    """
    page = context.get('page', None)
    if isinstance(page, Page):
        site = page.get_site()
        breadcrumb_pages = []

        # Traverse the page parents with get_parent() until we hit a site root
        while page.id != site.root_page_id and not page.is_root():
            page = page.get_parent()
            breadcrumb_pages = [page] + breadcrumb_pages

        return {
            'breadcrumb_pages': breadcrumb_pages,
        }
    else:
        return {}

    # else:
    #     raise Exception("'page' not found in template context")


@register.inclusion_tag('tags/footer_links.html', takes_context=True)
def footer_links(context, location):
    footer_links = None
    hidden_title = ''
    list_class = ''
    if location == 'upper':
        list_class = 'nhsie-footer-menu'
        hidden_title = 'Secondary menu links'
        footer_links = UpperFooterLinks.objects.all()

    elif location == 'lower':
        list_class = 'nhsuk-footer__list'
        hidden_title = 'Support links'
        footer_links = LowerFooterLinks.objects.all()

    return {
        'footer_links': footer_links,
        'hidden_title': hidden_title,
        'list_class': list_class,
    }