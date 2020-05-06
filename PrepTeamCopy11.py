#DEVELOPMENT PHASE
#Prep team - Jonathan Katz, Ngoc Tran, Elmer Iglesias, Amrish Patel
#IST440W - Luke Kasper
#April 20 2020
#Pair programming - Justin Hill

import RPi.GPIO as GPIO
import Adafruit_DHT
import Adafruit_CharLCD as LCD
import datetime
import time
from datetime import datetime, date
import subprocess
import sys
import requests

# LED Matrix
# Represent machine status
# Import all the modules 
import re
import requests
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

def Loop():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=sys_created_onRELATIVEGT%40minute%40ago%401&sysparm_limit=1'
    user = 'ndt7'
    pwd = 'Tui@920Tyson!'
    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    result = response.json()['result']
    emptyList = []

    while (result == emptyList):
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=sys_created_onRELATIVEGT%40minute%40ago%401&sysparm_limit=1'
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
        result = response.json()['result']
        emptyList = []
        print(result)
        time.sleep(25)
        if (result != emptyList):
        #import Your Main Program name here.
        #import latest file
            import PrepTeamX
            #import PrepTeamX6
            

Loop()
    