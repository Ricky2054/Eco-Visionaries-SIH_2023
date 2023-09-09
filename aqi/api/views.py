from django.http import JsonResponse

from datetime import timedelta

from accounts.utils import current_time, datetime_to_unix_time, unix_time_to_kolkata_datetime
from .utils import get_current_aqi_data, get_historic_aqi_data, get_loc_details, get_reverse_loc_details

#view to get aqi based on latitude and longitude
def get_aqi_using_cords(request):
    data = None
    error = ""
    response = {}
    status = 400
    try:
        #check if request method is GET 
        if request.method == "GET":
            lat = request.GET.get("latitude").strip() 
            long = request.GET.get("longitude").strip()  
            
            if lat != "" and long != "":
                current_data = get_current_aqi_data(lat, long)
                data = current_data if current_data != {} else None
                status = 200
                error = None
        
            else:
                error = "latitude and longitude fields are required"
                status = 400


        else:
            error = "Only GET method is allowed"
            status = 405
    
    except Exception as e:
        status = 500
        error = "Internal server error"
        print(e)
        pass

    response["data"] = data
    response["error"] = error
    response["status"] = status

    return JsonResponse(response)



#view to get historic aqi data
def get_historic_aqi_using_cords(request):

    data = None
    error = ""
    response = {}
    status = 400
    try:
        #check if request method is GET 
        if request.method == "GET":
            lat = request.GET.get("latitude").strip() 
            long = request.GET.get("longitude").strip() 
            duration = request.GET.get("duration").strip() 
            
            if lat != "" and long != "" and duration != "" and duration.isdigit():
                start_date = current_time - timedelta(days=int(duration))
                end_date = current_time - timedelta(days=1)

                # convert start and end date to unix format
                start_date_unix = datetime_to_unix_time(start_date) 
                end_date_unix = datetime_to_unix_time(end_date)

                current_data = get_historic_aqi_data(lat, long, start_date_unix, end_date_unix)
                data = current_data if len(current_data) != 0 else None
                status = 200
                error = None

            else:
                error = "latitude, longitude and duration fields are required"
                status = 400

        else:
            error = "Only GET method is allowed"
            status = 405
    
    except Exception as e:
        status = 500
        error = "Internal server error"
        print(e)
        pass

    response["data"] = data
    response["error"] = error
    response["status"] = status

    return JsonResponse(response)



#view to get latitude and longitude from 
def geocoding(request):
    data = None
    error = ""
    response = {}
    status = 400
    try:
        #check if request method is GET 
        if request.method == "GET":
            city_name = request.GET.get("city_name").strip().lower() 
            
            if city_name != "":
                data = get_reverse_loc_details(city_name)
                status = 200
                error = None
        
            else:
                error = "city_name field is required"
                status = 400


        else:
            error = "Only GET method is allowed"
            status = 405
    
    except Exception as e:
        status = 500
        error = "Internal server error"
        print(e)
        pass

    response["data"] = data
    response["error"] = error
    response["status"] = status
    
    return JsonResponse(response)




#view to get location details from latitude and longitude
def reverse_geocoding(request):
    data = None
    error = ""
    response = {}
    status = 400
    try:
        #check if request method is GET 
        if request.method == "GET":
            lat = request.GET.get("latitude").strip() 
            long = request.GET.get("longitude").strip()  
            
            if lat != "" and long != "":
                data = get_loc_details(lat, long)
                status = 200
                error = None
        
            else:
                error = "latitude and longitude fields are required"
                status = 400


        else:
            error = "Only GET method is allowed"
            status = 405
    
    except Exception as e:
        status = 500
        error = "Internal server error"
        print(e)
        pass

    response["data"] = data
    response["error"] = error
    response["status"] = status
    
    return JsonResponse(response)


