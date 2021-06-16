from django.urls import path

from . import views

urlpatterns = [path("", views.importer_view)]
