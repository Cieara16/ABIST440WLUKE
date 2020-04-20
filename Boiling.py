# Justin Hill - Team boil
# Ryan Carey - Team Close
import sys
import Adafruit_DHT
import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import requests
from datetime import datetime, date

# dh11 sensor
sensor = 11
pin = 4
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2
# Define Buzzer pin
buzzerPin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin, GPIO.OUT)

global temperature, humidity, start, end, duration

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

# Comment the line below to convert the temperature to Celcius.
temperature = temperature * 9 / 5.0 + 32
# added the line to get closer to designated temperature rather than room temperature
temperature *= 2

now = datetime.now()
currentTime = now.strftime("%H:%M:%S")


# identifying sensor and pin and returning the temp and humidity
def readTemperature(sensor, pin):
    return temperature, humidity
    time.sleep(1)


# function to initialize local variables
def __init__(self, temperature, humidity):
    self.humidity = humidity
    self.temperature = temperature


# retrieving most recent record from Mother Brew table
def GetFromMotherbrew():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=numberISNOTEMPTY%5Eactive%3Dtrue%5Ebrew_phase%3DBoil&sysparm_limit=1'
    user = 'kasper440'
    pwd = 'kasper440'
    # Servicenow Headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    # HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers)
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    global beerName, beerType, hops1, hops2, hops3, number, hops1Time, hops2Time, hops3Time, waterWeight
    beerName = response.json()['result'][0]['beer_name']
    beerType = response.json()['result'][0]['beer_type']
    hops1 = response.json()['result'][0]['boil_hops1']
    hops2 = response.json()['result'][0]['boil_hops2']
    hops3 = response.json()['result'][0]['boil_hops3']
    number = response.json()['result'][0]['number']
    hops1Time = response.json()['result'][0]['boil_hops_1_time']
    hops2Time = response.json()['result'][0]['boil_hops_2_time']
    hops3Time = response.json()['result'][0]['boil_hops_3_time']
    waterWeight = response.json()['result'][0]['water_by_weight']
    print('Ticket Number: ' + number)
    print('Beer Name: ' + beerName)
    print('Beer Type: ' + beerType)
    print('1st Hops: ' + hops1)
    print('2nd Hops: ' + hops2)
    print('3rd Hops: ' + hops3)
    time.sleep(1)
    # return the local variables
    return beerName, beerType, hops1, hops2, hops3, number, hops1Time, hops2Time, hops3Time, waterWeight


# retrieving BoilPi tasks from the LKBrewTasks table
def GetFromBrewTasks():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=active%3Dtrue%5Erpi_to_executeSTARTSWITHBoilPi%5Estate%3D-5&sysparm_limit=10'
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
    global boilWaterTask1, addHopsTask2, drainWortTask3, checkTempTask4
    boilWaterTask1 = response.json()['result'][0]['number']
    shortDescr1 = response.json()['result'][0]['short_description']
    addHopsTask2 = response.json()['result'][1]['number']
    shortDescr2 = response.json()['result'][1]['short_description']
    drainWortTask3 = response.json()['result'][2]['number']
    shortDescr3 = response.json()['result'][2]['short_description']
    checkTempTask4 = response.json()['result'][3]['number']
    shortDescr4 = response.json()['result'][3]['short_description']
    data = response.json()['result']  # [0]['what do you want to get']
    print('Task Number: ' + boilWaterTask1 + ' ' + shortDescr1)
    print('Task Number: ' + addHopsTask2 + ' ' + shortDescr2)
    print('Task Number: ' + drainWortTask3 + ' ' + shortDescr3)
    print('Task Number: ' + checkTempTask4 + ' ' + shortDescr4)
    time.sleep(1)

    return boilWaterTask1, shortDescr1, addHopsTask2, shortDescr2, drainWortTask3, shortDescr3, checkTempTask4, shortDescr4


def GetFromIngredients():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_ingredients?sysparm_limit=1'

    # Eg. User name="admin", Password="admin" for this code sample.
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
    data = response.json()
    hops = response.json()['result'][0]['hops']
    # print('Hops: ' + hops)
    # print(data)

    return hops


def Post():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_boil'
    user = 'kasper440'
    pwd = 'kasper440'
    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"sys_id\":\"\",\"short_description\":\"Boiling\",\"current_temperature\":\"" + str(
                                 temperature) + "\",\"sys_updated_on\":\"\"}")
    # Check for HTTP codes other than 200
    if response.status_code != 200 and response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response)
        exit()
    # Decode the JSON response into a dictionary and use the data
    data = response

    return data


def PostFinalTemp():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_boil'
    user = 'kasper440'
    pwd = 'kasper440'
    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"sys_id\":\"\",\"short_description\":\"Boiling\",\"current_temperature\":\"" + str(
                                 temperature) + "\",\"sys_updated_on\":\"\"}")
    # Check for HTTP codes other than 200
    if response.status_code != 200 and response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response)
        exit()
    # Decode the JSON response into a dictionary and use the data
    data = response
    return data


def systemCheck():
    # used to check system functionality before continuing
    # if all is good, then pass
    # if there are problems, then throw error
    pass


def AddWater():
    print('Amount of water: ' + waterWeight + 'gal.')
    print('Adding water to brew chamber...')
    time.sleep(15)
    print('Water added to brew chamber.')


def tempDisplay():
    print()
    print('Beginning Task: ' + boilWaterTask1)
    print('Making Beer: ' + beerName)
    print()
    timeloop = True
    count = 0

    while (timeloop and count < 60):
        try:
            # Turn backlight on
            lcd.set_backlight(0)
            if humidity is not None and temperature is not None:
                lcd.message('Temp={0:0.1f}*\nHumidity={1:0.1f}%\n'.format(temperature, humidity))
                count += 1
                time.sleep(1)
                print(count)
                if (count == hops1Time):
                    print('Beginning Task: ' + addHopsTask2)
                    print('Adding ' + hops1 + ' hops.')
                if (count == hops2Time):
                    print('Adding ' + hops2 + ' hops.')
                if (count == hops3Time):
                    print('Adding ' + hops3 + ' hops.')

            else:
                lcd.message('Failed to get reading. Try again!')
        except KeyboardInterrupt:
            # Turn the screen off
            lcd.clear()
            lcd.set_backlight(1)

    print(boilWaterTask1 + ' Boiling process complete')
    Post()


def WortCooled():
    global temperature
    print()
    print('Cooling Wort....')
    temperature -= 40
    time.sleep(10)
    if (temperature >= 79):
        print('Wort still too hot... decreasing temperature')
        temperature -= 30
        time.sleep(10)
    print()
    print('Wort has been cooled to ' + str(temperature) + ' degrees.')

    print('Sending data to Servicenow...')
    time.sleep(5)
    PostFinalTemp()


def WortDrained():
    print()
    print('Beginning Task: ' + drainWortTask3)
    print('Transferring wort to heat exchanger...')
    time.sleep(10)
    print('Wort has been transferred.')


def QualityCheck():
    GPIO.ouptut(buzzerPin, GPIO.LOW)
    time.sleep(1)
    print('Beginning Quality Check')


def PostToLogTable():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'admin'
    pwd = 'admin'

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"boiling_temperature\":\"" + str(temperature) + "\",\"boil_start_time\":\"" + str(
                                 start) + "\",\"boil_end_time\":\"" + str(end) + "\",\"boil_duration\":\"" + str(
                                 duration) + "\",\"boil_quality_check\":\"Complete\",\"boil_reset_clean\":\"\",\"boil_errors\":\"\"}")

    # Check for HTTP codes other than 200
    if response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)


def main():
    global start, end, duration
    #     processDuration = 0
    #     processDuration += 1
    print('Beginning the Boiling Process')
    start = datetime.now()
    print(start)
    time.sleep(1)
    GetFromMotherbrew()
    GetFromBrewTasks()
    GetFromIngredients()
    systemCheck()
    readTemperature(temperature, humidity)
    AddWater()
    tempDisplay()
    WortCooled()
    #     Quality Check()
    WortDrained()
    #     ResetClean()
    print("done")
    end = datetime.now()
    print('End time: ')
    print(end)
    duration = end - start
    print('Process Duration: ')
    print(duration)
    return start, end, duration
    PostToLogTable()
    import GetFromMotherBrew


main()


