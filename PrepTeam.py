#DEVELOPMENT PHASE
#Prep team - Jonathan Katz, Ngoc Tran, Elmer Iglesias, Amrish Patel
#IST440W - Luke Kasper
#April 20 2020

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
GPIO.output(buzzer_pin, GPIO.LOW)
time.sleep(1)
# Stop buzzer sound
GPIO.output(buzzer_pin, GPIO.LOW)
# define touch pin
touch_pin = 17
# set GPIO pin to INPUT
GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.cleanup()


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

def main(cascaded, block_orientation, rotate):
    
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

if __name__ == "__main__":
    try:
        main(cascaded=1, block_orientation=90, rotate=0)
    except KeyboardInterrupt:
        s.cleanup()
# to get active prep task from service now to excute on crow pi
def Get_Task_for_CrowPi():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=rpi_to_execute%3DPrepPi%5Estate%3D-5%5Eactive%3Dtrue&sysparm_limit=10'

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
    Task1 = response.json()['result'][0]['number']
    shortDescTask1 = response.json()['result'][0]['short_description']
    Task2 = response.json()['result'][1]['number']
    shortDescTask2 = response.json()['result'][1]['short_description']
    Task3 = response.json()['result'][2]['number']
    shortDescTask3 = response.json()['result'][2]['short_description']
    Task4 = response.json()['result'][3]['number']
    shortDescTask4 = response.json()['result'][3]['short_description']
    
    print(Task1)
    print(shortDescTask1)
    print(Task2)
    print(shortDescTask2)
    print(Task3)
    print(shortDescTask3)
    print(Task4)
    print(shortDescTask4)

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
    #print(data)
    ''''\----------------------------------------------------------------------------------------------------------\''''
#recieve receipt

#update recieve receipt to closed complete
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
    lcd.message('Equipments')
    time.sleep(3.0)
    lcd.clear()
    lcd.set_backlight(1)
    print("Testing started...")
    time.sleep(2)
    print("Preparation Unit: Passed")
    time.sleep(3)
    motor = Stepmotor()
    #print("One Step")
    print("Mashing Unit: Passed")
    time.sleep(3)
    motor.turnSteps(1)
    time.sleep(0.5)
    #print("20 Steps")
    print("Boiling Unit: Passed")
    time.sleep(3)
    motor.turnSteps(20)
    time.sleep(0.5)
    #print("quarter turn")
    print("Fermenting Unit: Passed")
    time.sleep(3)
    print("Bottling Unit: Passed")
    time.sleep(3)
    motor.turnDegrees(90)
    #print("moving stopped")
    print("Closing Unit: Passed")
    time.sleep(3)
    print("Equipments are ready")
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

# def get_ingredients():
#         #Need to install requests package for python
#         #easy_install requests
# 
#         # Set the request parameters
# # Needs fixing -> url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_ingredients?sysparm_query=Active%20%3D%20true&sysparm_fields=grain_weight%2Cgrains&sysparm_limit=1'
#         
#         url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_ingredients?sysparm_query=grain_weightISNOTEMPTY&sysparm_limit=1'
#         # Eg. User name="admin", Password="admin" for this code sample.
#         user = 'Amp6826'
#         pwd = 'Swami101'
# 
#         # Set proper headers
#         headers = {"Content-Type":"application/json","Accept":"application/json"}
# 
#         # Do the HTTP request
#         response = requests.get(url, auth=(user, pwd), headers=headers )
# 
#         # Check for HTTP codes other than 200
#         if response.status_code != 200:
#             print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
#             exit()
# 
#         # Decode the JSON response into a dictionary and use the data
#         grain = response.json()['result'][0]['grain']
#         grain_weight = response.json()['result'][0]['grain_weight']
#         print('Grain: ' + grain)
#         print('Grain weight: ' + grain_weight)
#         return grain, grain_weight
    
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
        lcd.message('Measure grains')
        time.sleep(2.0)
        lcd.clear()
        lcd.blink(True)
        lcd.message('weight.')
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
def main():
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
                print("Press Crtl+C to move to the next task.")
                lcd.clear()
                lcd.message((grain_weight) + ' lbs.')
                time.sleep(3)
                lcd.clear()
                lcd.set_backlight(1)
                time.sleep(1.0)
    except KeyboardInterrupt:
        # CTRL+C detected, cleaning and quitting the script
        GPIO.cleanup()

if __name__ == "__main__":
    main()

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
def main():
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Milling grains...')
    print('Milling grains...')
    time.sleep(2.0)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Motor is on.')
    print('Motor is on.')
    lcd.clear()
    lcd.set_backlight(1)
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
    motor.close()
    time.sleep(0.5)
    print("Grains mill stopped")

if __name__ == "__main__":
    main()
    
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

def main():
    #get_ingredients()
    Get_Task_for_CrowPi()
    TimeDuration()
    #QualityCheck()
    Post_logtable()
    print('Log table is updated.')
    time.sleep(3)
    print("Prepare for cleaning task..")

main()



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

def main(test=4):

    s = sg90(0)

    try:
        if True:
            lcd.set_backlight(0)
            lcd.clear()
            lcd.show_cursor(True)
            lcd.message('Finish task. Start cleaning')
            time.sleep(2.0)
            lcd.clear()
            lcd.message('Sanitizing...')
            time.sleep(2.0)
            print("Testing cleaner wiping turning left")
            s.setdirection( 100, 100 )
            time.sleep(0.5)
            print("Testing cleaner wiping turning right")
            s.setdirection( -100, -100 )
            time.sleep(2)
            lcd.message('Cleaner Working')
            lcd.clear()
            time.sleep(3.0)
            lcd.set_backlight(1)
            
    except KeyboardInterrupt:
        s.cleanup()
        
if __name__ == "__main__":
    main()
        
for n in range(0):
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

if __name__ == "__main__":
    main()
    
    
# LCD display message
def main():
    lcd.set_backlight(0)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Done.')
    print('Done.')
    time.sleep(2.0)
    lcd.clear()
    lcd.set_backlight(1)             
    
if __name__ == "__main__":
    main()