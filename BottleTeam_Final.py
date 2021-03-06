# IST 440
# Bottle Team
# Author: Riken, Eduard, Wilmer, Muhammad
import time
import Adafruit_DHT
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import requests
import datetime

# Used Motion gpio
motion_pin = 23
# configure down button for 5 gallon and assign gpio
button_pin_5_down = 13
# configure down button for 10 gallon and assign gpio
button_pin_10_up = 26
# Used power gpio
power_pin = 18
# set type of the sensor for temp
sensor = 11
# set pin number for temp
pin = 4
# configure right button for quality check and assign gpio
button_QC_right = 19
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2
temperature = 0
# set GPIO as GPIO.BOARD
GPIO.setmode(GPIO.BCM)
GPIO.setup(motion_pin, GPIO.IN)
# Setup button pin asBu input and power pins
GPIO.setup(button_pin_5_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin_10_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(power_pin, GPIO.OUT)
GPIO.output(power_pin, GPIO.LOW)
# Setup button pin asBu input and QC check
GPIO.setup(button_QC_right, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
# Turn backlight on
lcd.set_backlight(0)

global start_time, end_time, alcohol_input, Kegvolume, Kegquantity, Number, sysId


def Get_Rpi_BottleTask():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=rpi_to_execute%3DBottlePi%5Estate%3D-5%5Eactive%3Dtrue&sysparm_limit=1'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'rap5695'
    pwd = 'Rp13595@'

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
    user = 'rap5695'
    pwd = 'Rp13595@'

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Do the HTTP request and state with value 3 use to close task.
    response = requests.patch(url, auth=(user, pwd), headers=headers, data="{\"state\":\"3\"}")

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    print(brewtask + ': ' + shortDescription + ': Task is completed and Closed.')


def GetVolume():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=activeISNOTEMPTY%5EORDERBYDESCsys_created_on&sysparm_fields=keg_volume%2Ckeg_quantity%2Cnumber%2Csys_id%2Cabv&sysparm_limit=1'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'rap5695'
    pwd = 'Rp13595@'

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    global Kegvolume, Kegquantity, Number, motherbrewsysID, variableName
    Kegvolume = response.json()['result'][0]['keg_volume']
    Kegquantity = response.json()['result'][0]['keg_quantity']
    Number = response.json()['result'][0]['number']
    motherbrewsysID = response.json()['result'][0]['sys_id']
    variableName = response.json()['result'][0]['abv']
    print('Keg Volume: ' + Kegvolume + ' Gallons')
    print('Keg Quantity: ' + Kegquantity + ' Kegs ')
    print('Number: ' + Number)
    print('Alcohol Percentage: ' + variableName)
    print('sys ID: ' + motherbrewsysID)
    return Kegvolume, Kegquantity, Number, motherbrewsysID, variableName


# def update_to_closeteam():
#
#     url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2/' + str(motherbrewsysID)
#
#     # Eg. User name="admin", Password="admin" for this code sample.
#     user = 'rap5695'
#     pwd = 'Rp13595@'
#
#     # Set proper headers
#     headers = {"Content-Type":"application/json","Accept":"application/json"}
#
#     # Do the HTTP request
#     response = requests.patch(url, auth=(user, pwd), headers=headers ,data="{\"brew_phase\":\"Close\"}")
#
#     # Check for HTTP codes other than 200
#     if response.status_code != 200:
#         print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
#         exit()
#
#     # Decode the JSON response into a dictionary and use the data
#     data = response.json()
#     print('Update Brew Phase to Close Team')

def motion_detect_keg():
    # Turn backlight on
    lcd.set_backlight(0)
    point = True
    while point:
        if GPIO.input(motion_pin) == 0:
            print('Waiting for Keg')
            time.sleep(3)
            lcd.clear()
        elif GPIO.input(motion_pin) == 1:
            print('Keg is arrived\n')
            time.sleep(5)
            lcd.clear()
            point = False


def Fill_keg():
    print('Press the Button ' + Kegvolume + ' Gallons')
    point = True
    while point:
        # check if button pressed for 5 gallon
        if (GPIO.input(button_pin_5_down) == 0) and Kegvolume == "5":
            # set power on
            print('Button is Pressed for 5 Gallon')
            # GPIO.setwarnings(False)
            # Power on Buzzer for 3 seconds in 5 Gallons
            GPIO.output(power_pin, GPIO.HIGH)
            # Power is off automatically after 5 second
            time.sleep(3)
            GPIO.output(power_pin, GPIO.LOW)
            point = False

            # check if button pressed for 10 gallon
        elif (GPIO.input(button_pin_10_up) == 0) and Kegvolume == "15":
            # set power on
            print('Button is Pressed for 15 Gallon')
            # GPIO.setwarnings(False)
            # Power on Buzzer for 6 seconds in 10 Gallons
            GPIO.output(power_pin, GPIO.HIGH)
            # Power is off automatically after 6 second
            time.sleep(6)
            GPIO.output(power_pin, GPIO.LOW)
            point = False
    lcd.clear()


def Carbonation_temp():
    global temperature, humidity
    temperature = 0
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    # Might need to Record before and after temp and huminity
    try:
        for i in range(1):
            if humidity is not None and temperature is not None:
                print('Before temperature:\n     Temp= %.1f F' % (temperature))
                print('Before Humidity:\n     Humidity= ' + str(humidity) + ' %')
                # Comment the line below to convert the temperature to Celcius.
                temperature = temperature * 9 / 5.0 + 32
                temperature -= 60
                humidity -= 15
                # lcd.message('Temp={0:0.1f} & Humidity={1:0.1f}%'.format(temperature, humidity))
                # temp sensor will take reading after 2 second
                time.sleep(5)
                print('After adding Carbonation temperature:\n     Temp= %.1f F' % (temperature))
                print('After adding Carbonation Humidity:\n     Humidity= ' + str(humidity) + ' %')
            else:
                lcd.message('Failed to get reading. Try again!')
                # In 5 seconds LCD will turn off
            time.sleep(5)
            lcd.clear()
            lcd.set_backlight(1)
        return temperature, humidity
    except KeyboardInterrupt:
        print("Tempertaure sensor error")


def alcohol_content_1():
    print('Adding ' + str(variableName) + '% of alcohol to keg')
    print('Adding Alcohol to keg ..........')
    time.sleep(8)
    print('Alcohol Content is Added')


def QC():
    print('Requested for \nQuality Check \n')
    point = True
    while point:
        try:
            if (GPIO.input(button_QC_right) == 0):
                print('Quality Check is \nCompleted \n')
                # Wait half a second
                time.sleep(2)
                point = False
        except KeyboardInterrupt:
            GPIO.cleanup()
            print('Quality Check Error')


def Post():
    # Need to install requests package for python
    # easy_install requests
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table'
    # ?sysparm_fields=bottle_start_time%2Cbottle_end_time%2Ccarbonation%2Cabv%2Cu_bottle_quality_check%2Cbottle_reset_clean%2Cbottle_after_humidity%2Cbottle_after_temp

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'rap5695'
    pwd = 'Rp13595@'

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"bottle_start_time\":\"" + str(
                                 start_time) + "\",\"bottle_end_time\":\"" + str(
                                 end_time) + "\",\"abv\":\"" + str(
                                 variableName) + "\",\"carbonation\":\"" + str(
                                 temperature) + "\",\"bottle_after_temp\":\"" + str(
                                 temperature) + "\",\"bottle_after_humidity\":\"" + str(
                                 humidity) + "\",\"u_bottle_quality_check\":\"true\", \"number\":\"" + str(
                                 Number) + "\", \"bottle_reset_clean\":\"true\", \"bottle_before_humidity\":\"48.0\", \"bottle_before_temp\":\"29.0\"}")

    # Check for HTTP codes other than 200
    if response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)


def main():
    # run sequentially
    """
    brew = Keg()
    """
    global start_time, end_time, Kegquantity

    #     Get_Rpi_BottleTask()
    print()
    start_time = datetime.datetime.now()
    GetVolume()
    print()
    for i in range(int(Kegquantity)):
        i += 1
        print('Keg Number: ' + str(i))
        print()
        time.sleep(12)
        Get_Rpi_BottleTask()  # get keg position
        print()
        motion_detect_keg()
        print()
        update()  # close complete get keg postion
        time.sleep(12)
        print()
        Get_Rpi_BottleTask()
        print()
        Fill_keg()
        print()
        update()
        time.sleep(12)
        print()
        Get_Rpi_BottleTask()
        print()
        Carbonation_temp()
        print()
        update()
        time.sleep(12)
        print()
        Get_Rpi_BottleTask()
        print()
        alcohol_content_1()
        print()
        update()
        time.sleep(12)
        print()
        Get_Rpi_BottleTask()
        print()
        QC()
        print()
        update()
        time.sleep(12)
    end_time = datetime.datetime.now()
    # return start_time, end_time
    print()
    Get_Rpi_BottleTask()
    print()
    Post()
    print()
    update()
    print('Bottle Phase Complete for order')
    #update_to_closeteam()
    print('Change Brew Phase to Close team')
    # import GetFromMotherBrew()


if __name__ == "__main__":
    main()
