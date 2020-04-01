#Begin Brew class
import time
import requests

class Brew():
    temperature = 0
    boilTime = 0

    #function to initialize local variables
    def __init__(self, boilTemp, boilTempRange, boilDuration, maxTemp, minTemp, temperature):
        self.boilTemp = boilTemp
        self.boilTempRange = boilTempRange
        self.boilDuration = boilDuration
        self.maxTemp = maxTemp
        self.minTemp = minTemp
        self.temperature = temperature

    # We could just do the conversion once within the output statement rather that having a function. But I'm a dumbass so lemme know..
    def convertToFahrenheit(self):
        result = float((9 * self.temperature) / 5 + 32)
        return result
    def convertToCelcius(self):
        result = float((self.temperature - 32) * 5 / 9)
        return result

def postTest(self):
    pass

def boil(self):
        #method for maintaining temperature
        #Work in progress

def maintainTemp(self):

    maxTemp = 110
    minTemp = 100

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

def Get(self):
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_boil?sysparm_limit=1'

    # Eg. User name="admin", Password="admin" for this code sample.
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




def main(self):
    Get()
    postTest()

Sec = 0
timeLoop = True

# Begin Process. Not sure if we should include a 60min timer for boiling or leave that for the Brew master in between steps
while timeLoop:
    Sec += 1
    time.sleep(1)
    maintainTemp()
    if Sec == 60:
        exit()