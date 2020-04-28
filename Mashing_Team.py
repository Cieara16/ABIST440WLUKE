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

global temperatureCelsius, humidity, start, end, duration

humidity, temperatureCelsius = Adafruit_DHT.read_retry(sensor, pin)

lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

temperatureFarenheit = temperatureCelsius * 9 / 5.0 + 32

temperatureCelsius *= 2

def readTemp(sensor, pin):
    return temperature, humidity
    time.sleep(1)
    
def _init_(self, temperature, humidity):
    self.humidity = humidity
    self.temperature = temperature

def GetFromMotherbrew():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=active%3Dtrue%5EnumberISNOTEMPTY%5EORDERBYDESCsys_created_on&sysparm_limit=1'
    user = 'kasper440'
    pwd = 'kasper440'
    
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    
    response = requests.get(url, auth=(user, pwd), headers=headers)
    
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()
    
    global heatHlt, grainVol, ambientTemp, strikeVol, strikeTemp, waterVol, mashInWater, strikeWater
    heatHlt = response.json()['result'][0]['heat_hlt']
    grainVol = response.json() ['result'] [0] ['grain_volume']
    ambientTemp = response.json() ['result'][0]['ambient_temperature']
    strikeVol = response.json() ['result'] [0] ['strike_volume']
    strikeTemp = response.json() ['result'] [0] ['strike_temperature']
    waterVol = response.json() ['result'] [0] ['water_volume']
    mashInWater = response.json() ['result'] [0] ['mash_in_water']
    strikeWater = response.json() ['result'] [0] ['strike_water']
    print('Heat HLT: ' + heatHLT)
    print('Grain Volume: ' + grainVol)
    print('Ambient Temperature: '+ ambientTemp)
    print('Strike Volume: ' + strikeVol)
    print('Strike Temperature: ' + strikeTemp)
    print('Water Volume: ' + waterVol)
    print('Mash In Water: ' + mashInWater)
    print('Strike Water: ' + strikeWater)
    time.sleep(1)
    
    return heatHLT, grainVol, ambientTemp, strikeVol, strikeTemp, waterVol, mashInWater, strikeWater
    
def GetFromBrewTasks():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=rpi_to_execute%3DMashPi%5Estate%3D-5%5Eactive%3Dtrue&sysparm_limit=10' 
    user = 'kasper440'
    pwd = 'kasper440'
    
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    
    response = requests.get(url, auth=(user, pwd), headers=headers)
    
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()
    
    #global
  
def Post():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mash'
    user = 'kasper440'
    pwd = 'kasper440'
    
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"sys_id\":\"\",\"short_description\":\"Mashing\",\"current_temperature\":\""+ str(
                                 temperature) + "\",\"sys_updated_on\":\"\"}")
    
    if response.status_code != 200 and response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response)
        exit()
        
    data = response
    
    return data

def systemCheck():
    pass

def Clock():
    segment.begin()
    
    try:
        while(True):
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            second = now.second
            segment.clear()
            
            segment.set_digit(0, int(hour / 10))
            segment.set_digit(1, hour %10)
            
            segment.set_digit(2, int(minute / 10))
            segment.set_digit(3, minute % 10)
            
            segment.set_colon(second % 2)
            
            segment.write_display()
            
            time.sleep(0.25)
    except KeyboardInterrupt:
        segment.clear()
        segment.write_display()
        
def ResetClean():
    motor = '  '
    
def PostToLogTable():
    
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table'
    user = 'kasper440'
    pwd = 'kasper440'
    headers = {"Content-Type": "application/json", "accept": "application/json"}
    
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"mashing_temperature\":\"" + str(temperature) + "\",\"mash_start_time\":\"" + str(
                                 start) + "\",\"mash_end_time\":\"" + str(end) + "\",\"mash_duration\":\"" + str(
                                 duration) + "\",\"mash_quality_check\":\"True\",\"mash_reset_clean\":\"\",\"mash_errors\":\"\",\"number\":\"" + str(
                                 number) + "\"}")
    
    if response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()
        
    data = response.json()
    print(data)
    tables
    
def main():
    global start, end, duration
    print('Begin Mashing Process')
    
    start = datetime.now()
    print(start)
    time.sleep(1)
    GetFromMotherbrew()
    GetFromBrewTasks
    systemCheck()
    
    print("Complete")
    end = datetime.now()
    print('End time: ' + end)
    duration = end - start
    print('Processs Duration: ' + duration)
    PostToLogTable()
    
main()
import GetFromMotherBrew
