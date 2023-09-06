from django.shortcuts import render, redirect

# Create your views here.

#aqi page
def aqi(request):

    return render(request, "aqi/aqi.html")
