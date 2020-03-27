#Begin Brew class
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
        

    def maxTemperature(self, maxTemp):
        maxTemp = 350
        #if boil.temperature >= maxTemp:
        #print('Too hot, reducing heat...')
        #maintainTemp()
        return maxTemp
    def minTemperature(self, minTemp):
        minTemp = 100
        return minTemp

def main(self):
    Brew()
    #work in progress
    #new