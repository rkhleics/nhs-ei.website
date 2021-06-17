from cms.pages.models import BasePage, ComponentsPage, LandingPage
from django.shortcuts import render
from wagtail.core.models import Page


def importer_view(request):
    home_page = Page.objects.filter(title="Home")[0]
    context = {}
    context["component_pages"] = ComponentsPage.objects.child_of(home_page)
    context["base_pages"] = BasePage.objects.child_of(home_page)
    context["landing_pages"] = LandingPage.objects.child_of(home_page)

    return render(request, "importer/importer_base.html", context)
