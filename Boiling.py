# Justin Hill - Team boil
import sys
import Adafruit_DHT
import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import requests

# dh11 sensor
sensor = 11
pin = 4
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

global temperature
global humidity

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

# Comment the line below to convert the temperature to Celcius.
temperature = temperature * 9 / 5.0 + 32
# added the line to get closer to designated temperature rather than room temperature
temperature *= 2


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
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_limit=1'
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
    beerName = response.json()['result'][0]['beer_name']
    beerType = response.json()['result'][0]['beer_type']
    print('Beer Name: ' + beerName)
    print('Beer Type: ' + beerType)
    # return the local variables
    return beerName, beerType


# retrieving BoilPi tasks from the LKBrewTasks table
def GetFromBrewTasks():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=active%3Dtrue%5Erpi_to_executeSTARTSWITHBoilPi%5Estate%3D-5&sysparm_limit=1'
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
    taskNumber = response.json()['result'][0]['number']
    shortDescr = response.json()['result'][0]['short_description']
    data = response.json()['result']  # [0]['what do you want to get']
    print('Task Number: ' + taskNumber)
    print('Task: ' + shortDescr)
    time.sleep(1)
    # print(data)

    return taskNumber, shortDescr


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
    print('Hops: ' + hops)
    # print(data)

    return hops


def Post():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_boil'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'kasper440'
    pwd = 'kasper440'

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"sys_id\":\"\",\"short_description\":\"Boiling\",\"current_temperature\":\"" + str(
                                 temperature) + "\",\"sys_updated_on\":\"\"}")

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response
    print(data)


def systemCheck():
    # used to check system functionality before continuing
    # if all is good, then pass
    # if there are problems, then throw error
    pass


def tempDisplay():
    print()
    print('Boiling water...')
    timeloop = True
    count = 0

    while (temperature < 150 and timeloop and count < 30):
        try:
            # Turn backlight on
            lcd.set_backlight(0)
            if humidity is not None and temperature is not None:
                lcd.message('Temp={0:0.1f}*\nHumidity={1:0.1f}%\n'.format(temperature, humidity))
                # Post()
                count += 1
                time.sleep(1)
                print(count)
                if (count == 15):
                    print('Adding Hops')
            else:
                lcd.message('Failed to get reading. Try again!')
        except KeyboardInterrupt:
            # Turn the screen off
            lcd.clear()
            lcd.set_backlight(1)

    while (temperature >= 150 and timeloop and count < 30):
        try:

            if humidity is not None and temperature is not None:
                lcd.message('Very Hot!')
                lcd.message('Temp.={0:0.1f}Hum={0:01f}'.format(temperature, humidity))
                # Post()
                count += 1
                time.sleep(1)
                print(count)
                if (count == 15):
                    print('Adding Hops')
            else:
                lcd.message('Failed to get reading. Try again!')
        except KeyboardInterrupt:
            # Turn the screen off
            lcd.clear()
            lcd.set_backlight(1)


def WortCooled():
    global temperature
    print('Cooling Wort....')
    temperature -= 40
    time.sleep(5)
    print('Wort has been cooled to ' + str(temperature) + ' degrees.')


def WortDrained():
    print('Transferring wort to heat exchanger...')
    time.sleep(10)
    print('Wort has been transferred.')


def main():
    #     processDuration = 0
    #     processDuration += 1
    print('Boil Process Beginning')
    time.sleep(1)
    GetFromMotherbrew()
    GetFromBrewTasks()
    GetFromIngredients()
    systemCheck()
    readTemperature(temperature, humidity)
    tempDisplay()
    #     Post()
    WortCooled()
    WortDrained()
    #     Quality Check()
    #     ResetClean()
    #     print(processDuration)
    print("done")


main()
