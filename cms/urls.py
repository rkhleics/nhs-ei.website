from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from cms.search import views as search_views

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.search, name='search'),

]

# views to test static pages
from django.views.generic import TemplateView
urlpatterns += [
    path('nav-static', TemplateView.as_view(
        template_name='prototype_pages/nav_prototype.html'), 
        name='nav-static'),
    path('search-results-static', TemplateView.as_view(
        template_name='prototype_pages/search_results_prototype.html'),
        name='search-static'),
    path('content-page-static', TemplateView.as_view(
        template_name='prototype_pages/content_page_prototype.html'),
        name='content-static'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    # views for testing 404 and 500 templates
    urlpatterns += [
        path('test-404/', TemplateView.as_view(template_name='404.html')),
        path('test-500/', TemplateView.as_view(template_name='500.html')),
    ]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
