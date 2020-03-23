#fermenting team - Michaela Fox
#imports
#import time

#a lot of this is a palceolder for the time being to check functionality

#some list of ingrediants (going to print from service now though)
fermentingIngredients = ["hops"]
pickedIngredients = []

#setting variables
yeastAmount = 0

#function to pick ingredieants for fermenting
def PickedIngredients(fermentingIngredients, pickedIngredients):
    print()
    print(fermentingIngredients)
    userIngredient = str(input("Select an ingredient or 'exit' if you changed your mind: "))
    userIngredient = userIngredient.casefold()

    #add something
    if (userIngredient in fermentingIngredients) & (userIngredient not in pickedIngredients):
        pickedIngredients.append(userIngredient)
        print(userIngredient + "has been added to the list.")
        print(pickedIngredients)

    #user changed mind
    elif (userIngredient == 'exit'):
        return None

    #item not in the list
    elif (userIngredient not in fermentingIngredients):
        print("That ingredient is not in the list.")
        PickedIngredients(fermentingIngredients, pickedIngredients)

    #ingreidnt already in list
    elif (userIngredient in pickedIngredients):
        userIngredient = str(input("That ingredient is already picked. Would you like to pick another one? 'yes' or 'no': "))
        userIngredient = userIngredient.casefold()
        if (userIngredient == 'yes'):
            PickedIngredients(fermentingIngredients, pickedIngredients)
        elif (userIngredient == 'no'):
            return None
        else:
            userIngredient = str(input("That was not an option. 'yes' or 'no': "))
            userIngredient = userIngredient.casefold()

    #pass cuze nothing was selected
    else:
        return None

    #add another item to the list
    userIngredient = str(input("Would you like to add another ingredient? 'yes' or 'no': "))
    userIngredient = userIngredient.casefold()
    if (userIngredient == 'yes'):
        PickedIngredients(fermentingIngredients, pickedIngredients)
    elif (userIngredient == 'no'):
        return None
    else:
        userIngredient = str(input("That was not an option. Would you like to add another ingredient? 'yes' or 'no': "))
        userIngredient = userIngredient.casefold()

#function to remove ingrediants
def RemovedIngredients(fermentingIngredients, pickedIngredients):
    #nothing to remove
    if (not pickedIngredients):
        print("There are not ingredients to remove.")
        return None

    print()
    print(fermentingIngredients)
    userIngredient = str(input("Select an ingredient or 'exit' if you changed your mind: "))
    userIngredient = userIngredient.casefold()

    #remove something
    if (userIngredient in pickedIngredients):
        pickedIngredients.remove(userIngredient)
        print(userIngredient + "has been removed to the list.")
        print(pickedIngredients)

    #user changed mind
    elif (userIngredient == 'exit'):
        return None

    #item not in the list
    elif (userIngredient not in pickedIngredients):
        print("That ingredient is not in the list.")
        RemovedIngredients(fermentingIngredients, pickedIngredients)

    #ingreidnt already in list
    elif (userIngredient in pickedIngredients):
        userIngredient = istr(input("That ingredient is already removed. Would you like to remove another one? 'yes' or 'no': "))
        userIngredient = userIngredient.casefold()
        if (userIngredient == 'yes'):
            RemovedIngredients(fermentingIngredients, pickedIngredients)
        elif (userIngredient == 'no'):
            return None
        else:
            userIngredient = str(input("That was not an option. 'yes' or 'no': "))
            userIngredient = userIngredient.casefold()

    #pass cuze nothing happened
    else:
        pass

    #aremove another item to the list
    userIngredient = str(input("Would you like to remove another ingredient? 'yes' or 'no': "))
    userIngredient = userIngredient.casefold()
    if (userIngredient == 'yes'):
        RemovedIngredients(fermentingIngredients, pickedIngredients)
    else:
        return None

#function to add yeast
def AddYeast(yeastAmount):
    print()

    #adding yeast
    yeastAmount = float(input("How much yeast would you like to add: "))
    print(yeastAmount , "Will be added.")
    correctYeastAmount = str(input("Is this correct? 'yes' or 'no: "))
    correctYeastAmount = correctYeastAmount.casefold()
    #amount is correct
    if (correctYeastAmount == 'yes'):
        return None

    #amount is not correct
    elif (correctYeastAmount == 'no'):
        AddYeast(yeastAmount)

   #not a valid option
    else:
        correctYeastAmount = istr(input("That is not a valid option."))
        correctYeastAmount = correctYeastAmount.casefold()


print("This is going to be cylindraconal fermenting.")
print("This is going to be an open fermentation.")

#pick from list to add
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

#pick from list to remove
removeIngredients = str(input("Would you like to remove any ingredients? 'yes' or 'no': "))
removeIngredients = removeIngredients.casefold()
if (removeIngredients == 'yes'):
    RemovedIngredients(fermentingIngredients, pickedIngredients)
elif (removeIngredients == 'no'):
    pass
else:
    removeIngredients = str(input("That is not an option. 'yes' or 'no': "))
    removeIngredients = removeIngredients.casefold()

#adding yeast
addYeast =str(input("Would you like to add yeast: 'yes' or 'no': "))
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
print("These are the ingerients that could be picked: \n" , fermentingIngredients)
print("These are the items that will be used in the fermenting stage: \n" , pickedIngredients)
print("This is the amount of yeast that will be used: \n" , yeastAmount)
print()

#asking for 2nd fermentatiin and which kind
