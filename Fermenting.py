#Team Ferment - James Bee, Virginia Hoffman, Michaela Fox, and Samantha Scheer
#IST 440 - Luke Kasper

#imports
import AutoBrew
import RPi.GPIO as GPIO
import time
import requests
import Adafruit_DHT
import Adafruit_CharLCD as LCD
import os
import sys, subprocess
import math

#clock imports
import datetime
from Adafruit_LED_Backpack import SevenSegment

#service now imports
import requests

#from pymongo import MongoClient
#import pymongo

#led matrix
import re
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


#setting variables for lcdScreen
lcdColumns = 16
lcdRows    = 2

# setting variables (temp)
tempSensor = Adafruit_DHT.DHT11
tempPin = 4

# setting vairables for buzzer
buzzerPin = 18

#ledMartrix variables
cascaded = 1
block_orientation = 90
rotate = 0

#clock veriables
segment = SevenSegment.SevenSegment(address=0x70)

#recipie table Yeast
class RecipeiTableYeast():
    def YeastGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=yeast%3D&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def YeastUpdate():
       # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2/e674799fdb80d010777efae4e29619bd?sysparm_display_value=yeast%3D'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.put(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def YeastPost():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2/e674799fdb80d010777efae4e29619bd?sysparm_display_value=yeast%3D'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.patch(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

#recipie table ABV
class RecipieTableABV():
    def ABVGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=abv%3D&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def ABVUpdate():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2/aae575dfdb80d010777efae4e296198a?sysparm_display_value=abv%3D'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.put(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def ABVPost():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2/e674799fdb80d010777efae4e29619bd?sysparm_display_value=abv%3D'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.patch(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

#recipie table sugar
class RecipieTableSugar():
    def SugarGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=sugar_levels%3D&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def SugarUpdate():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2/f1d67ddfdb80d010777efae4e2961946?sysparm_display_value=sugar_levels%3D'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.put(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def SugarPost():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2/f1d67ddfdb80d010777efae4e2961946?sysparm_display_value=sugar_levels%3D'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.patch(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

#Log table time stamps
class FermentingTimeStamps():
    def FermentStartGET():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_query=fermenting_start_timeONToday%40javascript%3Ags.beginningOfToday()%40javascript%3Ags.endOfToday()&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def FermentStartUodate():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table/0106d14fdb489010777efae4e296191f?sysparm_display_value=fermenting_start_timeONToday%40javascript%3Ags.beginningOfToday()%40javascript%3Ags.endOfToday()'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.put(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def FermentStartPost():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table/0106d14fdb489010777efae4e296191f?sysparm_display_value=fermenting_start_timeONToday%40javascript%3Ags.beginningOfToday()%40javascript%3Ags.endOfToday()'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.patch(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def FermentEndGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_query=fermenting_end_timeONToday%40javascript%3Ags.beginningOfToday()%40javascript%3Ags.endOfToday()&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def FermentEndUpdate():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table/3aa65d4fdb489010777efae4e2961981?sysparm_display_value=fermenting_end_timeONToday%40javascript%3Ags.beginningOfToday()%40javascript%3Ags.endOfToday()'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.put(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def FermentEndPost():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table/3aa65d4fdb489010777efae4e2961981?sysparm_display_value=fermenting_end_timeONToday%40javascript%3Ags.beginningOfToday()%40javascript%3Ags.endOfToday()'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.patch(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

#temp log - log table
class FermentTemps():
    def tempGet():


    def temoUpdate():


    def tempPost():


#class steralize
class FermentClean():
    def CleanGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_query=ferment_tempature%3D&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def CLeanUpdate():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table/f34ec69fdbc0d010777efae4e296195e?sysparm_display_value=ferment_tempature%3D'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.put(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def CLeanPost():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table/93ec0a5fdbc0d010777efae4e296198d?sysparm_display_value=ferment_tempature%3D'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.patch(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

#quality check
class QualityCheck():
    def qualityCheckGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_query=ferment_tempature%3D&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def qauqlityCheckUpdate():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table/93ec0a5fdbc0d010777efae4e296198d?sysparm_display_value=ferment_tempature%3D'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.put(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)


    def qualityCheckPost():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table/93ec0a5fdbc0d010777efae4e296198d?sysparm_display_value=ferment_tempature%3D'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.patch(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

#class ferment duration
class FermentDuration():
    def durationGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_query=fermenting_duration%3Djavascript%3Ags.getDurationDate('
        0 % 200 % 3
        A0 % 3
        A0
        ')&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def durationUpdate():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table/d03f8e9fdbc0d010777efae4e29619c2?sysparm_display_value=fermenting_duration%3Djavascript%3Ags.getDurationDate('
        0 % 200 % 3
        A0 % 3
        A0
        ')'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.put(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def durationPost():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table/d03f8e9fdbc0d010777efae4e29619c2?sysparm_display_value=fermenting_duration%3Djavascript%3Ags.getDurationDate('
        0 % 200 % 3
        A0 % 3
        A0
        ')'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.patch(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

#class 2nd ferment
class SecondFerment():
    def secondFermentGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=secondary_fermentation%3D&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def secondFermentUpdate():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2/e74ebdd3dbc0d010777efae4e29619f3?sysparm_display_value=secondary_fermentation%3D'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.put(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def secondFermentPost():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2/f39efdd3dbc0d010777efae4e2961951?sysparm_display_value=secondary_fermentation%3D'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.patch(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

# function to display temp n humidity
def TempAndHumidityLCD(lcdColumns, lcdRows, tempSensor, tempPin):
    # Initialize the LCD using the pins
    lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

    temperature, humidity = Adafruit_DHT.read(tempSensor, tempPin)
    time.sleep(1)
    GPIO.cleanup()

    temperature = temperature * 9 / 5.0 + 32

    temperatureStr = str(temperature)
    humidityStr = str(humidity)

    # print temp
    lcd.set_backlight(0)
    lcd.message("Current temp \n" + temperatureStr + " F")
    time.sleep(5.0)
    lcd.clear()

    # print humidity
    lcd.set_backlight(0)
    lcd.message("Current humidity \n" + humidityStr + " %")
    time.sleep(5.0)
    lcd.clear()
    GPIO.cleanup()

# function to buzz wghen fermenting is done
def BuzzerDone(buzzerPin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzerPin, GPIO.OUT)

    # Make buzzer sound
    GPIO.output(buzzerPin, GPIO.HIGH)
    time.sleep(0.5)

    # Stop buzzer sound
    GPIO.output(buzzerPin, GPIO.LOW)

    GPIO.cleanup()
    
#led matrix function
def LEDMatrix(cascaded, block_orientation, rotate, msg):
    
    # create matrix device
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded=cascaded or 1, block_orientation=block_orientation, rotate=rotate or 0)
    # debugging purpose
    print("[-] Matrix initialized")

    # debugging purpose
    print("[-] Printing: %s" % msg)
    show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)
    GPIO.cleanup()
    
#function for stepmotor
def StepMotor():
    # set GPIO mode
    GPIO.setmode(GPIO.BCM)
    
    # These are the pins which will be used on the Raspberry Pi
    pin_A = 5
    pin_B = 6
    pin_C = 13
    pin_D = 19
    interval = 0.010

    # Declare pins as output
    GPIO.setup(pin_A,GPIO.OUT)
    GPIO.setup(pin_B,GPIO.OUT)
    GPIO.setup(pin_C,GPIO.OUT)
    GPIO.setup(pin_D,GPIO.OUT)
    GPIO.output(pin_A, False)
    GPIO.output(pin_B, False)
    GPIO.output(pin_C, False)
    GPIO.output(pin_D, False)
    
    for i in range (0, 31):
        GPIO.output(pin_D, True)
        time.sleep(interval)
        GPIO.output(pin_D, False)
        
    GPIO.cleanup()

#function for clock
def Clock():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second

    segment.clear()
    # Set hours
    segment.set_digit(0, int(hour / 10))     # Tens
    segment.set_digit(1, hour % 10)          # Ones
    # Set minutes
    segment.set_digit(2, int(minute / 10))   # Tens
    segment.set_digit(3, minute % 10)        # Ones
    # Toggle colon
    segment.set_colon(second % 2)              # Toggle colon at 1Hz

    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    segment.write_display()

    # Wait a quarter second (less than 1 second to prevent colon blinking getting$
    time.sleep(0.25)

#runs all other code
def Main():
    QualityCheck.qualityCheckGet()
    QualityCheck.qauqlityCheckUpdate()
    QualityCheck.qualityCheckPost()

    today = datetime.date.today()
    FermentingTimeStamps.FermentStartUodate()

    FermentingTimeStamps.FermentStartPost()


    segment = SevenSegment.SevenSegment(address=0x70)
    # Initialize the display. Must be called once before using the display.
    segment.begin()

    #initialize ledmatrix
    msg = ""
    LEDMatrix(cascaded, block_orientation, rotate, msg)
    
    #initialize LCD screen
    TempAndHumidityLCD(lcdColumns, lcdRows, tempSensor, tempPin)
    lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
    
    msg = "."

    temperature, humidity = Adafruit_DHT.read(tempSensor, tempPin)
    time.sleep(1)
    GPIO.cleanup()

    #get incoming temp from boil
    FermentingTimeStamps.FermentEndGet()
    temperature = response.json()['result']
    outgoingTemp = temperature['maxtemp']
    FermentingTimeStamps.FermentEndUpdate()


    temperature = temperature * 9 / 5.0 + 32
    lcd.set_backlight(0)
    lcd.message("Current temp\n" + temperature) #pulled from mother brew
    time.sleep(3.0)
    lcd.clear()
    GPIO.cleanup()

    #checking temp
    for i in range (0, 6):
        #temp too low
        if (temperature < 68):
            lcd.set_backlight(0)
            lcd.message("Temperature is\n" + "too low: "+ str(temperature) + " F")
            time.sleep(3.0)
            lcd.clear()
            GPIO.cleanup()
            
        #temp too high
        elif (temperature > 78):
            lcd.set_backlight(0)
            lcd.message("Temperature is\n" + "too high: " + str(temperature) + " F")
            time.sleep(3.0)
            lcd.clear()
            GPIO.cleanup()
        
        #temp acutally worked
        elif (temperature == 78):
            break
        i += 1
    
    lcd.set_backlight(0)
    lcd.message("Temperature is:\n" + str(temperature) + " F")
    time.sleep(5.0)
    lcd.clear()
    GPIO.cleanup()

    #update temp log
    FermentingTimeStamps.FermentEndPost()

    #pull yeast and sugar to check amounts
    RecipeiTableYeast.YeastGet()
    yeastAmount = response.json()['result']

    RecipieTableSugar.SugarGet()
    sugarAmount = response.json()['result']

    # if (yeastAmount == #right amount):
    RecipeiTableYeast.YeastUpdate()
    # else:
        # kill time to update yeast

    #if (suagrAmount == #right amount):
        RecipieTableSugar.SugarUpdate()
    #else:
        #kill time

    outgingYeastAmount = yeast['maxtemp']
    RecipeiTableYeast.YeastPost()

    outgoingSugarAmount = Sugar_levels['result']
    RecipieTableSugar.SugarPost()


    #update API level and gravity check
    RecipieTableABV.ABVGet()
    abv_level = response.json()['result']

    RecipieTableABV.ABVUpdate()
    # if (yeastAmount == #right amount):
        # do nothing
    # else:
        # kill time to update yeast

    RecipieTableABV.ABVPost()
    outgoingABVLevel = ABV['ABV']
    

    #choose second ferment - if/elif branch
    SecondFerment.secondFermentGet()
    secondary_fermentation= response.json()['result']

    if (secondary_fermentation == 'Kräusening'):
        BuzzerDone(buzzerPin)

    elif (secondary_fermentation == 'Bottle'):
        BuzzerDone(buzzerPin)

    elif (secondary_fermentation == 'Cask_Condistioning'):
        BuzzerDone(buzzerPin)

    elif (secondary_fermentation == 'Lagering'):
        BuzzerDone(buzzerPin)

    elif (secondary_fermentation == 'Secondary'):
        BuzzerDone(buzzerPin)

    elif (secondary_fermentation == 'Barrel_Agein'):
        BuzzerDone(buzzerPin)

    else:
        BuzzerDone(buzzerPin)

    #end time
    outgoingTemp = datetime.date.today()
    FermentingTimeStamps.FermentEndUpdate()

    FermentingTimeStamps.FermentEndPost()

    FermentDuration.durationGet()
    FermentDuration.durationUpdate()
    FermentDuration.durationPost()


    FermentClean.CleanGet()
    FermentClean.CLeanUpdate()
    FermentClean.CLeanPost()

    #push to boil


#run all the stuff
Main()
