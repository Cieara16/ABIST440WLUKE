# Justin Hill - Team boil
import sys
import Adafruit_DHT
import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import requests

# dh11 sensor
sensor = 11
pin = 4
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

# Comment the line below to convert the temperature to Celcius.
temperature = temperature * 9 / 5.0 + 32


def readTemperature(sensor, pin):
    return temperature, humidity
    time.sleep(1.0)


# function to initialize local variables
def __init__(self, boilTemp, boilTempRange, boilDuration, maxTemp, minTemp, temperature):
    self.boilTemp = boilTemp
    self.boilTempRange = boilTempRange
    self.boilDuration = boilDuration
    self.maxTemp = maxTemp
    self.minTemp = minTemp
    self.temperature = temperature


def Get():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_boil?sysparm_limit=1'

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

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)


def systemCheck():
    # used to check system functionality before continuing
    # if all is good, then pass
    # if there are problems, then throw error
    pass


def tempDisplay():
    while temperature < 150:
        try:
            # Turn backlight on
            lcd.set_backlight(0)
            if humidity is not None and temperature is not None:
                lcd.message('Temp={0:0.1f}*\nHumidity={1:0.1f}%\n'.format(temperature, humidity))
            else:
                lcd.message('Failed to get reading. Try again!')
            time.sleep(1.0)
        except KeyboardInterrupt:
            # Turn the screen off
            lcd.clear()
            lcd.set_backlight(1)

    while temperature >= 150:
        try:

            if humidity is not None and temperature is not None:
                lcd.message('Very Hot!')
                lcd.message('Temp.={0:0.1f}Hum={0:01f}'.format(temperature, humidity))
            else:
                lcd.message('Failed to get reading. Try again!')
        except KeyboardInterrupt:
            # Turn the screen off
            lcd.clear()
            lcd.set_backlight(1)


def Post():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_boil'

    user = 'kasper440'
    pwd = 'kasper440'

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers, data="{\"current_temperature\":\"\"}")

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)

#def convertToFahrenheit(self):
    # result = float((9 * self.temperature) / 5 + 32)
    # return result
#def convertToCelcius(self):
    # result = float((self.temperature - 32) * 5 / 9)
    # return result

def maintainTemp(self):

    maxTemp = 110
    minTemp = 100
    #this should be updated from the GET request from Servicenow
    #assuming temp is recorded as celsius would this work with the pi? Could we set this in the while loop timer below having it constantly record and check temp?
    if self.temperature < minTemp:
        self.temperature += 10
        print('Too cold, increasing heat...')
        return self
    elif self.temperature > maxTemp:
        self.temperature -= 10
        print("That's an awfully hot coffee pot")
        return self.temperature
    else:
        return self.temperature


def main():
    Get()
    systemCheck()
    readTemperature(temperature, humidity)
    tempDisplay()
    Post()
    # Sec = 0
    # timeLoop = True
    #
    # # Begin Process. Not sure if we should include a 60min timer for boiling or leave that for the Brew master in between steps
    # while timeLoop:
    #     Sec += 1
    #     time.sleep(1)
    #     maintainTemp()
    #     if Sec == 60:
    #         exit()

main()

