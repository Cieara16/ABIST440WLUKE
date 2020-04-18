# Team Ferment - James Bee, Virginia Hoffman, Michaela Fox, and Samantha Scheer
# IST 440 - Luke Kasper

# imports
#import AutoBrew
import RPi.GPIO as GPIO
import time
import requests
import json
import Adafruit_DHT
import Adafruit_CharLCD as LCD
import os
import sys, subprocess
import math

# clock imports
import datetime
from Adafruit_LED_Backpack import SevenSegment

# service now imports
import requests

# from pymongo import MongoClient 
# import pymongo

# led matrix
import re
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

# setting variables for lcdScreen
lcdColumns = 16
lcdRows = 2

# setting variables (temp)
tempSensor = Adafruit_DHT.DHT11
tempPin = 4

# setting vairables for buzzer
buzzerPin = 18

# ledMartrix variables
cascaded = 1
block_orientation = 90
rotate = 0

# clock veriables
segment = SevenSegment.SevenSegment(address=0x70)


# class for getting brew task fro boil
class BrewTask():
    def BrewTaskGET():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=sys_created_onRELATIVEGT%40minute%40ago%401&sysparm_limit=1'
        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = '***'

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
        
        startTask = response.json()['result'][0]['rpi_to_execute']
        print(startTask)
        FermentPi = startTask['FermentPi']

# recipie table Yeast
class RecipeiTableYeast():
    def Yeast1Get():
        # Set the request parameters 
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=yeast_type_1%3D&sysparm_limit=1' 
     
        # Eg. User name="admin", Password="admin" for this code sample. 
        user = 'mmf5571' 
        pwd = '***' 
     
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
        yeast1 = data['result'][0]['yeast_type_1']
        print("Yeast type 1: " + str(yeast1))
 
    def Yeast2Get(): 
        # Set the request parameters 
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=yeast_type_2%3D&sysparm_limit=1' 
 
        # Eg. User name="admin", Password="admin" for this code sample. 
        user = 'mmf5571' 
        pwd = '***' 
 
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
        yeast2 = data['result'][0]['yeast_type_2']
        print("Yeast type 2: " + str(yeast2))
 
    def Yeast3Get(): 
        # Set the request parameters 
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=yeast_type_3%3D&sysparm_limit=1' 
 
        # Eg. User name="admin", Password="admin" for this code sample. 
        user = 'mmf5571' 
        pwd = '***' 
 
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
        yeast3 = data['result'][0]['yeast_type_3']
        print("Yeast type 3: " + str(yeast3))
    
# recipie table ABV
class RecipieTableABV():
    def ABVGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=abv%3D&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = '***'

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
        ABVLevel = data['result'][0]['abv']
        print("ABV Level: " + str(ABVLevel))

# recipie table sugar
class RecipieTableSugar():
    def SugarGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=sugar_levels%3D&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = '***'

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
        sugarAmount = data['result'][0]['sugar_levels']
        print("Sugar Amount: " + str(sugarAmount))
        
# Log table time stamps
class FermentingTimeStamps():
    def FermentStartGET():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_query=fermenting_start_timeONToday%40javascript%3Ags.beginningOfToday()%40javascript%3Ags.endOfToday()&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = '***'

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
        
        #FermentTempStart = data['boil']
        #print("Max Temp: " + maxTemp)

    def FermentEndGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_query=fermenting_end_timeONToday%40javascript%3Ags.beginningOfToday()%40javascript%3Ags.endOfToday()&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = '***'

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

# # temp log - log table
# class FermentTemps():
#     def tempGet():
# 
#     TempAndHumidityLCD(lcdColumns, lcdRows, tempSensor, tempPin)
# 
#     temperature, humidity = Adafruit_DHT.read(tempSensor, tempPin)
#     time.sleep(1)
#     GPIO.cleanup()
# 
#     temperature = temperature * 9 / 5.0 + 32
#     lcd.set_backlight(0)
#     lcd.message("Current temp\n" + temperature)  # pulled from mother brew
#     time.sleep(3.0)
#     lcd.clear()
#     GPIO.cleanup()
# 
#     # checking temp
#     for i in range(0, 6):
#         # temp too low
#         if (temperature < 68):
#             lcd.set_backlight(0)
#             lcd.message("Temperature is\n" + "too low: " + str(temperature) + " F")
#             time.sleep(3.0)
#             lcd.clear()
#             GPIO.cleanup()
# 
#         # temp too high
#         elif (temperature > 78):
#             lcd.set_backlight(0)
#             lcd.message("Temperature is\n" + "too high: " + str(temperature) + " F")
#             time.sleep(3.0)
#             lcd.clear()
#             GPIO.cleanup()
# 
#         # temp acutally worked
#         elif (temperature == 78):
#             break
#         i += 1
# 
#     def temoUpdate():
# 
#     def tempPost():


# class steralize
class FermentClean():
    def CleanGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_query=ferment_tempature%3D&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = '***'

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

# quality check
class QualityCheck():
    def qualityCheckGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_query=ferment_tempature%3D&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = '***'

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
        
# class ferment duration
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
        pwd = '***'

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
        print(data)duration = data['result'][0]['fermentation_duration']
        print("Fermentation Duration: " + str(duration))
        
# class 2nd ferment
class SecondFerment():
    def secondFermentGet():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=secondary_fermentation%3D&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = '***'

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
        secondFerment = data['result'][0]['secondary_fermentation']
        print("Secondary Fermentation: " + str(secondFerment))        
        
        if (str(secondFerment) == 'Kräusening'):
            print("Kräusening selected.")
            print("Sent to conditioning tank.")
            print("Fermenting.")
            BuzzerDone(buzzerPin)
            print("Sent to bottle.")

        elif (str(secondFerment) == 'Bottle'):
            print("Bottle selected.")
            print("Fermenting.")
            BuzzerDone(buzzerPin)
            print("Sent to bottle.")

        elif (str(secondFerment) == 'Cask_Condistioning'):
            print("Cask Conditioning selected.")
            print("Putting into cask.")
            print("Fermenting.")
            BuzzerDone(buzzerPin)
            print("Sent to bottle.")

        elif (str(secondFerment) == 'Lagering'):
            print("Laggering selected.")
            print("Storing at celler temperature.")
            print("Fermenting.")
            BuzzerDone(buzzerPin)
            print("Sent to bottle.")

        elif (str(secondFerment) == 'Secondary'):
            print("Secondary Fermentation selected.")
            print("Fermenting.")
            BuzzerDone(buzzerPin)
            print("Sent to bottle.")

        elif (str(secondFerment) == 'Barrel_Agein'):
            print("Barrel Aging Selected.")
            print("Sent to barrel to sour.")
            print("Fermenting.")
            BuzzerDone(buzzerPin)
            print("Sent to bottle.")

        else:
            print("Fermenting.")
            BuzzerDone(buzzerPin)
            print("Sent to bottle.")
            
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


# led matrix function
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


# function for stepmotor
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
    GPIO.setup(pin_A, GPIO.OUT)
    GPIO.setup(pin_B, GPIO.OUT)
    GPIO.setup(pin_C, GPIO.OUT)
    GPIO.setup(pin_D, GPIO.OUT)
    GPIO.output(pin_A, False)
    GPIO.output(pin_B, False)
    GPIO.output(pin_C, False)
    GPIO.output(pin_D, False)

    for i in range(0, 31):
        GPIO.output(pin_D, True)
        time.sleep(interval)
        GPIO.output(pin_D, False)

    GPIO.cleanup()


# function for clock
def Clock():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second

    segment.clear()
    # Set hours
    segment.set_digit(0, int(hour / 10))  # Tens
    segment.set_digit(1, hour % 10)  # Ones
    # Set minutes
    segment.set_digit(2, int(minute / 10))  # Tens
    segment.set_digit(3, minute % 10)  # Ones
    # Toggle colon
    segment.set_colon(second % 2)  # Toggle colon at 1Hz

    # Write the display buffer to the hardware.  This must be called to
    # update the actual display LEDs.
    segment.write_display()

    # Wait a quarter second (less than 1 second to prevent colon blinking getting$
    time.sleep(0.25)


# runs all other code
def Main():
    BrewTask.BrewTaskGET()
    RecipeiTableYeast.YeastGet()

    segment = SevenSegment.SevenSegment(address=0x70)
    # Initialize the display. Must be called once before using the display.
    segment.begin()

    # initialize ledmatrix
    msg = ""
    LEDMatrix(cascaded, block_orientation, rotate, msg)

    # initialize LCD screen
    TempAndHumidityLCD(lcdColumns, lcdRows, tempSensor, tempPin)
    lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

    msg = "."

    temperature, humidity = Adafruit_DHT.read(tempSensor, tempPin)
    time.sleep(1)
    GPIO.cleanup()

    temperature = temperature * 9 / 5.0 + 32
    lcd.set_backlight(0)
    lcd.message("Current temp\n" + temperature)  # pulled from mother brew
    time.sleep(3.0)
    lcd.clear()
    GPIO.cleanup()

    # checking temp
    for i in range(0, 6):
        # temp too low
        if (temperature < 68):
            lcd.set_backlight(0)
            lcd.message("Temperature is\n" + "too low: " + str(temperature) + " F")
            time.sleep(3.0)
            lcd.clear()
            GPIO.cleanup()

        # temp too high
        elif (temperature > 78):
            lcd.set_backlight(0)
            lcd.message("Temperature is\n" + "too high: " + str(temperature) + " F")
            time.sleep(3.0)
            lcd.clear()
            GPIO.cleanup()

        # temp acutally worked
        elif (temperature == 78):
            break
        i += 1

    lcd.set_backlight(0)
    lcd.message("Temperature is:\n" + str(temperature) + " F")
    time.sleep(5.0)
    lcd.clear()
    GPIO.cleanup()

    # pull yeast and sugar to check amounts
    RecipeiTableYeast.Yeast1Get()
    RecipeiTableYeast.Yeast2Get()
    RecipeiTableYeast.Yeast3Get()

    RecipieTableSugar.SugarGet()

    # update API level and gravity check
    RecipieTableABV.ABVGet()

    # choose second ferment - if/elif branch
    SecondFerment.secondFermentGet()

    today = datetime.date.today()
 
     # end time
    outgoingTemp = datetime.date.today()

    FermentDuration.durationGet()


    QualityCheck.qualityCheckGet()


    FermentClean.CleanGet()
    Stepmotor()

    # push to boil

    print("Ferment Completed.")
    imprt CHeckForRecipie
# run all the stuff
Main()
