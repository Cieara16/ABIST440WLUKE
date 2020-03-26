#Project: Brewing
#Project Details: Brew Receipt
#Course: IST 440W
#Author: Deja Vasquez
#Date Developed: 03/24/2020
#Last Date Changed: 03/26/2020

print("=======================")
print(" Balrog Brewing ")
print("=======================")

finished=False

taxRate=0.10
itemNum=0
subtotal=0.0
tax=0.0
total=0.0

while(not finished):
    prompt = "Enter price for Item #" + str(itemNum + 1) + ": $"
    price = float(input(prompt))
    if (price == 0): #Zero will end the code and print
        finished = True
    else:
        subtotal += price
        itemNum += 1
        print("\tPrice entered: ${:.2f}".format(price))

tax = subtotal * taxRate
total = subtotal + tax

print("=======================")
print("Total Items Purchased: {:d}".format(itemNum))
print("Subtotal: ${:.2f}".format(tax))
print("Total: ${:.2f}".format(total))
print("=======================")
print(" Balrog Brewing Receipt")
print("=======================")
print("Thank you for your business!")

