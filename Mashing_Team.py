import sys
import Adafruit_DHT
import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import requests
from datetime import datetime, date
from Adafruit_LED_Backpack import SevenSegment

sensor = 11
pin = 4

lcd_columns = 16
lcd_rows = 2

buzzerPin = 18

segment = SevenSegment.SevenSegment(address=0x70)

global temperature, humidity, start, end, duration

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

temperature = temperature * 9 / 5.0 + 32

temperature *= 2


def readTemp(sensor, pin):
    return temperature, humidity
    time.sleep(1)


def _init_(self, temperature, humidity):
    self.humidity = humidity
    self.temperature = temperature


def GetFromMotherBrew():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=active%3Dtrue%5EnumberISNOTEMPTY%5EORDERBYDESCsys_created_on&sysparm_limit=1';
    user = 'kasper440'
    pwd = 'kasper440'

    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    response = requests.get(url, auth=(user, pwd), headers=headers)

    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()


def GetFromBrewTasks():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=active%3Dtrue%5Erpi_to_executeSTARTSWITHMashPi%5Estate%3D-5&sysparm_limit=10';
    user = 'kasper440'
    pwd = 'kasper440'

    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    response = requests.get(url, auth=(user, pwd), headers=headers)

    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()


def Post():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mash';
    user = 'kasper440'
    pwd = 'kasper440'

    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"sys_id\":\"\",\"short_description\":\"Mashing\",\"current_temperature\":\"" + str(
                                 temperature) + "\",\"sys_updated_on\":\"\"}")

    if response.status_code != 200 and response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response)
        exit()

    data = response

    return data





def main():
    # while(get_from_any_table("https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=ORDERBYDESCnumber%5Erpi_to_execute%3DMashPi%5Estate%3D-5&sysparm_limit=1";) != emptyList):
    main()
    import GetFromMotherBrew
