alcohol_input = float (input ("Enter alcohol percentage: "))
doubleChecking = input("Are you sure you want to enter "+str(alcohol_input)+"? (Y or N)").upper()
if doubleChecking == "Y":
    while alcohol_input < 2 or alcohol_input > 15:
        print("Please choose again, alcohol content has to be between 2 and 15")
        alcohol_input = float( input ("Enter alcohol percentage: "))
    print("Alcohol percent selected is " + str(alcohol_input) + "%")

if doubleChecking == "N":
    alcohol_input = float(input("Enter alcohol percentage: "))
    print(alcohol_input)