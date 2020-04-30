#Brian Tu, Eni Saraci, Nicolas Galindo, Yongkang Deng
import sys
import Adafruit_DHT
import time
import sys
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import requests
from datetime import datetime, date
from Adafruit_LED_Backpack import SevenSegment
import math

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

motion_pin = 23
# set GPIO as GPIO.BOARD
GPIO.setmode(GPIO.BCM)
# set pin mode as INPUT
GPIO.setup(motion_pin, GPIO.IN)

segment = SevenSegment.SevenSegment(address=0x70)

def getFromMb():
    #Need to install requests package for python
    #easy_install requests
    import requests
    
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=active%3Dtrue%5EnumberISNOTEMPTY%5EORDERBYDESCsys_created_on&sysparm_limit=10'
    
    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'bqt5061'
    pwd = 'LanTsui26'
    
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    
    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers )
    
    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    
    # Decode the JSON response into a dictionary and use the data
    global grain_weight, number, mash_temperature, waterMass, water_temp, sys_Id, order_Id
    order_Id = response.json()['result'][0]['order_id']
    grain_weight = response.json()['result'][0]['grain_weight']
    mash_temperature = response.json()['result'][0]['mash_temperature']
    waterMass = response.json()['result'][0]['water_by_weight']
    water_temp = response.json()['result'][0]['water_temperature']
    sys_Id = response.json()['result'][0]['sys_id']
    number = response.json()['result'][0]['number']
    print('Order No.: ' + number)
    time.sleep(2)
    print('Order ID: ' + order_Id)
    time.sleep(2)
    print('Record ID: ' + sys_Id)
    time.sleep(2)
    print('Grain weight: ' + grain_weight)
    time.sleep(2)
    print('Mash Temperature: ' + mash_temperature)
    time.sleep(2)
    print('Water Mass: ' + waterMass)
    time.sleep(2)
    print('Water Temperature: ' + water_temp)
    time.sleep(1)
    # return the local variables
    return grain_weight, number, mash_temperature, waterMass, water_temp, sys_Id, order_Id
getFromMb()
    

def GetFromBrewTasks():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=active%3Dtrue%5Erpi_to_executeSTARTSWITHMashPi%5Estate%3D-5&sysparm_limit=10'
    user = 'bqt5061'
    pwd = 'LanTsui26'
    
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    
    response = requests.get(url, auth=(user, pwd), headers=headers)
    
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()
    
    # Decode  the JSON response into dictionary and use the  data
    global Task1, shortDesc1, Task2, shortDesc2, Task3, shortDesc3, Task4, shortDesc4, Task5, shortDesc5, Task6, shortDesc6
    Task1 = response.json()['result'][0]['number']
    shortDesc1 = response.json()['result'][0]['short_description']
    Task2 = response.json()['result'][1]['number']
    shortDesc2 = response.json()['result'][1]['short_description']
    Task3 = response.json()['result'][2]['number']
    shortDesc3 = response.json()['result'][2]['short_description']
    Task4 = response.json()['result'][3]['number']
    shortDesc4 = response.json()['result'][3]['short_description']
    Task5 = response.json()['result'][4]['number']
    shortDesc5 = response.json()['result'][4]['short_description']
    Task6 = response.json()['result'][5]['number']
    shortDesc6 = response.json()['result'][5]['short_description']
    return Task1, shortDesc1, Task2, shortDesc2, Task3, shortDesc3, Task4, shortDesc4, Task5, shortDesc5, Task6, shortDesc6
#     print(Task5 + " :" + shortDesc5 )
#     time.sleep(1)
    
GetFromBrewTasks()

def heat_HLT():
    time.sleep(2)
    print("\n")
    print(Task6 + " :" + shortDesc6 )
    time.sleep(1)
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

    def main():

        print("Hot liquor tank")
        motor = Stepmotor()
        print("is running")
        motor.turnSteps(1)
        time.sleep(0.5)
        print("Heating in process")
        motor.turnSteps(20)
        time.sleep(0.5)
        print("Heating in process")
        motor.turnDegrees(90)
        print("Done.")
        print('Prepare the water')
        motor.close()

    if __name__ == "__main__":
        main()
heat_HLT()

#def check_Temp():
    
def addStrikeWater1():
    print("\n")
    print(Task1 + " :" + shortDesc1 )
    time.sleep(1)
    print('Adding water to the mash tun.')
    # define vibration pin
    vibration_pin = 27

    # Set board mode to GPIO.BOARD
    GPIO.setmode(GPIO.BCM)

    # Setup vibration pin to OUTPUT
    GPIO.setup(vibration_pin, GPIO.OUT)

    # turn on vibration
    GPIO.output(vibration_pin, GPIO.HIGH)
    # wait half a second
    time.sleep(5)
    # turn off vibration
    GPIO.output(vibration_pin, GPIO.LOW)
    # cleaup GPIO
    GPIO.cleanup()

    print('Mash tun is 3/4 full.')
    time.sleep(3)
    
addStrikeWater1()

def Sparging1():
    print("\n")
    print(Task3 + " :" + shortDesc3 )
    time.sleep(1)
    print('Start Sparging')
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

    def main():

        s = sg90(0)

        try:
            while True:
                print("Turn left")
                s.setdirection( 100, 10 )
                time.sleep(0.5)
                print("Turn right")
                s.setdirection( -100, -10 )
                time.sleep(0.5)
        except KeyboardInterrupt:
            s.cleanup()

    if __name__ == "__main__":
        main()
Sparging1()

def checkWaterVolume():
    print("\n")
    print(Task4 + " :" + shortDesc4 )
    time.sleep(2)
    print('Check water volume')
    buzzer_pin = 18

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)

    # Make buzzer sound
    GPIO.output(buzzer_pin, GPIO.LOW)
    time.sleep(2)
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
    time.sleep(2)
    print('Water volume is low')
    print('Adding more water')
    

time.sleep(3)
def addStrikeWater2():
    print("\n")
    print(Task1 + " :" + shortDesc1 )
    time.sleep(1)
    
    # define vibration pin
    vibration_pin = 27

    # Set board mode to GPIO.BOARD
    GPIO.setmode(GPIO.BCM)

    # Setup vibration pin to OUTPUT
    GPIO.setup(vibration_pin, GPIO.OUT)

    # turn on vibration
    GPIO.output(vibration_pin, GPIO.HIGH)
    # wait half a second
    time.sleep(5)
    # turn off vibration
    GPIO.output(vibration_pin, GPIO.LOW)
    # cleaup GPIO
    GPIO.cleanup()
    time.sleep(3)
    print('Mash tun is full')
    time.sleep(3)
    print('Continue sparging')
    
addStrikeWater2()

def Sparging2():
    print("\n")
    print(Task2 + " :" + shortDesc2 )
    time.sleep(1)
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

    def main():

        s = sg90(0)

        try:
            while True:
                print("Turn left")
                s.setdirection( 100, 10 )
                time.sleep(0.5)
                print("Turn right")
                s.setdirection( -100, -10 )
                time.sleep(0.5)
        except KeyboardInterrupt:
            s.cleanup()

    if __name__ == "__main__":
        main()
Sparging2()

time.sleep(2)
def Complete():
    buzzer_pin = 18

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)

    # Make buzzer sound
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(1)
    # Stop buzzer sound
    GPIO.output(buzzer_pin, GPIO.LOW)

    GPIO.cleanup()
Complete()
    
print('Mash is complete.')    

def PostMashrecord():
    
    #Need to install requests package for python
    #easy_install requests
    
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table'
    
    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'bqt5061'
    pwd = 'LanTsui26'
    
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    
    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers ,data="{\"mash_duration\":\"" + str(mash_duration) + "\",\"mash_end_time\":\"" + str(mash_end_time) + "\",\"mash_start_time\":\"" + str(mash_start_time) + "\",\"mash_reset_clean\":\"True\",\"mash_quality_check\":\"True\"}")
    
    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    
    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)
    
def main():
    PostMashrecord()

