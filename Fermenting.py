# Team Ferment - James Bee, Virginia Hoffman, Michaela Fox, and Samantha Scheer
# IST 440 - Luke Kasper

#imports
import RPi.GPIO as GPIO
import datetime
import time
from datetime import datetime, date
import requests
import json
import Adafruit_DHT
import Adafruit_CharLCD as LCD
import os
import sys, subprocess
import math

# clock imports
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
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=abvISNOTEMPTY%2525abvISNOTEMPTY%255Eyeast_type_1ISNOTEMPTY%2525abvISNOTEMPTY%255Eyeast_type_1ISNOTEMPTY%255Eyeast_type_2ISNOTEMPTY%2525abvISNOTEMPTY%255Eyeast_type_1ISNOTEMPTY%255Eyeast_type_2ISNOTEMPTY%255Eyeast_type_3ISNOTEMPTY%2526abvISNOTEMPTY%255Eyeast_type_1ISNOTEMPTY%255Eyeast_type_2ISNOTEMPTY%255Eyeast_type_3ISNOTEMPTY%255Ebeer_typeANYTHING%2525abvISNOTEMPTY%255Eyeast_type_1ISNOTEMPTY%255Eyeast_type_2ISNOTEMPTY%255Eyeast_type_3ISNOTEMPTY%255Ebeer_typeANYTHING%255Esugar_levelsISNOTEMPTY%2525abvISNOTEMPTY%255Eyeast_type_1ISNOTEMPTY%255Eyeast_type_2ISNOTEMPTY%255Eyeast_type_3ISNOTEMPTY%255Ebeer_typeANYTHING%255Esugar_levelsISNOTEMPTY%255Esecondary_fermentationANYTHING%numberISNOTEMPTY%beer_nameISNOTEMPTY%sys_idISNOTEMPTY&sysparm_limit=1'
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
    global beerType, yeast1, yeast2, yeast3, ABVLevel, sugarAmount, secondFerment, number, beerName, sysID
    sysIDRecord = response.json()['result']
    sysID = sysIDRecord[0]['sys_id']
    
    numRecord = response.json()['result']
    number = numRecord[0]['number']
    
    beerNameRecord = response.json()['result']
    beerName = beerNameRecord[0]['beer_name']
    
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
    
    print("Record number: " + number)
    print("Beer name: " + beerName)
    print("Type of beer: " + beerType)
    print("Yeast type 1: " + yeast1)
    print("Yeast type 2: " + yeast2)
    print("Yeast type 3: " + yeast3)
    print("ABV Level: " + ABVLevel)
    print("Sugar Amount: " + sugarAmount)
    print("Secondary Fermentation: " + secondFerment)
    
    return beerType, yeast1, yeast2, yeast3, ABVLevel, sugarAmount, secondFerment, number, beerName

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

    print()
    # Decode the JSON response into a dictionary and use the data
    global boilTemp, startTemp
    boilTemp = response.json()['result'][0]['boiling_temperature']
    print("Incoming temperature is: ", boilTemp)

    temperature, humidity = Adafruit_DHT.read(tempSensor, tempPin)
    time.sleep(1)
    GPIO.cleanup()

    #no incming temp
    try:
        startTemp = float(boilTemp) * 9 / 5.0 + 32
        lcd.set_backlight(0)
        print("Checking temperature.")
        lcd.message("Incoming temp:\n" + str(boilTemp))  # pulled from mother brew
        time.sleep(3.0)
        lcd.clear()
        GPIO.cleanup()
            
    #incoming temp
    except ValueError:
        boilTemp = 35
        startTemp = boilTemp
        
    return boilTemp, startTemp

def TempCheck():
    #different temps for different beers
    startTemp = float(boilTemp) * 9 / 5.0 + 32
    #ale 
    if (beerType == 'Ale'):
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
                    startTemp += 2

                # temp too high
                elif (startTemp > 72):
                    lcd.set_backlight(0)
                    lcd.message("Temperature is\n" + "too high: " + str(startTemp) + " F")
                    time.sleep(3.0)
                    lcd.clear()
                    GPIO.cleanup()
                    startTemp -= 2

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
    
    elif(beerType == 'Stout'):
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
                    startTemp += 2

                # temp too high
                elif (startTemp > 75):
                    lcd.set_backlight(0)
                    lcd.message("Temperature is\n" + "too high: " + str(startTemp) + " F")
                    time.sleep(3.0)
                    lcd.clear()
                    GPIO.cleanup()
                    startTemp -= 2

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

    elif (beerType == 'Lager'):
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
                    startTemp += 2

                # temp too high
                elif (startTemp > 55):
                    lcd.set_backlight(0)
                    lcd.message("Temperature is\n" + "too high: " + str(startTemp) + " F")
                    time.sleep(3.0)
                    lcd.clear()
                    GPIO.cleanup()
                    startTemp -= 2

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

    elif (beerType == 'IPA'):
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
                    startTemp += 2

                # temp too high
                elif (startTemp > 70):
                    lcd.set_backlight(0)
                    lcd.message("Temperature is\n" + "too high: " + str(startTemp) + " F")
                    time.sleep(3.0)
                    lcd.clear()
                    GPIO.cleanup()
                    startTemp -= 2

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
            
    
    
    #function to ferment
def SecondFerment():
    global fermentDuration
    if (str(secondFerment) == 'Kräusening'):
        print("Kräusening selected.")
        print("Sent to conditioning tank.")
        print("Fermenting for 3 days:")
        for i in range (0, 4):
            LEDMatrix(cascaded, block_orientation, rotate, msg)
        BuzzerDone(buzzerPin)
        fermentDuration = '3'

    elif (str(secondFerment) == 'Bottle'):
        print("Bottle selected.")
        print("Fermenting for 2 weeks:")
        for i in range(0, 11):
            LEDMatrix(cascaded, block_orientation, rotate, msg)
        BuzzerDone(buzzerPin)
        fermentDuration = '2'

    elif (str(secondFerment) == 'Cask Condistioning'):
        print("Cask Conditioning selected.")
        print("Putting into cask.")
        print("Fermenting for 5 days:")
        for i in range(0, 6):
            LEDMatrix(cascaded, block_orientation, rotate, msg)
        BuzzerDone(buzzerPin)
        fermentDuration = '5'

    elif (str(secondFerment) == 'Lagering'):
        print("Laggering selected.")
        print("Storing at celler temperature.")
        print("Fermenting for 3 months:")
        for i in range (0, 31):
            LEDMatrix(cascaded, block_orientation, rotate, msg)
        BuzzerDone(buzzerPin)
        fermentDuration = '3'

    elif (str(secondFerment) == 'Secondary'):
        print("Secondary Fermentation selected.")
        print("Fermenting for 2 weeks:")
        for i in range(0, 11):
            LEDMatrix(cascaded, block_orientation, rotate, msg)
        BuzzerDone(buzzerPin)
        fermentDuration = '2'

    elif (str(secondFerment) == 'Barrel Aging'):
        print("Barrel Aging Selected.")
        print("Sent to barrel to sour.")
        print("Fermenting for 1 month:")
        for i in range(0, 23):
            LEDMatrix(cascaded, block_orientation, rotate, msg)
        BuzzerDone(buzzerPin)
        fermentDuration = '1'

    else:
        fermentDuration = '2'
        
    return fermentDuration

#function for POST
def PostCRUD():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table'
    #?sysparm_fields=ferment_end_time%2fermenting_start_time%2fermenting_duration%2ferment_temperature%2abv%2number%2fermenting_quality_check%2fermenting_reset/clean%2second_fermentation

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'kasper440'
    pwd = 'kasper440'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers ,data="{\"fermenting_start_time\":\""+str(startTime)+"\",\"fermenting_end_time\":\""+str(endTime)+"\",\"ferment_tempature\":\""+str(startTemp)+"\",\"fermenting_duration\":\""+str(fermentDuration)+"\",\"abv\":\""+str(ABVLevel)+"\",\"number\":\""+str(number)+"\",\"ferment_yeasts_1_name\":\"" + str(yeast1)+ "\",\"ferment_yeasts_2_name\":\"" + str(yeast2)+ "\",\"ferment_yeasts_3_name\":\"" + str(yeast3)+"\",\"fermenting_quality_check\":\"true\",\"fermenting_reset_clean\":\"true\",\"second_fermentation\":\"true\"}")

    # Check for HTTP codes other than 200
    if response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response)
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    #print(data)
    print("Posted to Log Table.")
    
#function to send to bottle
def SendToBottle():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/' + str(sysID)
    
    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'kasper440'
    pwd = 'kasper440'
    
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    
    response = requests.patch(url, auth=(user, pwd), headers=headers, data="{\"state\":\"3\"}")
    
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    print("Sent " + beerName + "("+number+")" + " to Bottle Team. State set to pending.")


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
    #print("%s" % msg)

    # print hello world on the matrix display
    msg = "."
    # debugging purpose
    #print("%s" % msg)
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
    TempCheck()
    print()
    
    #getting times n duration
    global startTime, endTime, fermentDuration, nextTeam
    now = datetime.now()
    print()
    
    #steps
    print("Being moved to vessel.")
    print("Vessel is cooled and airated.")
    print(yeast1 + " is being added.")
    print(yeast2 + " is being added.")
    print(yeast3 + " is being added.")
    print("Aperature is being tilted to 60 degrees.")
    print("Doing quality check:")
    print()
    
    startTime = now.strftime("%H:%M:%S")
    print("Fermenting start time: " + str(startTime))
    
    #2nd ferment or normal ferment
    print("Fermenting:")
    for i in range (0, 11):
        LEDMatrix(cascaded, block_orientation, rotate, msg)
    BuzzerDone(buzzerPin)
    fermentDuration = '2 weeks'
    
    #after fermenting
    print("Moved to conditioning tank.")
    print("Flushing out extra yeast.")
    print()
    print("Checking for a second type of fermentation:")
    
    SecondFerment()
    print("Fermenting compelte.")
    
    #end time
    now = datetime.now()
    endTime = now.strftime("%H:%M:%S")
    print("Fermenting end time: " + str(endTime))

    #checks a cleaning
    print("Cleaning and resetting:")
    print()
    
    #update log table
    print("Posting to log table: ")
    PostCRUD()
    
    #send to bottle
    print("Sending to bottle:")
    nextTeam = "BottlePi"
    SendToBottle()

    print("Ferment phase Completed.")
    CheckForRecipie()
    
# run all the stuff
Main()
