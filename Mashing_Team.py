#Brian Tu, Eni Saraci, Nicholas Galindo, Yongkang Deng
import sys
import Adafruit_DHT
import time
import sys
import requests
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import requests
from datetime import datetime
from Adafruit_LED_Backpack import SevenSegment
import math

# Buzzer 1 

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
    global grain_weight, number, malt_type_1, malt_type_2, malt_type_3, sys_Id, order_Id
    order_Id = response.json()['result'][0]['order_id']
    grain_weight = response.json()['result'][0]['grain_weight']
    malt_type_1 = response.json()['result'][0]['malt_type_1']
    malt_type_2 = response.json()['result'][0]['malt_type_2']
    malt_type_3 = response.json()['result'][0]['malt_type_3']
    sys_Id = response.json()['result'][0]['sys_id']
    number = response.json()['result'][0]['number']
    print('Order No.: ' + number)
    time.sleep(2)
    print('Order ID: ' + order_Id)
    time.sleep(2)
    print('Record ID: ' + sys_Id)
    time.sleep(2)
    print("\n")
    print('Malt Type #1: ' + malt_type_1)
    print('Malt Type #2: ' + malt_type_2)
    print('Malt Type #3: ' + malt_type_3)
    print("\n")
    print('Grain weight: ' + grain_weight)
    time.sleep(2)
    print('Mash Temperature: 155F')
    time.sleep(2)
    print('Water Temperature: 170F' )
    time.sleep(1)
    # return the local variables
    return grain_weight, number, malt_type_1, malt_type_2, malt_type_3, sys_Id, order_Id
getFromMb()

def GetMashBrewTasks():
 # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=rpi_to_execute%3DMashPi%5Estate%3D-5%5Eactive%3Dtrue&sysparm_limit=1'
    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'bqt5061'
    pwd = 'LanTsui26'
    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers)
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()
    # Decode the JSON response into a dictionary and use the data
    global brewtask, shortDescription, sysId
#     mother_brew_record = response.json()['result']
    brewtask = response.json()['result'][0]['number']
    shortDescription = response.json()['result'][0]['short_description']
    sysId = response.json()['result'][0]['sys_id']
    print(brewtask + ': Following task will Run')
    print('Task Description: ' + shortDescription)
    print()
    return brewtask, shortDescription, sysId

def update():
    global sysId, brewtask, shortDescription
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/' + str(sysId)
    user = 'bqt5061'
    pwd = 'LanTsui26'
    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    # Do the HTTP request and state with value 3 use to close task.
    response = requests.patch(url, auth=(user, pwd), headers=headers, data="{\"state\":\"3\"}")
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()
    # Decode the JSON response into a dictionary and use the data
    print(brewtask + ': ' + shortDescription + ': Task is Closed Complete.')        

def main():
    #Declare Global
    global start_time
    start_time = datetime.now()
    print('\n')
    print('Start Time')
    print(start_time)

main()
        
def heat_HLT():
    print("\n")
    GetMashBrewTasks()
    time.sleep(2)
    #print(Task6 + " :" + shortDesc6 )
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
        print('\n')
        update()
        print('\n')
        print('Prepare the water')
        motor.close()

    if __name__ == "__main__":
        main()
heat_HLT()


#def check_Temp():
    
def addStrikeWater1():
    print("\n")
    GetMashBrewTasks()
    #print(Task1 + " :" + shortDesc1 )
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
    time.sleep(5)
    print('\n')
    update()
    
addStrikeWater1()

def addMaltType1():
    time.sleep(5)
    print("\n")
    GetMashBrewTasks()
    #print(Task8 + " :" + shortDesc8)
    time.sleep(5)
    print('Adding in Malt 1.')
    print('\n')
    update()
    
addMaltType1()

def addMaltType2():
    time.sleep(5)
    print("\n")
    GetMashBrewTasks()
    #print(Task9 + " :" + shortDesc9)
    time.sleep(5)
    print('Adding in Malt 2.')
    print('\n')
    update()
    
addMaltType2()

def Sparging1():
    time.sleep(5)
    print("\n")
    GetMashBrewTasks()
    #print(Task3 + " :" + shortDesc3 )
    time.sleep(5)
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
    print('\n')
    update()    
Sparging1()

def addMaltType3():
    time.sleep(5)
    print("\n")
    GetMashBrewTasks()
    #print(Task10 + " :" + shortDesc10)
    time.sleep(5)
    print('Adding in Malt 3')
    time.sleep(5)
    print('\n')
    update()
    
addMaltType3()

def checkWaterVolume():
    time.sleep(5)
    print("\n")
    GetMashBrewTasks()
    #print(Task4 + " :" + shortDesc4 )
    time.sleep(5)
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
    print('\n')
    update()

checkWaterVolume()    

time.sleep(3)
def addStrikeWater2():
    print("\n")
    GetMashBrewTasks()
    #print(Task1 + " :" + shortDesc1 )
    time.sleep(5)
    
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
    print('\n')
    update()
    print('\n')
    print('Continue sparging')
    
addStrikeWater2()

def Sparging2():
    time.sleep(5)
    print("\n")
    GetMashBrewTasks()
    #print(Task2 + " :" + shortDesc2 )
    time.sleep(5)
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
    time.sleep(5)    
    print('\n')    
    update()    
Sparging2()
time.sleep(2)

def CheckForQuality():
    print('\n')
    print('Starting Mashing Check')
    time.sleep(10)
    print('\n')
    print('Checking Mash')
    time.sleep(10)
    print ('\n')
    print('Ending Mashing Check')
CheckForQuality()

def Complete():
    buzzer_pin = 18

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)

    # Make buzzer sound
    GPIO.output(buzzer_pin, GPIO.LOW)
    time.sleep(1)
    # Stop buzzer sound
    GPIO.output(buzzer_pin, GPIO.LOW)

    GPIO.cleanup()
Complete()

print('\n')
print('Mash is complete.')

def main2():
    
    global end_time, time_duration
    end_time = datetime.now()
    print('\n')
    print('Ending Time')
    print(end_time)
    #duration
    time_duration = end_time - start_time
    print('\n')
    print('Process Duration')
    print(time_duration)

main2()

def ProcessReset():
    print('\n')
    print('Cleaning in Process')
    time.sleep(20)
    print('\n')
    print('Finished Cleaning')
ProcessReset()

def PostMashrecord():
    
    #Need to install requests package for python
    #easy_install requests
    import requests
    
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table'
    
    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'bqt5061'
    pwd = 'LanTsui26'
    
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    
    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers ,data="{\"mash_duration\":\"" + str(time_duration) + "\",\"mash_end_time\":\"" + str(end_time) + "\",\"mash_start_time\":\"" + str(start_time) + "\",\"mash_quality_check\":\"true\",\"mash_reset_clean\":\"true\",\"number\":\"" + str(number) + "\"}")
    
    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    
    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)

def main3():
    PostMashrecord()  
main3()

  
