import os
import requests

from accounts.utils import unix_time_to_kolkata_datetime, extract_date, format_date


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
        "rating": "very poor",
        "col": "#7E24CE"
    },
}


#city names
CITY_NAMES=['asansol', 'baruipur', 'durgapur', 'haldia', 'howrah', 'kolkata', 'barrackpore', 'durgapur', 'raniganj', 'sankrail', 'south suburban', 'calcutta', 'dankuni', 'haldia', 'kalyani', 'maldah', 'siliguri', 'uluberia']




#func to get aqi result from openweather api using lat and long
def get_current_aqi_data(lat, long):
    data = {}

    try:
        #sending request to openweather
        url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&appid={OPEN_WEATHER_API_KEY}"
        response = requests.get(url).json()
        

        #extracting the required data
        #converting unix date to Asia/Kolkata timezone
        dt = unix_time_to_kolkata_datetime(response["list"][0]["dt"])

        aqi = str(response["list"][0]["main"]["aqi"])
        aqi_status = AQI_INDEX[aqi]["rating"]
        col = AQI_INDEX[aqi]["col"]

        aqi_index = response["list"][0]["main"]["aqi"]
        no2 = response["list"][0]["components"]["no2"]
        so2 = response["list"][0]["components"]["so2"]
        pm10 = response["list"][0]["components"]["pm10"]
        # co = response["list"][0]["components"]["co"]
        # o3 = response["list"][0]["components"]["o3"]
        # pm2_5 = response["list"][0]["components"]["pm2_5"]

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

                cleaned_data.append({
                    "date": format_date(dt),
                    "pollutants": {
                        "no2": no2,
                        "so2": so2,
                        "pm10": pm10,
                    }
                })


    
    except Exception as e:
        print(e) 
        pass

    return cleaned_data



#func to get location details using coordinates
def get_reverse_loc_details(city_name):
    data = None

    try:
        #sending request to openweather
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={OPEN_WEATHER_API_KEY}"
        response = requests.get(url).json()
        
        if response is not None and len(response) != 0:
            data = {
                "latitude": response[0]["lat"],
                "longitude": response[0]["lon"],
            }

    except Exception as e:
        print(e)
        pass

    return data




#func to get location details using coordinates
def get_loc_details(lat, long):
    data = None

    try:
        #sending request to openweather
        url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={long}&limit=0&appid={OPEN_WEATHER_API_KEY}"
        response = requests.get(url).json()   

        data = {
            "city": response[0]["name"],
            "country": "India" if response[0]["country"].lower()=="in" else response[0]["country"],
            "state": response[0]["state"],
        }

    except Exception as e:
        print(e)
        pass

    return data




#func to get city details for map
def get_city_list_data():
    data = []

    try:
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

    
    except Exception as e:
        print(e)
        pass

    return data 




