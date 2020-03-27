#Project: Brewing
#Project Details: Brew Shipping Label
#Course: IST 440W
#Author: Deja Vasquez
#Date Developed: 03/25/2020
#Last Date Changed: 03/27/2020

def main():
    print('This program will calculate shipping, handling and taxes on your purchase.')
    calcSubtotal()

def calcSubtotal():
    while True:
        subtotal = float(input('Enter your subtotal please: '))
        if subtotal >= 1 and subtotal <= 9999:
            print('This is a valid amount.')
            break
        else:
            print('Invalid amount, please try again.')
            continue
    calcShipping(subtotal)

def calcShipping(subtotal):
    shippingCost = subtotal * .10
    calcHandling(subtotal, shippingCost)

def calcHandling(subtotal, shippingCost):
    handlingFee = 0
    if subtotal < 100:
        print('Your order is less $100.00, there is a 2 dollar handling fee.')
        handlingFee += 2
    else:
        print('Yay! Your order is more than $100.00, there is no handling fee.')
    calcTax(subtotal, shippingCost, handlingFee)

def calcTax(subtotal, shippingCost, handlingFee):
    tax = subtotal * .08
    calcTotal(subtotal, shippingCost, handlingFee, tax)

def calcTotal(subtotal, shippingCost, handlingFee, tax):
    print('\nProduct Total Information')
    print('\tSubtotal: ${}'.format(subtotal))
    print('\tShipping: ${}'.format(shippingCost))
    print('\tHandling: ${}'.format(handlingFee))
    print('\tSales tax: ${}'.format(tax))
    total: object = subtotal + shippingCost + handlingFee + tax
    print('\tGrand total: ${}'.format(total))

main()
