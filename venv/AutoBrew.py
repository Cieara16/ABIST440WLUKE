#Ryan Carey, team close.
#ruc230@psu.edu
#AutoBrew system as of 3/18/2020
#references: crowpi examples

import sys
import Adafruit_DHT
import enum
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
    def close(self):
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
class AutoBrew():
    currentTemp = 0
    waterByWeight = 0
    waterTemp = 0
    maltTypes = []
    maltWeights = []
    hopTypes = []
    hopWeights = []
    mashTemp = 0
    mashDuration = 0
    boilTemp = 0
    boilDuration = 0
    hopBackAdditives = []
    hopBackAmounts = []
    hopBackDuration = 0
    hopBackTemp = 0
    fermentationTemp = 0
    desiredABV = 0
    def __init__(self, waterByWeight, waterTemp, maltType, maltWeight, hopTypes, hopWeight, mashTemp, mashDuration, boilTemp, boilDuration, hopBackAdditives, hopBackAmounts, hopBackDuration, hopBackTemp, fermentationTemp, desiredABV):
        self.waterByWeight = waterByWeight
        self.waterTemp = waterTemp
        self.maltType = maltType
        self.maltWeight = maltWeight
        self.hopType = hopType
        self.hopWeight = hopWeight
        self.mashTemp = mashTemp
        self.mashDuration = mashDuration
        self.boilTemp = boilTemp
        self.boilDuration = boilDuration
        self.hopBackAdditives = hopBackAdditives
        self.hopBackAmounts = hopBackAmounts
        self.hopBackDuration = hopBackDuration
        self.hopBackTemp = hopBackTemp
        self.fermentationTemp = fermentationTemp
        self.desiredABV = desiredABV

    def main(self):
        newRecipe = AutoBrew(input("Enter the amount of water to be used: "), input("Enter the initial water temperateure: "), input("Enter the malt type: "), input("Enter the malt weight: "), input("Enter the hop  separated with commas").split(',').trim(" "), input("Enter the desired amount of hops by weight: "), input("Enter the mashing temp"), input("Enter the mash duration"), input("Enter the boiling temp"), input("Enter the boil duration: "), input("Enter the additives: ").split(',').trim(' '), input("Enter the additive amounts: ").split(',').trim(' '), input("Enter the hopback duration: "), input("Enter the hopback temperature: "), input("Enter the fermentation temp: "), input("Enter the desired abv: "))
        newRecipe.prep(boilTemp, boilDuration)
        newRecipe.pump_along()
        newRecipe.add_ingredient(maltBucket)
        newRecipe.mash(mashTemp, mashDuration)
        newRecipe.pump_along()
        newRecipe.add_ingredient(hopBucket)
        newRecipe.boil(boilTemp, boilDuration)
        newRecipe.pump_along()
        newRecipe.add_ingredient(additivesBucket)
        newRecipe.hopBack(hopBackDuration, hopBackTemp)
        newRecipe.pump_along()
        newRecipe.exchange_heat(goalTemp)
        newRecipe.ferment(fermentationTemp, desiredABV)
        newRecipe.bottle()
        newRecipe.print_label()

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
                    AutoBrew.reduce_heat() #needs implementing
                    return "Running too hot: " + self.currentTemp
                elif (self.currentTemp <= minTemp):
                    AutoBrew.heat_up() #needs implementing
                    return "Running too cool: " + self.currentTemp
                elif (minTemp <= self.currentTemp <= maxTemp):
                    return self.currentTemp
            else:
                print('Failed to get reading. Try again!')
    def add_ingredient(self, bucket):
        bucket.pour()
    def pump_along(self):
        return #TODO: implement pumps an array of pumps, step through the array as we go
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
    def close(self):
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