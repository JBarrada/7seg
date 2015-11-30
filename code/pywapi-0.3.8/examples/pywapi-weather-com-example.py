#!/usr/bin/env python3

import pywapi
import pprint
pp = pprint.PrettyPrinter(indent=4)

kalamata = pywapi.get_weather_from_weather_com('78728')

pp.pprint(kalamata)
