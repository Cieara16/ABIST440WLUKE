import time
import Adafruit_DHT
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import datetime
import requests


# start_time = time.time()
# your code
# elapsed_time = time.time() - start_time

class Keg():
    
    temperature = 0

    # function to initialize local variables
    def __init__(self, volume, carbonation_temp, quantity, time_duration, temperature):
        self.volume = volume
        self.carbonation_temp = carbonation_temp
        self.quantity = quantity
        self.time_duration = time_duration
        self.temperature = temperature

'''
work still in progress
Raspberry Pi function work perfect as in sequence 
'''



'''
Motion detection is useful for keg because this program will to detect keg arrival
at filling station. Also helpful to detect poistion of keg.
'''


def motion_detect_keg():
    # Used Motion gpio
    motion_pin = 23
    # set GPIO as GPIO.BOARD
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motion_pin, GPIO.IN)
    # Initialize the LCD using the pins
    lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
    # Turn backlight on
    lcd.set_backlight(0)

    def motion_detect_Point_A(motion_pin):
        while True:
            if GPIO.input(motion_pin) == 0:
                lcd.message('Waiting for Keg\n')
                time.sleep(0.5)
                lcd.clear()
            elif GPIO.input(motion_pin) == 1:
                lcd.message('Keg is arrived\n')
                time.sleep(1)
        GPIO.cleanup()

    motion_detect_Point_A(motion_pin)


'''
When the keg is arrived on automated belt, motion sensor will detect the keg
and alert employee to press button and LED display will show customer
selected volume. I have configure two button with different amount Up independent button
for 5 gallon and down independent button for 10 gallon. Once employee select
for 5 gallon, we calculate approximate time that it will take 2 minute and 3
seconds. After 2 minutes and 3 second button will off automatic.
'''


def press_button_to_fill():
    # configure down button for 5 gallon
    button_pin_5_down = 13
    # configure down button for 10 gallon
    button_pin_10_up = 26
    # Used power gpio
    power_pin = 18
    # set GPIO as GPIO.BOARD
    GPIO.setmode(GPIO.BCM)
    # Setup button pin asBu input and power pins
    GPIO.setup(button_pin_5_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button_pin_10_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(power_pin, GPIO.OUT)
    lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
    # Turn backlight on
    lcd.set_backlight(0)

    def Fill_keg(button_pin_5_down, power_pin, button_pin_10_up):
        while True:
            # check if button pressed for 5 gallon
            if (GPIO.input(button_pin_5_down) == 0):
                # set power on
                GPIO.output(power_pin, GPIO.HIGH)
                lcd.message('Button is \nPressed')
                # Power is off automatically after 5 second
                time.sleep(3)
                # check if button pressed for 10 gallon
            elif (GPIO.input(button_pin_10_up) == 0):
                # set power on
                GPIO.output(power_pin, GPIO.HIGH)
                lcd.message('Button is \nPressed')
                # Power is off automatically after 5 second
                time.sleep(6)
            else:
                # it's not pressed, set button off
                GPIO.output(power_pin, GPIO.LOW)
                lcd.message('Button is not \nPressed \n')
                time.sleep(1)
                lcd.clear()
        GPIO.cleanup()

    Fill_keg(button_pin_5_down, power_pin, button_pin_10_up)


'''
Carbonation refer to carbon dioxide dissolved in liquid, and the rate at which carbon
dioxide dissolve or is soluble depends on temperature. When tempertaure
is raised, the rate of dissolution in liquid is decreased, and vice versa
when the temperature is lowered.
'''


def carbonation_check():
    # set type of the sensor for temp
    sensor = 11
    # set pin number for temp
    pin = 4
    # Define LCD column and row size for 16x2 LCD.
    lcd_columns = 16
    lcd_rows = 2
    # Initialize the LCD using the pins
    lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
    # Initialize the temperature sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Turn backlight on
    lcd.set_backlight(0)

    def Carbonation_temp(humidity, temperature, lcd):
        # Might need to Record before and after temp and huminity
        for i in range(2):
            if humidity is not None and temperature is not None:
                lcd.message('Temp={0:0.1f} & \nHumidity={1:0.1f}%'.format(temperature, humidity))
                # temp sensor will take reading after 2 second
                time.sleep(2)
                # Record Temperature in text file
                with open("file.txt", "w+") as f:
                    f.write('Temp={0:0.1f} & \nHumidity={1:0.1f}%'.format(temperature, humidity))
                    f.write('\n')
            else:
                lcd.message('Failed to get reading. Try again!')
            # In 5 seconds LCD will turn off
            time.sleep(5)
            lcd.clear()
            lcd.set_backlight(1)
        GPIO.cleanup()

    Carbonation_temp(humidity, temperature, lcd)


def main():
    # calculate Time start and end process of each task
    # start1 = datetime.datetime.now()
    # motion_detect_keg()
    # end1 = datetime.datetime.now()
    # elapsed1 = (end1 - start1).seconds
    # print(elapsed1)

    # run sequentially
    # motion_detect_keg()
    # press_button_to_fill()
    # carbonation_check()

    brew = Keg()
    brew.motion_detect_keg()
    brew.press_button_to_fill()
    brew.carbonation_check()


if __name__ == "__main__":
    main()
.....................................
(Qualitycheck)

import time
import Adafruit_DHT
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO

# configure down button for 5 gallon and assign gpio
button_QC_right = 19
# define LED pin
led_pin = 8
# Used Motion gpio
motion_pin = 23
# set GPIO as GPIO.BOARD
GPIO.setmode(GPIO.BCM)
# set puin as input
GPIO.setup(led_pin, GPIO.OUT)
# set motion pin as output
GPIO.setup(motion_pin, GPIO.IN)
# Setup button pin asBu input and power pins
GPIO.setup(button_QC_right, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
# Turn backlight on
lcd.set_backlight(0)
# QC

# Motion detect keg
QC1 = "Quality Check is Completed"
QC2 = "Requested for Quality Check"
point = True


def quality_check(button_QC_right,led_pin,motion_pin,lcd,QC1,QC2,point):
    # When motion sensor detect keg
    while GPIO.input(motion_pin) == 1 and point:
        quality_check = False
        # When keg arrived at stage 2
        if (GPIO.input(button_QC_right) == 1) and quality_check == False:
            # turn on LED
            print(QC2)
            lcd.message('Requested for Quality Check')
            GPIO.output(led_pin, GPIO.HIGH)
            print('Hit right button')
            GPIO.wait_for_edge(button_QC_right, GPIO.FALLING)
            time.sleep(10)
            # after Quality check complete employee press button for QC Completed
            if GPIO.input(button_QC_right) == 1:
                # turn off LED
                GPIO.output(led_pin, GPIO.LOW)
                print(QC1)
                lcd.message('Quality Check is Completed')
                # Wait half a second
                time.sleep(10)
                point = True

    GPIO.cleanup()


quality_check(quality_check)
