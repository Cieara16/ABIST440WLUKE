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
    
class Mashing(object):
	def __init__(self, ratio, tempoftarget, weightofgrain, tempofgrain, timeofboil, sizeofbatch, lossoftrub, lossoftun):

		self.ratio = ratio
		self.tempoftarget = tempoftarget
		self.weightofgrain = weightofgrain
		self.tempofgrain = tempofgrain
		self.timeofboil = timeofboil
		self.sizeofbatch = sizeofbatch
		self.lossoftrub = lossoftrub
		self.lossoftun = lossoftun
		
    def strikeTemp(self):
		#This is calculating the strike water temperature#
		return round(((.2/(float(self.ratio))*(float(self.tempoftarget) - float(self.tempofgrain)) +float(self.tempoftarget))),2)

    def strikeVol(self):
		#This is calculating the water volume#
		return round(((self.ratio * self.weightofgrain)/4), 2)

    def volofsparge(self):
#This procedure calculates the volume of water that is needed in order to start sparging phase#
		return  self.totalofwater() - self.volstrike()
	
	def totalofwater(self):
#This procedure calculates the amount of water needed for the brewing procedure along with the losses during this phase#
		return round((self._preboilvol() + self.lossoftun + self._absorption()),2)
		
	def absorption(self):
                        #This procedure calculates the amount of water lost during absorption process# 
		return (self.weightofgrain *.15)

    def lossofmashtun(self):
		#Procedure used to calculate the amount of water that was lost in the mash tun due to transferring to the boil kettle#                                
		return (((self.volofstrike() - (self._absorption()) - self.lossoftun)))
	
	def rateofevap(self):
		#Procedure to calculate the amount of water that was lost to evaporation in the boil phase#
		rateofevap = .10 #The rate of evaporation per hour
		return round(1-(rateofevap*(self.timeofboil/60)), 2)
		
	def lossofshrink(self):
		#Procedure to calculate the amount of water lost due to cooling of the wort.
		# 4 percent is the standard shrink factor.
		return 1 - .04

	def volofpreboil(self):
		#Procedure to calculate the amount of water needed during pre boil#
		return round((((self.sizeofbatch + self.lossoftrub)/self._lossofshrink())/self._rateofevap()),2)
	
if __name__ == "__main__":
	sizeofbatch = 5    #Gallons
	ratio = 1.25     #Quarts
	tempofmash = 152   #Fahrenheit
	weightofgrain = 11 #Pounds
	tempofgrain = 70   #Fahrenheit
	timeofboil = 60    #Minutes
	#This process depends on the system
	#Gallons:
	lossoftrub= 0     
	lossoftun= 0      

	mash = Mashing(weightofgrain, timeofboil, tempofmash, ratio, sizeofbatch, lossoftrub, tempofgrain, lossoftun) 
#{0} Fahrenheit - Temperature of Strike Water#
	print(mash.strikeTemp())

#{0} Gallons - Volume of Strike Water#
	print(mash.strikeVol())

#{0} Gallons - Volume of Sparge Water#
	print(mash.spargeVol())

#{0} Gallons - Amount of Water Needed#
	print(mash.totalWaterNeeded())

#{0} Gallons - Mash process absorbed by grain#
	print(mash._absorption())

#{0} Gallons - First outcomes #
	print(mash._mashlossoftun())

#{0} Gallons -Amount during Pre Boil #
	print(mash._preboilamount())

#{0} Gallons - Amount lost after evaporation during {1} minute boil#
	print(mash._preboillamount()-(mash._preboilamount()*mash._rateofevap()),mash.timeofboil)

#{0} Gallons -Amount that was lost to shrinking after reducing wort temperature.#
	print(mash._preboilamount()*mash._rateofevap()-5)
    
    
def main():

main()
import GetFromMotherBrew
