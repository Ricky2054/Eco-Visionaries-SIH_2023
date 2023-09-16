from django.shortcuts import render, redirect

from accounts.utils import current_time
import os

# Create your views here.

OPEN_WEATHER_API_KEY = os.environ.get("OPEN_WEATHER_API_KEY")

#aqi page
def aqi(request):
    context = {
        "current_time": current_time
    }

    return render(request, "aqi/aqi.html", context)

