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
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

# Buzzer 1 
# Goes off to indicated the start of the Preparation process

buzzer_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Make buzzer sound
GPIO.output(buzzer_pin, GPIO.HIGH)
time.sleep(1)
# Stop buzzer sound
GPIO.output(buzzer_pin, GPIO.LOW)
# define touch pin
touch_pin = 17
# set GPIO pin to INPUT
GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

motion_pin = 23
# set GPIO as GPIO.BOARD
GPIO.setmode(GPIO.BCM)
# set pin mode as INPUT
GPIO.setup(motion_pin, GPIO.IN)


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

def displayBalrog(cascaded=1, block_orientation=90, rotate=0):
    
    # create matrix device
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded=cascaded or 1, block_orientation=block_orientation, rotate=rotate or 0)
    # debugging purpose
    #print("[-] Matrix initialized")
    print("Order confirmed.")
    
    # print hello world on the matrix display
    msg = "Balrog Brewery"
    # debugging purpose
    print("[-] Printing: %s" % msg)
    show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)
    print("Brew task confirmed")
    
btn = 0
if btn == 0:
    displayBalrog()
    
# to get active prep task from service now to excute on crow pi
def Get_BrewTask_for_CrowPi():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=active%3Dtrue%5Erpi_to_executeSTARTSWITHPrepPi%5Estate%3D-5&sysparm_limit=10'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'Amp6826'
    pwd = 'Swami101'

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    global Task1, shortDescTask1, Task2, shortDescTask2, Task3, shortDescTask3, Task4, shortDescTask4, Task5, shortDescTask5, Task6, shortDescTask6, Task7, shortDescTask7, Task8, shortDescTask8
    Task1 = response.json()['result'][0]['number']
    shortDescTask1 = response.json()['result'][0]['short_description']
    Task2 = response.json()['result'][1]['number']
    shortDescTask2 = response.json()['result'][1]['short_description']
    Task3 = response.json()['result'][2]['number']
    shortDescTask3 = response.json()['result'][2]['short_description']
    Task4 = response.json()['result'][3]['number']
    shortDescTask4 = response.json()['result'][3]['short_description']
    Task5 = response.json()['result'][4]['number']
    shortDescTask5 = response.json()['result'][4]['short_description']
    Task6 = response.json()['result'][5]['number']
    shortDescTask6 = response.json()['result'][5]['short_description']
    Task7 = response.json()['result'][6]['number']
    shortDescTask7 = response.json()['result'][6]['short_description']
    Task8 = response.json()['result'][7]['number']
    shortDescTask8 = response.json()['result'][7]['short_description']
    
    print(Task1 + " :" + shortDescTask1)
    time.sleep(1)
    print(Task2 + " :" + shortDescTask2)
    time.sleep(1)
    print(Task3 + " :" + shortDescTask3)
    time.sleep(1)
    print(Task4 + " :" + shortDescTask4)
    time.sleep(1)
    print(Task5 + " :" + shortDescTask5)
    time.sleep(1)
    print(Task6 + " :" + shortDescTask6)
    time.sleep(1)
    print(Task7 + " :" + shortDescTask7)
    time.sleep(1)
    print(Task8 + " :" + shortDescTask8)
    time.sleep(1)
    return Task1, shortDescTask1, Task2, shortDescTask2, Task3, shortDescTask3, Task4, shortDescTask4, Task5, shortDescTask5, Task6, shortDescTask6, Task7, shortDescTask7, Task8, shortDescTask8

btn = 0
if btn == 0:
    Get_BrewTask_for_CrowPi()

    
def Create_Prices():
    print('receipt code will go here')
    

def GetFromMotherbrew():   
    #recieve order from user

    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/3adbbe8e1bc81010befe0d88cc4bcbcf'
    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'jbk5490'
    pwd = 'Limewild1234'
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    # Do the HTTP request
    response = requests.patch(url, auth=(user, pwd), headers=headers ,data="{\"state\":\"0\"}")
    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
#welcome the user
        
# Task 1 - Confirm Brew Task
    #print(data)
    '''\------------------------------------------------------------------------------------------------------------\''''
    #process payment

    #update process payment to closed complete
def CC1(test=4):
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/49d399fe1b409010befe0d88cc4bcb41'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'jbk5490'
    pwd = 'Limewild1234'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.patch(url, auth=(user, pwd), headers=headers ,data="{\"state\":\"0\"}")

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()

CC = 4
if CC == 4:
    CC1()

    #print(data)
    ''''\----------------------------------------------------------------------------------------------------------\''''
#recieve receipt

#update recieve receipt to closed complete
def CC2(test=4):
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/0dd399fe1b409010befe0d88cc4bcb43'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'jbk5490'
    pwd = 'Limewild1234'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.patch(url, auth=(user, pwd), headers=headers ,data="{\"state\":\"0\"}")

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()

Cl2 = 4
if Cl2 == 4:
    CC2()
#print(data)

#CONFIRM ORDER FROM MOTHERBREW TABLE

#update confirm order to closed complete
url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/19c659721b809010befe0d88cc4bcbf3'

# Eg. User name="admin", Password="admin" for this code sample.
user = 'jbk5490'
pwd = 'Limewild1234'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
response = requests.patch(url, auth=(user, pwd), headers=headers ,data="{\"state\":\"3\"}")

# Check for HTTP codes other than 200
if response.status_code != 200: 
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()

# Decode the JSON response into a dictionary and use the data
data = response.json()
#print(data)


#confirm brew tasks

#update confirm brew tasks to closed complete

#post crud to post prep log in log table
def Post_logtable():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_fields=preperation_quality_check%2Cprep_time_start%2Cprep_time_end%2Cpreperation_rest_clean%2Csys_id'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'Amp6826'
    pwd = 'Swami101'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers, data="{\"sys_id\":\"\",\"preperation_quality_check\":\""'''+bool(qualitycheck)+'''"\",\"prep_time_start\":\""+str(start1)+"\",\"prep_time_end\":\"" +str(
                                 end1)+"\",\"preperation_rest_clean\":\"\"}" )

    # Check for HTTP codes other than 200
    if response.status_code != 200 and response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response
    #print(data)

# TASK 1 - Test equipment
# Stepper motor 1

import math
class Stepmotor:

    def __init__(self):

        # set GPIO mode
        GPIO.setmode(GPIO.BCM)
        # These are the pins which will be used on the Raspberry Pi
        self.pin_A = 5
        self.pin_B = 6
        self.pin_C = 13
        self.pin_D = 19
        self.interval = 0.010

        # Declare pins as output
        GPIO.setup(self.pin_A,GPIO.OUT)
        GPIO.setup(self.pin_B,GPIO.OUT)
        GPIO.setup(self.pin_C,GPIO.OUT)
        GPIO.setup(self.pin_D,GPIO.OUT)
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

    def turn(self,count):
        for i in range (int(count)):
            self.Step1()
            self.Step2()
            self.Step3()
            self.Step4()
            self.Step5()
            self.Step6()
            self.Step7()
            self.Step8()

    def close(self):
        # cleanup the GPIO pin use
        GPIO.cleanup()

    def turnSteps(self, count):
        # Turn n steps
        # (supply with number of steps to turn)
        for i in range (count):
            self.turn(1)

    def turnDegrees(self, count):
        # Turn n degrees (small values can lead to inaccuracy)
        # (supply with degrees to turn)
        self.turn(round(count*512/360,0))

    def turnDistance(self, dist, rad):
        # Turn for translation of wheels or coil (inaccuracies involved e.g. due to thickness of rope)
        # (supply with distance to move and radius in same metric)
        self.turn(round(512*dist/(2*math.pi*rad),0))

#Testing all equipment
    
def main(test=0):
    lcd.set_backlight(0)
    lcd.message('Testing all')
    time.sleep(3.0)
    lcd.clear()
    lcd.message('Equipment')
    time.sleep(3.0)
    lcd.clear()
    print("moving started")
    lcd.message('Testing mill')
    motor = Stepmotor()
    print("One Step")
    motor.turnSteps(1)
    time.sleep(0.5)
    print("20 Steps")
    motor.turnSteps(20)
    time.sleep(0.5)
    print("quarter turn")
    motor.turnDegrees(90)
    print("moving stopped")
    lcd.clear()
    motor.close()


for n in range(-1,1):
    if n == 0:
        start = time.time()
        val = main(n)
        duration = time.time() - start
        durationInString = str(duration)
        "{:<2}".format(durationInString)
        print(durationInString)
        lcd.set_backlight(0)
        lcd.message("Seconds: ")
        lcd.message(durationInString)
        time.sleep(5.0)
        lcd.clear()
        print(f'calc for n={n} took {duration:.2f}s')
        break
        main()
        break
    

#update test equipment to closed complete
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/d1c699721b809010befe0d88cc4bcb66'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'jbk5490'
    pwd = 'Limewild1234'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.patch(url, auth=(user, pwd), headers=headers ,data="{\"state\":\"3\"}")

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)

    
global grain, grain_weight

def get_ingredients():
        #Need to install requests package for python
        #easy_install requests

        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=active%3Dtrue%5EnumberISNOTEMPTY%5EORDERBYDESCsys_created_on&sysparm_limit=10'
        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'Amp6826'
        pwd = 'Swami101'

        # Set proper headers
        headers = {"Content-Type":"application/json","Accept":"application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers )

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        global grain, grain_weight
        grain = response.json()['result'][0]['grain']
        grain_weight = response.json()['result'][0]['grain_weight']
        print('Grain: ' + grain)
        print('Grain weight: ' + grain_weight)
        return grain, grain_weight
    
# Gather the grains
btn = 1
if btn == 1:
    try:
        # Turn backlight on
        lcd.clear()
        lcd.set_backlight(0)
        lcd.message('Bob has gathered')
        time.sleep(2.0)
        # Demo showing the cursor.
        lcd.clear()
        lcd.show_cursor(True)
        lcd.message('the grains.')
        time.sleep(2.0)
        lcd.clear()
        lcd.blink(True)
        lcd.message('Moving to next')
        time.sleep(2.0)
        lcd.clear()
        lcd.blink(True)
        lcd.message('task.')
        time.sleep(1.0)
        lcd.clear()
        lcd.message('Measure ')
        time.sleep(2.0)
        lcd.clear()
        lcd.blink(True)
        lcd.message('Grains weight..')
        time.sleep(1.0)
        lcd.clear()
        lcd.set_backlight(1)

    except KeyboardInterrupt:
        # Turn the screen off
        lcd.clear()
        lcd.set_backlight(1)

#update gather the grains to closed complete
url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/55c699721b809010befe0d88cc4bcb67'

# Eg. User name="admin", Password="admin" for this code sample.
user = 'jbk5490'
pwd = 'Limewild1234'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
response = requests.patch(url, auth=(user, pwd), headers=headers ,data="{\"state\":\"3\"}")

# Check for HTTP codes other than 200
if response.status_code != 200: 
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()

# Decode the JSON response into a dictionary and use the data
data = response.json()
print(data)

# Measure the grains weight
# Sensor
def main4(test=4):
    # (GET) the grains and weight
    # Set the request parameters     
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_ingredients?sysparm_query=grain_weightISNOTEMPTY&sysparm_limit=1'
    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'Amp6826'
    pwd = 'Swami101'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers )

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    #grain = response.json()['result'][0]['grain']
    grain_weight = response.json()['result'][0]['grain_weight']
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    lcd.set_backlight(0)
    lcd.message('Use Scale')
    try:
        while True:
            # check if touch detected
            if(GPIO.input(touch_pin)):
                print('Weight measured')
                lcd.clear()
                lcd.message('Weight measured')
                print((grain_weight) + ' lbs.')
                lcd.clear()
                lcd.message((grain_weight) + ' lbs.')
                time.sleep(3)
                lcd.clear()
                lcd.set_backlight(1)
                time.sleep(1.0)
    except KeyboardInterrupt:
        # CTRL+C detected, cleaning and quitting the script
        GPIO.cleanup()

for n in range(-1,1):
    if n == 0:
        start = time.time()
        val = main4(n)
        duration = time.time() - start
        durationInString = str(duration)
        "{:<2}".format(durationInString)
        print(durationInString)
        lcd.set_backlight(0)
        lcd.clear()
        lcd.message("Seconds: ")
        lcd.message(durationInString)
        time.sleep(5.0)
        lcd.clear()
        print(f'calc for n={n} took {duration:.2f}s')
        break
        main()
        break

# Mill the grains
# LCD display message
def main():
    lcd.set_backlight(0)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Next task...')
    print('Next task...')
    time.sleep(2.0)
    
if __name__ == "__main__":
    main()

# Motor mills the grains
def main3(test=4):
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Milling grains...')
    print('Milling grains...')
    time.sleep(2.0)
    print('Motor is on.')
    print("Grain 1 in")
    time.sleep(0.5)
    motor = Stepmotor()
    print("Grain 2 in")
    time.sleep(0.5)
    motor.turnSteps(1)
    time.sleep(0.5)
    print("Grain 3 in")
    motor.turnSteps(20)
    time.sleep(0.5)
    lcd.message("Mill is running...")
    print("Mill is running...")
    motor.turnDegrees(360)
    lcd.clear()
    lcd.set_backlight(1)
    motor.close()
    time.sleep(0.5)
    print("Grains mill stopped")

for n in range(-1,1):
    n = 0
    start = time.time()
    val = main3(n)
    duration = time.time() - start
    durationInString = str(duration)
    "{:<2}".format(durationInString)
    print(durationInString)
    lcd.set_backlight(0)
    lcd.message("Seconds: ")
    lcd.message(durationInString)
    time.sleep(5.0)
    lcd.clear()
    print(f'calc for n={n} took {duration:.2f}s')
    break
    main3()
    break
    
#update run the mill to closed complete
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/d5c699721b809010befe0d88cc4bcb68'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'jbk5490'
    pwd = 'Limewild1234'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.patch(url, auth=(user, pwd), headers=headers ,data="{\"state\":\"3\"}")

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)

#transfer grains to mash

#update transfer grains to mash to closed complete
url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/59c699721b809010befe0d88cc4bcb69'

# Eg. User name="admin", Password="admin" for this code sample.
user = 'jbk5490'
pwd = 'Limewild1234'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
response = requests.patch(url, auth=(user, pwd), headers=headers ,data="{\"state\":\"3\"}")

# Check for HTTP codes other than 200
if response.status_code != 200: 
    print('Status:', res)

# Last task - TRansfer grains to mash tun

# define motion pin
motion_pin = 23
# set GPIO as GPIO.BOARD
GPIO.setmode(GPIO.BCM)
# set pin mode as INPUT
GPIO.setup(motion_pin, GPIO.IN)
def Transfer_Grains(test=4):
    lcd.set_backlight(0)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Transferring')
    time.sleep(3)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Grains')
    time.sleep(3)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('To Mashtun')
    time.sleep(3)
    lcd.clear()
    print('Transferring grains')
    time.sleep(5)
    try:
        if True:
            if(GPIO.input(motion_pin) == 0):
                time.sleep(10)
                print("Grains not found")
            elif(GPIO.input(motion_pin) == 1):
                lcd.clear()
                lcd.show_cursor(True)
                lcd.message('Grains moved')
                time.sleep(3)
                lcd.clear()
                print("Grains moved")
    except KeyboardInterrupt:
         GPIO.cleanup()

btn = 4
if btn == 4:
    Transfer_Grains()


# Clean Up Task
# Servo 

#calculate process duration of prep
def TimeDuration():
    global start1, end1
    start1 = datetime.now()
    #QualityCheck()
    #Task2
    #Task3
    end1 = datetime.now()
    elapsed1 = (end1 - start1).seconds
    print(elapsed1)
    return start1, end1

def main7():
    #get_ingredients()
    #Get_Task_for_CrowPi()
    TimeDuration()
    #QualityCheck()
    Post_logtable()
    print('Log table is updated.')
    time.sleep(3)
    print("Prepare for cleaning task..")

main7()



#Servo   
class sg90:

  def __init__( self, direction):

    self.pin = 25
    GPIO.setmode( GPIO.BCM )
    GPIO.setup( self.pin, GPIO.OUT )
    self.direction = int( direction )
    self.servo = GPIO.PWM( self.pin, 50 )
    self.servo.start(0.0)

  def cleanup( self ):

    self.servo.ChangeDutyCycle(self._henkan(0))
    time.sleep(0.3)
    self.servo.stop()
    GPIO.cleanup()

  def currentdirection( self ):

    return self.direction

  def _henkan( self, value ):

    return 0.05 * value + 7.0

  def setdirection( self, direction, speed ):

    for d in range( self.direction, direction, int(speed) ):
      self.servo.ChangeDutyCycle( self._henkan( d ) )
      self.direction = d
      time.sleep(0.1)
    self.servo.ChangeDutyCycle( self._henkan( direction ) )
    self.direction = direction

def main2(test=4):

    s = sg90(0)

    try:
        if True:
            lcd.set_backlight(0)
            lcd.clear()
            lcd.show_cursor(True)
            lcd.message('Start cleaning')
            time.sleep(2.0)
            lcd.clear()
            lcd.message('Sanitizing...')
            time.sleep(2.0)
            print("Swipe left")
            s.setdirection( 100, 100 )
            time.sleep(0.5)
            print("Swipe right")
            s.setdirection( -100, -100 )
            lcd.clear()
            time.sleep(3.0)
            lcd.set_backlight(1)
            
    except KeyboardInterrupt:
        s.cleanup()
            
for n in range(-1,1):
    n = 0
    start = time.time()
    val = main2(n)
    duration = time.time() - start
    durationInString = str(duration)
    "{:<2}".format(durationInString)
    print(durationInString)
    lcd.set_backlight(0)
    lcd.message("Seconds: ")
    lcd.message(durationInString)
    time.sleep(5.0)
    lcd.clear()
    print(f'calc for n={n} took {duration:.2f}s')
    break
    main2()
    break
    

# LCD display message
def main5():
    lcd.set_backlight(0)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Done.')
    print('Done.')
    time.sleep(2.0)
#     lcd.set_backlight(3)
#     lcd.clear()
    
btn = 3
if btn == 3:
    main5()

def done():
    buzzer_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

# Make buzzer sound
GPIO.output(buzzer_pin, GPIO.HIGH)
time.sleep(1)
# Stop buzzer sound
GPIO.output(buzzer_pin, GPIO.LOW)
# define touch pin
touch_pin = 17
# set GPIO pin to INPUT
GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

btn = 5
if btn == 5:
    done()

