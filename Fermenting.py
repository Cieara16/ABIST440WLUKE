# Team Ferment - James Bee, Virginia Hoffman, Michaela Fox, and Samantha Scheer
# IST 440 - Luke Kasper

#imports
import RPi.GPIO as GPIO
import time
import datetime
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
msg = ""
#LEDMatrix(cascaded, block_orientation, rotate, msg)
cascaded = 1
block_orientation = 90
rotate = 0

#startup pi parts
segment = SevenSegment.SevenSegment(address=0x70)
# Initialize the display. Must be called once before using the display.
segment.begin()

#LCD screen
#TempAndHumidityLCD(lcdColumns, lcdRows, tempSensor, tempPin)
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
msg = "."

#get recipie
def CheckForRecipie():
    import CheckForRecipie

#get crud
def MotherBrewGet():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=abvISNOTEMPTY%2525abvISNOTEMPTY%255Eyeast_type_1ISNOTEMPTY%2525abvISNOTEMPTY%255Eyeast_type_1ISNOTEMPTY%255Eyeast_type_2ISNOTEMPTY%2525abvISNOTEMPTY%255Eyeast_type_1ISNOTEMPTY%255Eyeast_type_2ISNOTEMPTY%255Eyeast_type_3ISNOTEMPTY%2526abvISNOTEMPTY%255Eyeast_type_1ISNOTEMPTY%255Eyeast_type_2ISNOTEMPTY%255Eyeast_type_3ISNOTEMPTY%255Ebeer_typeANYTHING%2525abvISNOTEMPTY%255Eyeast_type_1ISNOTEMPTY%255Eyeast_type_2ISNOTEMPTY%255Eyeast_type_3ISNOTEMPTY%255Ebeer_typeANYTHING%255Esugar_levelsISNOTEMPTY%2525abvISNOTEMPTY%255Eyeast_type_1ISNOTEMPTY%255Eyeast_type_2ISNOTEMPTY%255Eyeast_type_3ISNOTEMPTY%255Ebeer_typeANYTHING%255Esugar_levelsISNOTEMPTY%255Esecondary_fermentationANYTHING&sysparm_limit=1'
    user = 'kasper440'
    pwd = 'kasper440'

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()
        
    # Decode the JSON response into a dictionary and use the data
    global beerType, yeast1, yeast2, yeast3, ABVLevel, sugarAmount, secondFerment 
    beerTypeRecord = response.json()['result']
    beerType = beerTypeRecord[0]['beer_type']
    
    yeast1Record = response.json()['result']
    yeast1 = yeast1Record[0]['yeast_type_1']
    
    yeast2Record = response.json()['result']
    yeast2 = yeast2Record[0]['yeast_type_2']
    
    yeast3Record = response.json()['result']
    yeast3 = yeast3Record[0]['yeast_type_3']
    
    ABVLevelRecord = response.json()['result']
    ABVLevel = ABVLevelRecord[0]['abv']
    
    sugarAmountRecord = response.json()['result']
    sugarAmount = sugarAmountRecord[0]['sugar_levels']
    
    secondFermentRecord = response.json()['result']
    secondFerment = secondFermentRecord[0]['secondary_fermentation']
    
    print("Type of beer: " + beerType)
    print("Yeast type 1: " + yeast1)
    print("Yeast type 2: " + yeast2)
    print("Yeast type 3: " + yeast3)
    print("ABV Level: " + ABVLevel)
    print("Sugar Amount: " + sugarAmount)
    print("Secondary Fermentation: " + secondFerment)

#boil temps
def BoilTempGet():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_query=boil_end_timeONToday%2540javascript%253Ags.beginningOfToday()%2540javascript%253Ags.endOfToday()&sysparm_limit=1'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'kasper440'
    pwd = 'kasper440'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers )

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    global boilTemp
    global startTemp
    boilTemp = response.json()['result'][0]['boiling_temperature']
    print("Incoming temperature is: ", boilTemp)

    temperature, humidity = Adafruit_DHT.read(tempSensor, tempPin)
    time.sleep(1)
    GPIO.cleanup()

    startTemp = float(boilTemp) * 9 / 5.0 + 32
    lcd.set_backlight(0)
    print("Printing temperature: ")
    lcd.message("Incoming temp:\n" + str(boilTemp))  # pulled from mother brew
    time.sleep(3.0)
    lcd.clear()
    GPIO.cleanup()

def SecondFerment():
    #different temps for different beers
    #ale
    if (beerType == 'ale'):
        print("Temperature for an ale needs to be 72 degrees F.")
        #temp was right for ale
        if (startTemp == 72):
            lcd.set_backlight(0)
            lcd.message("Drink Type: Ale\n" + "Temp: " + str(startTemp) + " F")
            time.sleep(3.0)
            lcd.clear()
            GPIO.cleanup()
            pass

        #temp wasn't right for ale
        elif (startTemp != 72):
            for i in range(0, 6):
                # temp too low
                if (startTemp < 72):
                    lcd.set_backlight(0)
                    lcd.message("Temperature is\n" + "too low: " + str(startTemp) + " F")
                    time.sleep(3.0)
                    lcd.clear()
                    GPIO.cleanup()

                # temp too high
                elif (startTemp > 72):
                    lcd.set_backlight(0)
                    lcd.message("Temperature is\n" + "too high: " + str(startTemp) + " F")
                    time.sleep(3.0)
                    lcd.clear()
                    GPIO.cleanup()

                # temp acutally worked
                elif (startTemp == 72):
                    break
                i += 1

            #print ending temp
            lcd.set_backlight(0)
            lcd.message("Drink Type: Ale\n" + "Temp: " + str(startTemp) + " F")
            time.sleep(3.0)
            lcd.clear()
            GPIO.cleanup()

    #stout
    elif (beerType == 'stout'):
        print("Temperature for a stout needs to be 75 degrees F.")
        #temp was right for stout
        lcd.set_backlight(0)
        lcd.message("Drink Type: Ale\n" + "Temp: " + str(startTemp) + " F")
        time.sleep(3.0)
        lcd.clear()
        GPIO.cleanup()

        #temp was right
        if (startTemp == 75):
            lcd.set_backlight(0)
            lcd.message("Drink Type: Ale\n" + "Temp: " + str(startTemp) + " F")
            time.sleep(3.0)
            lcd.clear()
            GPIO.cleanup()
            pass

        # temp wasn't right for ale
        elif (startTemp != 75):
            for i in range(0, 6):
                # temp too low
                if (startTemp < 75):
                    lcd.set_backlight(0)
                    lcd.message("Temperature is\n" + "too low: " + str(startTemp) + " F")
                    time.sleep(3.0)
                    lcd.clear()
                    GPIO.cleanup()

                # temp too high
                elif (startTemp > 75):
                    lcd.set_backlight(0)
                    lcd.message("Temperature is\n" + "too high: " + str(startTemp) + " F")
                    time.sleep(3.0)
                    lcd.clear()
                    GPIO.cleanup()

                # temp acutally worked
                elif (startTemp == 75):
                    break
                i += 1

            # print ending temp
            lcd.set_backlight(0)
            lcd.message("Drink Type: Ale\n" + "Temp: " + str(startTemp) + " F")
            time.sleep(3.0)
            lcd.clear()
            GPIO.cleanup()

    elif (beerType == 'lager'):
        #temp was right for lager
        print("Temperature for a lager needs to be 55 degrees F.")
        # temp was right for stout
        lcd.set_backlight(0)
        lcd.message("Drink Type: Ale\n" + "Temp: " + str(startTemp) + " F")
        time.sleep(3.0)
        lcd.clear()
        GPIO.cleanup()

        # temp was right
        if (startTemp == 55):
            lcd.set_backlight(0)
            lcd.message("Drink Type: Ale\n" + "Temp: " + str(startTemp) + " F")
            time.sleep(3.0)
            lcd.clear()
            GPIO.cleanup()
            pass

        # temp wasn't right for ale
        elif (startTemp != 55):
            for i in range(0, 6):
                # temp too low
                if (startTemp < 55):
                    lcd.set_backlight(0)
                    lcd.message("Temperature is\n" + "too low: " + str(startTemp) + " F")
                    time.sleep(3.0)
                    lcd.clear()
                    GPIO.cleanup()

                # temp too high
                elif (startTemp > 55):
                    lcd.set_backlight(0)
                    lcd.message("Temperature is\n" + "too high: " + str(startTemp) + " F")
                    time.sleep(3.0)
                    lcd.clear()
                    GPIO.cleanup()

                # temp acutally worked
                elif (temperature == 55):
                    break
                i += 1

            # print ending temp
            lcd.set_backlight(0)
            lcd.message("Drink Type: Ale\n" + "Temp: " + str(startTemp) + " F")
            time.sleep(3.0)
            lcd.clear()
            GPIO.cleanup()

    elif (beerType == 'ipa'):
        #temp was right for ipa
        print("Temperature for an IPA needs to be 70 degrees F.")
        # temp was right for stout
        lcd.set_backlight(0)
        lcd.message("Drink Type: Ale\n" + "Temp: " + str(startTemp) + " F")
        time.sleep(3.0)
        lcd.clear()
        GPIO.cleanup()

        # temp was right
        if (startTemp == 70):
            lcd.set_backlight(0)
            lcd.message("Drink Type: Ale\n" + "Temp: " + str(startTemp) + " F")
            time.sleep(3.0)
            lcd.clear()
            GPIO.cleanup()
            pass

        # temp wasn't right for ale
        elif (startTemp != 70):
            for i in range(0, 6):
                # temp too low
                if (startTemp < 70):
                    lcd.set_backlight(0)
                    lcd.message("Temperature is\n" + "too low: " + str(startTemp) + " F")
                    time.sleep(3.0)
                    lcd.clear()
                    GPIO.cleanup()

                # temp too high
                elif (startTemp > 70):
                    lcd.set_backlight(0)
                    lcd.message("Temperature is\n" + "too high: " + str(startTemp) + " F")
                    time.sleep(3.0)
                    lcd.clear()
                    GPIO.cleanup()

                # temp acutally worked
                elif (startTemp == 70):
                    break
                i += 1

            # print ending temp
            lcd.set_backlight(0)
            lcd.message("Drink Type: Ale\n" + "Temp: " + str(startTemp) + " F")
            time.sleep(3.0)
            lcd.clear()
            GPIO.cleanup()
    
#function for POST
def PostCRUD():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_display_value=All'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'kasper440'
    pwd = 'kasper440'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data = "{\fermenting_start_time\":\"" + str(startTime)
                             + "\",\"fermenting_end_time\":\"" + str(endTime)
                             + "\",\"ferment_temeprature\":\"" + str(boilTemp)
                             + "\",\"fermenting_end_time\":\"" + str(endTime)
                             + "\",\"fermenting_duration\":\"" + str(fermentDuration)
                             + "\",\"abv\":\"" + str(ABVLevel)
                             + "\",\"fermenting_quality_check\":\"true\"}"
                             + "\",\"fermenting_reset/clean\":\"true\"}"
                             + "\",\"second_fermentation\":\"true\"}")

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
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


# led matrix function
def LEDMatrix(cascaded, block_orientation, rotate, msg):
    # create matrix device
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded=cascaded or 1, block_orientation=block_orientation, rotate=rotate or 0)
    # debugging purpose
    print("[-] Matrix initialized")

    # print hello world on the matrix display
    msg = "."
    # debugging purpose
    print("[-] Printing: %s" % msg)
    show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)


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

# runs all other code
def Main(): # ledMartrix variables
    CheckForRecipie()
    MotherBrewGet()
    BoilTempGet()
    
    #getting times n duration
    global startTime 
    startTime = datetime.datetime.now()
    print("Fermenting start time: " + str(startTime))
    
    #2nd ferment or normal ferment
    SecondFerment()
    global fermentDuration

    if (str(secondFerment) == 'Kräusening'):
        print("Kräusening selected.")
        print("Sent to conditioning tank.")
        print("Fermenting for 3 days.")
        for i in range (0, 4):
            LEDMatrix(cascaded, block_orientation, rotate, msg)
        BuzzerDone(buzzerPin)
        fermentDuration = '3 days'
        print("Sent to bottle.")

    elif (str(secondFerment) == 'Bottle'):
        print("Bottle selected.")
        print("Fermenting for 2 weeks.")
        for i in range(0, 11):
            LEDMatrix(cascaded, block_orientation, rotate, msg)
        BuzzerDone(buzzerPin)
        fermentDuration = '2 weeks'
        print("Sent to bottle.")

    elif (str(secondFerment) == 'Cask_Condistioning'):
        print("Cask Conditioning selected.")
        print("Putting into cask.")
        print("Fermenting for 5 days.")
        for i in range(0, 6):
            LEDMatrix(cascaded, block_orientation, rotate, msg)
        BuzzerDone(buzzerPin)
        fermentDuration = '5 days'
        print("Sent to bottle.")

    elif (str(secondFerment) == 'Lagering'):
        print("Laggering selected.")
        print("Storing at celler temperature.")
        print("Fermenting for 3 months.")
        for i in range (0, 31):
            LEDMatrix(cascaded, block_orientation, rotate, msg)
        BuzzerDone(buzzerPin)
        fermentDuration = '3 months'
        print("Sent to bottle.")

    elif (str(secondFerment) == 'Secondary'):
        print("Secondary Fermentation selected.")
        print("Fermenting for 2 weeks.")
        for i in range(0, 11):
            LEDMatrix(cascaded, block_orientation, rotate, msg)
        BuzzerDone(buzzerPin)
        fermentDuration = '2 weeks'
        print("Sent to bottle.")

    elif (str(secondFerment) == 'Barrel_Agein'):
        print("Barrel Aging Selected.")
        print("Sent to barrel to sour.")
        print("Fermenting for 1 month.")
        for i in range(0, 23):
            LEDMatrix(cascaded, block_orientation, rotate, msg)
        BuzzerDone(buzzerPin)
        fermentDuration = '1 month'
        print("Sent to bottle.")

    else:
        print("Fermenting.")
        for i in range (0, 11):
            LEDMatrix(cascaded, block_orientation, rotate, msg)
        BuzzerDone(buzzerPin)
        fermentDuration = '2 weeks'
        print("Sent to bottle.")

    #end time
    global endTime
    endTime = datetime.datetime.now()
    print("Fermenting start time: " + str(endTime))

    #checks a cleaning
    PostCRUD()

    print("Ferment Completed.")
    CheckForRecipie()
    
# run all the stuff
Main()
