#Justin Hill
#Programming-2 (Decision Making)

print('This program will calculate the cost to ship an item that weighs a certain amount')
print()
weight = float(input('Please enter the weight of the package(in lbs): '))
cost = float(0)

if weight < 0:
    print('Invalid input value!')
elif 0 <= weight <= 2:
    cost = 1.50
    print('Shipping cost = $', cost)
elif 2 < weight < 6:
    cost = 3
    print('Shipping cost = $', cost)
elif 6 <= weight < 10:
    cost = 4
    print('Shipping cost = $', cost)
else:
    cost = 4.75
    print('Shipping cost = $', cost)
