# fermenting team - Michaela Fox
# imports
import AutoBrew
import RPi.GPIO as GPIO
import time
import requests
import Adafruit_DHT
import os
import sys, subprocess

# a lot of this is a palceolder for the time being to check functionality

# some list of ingrediants (going to print from service now though)
fermentingIngredients = ["hops"]
pickedIngredients = []

# setting variables (temp)
currentTempC = 0
currentTempF = 0

# (ingrediants)
yeastAmount = 0
fermentType = ""
secondFerment = ""

# setting variables (temp)
tempSensor = Adafruit_DHT.DHT11
tempPin = 4


# function to et temp reading
def TempReading(tempSensor, tempPin):
    temperature = Adafruit_DHT.read(tempSensor, tempPin)
    return temperature
    time.sleep(1)

# temp as a subprocess to run in background
# currentTemp = subprocess.Popen(TempReading(tempSensor, tempPin), shell=True)

secondFerment = ""

# function to pick ingredieants for fermenting
def PickedIngredients(fermentingIngredients, pickedIngredients):
    print()
    print(fermentingIngredients)
    userIngredient = str(input("Select an ingredient or 'exit' if you changed your mind: "))
    userIngredient = userIngredient.casefold()

    # add something
    if (userIngredient in fermentingIngredients) & (userIngredient not in pickedIngredients):
        pickedIngredients.append(userIngredient)
        print(userIngredient + "has been added to the list.")
        print(pickedIngredients)

    # user changed mind
    elif (userIngredient == 'exit'):
        return None

    # item not in the list
    elif (userIngredient not in fermentingIngredients):
        print("That ingredient is not in the list.")
        PickedIngredients(fermentingIngredients, pickedIngredients)

    # ingreidnt already in list
    elif (userIngredient in pickedIngredients):
        userIngredient = str(
            input("That ingredient is already picked. Would you like to pick another one? 'yes' or 'no': "))
        userIngredient = userIngredient.casefold()
        if (userIngredient == 'yes'):
            PickedIngredients(fermentingIngredients, pickedIngredients)
        elif (userIngredient == 'no'):
            return None
        else:
            userIngredient = str(input("That was not an option. 'yes' or 'no': "))
            userIngredient = userIngredient.casefold()

    # pass cuze nothing was selected
    else:
        return None

    # add another item to the list
    userIngredient = str(input("Would you like to add another ingredient? 'yes' or 'no': "))
    userIngredient = userIngredient.casefold()
    if (userIngredient == 'yes'):
        PickedIngredients(fermentingIngredients, pickedIngredients)
    elif (userIngredient == 'no'):
        return None
    else:
        userIngredient = str(input("That was not an option. Would you like to add another ingredient? 'yes' or 'no': "))
        userIngredient = userIngredient.casefold()


# function to remove ingrediants
def RemovedIngredients(fermentingIngredients, pickedIngredients):
    # nothing to remove
    if (not pickedIngredients):
        print("There are not ingredients to remove.")
        return None

    print()
    print(fermentingIngredients)
    userIngredient = str(input("Select an ingredient or 'exit' if you changed your mind: "))
    userIngredient = userIngredient.casefold()

    # remove something
    if (userIngredient in pickedIngredients):
        pickedIngredients.remove(userIngredient)
        print(userIngredient + "has been removed to the list.")
        print(pickedIngredients)

    # user changed mind
    elif (userIngredient == 'exit'):
        return None

    # item not in the list
    elif (userIngredient not in pickedIngredients):
        print("That ingredient is not in the list.")
        RemovedIngredients(fermentingIngredients, pickedIngredients)

    # ingreidnt already in list
    elif (userIngredient in pickedIngredients):
        userIngredient = str(input("That ingredient is already removed. Would you like to remove another one? 'yes' or 'no': "))
        userIngredient = userIngredient.casefold()
        if (userIngredient == 'yes'):
            RemovedIngredients(fermentingIngredients, pickedIngredients)
        elif (userIngredient == 'no'):
            return None
        else:
            userIngredient = str(input("That was not an option. 'yes' or 'no': "))
            userIngredient = userIngredient.casefold()

    # pass cuze nothing happened
    else:
        pass

    # aremove another item to the list
    userIngredient = str(input("Would you like to remove another ingredient? 'yes' or 'no': "))
    userIngredient = userIngredient.casefold()
    if (userIngredient == 'yes'):
        RemovedIngredients(fermentingIngredients, pickedIngredients)
    else:
        return None


# function to add yeast
def AddYeast(yeastAmount):
    print()

    # adding yeast
    yeastAmount = float(input("How much yeast would you like to add or 'exit' if you changed your mind: "))
    print(yeastAmount, "Will be added.")
    correctYeastAmount = str(input("Is this correct? 'yes' or 'no: "))
    correctYeastAmount = correctYeastAmount.casefold()
    # amount is correct
    if (correctYeastAmount == 'yes'):
        return None

    # amount is not correct
    elif (correctYeastAmount == 'no'):
        AddYeast(yeastAmount)

    #user changed mind
    elif (yeastAmount == 'exit'):
        return None

    # not a valid option
    else:
        correctYeastAmount = str(input("That is not a valid option."))
        correctYeastAmount = correctYeastAmount.casefold()

#class for snd fermenting types
class FermentingTypes():

    #function for krausening
    def Krausening(secondFerment):
        print("Adding the fermenting wart and fresh carbon dioxide.")
        print("Moved to the conditioning tank.")
        print("Sending off to be bottled.")

    #function for laggering
    def Laggering(secondFerment):
        storageTime = int(input("How many months would you like it to be stored for? 1 - 6 Months: "))
        if (storageTime > 0 & storageTime < 7):
            for storageTime in 1, 7:
                print(storageTime, "months was selected.")
                print("Storage time complete.")
        elif storageTime < 1 & storageTime > 6:
            while (storageTime < 1 | storageTime > 6):
                storageTime = int(input("That is not a valid option. 1 - 6 Months: "))
        print("Sending off to bottle.")

    #function for secondary
    def SecondaryFermentation(secondFerment):
        print("Refermenting.")
        print("Sending off to bottle.")

    #function for bottle
    def Bottle(secondFerment):
        addSugar = str(input("Would you like to add more sugar? 'yes' or 'no': "))
        addSugar = addSugar.casefold()

        #add suagr
        if (addSugar == 'yes'):
            sugarAmount = input("How much would you like to add or 'exit': ")
            sugarAmount = sugarAmount.casefold()
            if (sugarAmount == 'exit'):
                pass
            else:
                print(sugarAmount, "will be added.")
                print("Sugar has been added.")

        addWart = str(input("Would you like to add more wart? 'yes' or 'no': "))
        addWart = addSugar.casefold()
        # add wart
        if (addWart == 'yes'):
            wartAmount = input("How much would you like to add or 'exit': ")
            wartAmount = wartAmount.casefold()
            if (wartAmount == 'exit'):
                pass
            else:
                print(wartAmount, "will be added.")
                print("Wart has been added.")

        print("Sending to bottle.")

    #function of cask
    def CackConditioning(secondFerment):
        print("Putting into cask.")
        print("Fermenting.")
        print("Sending off to bottle.")

    #function for barrel
    def BarrelAging(secondFerment):
        print("Putting into barrel.")
        print("Fermenting.")
        print("Sending to bottle")

#temp reading beofre start of anything
print("Current temperature and humidity: ")
print(TempReading(tempSensor, tempPin))

print("This is going to be cylindraconal fermenting.")
print("This is going to be an open fermentation.")

# pick from list to add
print(fermentingIngredients)
addIngredients = str(input("Would you like to add any ingredients? 'yes' or 'no': "))
addIngredients = addIngredients.casefold()
if (addIngredients == 'yes'):
    PickedIngredients(fermentingIngredients, pickedIngredients)
elif (addIngredients == 'no'):
    pass
else:
    addIngredients = str(input("That is not an option. 'yes' or 'no': "))
    addIngredients = addIngredients.casefold()

# pick from list to remove
removeIngredients = str(input("Would you like to remove any ingredients? 'yes' or 'no': "))
removeIngredients = removeIngredients.casefold()
if (removeIngredients == 'yes'):
    RemovedIngredients(fermentingIngredients, pickedIngredients)
elif (removeIngredients == 'no'):
    pass
else:
    removeIngredients = str(input("That is not an option. 'yes' or 'no': "))
    removeIngredients = removeIngredients.casefold()

# adding yeast
addYeast = str(input("Would you like to add yeast: 'yes' or 'no': "))
addYeast = addYeast.casefold()
if (addYeast == 'yes'):
    AddYeast(yeastAmount)
elif (addYeast == 'no'):
    pass
else:
    addYeast = str(input("That is not an option. 'yes' or 'no': "))
    addYeast = addYeast.casefold()

print()
print("Test: ")
print("These are the ingredients that could be picked: \n", fermentingIngredients)
print("These are the items that will be used in the fermenting stage: \n", pickedIngredients)
print("This is the amount of yeast that will be used: \n", yeastAmount)
print()

# asking for 2nd fermenting and which kind
print("The types of secondary fermenting that area available are: \n'"
          "(1)Krausening', '(2)Laggering', '(3)Secondary Ferment', '(4)Bottle', (5)'Cask Conditioning', and '(6)Barrel Aging'\n")
secondFerment = str(input("Which type of secondary fermenting type would you like to pick or 'exit' to send to bottle: "))
secondFerment = secondFerment.casefold()

if (secondFerment == '1'):
    print("Current temperature and humidity: ")
    print(TempReading(tempSensor, tempPin))
    FermentingTypes.Krausening(secondFerment)

elif (secondFerment == '2'):
    print("Current temperature and humidity: ")
    print(TempReading(tempSensor, tempPin))
    FermentingTypes.Laggering(secondFerment)

elif (secondFerment == '3'):
    print("Current temperature and humidity: ")
    print(TempReading(tempSensor, tempPin))
    FermentingTypes.SecondaryFermentation(secondFerment)

elif (secondFerment == '4'):
    FermentingTypes.Bottle(secondFerment)
    print("Current temperature and humidity: ")
    print(TempReading(tempSensor, tempPin))


elif(secondFerment == '5'):
    print("Current temperature and humidity: ")
    print(TempReading(tempSensor, tempPin))
    FermentingTypes.CackConditioning(secondFerment)

elif (secondFerment == '6'):
    print("Current temperature and humidity: ")
    print(TempReading(tempSensor, tempPin))
    FermentingTypes.BarrelAging(secondFerment)

elif (secondFerment == 'exit'):
    print("Current temperature and humidity: ")
    print(TempReading(tempSensor, tempPin))
    print("Sending to bottle.")
    pass
else:
    secondFerment = str(input("That was not an option. 'yes' or 'no': "))
    secondFerment = secondFerment.casefold()

