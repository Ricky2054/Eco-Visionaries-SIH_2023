from django.urls import path

from aqi.api.views import get_aqi_using_cords, get_aqi_using_city_name, get_historic_aqi_using_cords, geocoding, reverse_geocoding, get_city_list, get_future_aqi_data

from aqi.views import *

urlpatterns = [
    path("", aqi, name="aqi"),

    #api urls
    path("api/get_aqi/", get_aqi_using_cords, name="aqi_using_cords"),
    path("api/get_future_aqi/", get_future_aqi_data, name="get_future_aqi_data"),
    path("api/get_aqi/<city_name>", get_aqi_using_city_name, name="get_aqi_using_city_name"),
    path("api/get_aqi/historic/", get_historic_aqi_using_cords, name="historic_aqi_using_cords"),

    path("api/geocoding/", geocoding, name="geocoding"),
    path("api/reverse_geocoding/", reverse_geocoding, name="reverse_geocoding"),

    path("api/get_city_list/", get_city_list, name="get_city_list"),
]
