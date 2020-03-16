#Justin Hill

print('Create a password and then enter it again to gain access. If you enter a wrong password 3 times incorrectly it will lock out your account')
print()
password = input('Create a password: ')
user_input = input('Enter your password again: ')
pw_attempt = 0

while user_input != password:
    print('Wrong passowrd, Try again')
    user_input = input('Enter your password: ')
    pw_attempt = pw_attempt + 1
    if pw_attempt == 3:
        print('Account locked')
        break
    

print('Access Granted')


















#    print('You must change your password before you can continue')
#    user_input2 = str(input('Enter your knew password: '))
#    print('Password changed successfully!')
#    print('Your new passowrd is', user_input2)

#if password == user_input2:
#    print('Access granted')
#else:
#    print('Access denied')

    

