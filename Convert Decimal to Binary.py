#intro display message
print('Hello!')
print('This program is constructed to convert a decimal number to binary.')
print()
def Conv_Dec2Bin(decimal):
    if decimal >= 1:
        Conv_Dec2Bin(decimal // 2)
    print(decimal % 2, end='')

#input decimal number
dec_num = int(input('Please enter a decimal number: '))
print(dec_num, 'in binary = ', end='')
Conv_Dec2Bin(dec_num)


#tested some other methods of converting decimal to binary

#decimal = int(input('Enter a decimal number: '))
#print(decimal, 'is', bin(decimal), 'in binary!')
#print(decimal, 'is', hex(decimal), 'in hexidecimal!')
          
