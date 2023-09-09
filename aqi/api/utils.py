import os
import requests

from accounts.utils import unix_time_to_kolkata_datetime, extract_date, format_date


AIR_VISUAL_API_KEY = os.environ.get("AIR_VISUAL_API_KEY")
OPEN_WEATHER_API_KEY = os.environ.get("OPEN_WEATHER_API_KEY")


AQI_INDEX = {
    "1": {
        "rating": "good",
        "col": "#16a34a"
    },
    "2": {
        "rating": "fair",
        "col": "#115e59"
    },
    "3": {
        "rating": "moderate",
        "col": "#ca8a04"
    },
    "4": {
        "rating": "poor",
        "col": "#b91c1c"
    },
    "5": {
        "rating": "very poor",
        "col": "#881337"
    },
}

#func to get aqi result from openweather api
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
        co = response["list"][0]["components"]["co"]
        no2 = response["list"][0]["components"]["no2"]
        o3 = response["list"][0]["components"]["o3"]
        so2 = response["list"][0]["components"]["so2"]
        pm2_5 = response["list"][0]["components"]["pm2_5"]
        pm10 = response["list"][0]["components"]["pm10"]

        data["date"] = format_date(dt, '%d-%m-%Y %H:%M')
        data["aqi_status"] = aqi_status
        data["aqi_index"] = aqi_index
        data["col"] = col
        data["co"] = co
        data["no2"] = no2
        data["o3"] = o3
        data["so2"] = so2
        data["pm2_5"] = pm2_5
        data["pm10"] = pm10

        #calculating the percentage for each pollutants
        data["co_percent"] = round((co/15400*100), 2)
        data["no2_percent"] = round((no2/200*100), 2)
        data["o3_percent"] = round((o3/180*100), 2)
        data["so2_percent"] = round((so2/350*100), 2)
        data["pm2_5_percent"] = round((pm2_5/75*100), 2)
        data["pm10_percent"] = round((pm10/200*100), 2)

    
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

                # aqi_index = data["main"]["aqi"]
                co = data["components"]["co"]
                no2 = data["components"]["no2"]
                o3 = data["components"]["o3"]
                so2 = data["components"]["so2"]
                # pm2_5 = data["components"]["pm2_5"]
                pm10 = data["components"]["pm10"]

                cleaned_data.append({
                    "date": format_date(dt),
                    # "aqi_index": aqi_index,
                    # "co": co,
                    "no2": no2,
                    # "o3": o3,
                    "so2": so2,
                    # "pm2_5": pm2_5,
                    "pm10": pm10,
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


