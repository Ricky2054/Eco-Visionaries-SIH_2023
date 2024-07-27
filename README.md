## Introduction
This application is developed for SIH 2023 on Problem Statement: **Air and water quality index and environment monitoring**, under theme: **Agriculture, FoodTech and Rural Development**.
This codebase is just a prototype for the idea.
The semantic working diagram of this project is given below.

![Working Model-bg](https://github.com/Mr-Atanu-Roy/Eco-Visionaries-SIH_2023/assets/100309120/4ba2ded3-4a87-4690-8eae-36a2158a8514)


## Features


- Monitoring of AQI and WQI through sensors 
- Advanced and easy AQI monitoring
- Realtime AQI status of various cities shown on the map
- Future prediction of AQI and WQI with the pollutant’s concentration through AI/ML 
- Based on the present as well as the future predicted values of AQI, the probable sites for plantation can be proposed
- With the proposed WQI detection scheme, samples of drinking water in a particular area will be monitored through image processing/sensors and based on the results suggestions/alerts to the concern authority will be delivered


## Tech Stack

**Client Side:** HTML, CSS, SCSS, TailwindCSS, JavaScript, JQuery

**Server Side:** Python, Django, Redis

**Database:** SQLite (can be upgraded to MySQL/Postgress)

**Integration:** OpenWeather API, Leaflet

**ML:** Statsmodels

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- Django settings

`DEBUG = TRUE`

`SECRET_KEY = "django-insecure-6e8hq7rb_dy*h+ert@6w4%ju7z2k59+5r_jc)9l)%2#k)q04y5"`

`OPEN_WEATHER_API_KEY = "YOUR OPENWEATHER API KEY"`

For the `OPEN_WEATHER_API_KEY`, visit https://openweathermap.org/appid and get the API KEY



## Installation

Create a folder and open terminal and install this project by
command 
```bash
git clone https://github.com/Mr-Atanu-Roy/Eco-Visionaries-SIH_2023

```
or simply download this project from https://github.com/Mr-Atanu-Roy/Eco-Visionaries-SIH_2023

In project directory Create a virtual environment of any name(say env)

```bash
  virtualenv env

```
Activate the virtual environment

For windows:
```bash
  env\Script\activate

```
Install dependencies
```bash
  pip install -r requirements.txt

```
To migrate the database run migrations commands
```bash
  py manage.py makemigrations
  py manage.py migrate

```

Create a super user
```bash
  py manage.py createsuperuser

```


To run the project in your localserver
```bash
  py manage.py runserver

```
**Note: Redis Server must be installed on your system**

## Authors

- [@Atanu Roy](https://github.com/Mr-Atanu-Roy)
- [@Ricky](https://github.com/Ricky2054)
- [@Sagarika](https://github.com/Sagarika-02)

