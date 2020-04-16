#Need to install requests package for python
#easy_install requests
import requests
import datetime
import time
import Adafruit_DHT
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO

# to get active prep task from service now to excute on crow pi
def Get_Task_for_CrowPi():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=rpi_to_execute%3DPrepPi%5Estate%3D-5%5Eactive%3Dtrue&sysparm_limit=1'

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
    data = response.json()
    print(data)

#post curd to post prep log in log table
def Post(start1, end1, qualitycheck):
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table?sysparm_fields=preperation_quality_check%2Cprep_time_start%2Cprep_time_end%2Cpreperation_rest_clean%2Csys_id'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'Amp6826'
    pwd = 'Swami101'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers, data="{\"sys_id\":\"\",\"preperation_quality_check\":\""+bool(qualitycheck)+"\",\"prep_time_start\":\""+datetime(start1)+"\",\"prep_time_end\":\"" + datetime(
                                 end1)+"\",\"preperation_rest_clean\":\"\"}" )

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)

#quality fuction once employee done with QC brew master sound buzzer to confrim QC
def QualityCheck():
    # button  used as buzzer to check the quality
    # change
    Qc_empbutton_left = 25
    # buzzer
    buzzerpin = 18
    # set GPIO as GPIO.BOARD
    GPIO.setmode(GPIO.BCM)
    # Setup button pin asBu input and power pins
    GPIO.setup(Qc_empbutton_left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # buzzer
    GPIO.setup(buzzerpin, GPIO.OUT)
    # Initialize the LCD using the pins
    lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
    # Turn backlight on
    lcd.set_backlight(0)

    def quality_check(Qc_empbutton_left, lcd, Prep, buzzerpin):
        # regular quality check using lcd screen
        Prep = True
        while Prep:
            quality_check = False
            # Prep employee sets quality check
            if GPIO.input(Qc_empbutton_left) == 1:
                # turn on LED
                lcd.message('Quality Check request by employee')
                GPIO.output(buzzerpin, GPIO.LOW)
                time.sleep(5)
                # after Quality check complete employee press button for QC Completed
            elif GPIO.input(Qc_empbutton_left) == 0:
                lcd.message('Employee completed the Quality Check ')
                GPIO.output(buzzerpin, GPIO.HIGH)
                time.sleep(0.8)
                # Wait half a second
                time.sleep(5)
                Prep = False
            else:
                lcd.message('Waiting for Request order')
                time.sleep(3)

    quality_check(quality_check)

#calculate process duration of prep
def TimeDuration():

    start1 = datetime.datetime.now()
    QualityCheck()
    #Task2
    #Task3
    end1 = datetime.datetime.now()
    elapsed1 = (end1 - start1).seconds
    print(elapsed1)

def main():
    Get_Task_for_CrowPi()
    TimeDuration()
    QualityCheck()
    Post()

main()


