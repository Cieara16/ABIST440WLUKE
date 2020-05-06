#Prep team - Jonathan Katz, Ngoc Tran, Elmer Iglesias, Amrish Patel
#Mostly complete - still adding minor things
#IST440W - Luke Kasper

import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import time
import sys
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

# Buzzer 1
# represents the start of the milling process

#this is where the original code starts

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

#welcome the user
def main(cascaded, block_orientation, rotate):
    
    # create matrix device
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded=cascaded or 1, block_orientation=block_orientation, rotate=rotate or 0)
    # debugging purpose
    print("[-] Matrix initialized")

    # print hello world on the matrix display
    msg = "Balrog Brewery"
    # debugging purpose
    print("[-] Printing: %s" % msg)
    show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)


if __name__ == "__main__":
    
    # cascaded = Number of cascaded MAX7219 LED matrices, default=1
    # block_orientation = choices 0, 90, -90, Corrects block orientation when wired vertically, default=0
    # rotate = choices 0, 1, 2, 3, Rotate display 0=0°, 1=90°, 2=180°, 3=270°, default=0
   
    try:
        main(cascaded=1, block_orientation=90, rotate=0)
    except KeyboardInterrupt:
        s.cleanup()

#recieve order from user

#update recieve order state to closed complete
#Need to install requests package for python
#easy_install requests

# Set the request parameters
url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/3adbbe8e1bc81010befe0d88cc4bcbcf'

# Eg. User name="admin", Password="admin" for this code sample.
user = 'jbk5490'
pwd = ''

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
print(data)

#process payment

#update process payment to closed complete
url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/49d399fe1b409010befe0d88cc4bcb41'

# Eg. User name="admin", Password="admin" for this code sample.
user = 'jbk5490'
pwd = ''

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
print(data)

#recieve receipt

#update recieve receipt to closed complete
url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/0dd399fe1b409010befe0d88cc4bcb43'

# Eg. User name="admin", Password="admin" for this code sample.
user = 'jbk5490'
pwd = ''

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
print(data)

#confirm order

#update confirm order to closed complete
url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/19c659721b809010befe0d88cc4bcbf3'

# Eg. User name="admin", Password="admin" for this code sample.
user = 'jbk5490'
pwd = ''

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

#confirm brew tasks

#update confirm brew tasks to closed complete


#test equipment
# Step motor
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
    lcd.set_backlight(1)
    print("moving started")
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
            lcd.message('Testing cleaner')
            time.sleep(2.0)
            lcd.clear()
            print("Testing cleaner wiping turning left")
            s.setdirection( 100, 100 )
            time.sleep(0.5)
            print("Testing cleaner wiping turning right")
            s.setdirection( -100, -100 )
            time.sleep(0.5)
            lcd.message('Cleaner Working')
            lcd.clear()
            time.sleep(3.0)
            lcd.set_backlight(1)
    except KeyboardInterrupt:
        s.cleanup()
        
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

#update test equipment to closed complete
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/d1c699721b809010befe0d88cc4bcb66'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'jbk5490'
    pwd = ''

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

#gather the grains
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
        lcd.set_backlight(1)

    except KeyboardInterrupt:
        # Turn the screen off
        lcd.clear()
        lcd.set_backlight(1)

#update gather the grains to closed complete
url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/55c699721b809010befe0d88cc4bcb67'

# Eg. User name="admin", Password="admin" for this code sample.
user = 'jbk5490'
pwd = ''

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

def main():
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
                time.sleep(2.0)
                lcd.clear()
                lcd.set_backlight(1)
                time.sleep(1.0)
    except KeyboardInterrupt:
        # CTRL+C detected, cleaning and quitting the script
        GPIO.cleanup()

if __name__ == "__main__":
    main()

def main():
    lcd.set_backlight(0)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('check')
    time.sleep(2.0)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('next task.')
    time.sleep(2.0)
    
if __name__ == "__main__":
    main()

#run the mill
def main():
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Milling. Step')
    time.sleep(2.0)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Motor is on.')
    lcd.clear()
    lcd.set_backlight(1)
    print("moving started")
    motor = Stepmotor()
    print("One Step")
    motor.turnSteps(1)
    time.sleep(0.5)
    print("20 Steps")
    motor.turnSteps(20)
    time.sleep(0.5)
    print("360 turn")
    motor.turnDegrees(360)
    print("moving stopped")
    motor.close()

if __name__ == "__main__":
    main()
#update run the mill to closed complete
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/d5c699721b809010befe0d88cc4bcb68'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'jbk5490'
    pwd = ''

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
pwd = ''

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

def main():
    lcd.set_backlight(0)
    lcd.clear()
    lcd.message('Phase now')
    time.sleep(2.0)
    lcd.clear()
    lcd.message('Set to')
    time.sleep(2.0)
    lcd.clear()
    lcd.message('Mashing')
    time.sleep(10.0)
    lcd.clear()
    lcd.set_backlight(1)

if __name__ == "__main__":
    main()

#set brew state to mash
