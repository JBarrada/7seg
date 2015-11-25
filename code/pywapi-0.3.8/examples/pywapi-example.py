#!/usr/bin/env python

import pywapi

weather_com_result = pywapi.get_weather_from_weather_com('78728')
yahoo_result = pywapi.get_weather_from_yahoo('78728')
noaa_result = pywapi.get_weather_from_noaa('KATT')

print "Weather.com says: It is " + weather_com_result['current_conditions']['text'].lower() + " and " + str(float(weather_com_result['current_conditions']['temperature'])*1.8+32.0) + "F now in Austin"

print("Yahoo says: It is " + yahoo_result['condition']['text'].lower() + " and " + str(float(yahoo_result['condition']['temp'])*1.8+32.0) + "F now in Austin.")

print("NOAA says: It is " + noaa_result['weather'].lower() + " and " + noaa_result['temp_c'] + "C now in Austin.")
