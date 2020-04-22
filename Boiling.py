# Justin Hill - Team boil
# Ryan Carey - Team Close
import sys
import Adafruit_DHT
import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import requests
from datetime import datetime, date
from Adafruit_LED_Backpack import SevenSegment

# dh11 sensor
sensor = 11
pin = 4
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2
# Define Buzzer pin
buzzerPin = 18
# Define Segment Address
segment = SevenSegment.SevenSegment(address=0x70)

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


# identifying sensor and pin and returning the temp and humidity
def readTemperature(sensor, pin):
    return temperature, humidity
    time.sleep(1)


# function to initialize local variables
def __init__(self, temperature, humidity):
    self.humidity = humidity
    self.temperature = temperature


# retrieving most recent record from Mother Brew table and all necessary items from that record to run the program
def GetFromMotherbrew():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=active%3Dtrue%5EnumberISNOTEMPTY%5EORDERBYDESCsys_created_on&sysparm_limit=1'
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

    # Decode the JSON response into a dictionary and use the data as local variables
    global beerName, beerType, hops1, hops2, hops3, number, hops1Time, hops2Time, hops3Time, waterWeight, sysId
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
    sysId = response.json()['result'][0]['sys_id']
    print('Ticket Number: ' + number)
    print('Beer Name: ' + beerName)
    print('Beer Type: ' + beerType)
    print('1st Hops: ' + hops1)
    print('2nd Hops: ' + hops2)
    print('3rd Hops: ' + hops3)
    print('Record ID: ' + sysId)
    time.sleep(1)
    # return the local variables
    return beerName, beerType, hops1, hops2, hops3, number, hops1Time, hops2Time, hops3Time, waterWeight, sysId


# Function for retrieving BoilPi tasks from the LKBrewTasks table
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

    # Decode the JSON response into a dictionary and use the data as local variables
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


# Function for GET request from ingredients table
def GetFromIngredients():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_ingredients?sysparm_limit=1'
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
    # Decode the JSON response into a dictionary and use the data as local variables
    data = response.json()
    hops = response.json()['result'][0]['hops']
    # print('Hops: ' + hops)
    # print(data)
    return hops


# Function for posting data to Servicenow. Can be changed..
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


# Posting the final temperature after cooling the wort to Servicenow
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


# used to check system functionality before continuing
# if all is good, then pass
# if there are problems, then throw error
def systemCheck():
    pass


# Function for adding water to the brew chamber
# Amount of water requested by customer in Servicenow
def AddWater():
    print('Amount of water: ' + waterWeight + 'gal.')
    print('Adding water to brew chamber...')
    time.sleep(15)
    print('Water added to brew chamber.')
    time.sleep(1)


# Function for onboard segment clock to display current time
def Clock():
    segment.begin()
    # Continually update the time on a 4 char, 7-segment display
    try:
        while (True):
            now = datetime.now()
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
    except KeyboardInterrupt:
        segment.clear()
        segment.write_display()


# Reading temperature and humidity from the dh11 sensor and displaying it
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
                if (count == int(hops1Time)):
                    print('Beginning Task: ' + addHopsTask2)
                    print('Adding ' + hops1 + ' hops.')
                if (count == int(hops2Time)):
                    print('Adding ' + hops2 + ' hops.')
                if (count == int(hops3Time)):
                    print('Adding ' + hops3 + ' hops.')

            else:
                lcd.message('Failed to get reading. Try again!')

        except KeyboardInterrupt:
            # Turn the screen off
            lcd.clear()
            lcd.set_backlight(1)

    print(boilWaterTask1 + ' Boiling process complete')
    print()
    time.sleep(5)
    Post()


# Function for cooling the wort so the fermenting team can take over
def WortCooled():
    global temperature
    print('Cooling Wort....')
    temperature -= 40
    time.sleep(20)
    print('Wort has been cooled to ' + str(temperature) + ' degrees.')
    if (temperature >= 79):
        print('Wort still too hot... decreasing temperature')
        temperature -= 30
        time.sleep(20)
    print()
    print('Wort has been cooled to ' + str(temperature) + ' degrees.')
    print('Sending data to Servicenow...')
    time.sleep(10)
    print('Data sent.')
    PostFinalTemp()


# Function to transfer wort to heat exchanger
def WortDrained():
    print()
    print('Beginning ' + drainWortTask3)
    print('Transferring wort to heat exchanger...')
    time.sleep(10)
    print('Wort has been transferred.')
    print(drainWortTask3 + ' Complete.')
    print()
    time.sleep(1)


# Function for quality check
def QualityCheck():
    print('Beginning Quality Check')
    print('Beginning ' + checkTempTask4)
    print('Checking temperature...')
    time.sleep(20)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzerPin, GPIO.OUT)
    # Make buzzer sound
    GPIO.output(buzzerPin, GPIO.HIGH)
    time.sleep(1)
    # Stop buzzer sound
    GPIO.output(buzzerPin, GPIO.LOW)
    GPIO.cleanup()
    print('Quality Check Complete')


def ResetClean():
    motor = ' '


#     motor = Stepmotor()
#     print('Beginning Quality Check')
#     motor.turnSteps(1)
#     print('One Step')
#     time.sleep(1)
#     motor.turnSteps(20)
#     print('20 steps')
#     print("quarter turn")
#     motor.turnDegrees(90)
#     print("moving stopped")
#     motor.close()

# Function for posting final data to the Log Table in Servicenow
def PostToLogTable():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table'
    user = 'kasper440'
    pwd = 'kasper440'
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"boiling_temperature\":\"" + str(temperature) + "\",\"boil_start_time\":\"" + str(
                                 start) + "\",\"boil_end_time\":\"" + str(end) + "\",\"boil_duration\":\"" + str(
                                 duration) + "\",\"boil_quality_check\":\"True\",\"boil_reset_clean\":\"\",\"boil_errors\":\"\",\"number\":\"" + str(
                                 number) + "\"}")
    # Check for HTTP codes other than 200
    if response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()
    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)

def main():
    global start, end, duration
    print('Beginning the Boiling Process')
    # Clock()
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
    WortDrained()
    QualityCheck()
    # ResetClean()
    print("done")
    end = datetime.now()
    print('End time: ')
    print(end)
    duration = end - start
    print('Process Duration: ')
    print(duration)
    PostToLogTable()
    lcd.clear()
    segment.clear()


# Run the program
main()
import GetFromMotherBrew

