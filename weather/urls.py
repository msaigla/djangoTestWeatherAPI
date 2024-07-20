from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path("", views.index, name="main"),
    path("get_cities/", views.get_cities, name="get_cities"),
    path("get_weather/", views.get_weather, name="get_weather"),
    path("get_history_user_weather/", views.get_history_user_weather, name="get_history_user_weather"),
    path("count_search_city/", views.count_search_city, name="count_search_city")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
