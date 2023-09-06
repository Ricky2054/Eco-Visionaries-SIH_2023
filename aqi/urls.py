from django.urls import path
from .views import *

urlpatterns = [
    path("", aqi, name="aqi"),
]
