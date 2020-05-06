#DEVELOPMENT PHASE
#Prep team - Jonathan Katz, Ngoc Tran, Elmer Iglesias, Amrish Patel
#IST440W - Luke Kasper
#April 20 2020

import RPi.GPIO as GPIO
import Adafruit_DHT
import Adafruit_CharLCD as LCD
import datetime
import time
import math
from datetime import datetime, date
import subprocess
import sys
import requests
import re
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

# Buzzer 1 
# Goes off to initialize the start of the Preparation process

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
time.sleep(3)

# LED Matrix
# Represent machine status
# Import all the modules 
start1 = datetime.now()
def displayBalrog(cascaded=1, block_orientation=90, rotate=0):
    
    # create matrix device
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded=cascaded or 1, block_orientation=block_orientation, rotate=rotate or 0)
    # debugging purpose
    #print("[-] Matrix initialized")
    
    # print hello world on the matrix display
    msg = "Balrog Brewery"
    print('Balrog Brewery')
    time.sleep(1)
    # debugging purpose
    show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)
    
displayBalrog()

    
# to get active prep task from service now to excute on crow pi
def Get_BrewTask_for_CrowPi():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=active%3Dtrue%5Erpi_to_executeSTARTSWITHPrepPi%5Estate%3D-5&sysparm_limit=10'
    #(reference)url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=rpi_to_execute%3DBoilPi%5Eassigned_to%3Db03e1893db2240506b4a9646db961931%5Estate%3D-5&sysparm_limit=1'
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
    
    print('\nBrew Tasks confirmed.')
    time.sleep(1)
    print(Task1 + ": " + shortDescTask1)
    time.sleep(1.5)
    print(Task6 + ": " + shortDescTask6)
    time.sleep(1.5)
    print(Task2 + ": " + shortDescTask2)
    time.sleep(1.5)
    print(Task4 + ": " + shortDescTask4)
    time.sleep(1.5)
    print(Task3 + ": " + shortDescTask3)
    time.sleep(1.5)
    print(Task7 + ": " + shortDescTask7)
    time.sleep(1.5)
    print(Task8 + ": " + shortDescTask8)
    time.sleep(1.5)
    print(Task5 + ": " + shortDescTask5)
    time.sleep(1.5)
    return Task1, shortDescTask1, Task2, shortDescTask2, Task3, shortDescTask3, Task4, shortDescTask4, Task5, shortDescTask5, Task6, shortDescTask6, Task7, shortDescTask7, Task8, shortDescTask8
    

btn = 0
if btn == 0:
    Get_BrewTask_for_CrowPi()    

# Get data from Mother Brew Table 
def Getmotherbrew_tbl():

    # Set the request parameters
    #(This work)url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=%5EORDERBYDESCsys_created_on%5Eactive%3Dtrue&sysparm_fields=number%2Cbeer_name%2Cbeer_type%2Corder_id%2Ccustomer_id%2Cgrain_type_1%2Cgrain_type_2%2Cgrain_type_3%2Cgrain_weight%2Cpayment_id%2Ckeg_quantity%2Ckeg_volume%2Ckeg_price%2Cgrain_price%2Csys_id&sysparm_limit=10'
    
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=%5EORDERBYDESCsys_created_on%5Eactive%3Dtrue&sysparm_fields=number%2Cbeer_name%2Cbeer_type%2Corder_id%2Ccustomer_id%2Cgrain_type_1%2Cgrain_type_2%2Cgrain_type_3%2Cgrain_weight%2Cmalt_type%2Cmalt_type_2%2Cmalt_type_3%2Cboil_hops_1_time%2Cboil_hops_2_time%2Cboil_hops_3_time%2Cyeast_type_1%2Cyeast_type_2%2Cyeast_type_3%2Cpayment_id%2Ckeg_quantity%2Ckeg_volume%2Ckeg_price%2Cgrain_price%2Cyeast_price%2Csys_id&sysparm_limit=10'
    
    #New one, show ID but doesn't pull the latest records
    #url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=active%3Dtrue%20and%20order%20by%20desc&sysparm_fields=number%2Cbeer_name%2Cbeer_type%2Corder_id%2Ccustomer_id%2Cgrain_type_1%2Cgrain_type_2%2Cgrain_type_3%2Cgrain_weight%2Cpayment_id%2Ckeg_quantity%2Ckeg_volume%2Cgrain_price%2Csys_id&sysparm_limit=10'
    
    #Amrish(latest record)  
    #url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=%5EORDERBYDESCsys_created_on%5Eactive%3Dtrue&sysparm_fields=number%2Cbeer_name%2Cbeer_type%2Cgrain_type_1%2Cgrain_type_2%2Cgrain_type_3%2Cgrain_weight%2Cgrain_price&sysparm_limit=1'
    
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
    global number, beername, beertype, Grainprice, Grainweight, GrainType1, GrainType2, GrainType3, customer_id, payment_id, order_id, keg_quantity, keg_volume, keg_price, malt_price, malt2, malt3, hops2, hops3, yeast2, yeast3  

    number = response.json()['result'][0]['number']
    order_id = response.json()['result'][0]['order_id']
    customer_id = response.json()['result'][0]['customer_id']
    payment_id = response.json()['result'][0]['payment_id']
    beername = response.json()['result'][0]['beer_name']
    beertype = response.json()['result'][0]['beer_type']
    
    Grainprice = response.json()['result'][0]['grain_price']
    Grainweight = response.json()['result'][0]['grain_weight']
    GrainType1 = response.json()['result'][0]['grain_type_1']
    GrainType2 = response.json()['result'][0]['grain_type_2']
    GrainType3 = response.json()['result'][0]['grain_type_3']
    
    keg_quantity = response.json()['result'][0]['keg_quantity']
    keg_volume = response.json()['result'][0]['keg_volume']
    keg_price = response.json()['result'][0]['keg_price']
    yeast_price = response.json()['result'][0]['yeast_price']
    
    malt2 = response.json()['result'][0]['malt_type_2']
    malt3 = response.json()['result'][0]['malt_type_3']
    hops2 = response.json()['result'][0]['boil_hops_2_time']
    hops3 = response.json()['result'][0]['boil_hops_3_time']
    yeast2 = response.json()['result'][0]['yeast_type_2']
    yeast3 = response.json()['result'][0]['yeast_type_3']
    
    return number, beername, beertype, Grainprice, Grainweight, GrainType1, GrainType2, GrainType3, customer_id, payment_id, order_id, keg_quantity, keg_volume, keg_price, yeast_price, malt2, malt3, hops2, hops3, yeast2, yeast3  

Getmotherbrew_tbl()

total_price = 0
def total():
    global total_price
    #total_price = (grains + malt + hops + yeast)*keg_volume * keg_quantity
    Grain_count = 1
    Grainprice = .15
    if GrainType2 != 'null' or GrainType2:
        Grain_count += 1
    if GrainType3 != 'null' or GrainType3:
        Grain_count += 1 
    Grainprice = Grain_count * .15
    
    Malt_count = 1
    Maltprice = .15
    if malt2 != 'null' or malt2:
        Malt_count += 1
    if malt3 != 'null' or malt3:
        Malt_count += 1 
    Maltprice = Malt_count * .15
    
    Hops_count = 1
    Hopsprice = .04
    if hops2 != 'null' or hops2:
        Hops_count += 1
    if hops3 != 'null' or hops3:
        Hops_count += 1 
    Hopsprice = Hops_count * .04
    
    Yeast_count = 1
    Yeastprice = 2
    if yeast2 != 'null' or yeast2:
        Yeast_count += 1
    if yeast3 != 'null' or yeast3:
        Yeast_count += 1 
    Yeastprice = Yeast_count * 2
    
    total_price = (Grainprice + Maltprice + Hopsprice + Yeastprice)*int(keg_quantity) * int(keg_volume) 
    
    print('\n')
    print('Grains price:$', round(Grainprice,2))
    time.sleep(.5)
    print('Malt price:$', round(Maltprice,2))
    time.sleep(.5)
    print('Hops price:$', round(Hopsprice,2))
    time.sleep(0.5)
    print('Yeast price:$', round(Yeastprice,2))
    time.sleep(1.5)
    print('Total price: $' + str(round(total_price, 2)))
    final_price = (f'$'+str(round(total_price, 2)))   

for n in range(-1,1):
    if n == 0:
    
        total()
        break
    
#update confirm brew tasks to closed complete

# TASK 2 - Test equipment
# Stepper motor 1
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

#TASK 3
#Testing all equipment    
def Test_Equipment(test=0):
    print('\n')
    print(Task6 + ": " + shortDescTask6)
    #time.sleep(3)
    lcd.set_backlight(0)
    lcd.message('Testing all')
    #time.sleep(4.0)
    lcd.clear()
    lcd.message('Equipment')
    #time.sleep(4.0)
    lcd.clear()
    print("Moving started")
    lcd.message('Testing')
    motor = Stepmotor()
    motor.turnSteps(1)
    #time.sleep(0.5)
    motor.turnSteps(20)
    time.sleep(0.5)
    print("Quarter turn")
    motor.turnDegrees(90)
    print("Moving stopped")
    lcd.clear()
    motor.close()


for n in range(-1,1):
    if n == 0:
        start = time.time()
        val = Test_Equipment(n)
        duration = time.time() - start
        durationInString = str(duration)
        "{:<2}".format(durationInString)
        lcd.set_backlight(0)
        lcd.message("Seconds: ")
        lcd.message(durationInString)
        time.sleep(6.0)
        lcd.clear()
        print(f'Testing equipment took {duration:.2f}s')
        break
        Test_Equipment()
        break

# TASK 4
# Gather the grains
print('\n')
print(Task2 + ": " + shortDescTask2)
time.sleep(2)
print('Brewmaster has gathered the grains.')
time.sleep(2)
print('Grain Type 1: ' + GrainType1)
time.sleep(2)
print('Grain Type 2: ' + GrainType2)
time.sleep(2)
print('Grain Type 3: ' + GrainType3)

btn = 1
if btn == 1:
    try:
        # Turn backlight on
        lcd.clear()
        lcd.set_backlight(0)
        lcd.message('Brewmaster')
        time.sleep(4.0)
        # Demo showing the cursor.
        lcd.clear()
        lcd.show_cursor(True)
        lcd.message('has gathered')
        time.sleep(4.0)
        # Demo showing the cursor.
        lcd.clear()
        lcd.show_cursor(True)
        lcd.message('the grains.')
        time.sleep(4.0)
        lcd.clear()
        lcd.blink(True)
        lcd.message('Moving to next')
        time.sleep(4.0)
        lcd.clear()
        lcd.blink(True)
        lcd.message('task.')
        time.sleep(2.0)
        lcd.clear()
        lcd.message('Measure ')
        time.sleep(3.0)
        lcd.clear()
        lcd.blink(True)
        lcd.message('Grains weight..')
        time.sleep(4)
        lcd.clear()
        lcd.set_backlight(1)

    except KeyboardInterrupt:
        # Turn the screen off
        lcd.clear()
        lcd.set_backlight(1)

 #update gather the grains to closed complete

# TASK 5
# Measure the grains weight
# Sensor
def measure_weight(test=4):
    print('\n')
    print(Task3 + ": " + shortDescTask3)
    time.sleep(1.5)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(touch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    lcd.set_backlight(0)
    lcd.message('Use Scale')
    print('Use the scale')
    try:
        while True:
            # check if touch detected
            if(GPIO.input(touch_pin)):
                print('Weight measured')
                lcd.clear()
                lcd.message('Weight measured')
                print(Grainweight + 'lbs.')
                lcd.clear()
                lcd.message(Grainweight + ' lbs.')
                time.sleep(4)
                lcd.clear()
                lcd.set_backlight(1)
                time.sleep(1.0)
    except KeyboardInterrupt:
        # CTRL+C detected, cleaning and quitting the script
        GPIO.cleanup()

for n in range(-1,1):
    if n == 0:
        start = time.time()
        val = measure_weight(n)
        duration = time.time() - start
        durationInString = str(duration)
        "{:<2}".format(durationInString)
        lcd.set_backlight(0)
        lcd.clear()
        lcd.message("Seconds: ")
        lcd.message(durationInString)
        time.sleep(6.0)
        lcd.clear()
        print(f'Measuring weight took {duration:.2f}s')
        break
        measure_weight()
        break

# TASK 6
# Mill the grains
# LCD display message
print('\n')
print(Task7 + ": " + shortDescTask7)
time.sleep(1.5)
def next_task():
    lcd.set_backlight(0)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Next task...')
#     print('\n')
#     print(Task7 + ": " + shortDescTask7)
    time.sleep(1.5)
    
if __name__ == "__main__":
    next_task()

# Motor mills the grains
def mill_grains(test=4):
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Milling grains...')
    time.sleep(3.0)
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
    val = mill_grains(n)
    duration = time.time() - start
    durationInString = str(duration)
    "{:<2}".format(durationInString)
    lcd.set_backlight(0)
    lcd.message("Seconds: ")
    lcd.message(durationInString)
    time.sleep(6.0)
    lcd.clear()
    print(f'Milling grains took {duration:.2f}s')
    break
    mill_grains()
    break
    
# TASK 7
#Transfer grains to mash tun
#define motion pin
motion_pin = 23
# set GPIO as GPIO.BOARD
GPIO.setmode(GPIO.BCM)
# set pin mode as INPUT
GPIO.setup(motion_pin, GPIO.IN)
def Transfer_Grains(test=4):
    print('\n')
    print(Task8 + ": " + shortDescTask8)
    time.sleep(1.5)
    lcd.set_backlight(0)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Transferring')
    time.sleep(4)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Grains')
    time.sleep(4)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('To Mashtun')
    time.sleep(4)
    lcd.clear()
    print('Transferring grains')
    time.sleep(6)
    try:
        if True:
            if(GPIO.input(motion_pin) == 0):
                time.sleep(8)
                print("Grains not found")
            elif(GPIO.input(motion_pin) == 1):
                lcd.clear()
                lcd.show_cursor(True)
                lcd.message('Grains moved')
                time.sleep(4)
                lcd.clear()
                print("Grains moved")
    except KeyboardInterrupt:
         GPIO.cleanup()

btn = 4
if btn == 4:
    Transfer_Grains()
    

# TASK 8
# Clean Up Task
# Servo 
#calculate process duration of prep
# def TimeDuration():
#     global start1, end1
#     start1 = datetime.now()
#     end1 = datetime.now()
#     elapsed1 = (end1 - start1).seconds
# 
#     return start1, end1

# def TimeDuration7():
#     TimeDuration()
#     time.sleep(4)  
#     TimeDuration()


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

def Cleaning(test=4):

    s = sg90(0)

    try:
        if True:
            print('\n')
            print(Task5 + ": " + shortDescTask5)
            time.sleep(1.5)
            lcd.set_backlight(0)
            lcd.clear()
            lcd.show_cursor(True)
            lcd.message('Start cleaning')
            time.sleep(3.0)
            lcd.clear()
            lcd.message('Sanitizing...')
            time.sleep(3.0)
            print("Swipe left")
            s.setdirection( 100, 100 )
            time.sleep(0.5)
            print("Swipe right")
            time.sleep(0.5)
            print('Done.')
            s.setdirection( -100, -100 )
            lcd.clear()
            time.sleep(4.0)
            lcd.set_backlight(1)
            
    except KeyboardInterrupt:
        s.cleanup()
            
for n in range(-1,1):
    n = 0
    start = time.time()
    val = Cleaning(n)
    duration = time.time() - start
    durationInString = str(duration)
    "{:<2}".format(durationInString)
    lcd.set_backlight(0)
    lcd.message("Seconds: ")
    lcd.message(durationInString)
    time.sleep(6.0)
    lcd.clear()
    print(f'Cleaning took {duration:.2f}s')
    break
    Cleaning()
    break

# LCD display message
def Update_Log():
    lcd.set_backlight(0)
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Done.')
    print('Log table is updated.')
    time.sleep(3.0)
    print('Done.')
    time.sleep(3.0)
    lcd.set_backlight(3)
    lcd.clear()
    
btn = 3
if btn == 3:
    Update_Log()

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

#--------------------------------------------------------------------------------------------------------------------------
#post crud to post prep log in log table
end1 = datetime.now()
def Post():

    # Set the request parameters
    #(THIS works!But not enough) url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_fields=preperation_rest_clean%2Cprep_time_end%2Cpreperation_quality_check%2Cprep_time_start%2Cnumber'
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_fields=preperation_rest_clean%2Cprep_time_end%2Cpreperation_quality_check%2Cprep_time_start%2Cnumber%2Ctotal_price'


    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'amp6826'
    pwd = 'Swami101'

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    final_price = f'$'+ str(round(total_price, 2))
    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"prep_time_start\":\"" + str(start1) + "\",\"prep_time_end\":\"" + str(end1) + "\",\"total_price\":\"" + final_price + "\",\"preperation_quality_check\":\"true\",\"preperation_rest_clean\":\"true\",\"number\":\"" + str(number) + "\"}")

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)
    
Post()
#-----------------------------------------------------------------------------------------------------------------------------------------------