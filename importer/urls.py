from django.urls import path
from .views import top_pages_with_children, top_pages_without_children, url_errors, dashboard


urlpatterns = [
    path('', dashboard, name='dashboard'),
    # export csv urls
    path('top-pages-with-children/', top_pages_with_children, name='top-pages-with-children'),
    path('top-pages-without-children/', top_pages_without_children, name='top-pages-without-children'),
    path('url-errors/', url_errors, name='url-errors'),
]
