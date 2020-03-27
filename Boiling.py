class Brew():
    temperature = 0
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

    def minTemperature(self, maxTemp):
        maxTemp = 350
        return maxTemp
    def maxTemperature(self, minTemp):
        minTemp = 100
        return minTemp

def main(self):
    Brew()