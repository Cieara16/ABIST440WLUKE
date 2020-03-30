#Begin Brew class
import time

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



def boil(self):
        #method for maintaining temperature
        #Work in progress

def maintainTemp(self):
    #method for maintaining temperature
    #for i in range[minTemperature]:
    #temperature -= temperature

    maxTemp = 110
    minTemp = 100

    #assuming temp is recorded as celsius would this work with the pi? Could we set this in the while loop timer below having it constantly record and check temp?
    if self.temperature < minTemp:
        self.temperature += 10
        print('Too cold, increasing heat...')
        return self
    elif self.temperature > maxTemp:
        self.temperature -= 10
        print('Too hot, reducing heat...')
        return self.temperature
    else:
        return self.temperature

"""
    def maxTemperature(self, maxTemp):
        maxTemp = 110
        #if boil.temperature >= maxTemp:
        #print('Too hot, reducing heat...')
        #maintainTemp()
        return maxTemp
    def minTemperature(self, minTemp):
        minTemp = 100
        return minTemp
"""

def main(self):
    Brew()

Sec = 0
timeLoop = True

# Begin Process. Not sure if we should include a 60min timer for boiling or leave that for the Brew master in between steps
while timeLoop:
    Sec += 1
    time.sleep(1)
    if Sec == 3600:
        #I suppose code to execute and control temp with boiling will go here?
        exit()