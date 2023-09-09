from django.urls import path

from aqi.api.views import get_aqi_using_cords, get_historic_aqi_using_cords, geocoding, reverse_geocoding

from aqi.views import *

urlpatterns = [
    path("", aqi, name="aqi"),

    #api urls
    path("api/get_aqi/", get_aqi_using_cords, name="aqi_using_cords"),
    path("api/get_aqi/historic/", get_historic_aqi_using_cords, name="historic_aqi_using_cords"),

    path("api/geocoding/", geocoding, name="geocoding"),
    path("api/reverse_geocoding/", reverse_geocoding, name="reverse_geocoding"),
]
