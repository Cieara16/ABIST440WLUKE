#Justin Hill
#Programming-1 (Basic Data Process)

#Write a program to calculate net pay a worker should receive. The program asks the user to enter work hours and pay rate for a worker, and then calculates and displays how much the worker should be paid.
#Assuming income tax rate to be 5%, the net pay for the worker should be calculated as

#pay rate * work hours * (1 - 0.05)

print('Hello!')
print('This program will calculate your net pay.')
print()
hours = float(input('Please enter the hours that you have worked: '))
rate = float(input('Please enter your hourly wage: '))
print()
gross_pay = hours * rate
net_pay = hours * rate * (1 - 0.05)
taxes = gross_pay - net_pay
#added some extra steps here for better formating
print('Hours worked: ', hours)
print('Pay rate: ', rate)
print('Your gross pay is: ', gross_pay)
print('Total taxes deducted: ', taxes)
print()
print('Your net pay is: ', net_pay)

