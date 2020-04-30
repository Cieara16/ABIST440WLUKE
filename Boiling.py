# Justin Hill - Team boil
# Ryan Carey - Team Close

# import system libraries
import sys
import math
import time
import datetime
import requests
# import CrowPi stuff
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import Adafruit_DHT
from datetime import datetime, date
from Adafruit_LED_Backpack import SevenSegment
# import LED Matrix stuff
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

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
# Initialize the display. Must be called once before using the display.
segment.begin()

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
    global beerName, beerType, hops1, hops2, hops3, number, hops1Time, hops2Time, hops3Time, kegVol, kegQty, sysId, boilId, hopNumber
    data = response.json()
    print(data)
    beerName = response.json()['result'][0]['beer_name']
    beerType = response.json()['result'][0]['beer_type']
    hops1 = response.json()['result'][0]['boil_hops1']
    hops2 = response.json()['result'][0]['boil_hops2']
    hops3 = response.json()['result'][0]['boil_hops3']
    number = response.json()['result'][0]['number']
    boilId = response.json()['result'][0]['boil_id']
    hops1Time = response.json()['result'][0]['boil_hops_1_time']
    hops2Time = response.json()['result'][0]['boil_hops_2_time']
    hops3Time = response.json()['result'][0]['boil_hops_3_time']
    kegVol = response.json()['result'][0]['keg_volume']
    kegQty = response.json()['result'][0]['keg_quantity']
    sysId = response.json()['result'][0]['sys_id']
    print('Ticket Number: ' + number)
    print('Boil ID: ' + boilId)
    print('Beer Name: ' + beerName)
    print('Beer Type: ' + beerType)
    print('1st Hops: ' + hops1)
    print('2nd Hops: ' + hops2)
    print('3rd Hops: ' + hops3)
    print('Record ID: ' + sysId)
    time.sleep(1)
    hopNumber = 0
    if (hops1 is not None):
        hopNumber = 1
    if (hops2 is not None):
        hopNumber = 2
    if (hops3 is not None):
        hopNumber = 3
    print('No. of hops: ' + str(hopNumber))
    # return the local variables
    return beerName, beerType, hops1, hops2, hops3, number, hops1Time, hops2Time, hops3Time, kegVol, kegQty, sysId, boilId, hopNumber


# Function for retrieving BoilPi tasks from the LKBrewTasks table
def GetFromBrewTasks():
    # query rpi_to_executeSTARTSWITHBoilPi^active=true^assigned_to=b03e1893db2240506b4a9646db961931
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=rpi_to_execute%3DBoilPi%5Eassigned_to%3Db03e1893db2240506b4a9646db961931%5Estate%3D-5&sysparm_limit=1'
    # url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=active%3Dtrue%5Erpi_to_executeSTARTSWITHBoilPi%5Estate%3D-5&sysparm_limit=10'
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

    global task, shortDescTask, sysIdTask
    task = response.json()['result'][0]['number']
    shortDescTask = response.json()['result'][0]['short_description']
    sysIdTask = response.json()['result'][0]['sys_id']

    print()
    print(task + ': ' + shortDescTask)
    print()
    return task, shortDescTask, sysIdTask


def UpdateBrewTasks():
    global sysIdTask
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/' + str(sysIdTask)
    user = 'kasper440'
    pwd = 'kasper440'

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Do the HTTP request
    response = requests.patch(url, auth=(user, pwd), headers=headers, data="{\"state\":\"3\"}")

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    print(task + ': ' + shortDescTask + ': Updated to closed complete.')


# Function for posting data to Servicenow. Can be changed..
def Post():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_boil'
    user = 'kasper440'
    pwd = 'kasper440'
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"sys_id\":\"\",\"short_description\":\"Boiling\",\"current_temperature\":\"" + str(
                                 temperature) + "\",\"sys_updated_on\":\"\"}")
    if response.status_code != 200 and response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response)
        exit()
    data = response
    return data


# Posting the final temperature after cooling the wort to Servicenow
def PostFinalTemp():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_boil'
    user = 'kasper440'
    pwd = 'kasper440'
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"sys_id\":\"\",\"short_description\":\"Boiling\",\"current_temperature\":\"" + str(
                                 temperature) + "\",\"sys_updated_on\":\"\"}")
    if response.status_code != 200 and response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response)
        exit()
    data = response
    return data


def displayBalrog(cascaded, block_orientation, rotate):
    # create matrix device
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded=cascaded or 1, block_orientation=block_orientation, rotate=rotate or 0)
    # debugging purpose
    print("[-] Matrix initialized")
    msg = "Boil Phase"
    show_message(device, msg, fill="blue", font=proportional(CP437_FONT), scroll_delay=0.1)


# Function for adding water to the brew chamber
def AddWater():
    global sysIdTask
    GetFromBrewTasks()  # Mash Liqued added
    time.sleep(10)
    UpdateBrewTasks()  # Mash Liquid Added - Closed Complete
    time.sleep(10)
    GetFromBrewTasks()  # Volume of water selected - Closed Complete
    print('Keg Volume: ' + kegVol)
    print('Keg Quantity: ' + kegQty)
    global hopAmount
    hopAmount = 0

    if (int(kegVol) == 5):
        hopAmount = int(kegQty) * 7 * hopNumber
    if (int(kegVol) == 15):
        hopAmount = int(kegQty) * 21 * hopNumber

    final = int(kegVol) * int(kegQty)
    print('Amount of water: ' + str(final) + ' gal.')
    UpdateBrewTasks()  # Volume of water selected - Closed Complete
    time.sleep(10)
    GetFromBrewTasks()  # Water Added to brew chamber
    print('Grams of Hops: ' + str(hopAmount))
    print('Adding water to brew chamber...')
    time.sleep(10)
    print('Water added to brew chamber.')
    #     UpdateBrewTasks() #Water Added to brew chamber - Closed Complete
    #     time.sleep(10)

    return hopAmount


# Function for onboard segment clock to display current time
def Clock():
    segment = SevenSegment.SevenSegment(address=0x70)
    # Continually update the time on a 4 char, 7-segment display
    try:
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
    GetFromBrewTasks()  # Set Default Boil Time
    time.sleep(10)
    UpdateBrewTasks()  # Set Default Boil Time - Closed Complete
    time.sleep(10)
    print('Making Beer: ' + beerName)
    print()
    timeloop = True
    count = -1

    GetFromBrewTasks()  # water and mash are boiled
    time.sleep(10)
    UpdateBrewTasks()  # water and mash are boiled - Closed Complete
    time.sleep(10)

    GetFromBrewTasks()  # Amount of hops1 selected
    time.sleep(10)
    UpdateBrewTasks()  # amount of hops 1 - Closed Complete
    time.sleep(10)

    GetFromBrewTasks()  # Check hops1 amount
    time.sleep(10)
    UpdateBrewTasks()  # check hops1 amount - Closed Complete
    time.sleep(10)

    GetFromBrewTasks()  # select hops1 boil time
    time.sleep(10)
    UpdateBrewTasks()  # select hops1 boil time - Closed Complete
    time.sleep(10)

    GetFromBrewTasks()  # check hop 1 boil time
    time.sleep(10)
    UpdateBrewTasks()  # check hop 1 boil time - Closed Complete
    time.sleep(10)

    while (timeloop and count < 60):
        try:
            # Turn backlight on
            lcd.set_backlight(0)
            if humidity is not None and temperature is not None:
                lcd.message('Temp={0:0.1f}*\nHumidity={1:0.1f}%\n'.format(temperature, humidity))
                count += 1
                time.sleep(1)
                print(count)
                if (hops1Time is None):
                    exit()
                else:
                    if (count == int(hops1Time)):
                        print('Adding ' + str(hopAmount) + 'g of ' + hops1 + ' hops.')
                        GetFromBrewTasks()  # hops 1 boiled
                        time.sleep(10)
                        UpdateBrewTasks()  # hops 1 boiled - Closed Complete
                        time.sleep(10)
                    if (hops2 is not None and count == int(hops2Time)):
                        print('Adding ' + str(hopAmount) + 'g of ' + hops2 + ' hops.')
                        GetFromBrewTasks()  # hops 2 boiled
                        time.sleep(10)
                        UpdateBrewTasks()  # hops 2 boiled - Closed Complete
                        time.sleep(10)
                    if (hops3 is not None and count == int(hops3Time)):
                        print('Adding ' + str(hopAmount) + 'g of ' + hops3 + ' hops.')
                        GetFromBrewTasks()  # hops 3 boiled
                        time.sleep(10)
                        UpdateBrewTasks()  # hops 3 boiled - Closed Complete
                        time.sleep(10)
            else:
                lcd.message('Failed to get reading. Try again!')

        except KeyboardInterrupt:
            # Turn the screen off
            lcd.clear()
            lcd.set_backlight(1)

    time.sleep(10)
    Post()


# Function to transfer wort to heat exchanger
def WortDrained():
    print()
    GetFromBrewTasks()  # Solids separated
    time.sleep(10)
    UpdateBrewTasks()  # solid separated - Closed Complete
    time.sleep(10)
    GetFromBrewTasks()  # wort drained
    time.sleep(10)
    UpdateBrewTasks()  # wort drained - Closed Complete
    print('Transferring wort to heat exchanger...')
    time.sleep(10)
    print('Wort has been transferred.')
    print()
    time.sleep(1)


# Function for cooling the wort so the fermenting team can take over
def WortCooled():
    global temperature
    print('Cooling Wort....')
    time.sleep(20)
    print('Wort has been cooled to ' + str(temperature) + ' degrees.')
    if (temperature >= 79):
        print('Wort still too hot... decreasing temperature')
    while (temperature > 79):
        temperature -= 5
        print(temperature)
        time.sleep(0.5)
    print()
    print('Wort has been cooled to ' + str(temperature) + ' degrees.')
    GetFromBrewTasks()  # wort cooled
    time.sleep(10)
    UpdateBrewTasks()  # wort cooled- Closed Complete
    print('Sending data to Servicenow...')
    time.sleep(5)
    print('Data sent.')
    PostFinalTemp()


# Function for quality check
def QualityCheck():
    print('Beginning Quality Check')
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
    print()


# Class for Stepmotor
class Stepmotor:

    def __init__(self):
        # set GPIO mode
        GPIO.setmode(GPIO.BCM)
        # These are the pins which will be used on the Raspberry Pi
        self.pin_A = 5
        self.pin_B = 6
        self.pin_C = 13
        self.pin_D = 19
        self.interval = 0.001

        # Declare pins as output
        GPIO.setup(self.pin_A, GPIO.OUT)
        GPIO.setup(self.pin_B, GPIO.OUT)
        GPIO.setup(self.pin_C, GPIO.OUT)
        GPIO.setup(self.pin_D, GPIO.OUT)
        GPIO.output(self.pin_A, False)
        GPIO.output(self.pin_B, False)
        GPIO.output(self.pin_C, False)
        GPIO.output(self.pin_D, False)

    def Step1(self):
        GPIO.output(self.pin_D, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)

    def Step2(self):
        GPIO.output(self.pin_D, True)
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)
        GPIO.output(self.pin_C, False)

    def Step3(self):
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_C, False)

    def Step4(self):
        GPIO.output(self.pin_B, True)
        GPIO.output(self.pin_C, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_B, False)
        GPIO.output(self.pin_C, False)

    def Step5(self):
        GPIO.output(self.pin_B, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_B, False)

    def Step6(self):
        GPIO.output(self.pin_A, True)
        GPIO.output(self.pin_B, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_A, False)
        GPIO.output(self.pin_B, False)

    def Step7(self):
        GPIO.output(self.pin_A, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_A, False)

    def Step8(self):
        GPIO.output(self.pin_D, True)
        GPIO.output(self.pin_A, True)
        time.sleep(self.interval)
        GPIO.output(self.pin_D, False)
        GPIO.output(self.pin_A, False)

    def turn(self, count):
        for i in range(int(count)):
            self.Step1()
            self.Step2()
            self.Step3()
            self.Step4()
            self.Step5()
            self.Step6()
            self.Step7()
            self.Step8()

    def close(self):
        GPIO.cleanup()

    def turnSteps(self, count):
        for i in range(count):
            self.turn(1)

    def turnDegrees(self, count):
        self.turn(round(count * 512 / 360, 0))

    def turnDistance(self, dist, rad):
        self.turn(round(512 * dist / (2 * math.pi * rad), 0))


# Servo Motor Class
class sg90:

    def __init__(self, direction):
        self.pin = 25
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.direction = int(direction)
        self.servo = GPIO.PWM(self.pin, 50)
        self.servo.start(0.0)

    def cleanup(self):
        self.servo.ChangeDutyCycle(self._henkan(0))
        time.sleep(0.3)
        self.servo.stop()
        GPIO.cleanup()

    def currentdirection(self):
        return self.direction

    def _henkan(self, value):
        return 0.05 * value + 7.0

    def setdirection(self, direction, speed):
        for d in range(self.direction, direction, int(speed)):
            self.servo.ChangeDutyCycle(self._henkan(d))
            self.direction = d
            time.sleep(0.1)
        self.servo.ChangeDutyCycle(self._henkan(direction))
        self.direction = direction


def ResetClean():
    print('Begining Reset/Cleaning Process')
    print()
    time.sleep(10)
    print("Stepmotor: moving started")
    motor = Stepmotor()
    motor.turnSteps(20)
    time.sleep(0.5)
    motor.turnSteps(20)
    time.sleep(0.5)
    motor.turnDegrees(720)
    print("Stepmotor: moving stopped")
    motor.close()
    print('Beginning Cleaning...')
    s = sg90(0)
    try:
        print("Servo: Turn left..")
        s.setdirection(100, 10)
        print("Servo: Turn right..")
        s.setdirection(-100, -10)
        print("Servo: Turn left..")
        s.setdirection(100, 10)
        print("Servo: Turn right..")
        s.setdirection(-100, -10)
        print("Servo: Turn left..")
        s.setdirection(100, 10)
        print("Servo: Turn right..")
        s.setdirection(-100, -10)
        time.sleep(2)
    except KeyboardInterrupt:
        s.cleanup()
    print('Cleaning complete.')


# Function for posting final data to the Log Table in Servicenow
def PostToLogTable():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table'
    user = 'kasper440'
    pwd = 'kasper440'
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"boiling_temperature\":\"" + str(temperature) + "\",\"boil_start_time\":\"" + str(
                                 start) + "\",\"boil_end_time\":\"" + str(end) + "\",\"boil_duration\":\"" + str(
                                 duration) + "\",\"number\":\"" + str(number) + "\",\"boil_id\":\"" + str(
                                 boilId) + "\",\"boil_quality_check\":\"true\",\"boil_reset_clean\":\"true\",\"boil_hops_1_name\":\"" + str(
                                 hops1) + "\",\"boil_hops_1_amount\":\"" + str(
                                 hopAmount) + "\",\"boil_hops_2_name\":\"" + str(
                                 hops2) + "\",\"boil_hops_2_amount\":\"" + str(
                                 hopAmount) + "\",\"boil_hops_3_name\":\"" + str(
                                 hops3) + "\",\"boil_hops_3_amount\":\"" + str(hopAmount) + "\"}")
    # response = requests.post(url, auth=(user, pwd), headers=headers ,data="{\"boiling_temperature\":\""+str(temperature)+"\",\"boil_start_time\":\""+str(start)+"\",\"boil_end_time\":\""+str(end)+"\",\"boil_duration\":\""+str(duration)+"\",\"number\":\""+str(number)+"\",\"boil_id\":\""+str(boilId)+"\",\"boil_quality_check\":\"Complete\",\"boil_reset_clean\":\"Complete\",\"boil_errors\":\"N/A\"}")
    if response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()
    data = response.json()
    print('Data posted to Log Table')


def main():
    global start, end, duration
    print('Beginning the Boiling Process')
    Clock()
    displayBalrog(cascaded=1, block_orientation=90, rotate=0)
    start = datetime.now()
    print(start)
    time.sleep(1)
    GetFromMotherbrew()
    readTemperature(temperature, humidity)
    AddWater()
    tempDisplay()
    WortDrained()
    WortCooled()
    QualityCheck()
    ResetClean()
    print("done")
    Clock()
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
# import GetFromMotherBrew

