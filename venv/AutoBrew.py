#Ryan Carey, team close.
#ruc230@psu.edu
#AutoBrew system as of 3/23/2020
#references: crowpi examples

import sys
import Adafruit_DHT
import enum
import pymongo
# this is a self-pouring bucket class. it must be passed a bucketType so we know which bucket it is. The stepmotor has a pour() method which rotates one full revolution. then the gpio pins are reset.
class bucketType(enum.Enum):
    Malt = 0
    Hops = 1
    Additives = 2
class bucket():
    bucketType = bucketType.Malt
    initialWeight = 0
    def __init__(self, bucketType, bluetoothScale):
        initialWeight = bluetoothScale.get_weight() #TODO: implement bluetooth scales
        bucketFlipper = Stepmotor()
    def pour(self):
        self.bucketFlipper.turnDegrees(360)
        bucketFlipper.gpioReset()
# all ranges are assumed to be { min, max } for temperatures and matched up for the same phase. if you want 1 oz cinnamon, 2 oz vanilla added during the boil in the hopback, you would have hopBackAdditives = { "Cinnamon", "Vanilla" } and hopBackAmounts = {1, 2}
class AutoBrew():
    currentTemp = 0
    customerID = 0
    beerName = ""
    waterByWeight = 0
    waterTempRange = []
    maltTypes = []
    maltWeights = []
    hopTypes = []
    hopWeights = []
    mashTemp = 0
    mashDuration = 0
    boilTempRange = []
    boilDuration = 0
    hopBackAdditives = []
    hopBackAmounts = []
    hopBackDuration = 0
    hopBackTempRange = []
    fermentationTempRange = []
    desiredABV = 0
    def __init__(self, customerID, beerName, waterByWeight, waterTemp, maltType, maltWeight, hopTypes, hopWeight, mashTemp, mashDuration, boilTempRange, boilDuration, hopBackAdditives, hopBackAmounts, hopBackDuration, hopBackTemp, fermentationTemp, desiredABV):
        self.customerID = customerID
        self.beerName = beerName
        self.waterByWeight = waterByWeight
        self.waterTemp = waterTemp
        self.maltType = maltType
        self.maltWeight = maltWeight
        self.hopType = hopType
        self.hopWeight = hopWeight
        self.mashTemp = mashTemp
        self.mashDuration = mashDuration
        self.boilTempRange = boilTempRange
        self.boilDuration = boilDuration
        self.hopBackAdditives = hopBackAdditives
        self.hopBackAmounts = hopBackAmounts
        self.hopBackDuration = hopBackDuration
        self.hopBackTempRange = hopBackTempRange
        self.fermentationTemp = fermentationTemp
        self.desiredABV = desiredABV

#The main program controlling the whole brewing process.
    def main(self):
        newRecipe = AutoBrew()
        newRecipe.prep(boilTemp, boilDuration)
        newRecipe.pump_along()
        newRecipe.add_ingredient(maltBucket)
        newRecipe.mash(mashTemp, mashDuration)
        newRecipe.pump_along()
        newRecipe.add_ingredient(hopBucket)
        newRecipe.boil(boilTempRange, boilDuration, hopBackDuration, hopBackTempRange)
        newRecipe.pump_along()
        newRecipe.add_ingredient(additivesBucket)
        newRecipe.pump_along()
        newRecipe.exchange_heat(goalTemp)
        newRecipe.ferment(fermentationTempRange, desiredABV)
        newRecipe.bottle(beerName)
        newRecipe.print_label(productionDate, finalABV)
        newRecipe.close()

    def maintain_temp(self, container, minTemp, maxTemp): #logic to keep temperatures within a specific range using the dht11 sensor. That sensor only reads values every 2 seconds and is not waterproof, so it's not ideal. Explore other sensors.
        # set type of the sensor
        sensor = 11
        # set pin number
        pin = 4
        while (true):
            # Try to grab a sensor reading.  Use the read_retry method which will retry up
            # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            # convert the temperature to Fahrenheit.
            temperature = temperature * 9/5.0 + 32
            # Note that sometimes you won't get a reading and
            # the results will be null (because Linux can't
            # guarantee the timing of calls to read the sensor).
            # If this happens try again!
            if temperature is not None:
                self.currentTemp = temperature
                if (self.currentTemp >= maxTemp):
                    AutoBrew.reduce_heat() #needs implementing probably just turning off the heating element, but could have a section for the heat exchanger as well
                    return "Running too hot: " + self.currentTemp
                elif (self.currentTemp <= minTemp):
                    AutoBrew.heat_up() #needs implementing. Turn on a heating element.
                    return "Running too cool: " + self.currentTemp
                elif (minTemp <= self.currentTemp <= maxTemp):
                    return self.currentTemp
            else:
                print('Failed to get reading. Try again!')
    def add_ingredient(self, bucket):
        bucket.pour()
    def pump_along(self):
        return #TODO: implement pumps an array of pumps, step through the array as we go
    def close(self):
        newRecipe.print_label(productionDate, finalABV) #implement

# This section comes from the crowpi kit directly. I left it as is.
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
        GPIO.setup(self.pin_A, GPIO.OUT)
        GPIO.setup(self.pin_B, GPIO.OUT)
        GPIO.setup(self.pin_C, GPIO.OUT)
        GPIO.setup(self.pin_D, GPIO.OUT)
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
    def turn(self, count):
        for i in range(int(count)):
            self.Step1()
            self.Step2()
            self.Step3()
            self.Step4()
            self.Step5()
            self.Step6()
            self.Step7()
            self.Step8()
    def gpioReset(self):
        # cleanup the GPIO pin use
        GPIO.cleanup()
    def turnSteps(self, count):
        # Turn n steps
        # (supply with number of steps to turn)
        for i in range(count):
            self.turn(1)
    def turnDegrees(self, count):
        # Turn n degrees (small values can lead to inaccuracy)
        # (supply with degrees to turn)
        self.turn(round(count * 512 / 360, 0))