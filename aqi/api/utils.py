import os
import requests

from accounts.utils import unix_time_to_kolkata_datetime, extract_date, format_date, cache_set, cache_get


AIR_VISUAL_API_KEY = os.environ.get("AIR_VISUAL_API_KEY")
OPEN_WEATHER_API_KEY = os.environ.get("OPEN_WEATHER_API_KEY")

#aqi index classification
AQI_INDEX = {
    "1": {
        "rating": "good",
        "col": "#22C55E"
    },
    "2": {
        "rating": "fair",
        "col": "#059669"
    },
    "3": {
        "rating": "moderate",
        "col": "#FACC15"
    },
    "4": {
        "rating": "poor",
        "col": "#F43F5E"
    },
    "5": {
        "rating": "hazardous",
        "col": "#7E24CE"
    },
}


#city names
CITY_NAMES = ['alipurduar', 'asansol', 'baharampur', 'bally', 'balurghat', 'bangaon', 'bankura', 'bardhaman', 'basirhat', 'bolpur', 'chakdaha', 'cooch behar', 'dankuni', 'darjeeling', 'dhulian', 'durgapur', 'habra', 'haldia', 'jalpaiguri', 'jangipur', 'kharagpur', 'kolkata', 'krishnanagar', 'malda', 'medinipur', 'nabadwip', 'purulia', 'ranaghat', 'shantipur', 'siliguri', 'asansol', 'barrackpore', 'baruipur', 'calcutta', 'dankuni', 'durgapur', 'haldia', 'howrah', 'kalyani', 'kolkata', 'maldah', 'raniganj', 'sankrail', 'siliguri', 'uluberia']


#func to calculate AQI as per Indian Standards
def aqi_indian(so2, no2, pm10):
    aqi = None

    try:
        #calculating for pm10
        if pm10 <= 50:
            BP_Hi = 50
            BP_Lo = 0
            I_Hi = 50
            I_Lo = 0
        if pm10 >= 51 and pm10 <= 100:
            BP_Hi = 100
            BP_Lo = 51
            I_Hi = 100
            I_Lo = 51
        if pm10 >= 101 and pm10 <= 250:
            BP_Hi = 250
            BP_Lo = 101
            I_Hi = 200
            I_Lo = 101
        if pm10 >= 251 and pm10 <= 350:
            BP_Hi = 350
            BP_Lo = 251
            I_Hi = 300
            I_Lo = 201
        if pm10 >= 351 and pm10 <= 430:
            BP_Hi = 430
            BP_Lo = 351
            I_Hi = 400
            I_Lo = 301
        if pm10 > 430:
            BP_Hi = 430
            BP_Lo = 351
            I_Hi = 500
            I_Lo = 401

        pm10_sub_index = (((I_Hi-I_Lo)/(BP_Hi-BP_Lo))*(pm10-BP_Lo))+I_Lo

        #calculating for so2
        if so2 <= 40:
            BP_Hi = 40
            BP_Lo = 0
            I_Hi = 50
            I_Lo = 0
        if so2 >= 41 and so2 <= 80:
            BP_Hi = 80
            BP_Lo = 41
            I_Hi = 100
            I_Lo = 51
        if so2 >= 81 and so2 <= 380:
            BP_Hi = 380
            BP_Lo = 81
            I_Hi = 200
            I_Lo = 101
        if so2 >= 381 and so2 <= 800:
            BP_Hi = 800
            BP_Lo = 381
            I_Hi = 300
            I_Lo = 201
        if so2 >= 801 and so2 <= 1600:
            BP_Hi = 1600
            BP_Lo = 801
            I_Hi = 400
            I_Lo = 301
        if so2 > 1600:
            BP_Hi = 430
            BP_Lo = 351
            I_Hi = 500
            I_Lo = 401

        so2_sub_index = (((I_Hi-I_Lo)/(BP_Hi-BP_Lo))*(pm10-BP_Lo))+I_Lo

        #calculating for no2
        if no2 <= 40:
            BP_Hi = 40
            BP_Lo = 0
            I_Hi = 50
            I_Lo = 0
        if no2 >= 41 and no2 <= 80:
            BP_Hi = 80
            BP_Lo = 41
            I_Hi = 100
            I_Lo = 51
        if no2 >= 81 and no2 <= 180:
            BP_Hi = 180
            BP_Lo = 81
            I_Hi = 200
            I_Lo = 101
        if no2 >= 181 and no2 <= 280:
            BP_Hi = 280
            BP_Lo = 181
            I_Hi = 300
            I_Lo = 201
        if no2 >= 281 and no2 <= 400:
            BP_Hi = 400
            BP_Lo = 281
            I_Hi = 400
            I_Lo = 301
        if no2 > 400:
            BP_Hi = 430
            BP_Lo = 351
            I_Hi = 500
            I_Lo = 401

        no2_sub_index = (((I_Hi-I_Lo)/(BP_Hi-BP_Lo))*(pm10-BP_Lo))+I_Lo
            
        
        aqi = round(max(pm10_sub_index, so2_sub_index, no2_sub_index), 2)

    except Exception as e:
        print(e) 
        pass

    return aqi 



#func to get aqi result from openweather api using lat and long
def get_current_aqi_data(lat, long):
    data = {}

    try:
        key = f"{lat}_{long}_current_aqi"
        #check if cache data exists
        cached_data = cache_get(key)
        if cached_data:
            data = cached_data
        else:
            #sending request to openweather
            url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&appid={OPEN_WEATHER_API_KEY}"
            response = requests.get(url).json()
            

            #extracting the required data
            #converting unix date to Asia/Kolkata timezone
            dt = unix_time_to_kolkata_datetime(response["list"][0]["dt"])

            aqi = str(response["list"][0]["main"]["aqi"])
            aqi_status = AQI_INDEX[aqi]["rating"]
            col = AQI_INDEX[aqi]["col"]


            no2 = response["list"][0]["components"]["no2"]
            so2 = response["list"][0]["components"]["so2"]
            pm10 = response["list"][0]["components"]["pm10"]
            aqi_index = aqi_indian(so2, no2, pm10)

            data["date"] = format_date(dt, '%d-%m-%Y %H:%M')
            data["aqi_status"] = aqi_status
            data["aqi_index"] = aqi_index
            data["col"] = col

            # getting the prominent pollutant name 
            pollutants = {
                "no2": no2,
                "so2": so2,
                "pm10": pm10
            }
            prominent_pollutant = max(pollutants, key=lambda k: pollutants[k])
            pollutants["prominent"] = prominent_pollutant

            data["pollutants"] = pollutants

            #calculating the percentage for each pollutants      
            data["pollutant_percent"] = {
                "no2": round((no2/200*100), 2),
                "so2": round((so2/350*100), 2),
                "pm10": round((pm10/200*100), 2)
            }

            #setting the cache for 15min
            cache_set(key, data, ttl_sec=60*15)
    
    except Exception as e:
        print(e) 
        pass

    return data


#func to get current aqi data based on city name
def get_city_current_aqi_data(city_name):
    data = {}

    try:
        #getting the lat and long of city
        loc = get_reverse_loc_details(city_name)
        if loc is not None:
            lat = loc["latitude"]
            long = loc["longitude"]

            #getting AQI data using lat and long
            aqi_data = get_current_aqi_data(lat, long)
            if aqi_data != None:
                data = aqi_data
                data["loc"] = {
                    "latitude": lat,
                    "longitude": long,
                }  
    
    except Exception as e:
        print(e) 
        pass

    return data



#func to get historic aqi result from openweather api
def get_historic_aqi_data(lat, long, start_date, end_date):
    cleaned_data = []

    try:
        key = f"{lat}_{long}_historic_aqi"
        #check if data is present in cache
        cached_data = cache_get(key)
        if cached_data:
            cleaned_data = cached_data
        else:
            #sending request to openweather
            url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={long}&start={start_date}&end={end_date}&appid={OPEN_WEATHER_API_KEY}"
            response = requests.get(url).json()

            prev_dt = None
            for data in response["list"]:
                #extracting the required data
                #converting unix date to Asia/Kolkata timezone and then extracting date only
                dt = extract_date(unix_time_to_kolkata_datetime(data["dt"]))

                #append only the first data for a single date
                if dt != prev_dt:
                    prev_dt = dt

                    no2 = data["components"]["no2"]
                    so2 = data["components"]["so2"]
                    pm10 = data["components"]["pm10"]
                    aqi_index = aqi_indian(so2, no2, pm10)

                    cleaned_data.append({
                        "date": format_date(dt),
                        "aqi_index": aqi_index,
                        "pollutants": {
                            "no2": no2,
                            "so2": so2,
                            "pm10": pm10,
                        }
                    })
            #set the cache for 1day
            cache_set(key, cleaned_data, ttl_sec=60*60*24)

    
    except Exception as e:
        print(e) 
        pass

    return cleaned_data



#func to get location details using coordinates
def get_reverse_loc_details(city_name):
    data = None

    try:
        key = f"{city_name}_reverse_loc_details"
        #check if data exists in cache
        cache_data = cache_get(key)
        if cache_data:
            data = cache_data
        else:
            #sending request to openweather
            url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={OPEN_WEATHER_API_KEY}"
            response = requests.get(url).json()
            
            if response is not None and len(response) != 0:
                data = {
                    "latitude": response[0]["lat"],
                    "longitude": response[0]["lon"],
                }

            #set the cache for 5days
            cache_set(key, data, ttl_sec=60*60*24*5)

    except Exception as e:
        print(e)
        pass

    return data




#func to get location details using coordinates
def get_loc_details(lat, long):
    data = None

    try:
        key = f"{lat}_{long}_loc_details"
        #check if data exists in cache
        cache_data = cache_get(key)
        if cache_data:
            data = cache_data
        else:
            #sending request to openweather
            url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={long}&limit=0&appid={OPEN_WEATHER_API_KEY}"
            response = requests.get(url).json()   

            data = {
                "city": response[0]["name"],
                "country": "India" if response[0]["country"].lower()=="in" else response[0]["country"],
                "state": response[0]["state"],
            }

            #setting cache for 5days
            cache_set(key, data, ttl_sec=60*60*24*5)

    except Exception as e:
        print(e)
        pass

    return data




#func to get city details for map
def get_city_list_data():
    data = []

    try:
        key = f"city_list_data"
        #check if data is present in cache
        cached_data = cache_get(key)
        if cached_data:
            data = cached_data
        else:
            #getting city details for each city
            for city in CITY_NAMES:

                #getting city coordinates
                coordinates = get_reverse_loc_details(city)

                #check if coordinates is None
                if coordinates is not None:
                    lat = coordinates["latitude"]
                    long = coordinates["longitude"]

                    #getting AQI details
                    aqi_data = get_current_aqi_data(lat, long)

                    #check if aqi_data is None
                    if aqi_data is not None:

                        data.append({
                            "geometry": {
                                "latitude": lat,
                                "longitude": long
                            },
                            "properties": {
                                "name": city,
                                "aqi_status": aqi_data["aqi_status"],
                                "pm10": aqi_data["pollutants"]["pm10"],
                                "so2": aqi_data["pollutants"]["so2"],
                                "no2": aqi_data["pollutants"]["no2"],
                            }
                        })

            #setting the cache for 1hr
            cache_set(key, data, ttl_sec=60*60)

    
    except Exception as e:
        print(e)
        pass

    return data 




