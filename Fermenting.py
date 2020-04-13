#Team Ferment - James Bee, Virginia Hoffman, Michaela Fox, and Samantha Scheer
#IST 440 - Luke Kasper

#imports
import AutoBrew
import RPi.GPIO as GPIO
import time
import requests
import Adafruit_DHT
import Adafruit_CharLCD as LCD
import os
import sys, subprocess
import requests
#from pymongo import MongoClient
#import pymongo

#setting variables for lcdScreen
lcdColumns = 16
lcdRows    = 2

# setting variables (temp)
tempSensor = Adafruit_DHT.DHT11
tempPin = 4

# setting vairables for buzzer
buzzerPin = 18

#recipie table
class RecipieTable:
    def RecipieGetCRUD():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_recipe?sysparm_limit=100'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'kasper440'
        pwd = 'kasper440'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers, data="{\"recipe_name\":\"Peanut Butter\"}")

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def RecipiePostCRUD():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_recipe'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'kasper440'
        pwd = 'kasper440'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.post(url, auth=(user, pwd), headers=headers, data="{\"recipe_name\":\"Umm\"}")

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def RecipieUpdateCRUD():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_recipe?sysparm_display_value=ed7e0aea1b67c850befe0d88cc4bcbab'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'sls1058'
        pwd = 'Ummidk123!'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.post(url, auth=(user, pwd), headers=headers, data="{\"recipe_name\":\"Ale\"}")

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def RecepieDeleteCRUD():
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_recipe/2cb47fe61b6bc850befe0d88cc4bcbc2'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'kasper440'
        pwd = 'kasper440'

        # Set proper headers
        headers = {"Content-Type":"application/json","Accept":"application/json"}

        # Do the HTTP request
        response = requests.delete(url, auth=(user, pwd), headers=headers )

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)

    def RecipieMongoCRUD():
        client = MongoClient('localhost', 27017)
        db = client['recipes_db']
        recipes = db['recipes']

        # Set the request parameters
        '''
        Use sysparm_fields=field_name => field_name is the field you want to read
        separate fields using commas in case you want to read more than one field from a table
        '''

        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_recipe?sysparm_limit=1'

        # Use IST440 for both user and pwd
        user = 'kasper440'
        pwd = 'kasper440'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        # GET is the request to read data
        response = requests.get(url, auth=(user, pwd), headers=headers)

        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(type(data))
        print()
        print("This is a json dictionary: ", data, "Type: ", type(data))

        # Now we need to get the list of key value pairs from our dict
        print()
        recipe_names_pairs = data['result']
        print("This is a list: ", recipe_names_pairs)
        print()

        # Check type
        print("Recipe_names_pairs is of the list type and can now be used to create documents in mongddb: ",
              type(recipe_names_pairs))
        print()
        # db.collection_recipe.insert(recipe_names_pairs)

        # For loop to iterate through the key value pairs obtained from the json response
        # and check if any has previously been inserted in the collection

        for doc in recipe_names_pairs:
            try:
                # insert into db collection
                # print("Inserting ",  doc, " into db...")
                message = "Inserting  into db..."
                db.recipes.insert_one(doc)
            except pymongo.errors.DuplicateKeyError:
                # skip document because it already exists in the local db collection
                continue

#lkbretasks table
class LKBrewTasks():
    def LKGetCRUD():
        # Need to install requests package for python
        # easy_install requests
        import requests
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_limit=1'
        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'admin'
        pwd = 'admin'
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

    def LKPostCRUD():
        # Need to install requests package for python
        # easy_install requests
        import requests
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask'
        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'admin'
        pwd = 'admin'
        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        # Do the HTTP request
        response = requests.post(url, auth=(user, pwd), headers=headers)
        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()
        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)


# function to display temp n humidity
def TempAndHumidityLCD(lcdColumns, lcdRows, tempSensor, tempPin):
    # Initialize the LCD using the pins
    lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)

    temperature, humidity = Adafruit_DHT.read(tempSensor, tempPin)
    time.sleep(1)
    GPIO.cleanup()

    temperature = temperature * 9 / 5.0 + 32

    temperatureStr = str(temperature)
    humidityStr = str(humidity)

    # print temp
    lcd.set_backlight(0)
    lcd.message("Current temp \n" + temperatureStr + " F")
    time.sleep(5.0)
    lcd.clear()

    # print humidity
    lcd.set_backlight(0)
    lcd.message("Current humidity \n" + humidityStr + " %")
    time.sleep(5.0)
    lcd.clear()
    GPIO.cleanup()


# function to buzz wghen fermenting is done
def BuzzerDone(buzzerPin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzerPin, GPIO.OUT)

    # Make buzzer sound
    GPIO.output(buzzerPin, GPIO.HIGH)
    time.sleep(0.5)

    # Stop buzzer sound
    GPIO.output(buzzerPin, GPIO.LOW)

    GPIO.cleanup()

#runs all other code
def Main():
    print(TempAndHumidityLCD(lcdColumns, lcdRows, tempSensor, tempPin))
    print(BuzzerDone(buzzerPin))

    #recipie table
    RecipieTable.RecipieGetCRUD()
    RecipieTable.RecipiePostCRUD()
    RecipieTable.RecipieUpdateCRUD()
    RecipieTable.RecepieDeleteCRUD()

    #LK brew tasks table
    LKBrewTasks.LKGetCRUD()
    LKBrewTasks.LKPostCRUD()

#run all the stuff
Main()
