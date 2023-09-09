from django.shortcuts import render, redirect

import requests
import os

# Create your views here.

AIR_VISUAL_API_KEY = os.environ.get("AIR_VISUAL_API_KEY")
OPEN_WEATHER_API_KEY = os.environ.get("OPEN_WEATHER_API_KEY")

#aqi page
def aqi(request):


    return render(request, "aqi/aqi.html")

