from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("get_cities/", views.get_cities, name="get_cities"),
    path("get_weather/", views.get_weather, name="get_weather")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
