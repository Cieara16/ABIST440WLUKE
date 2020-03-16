#Justin Hill

import math
print('Square roots of numbers between 10 and 100')
print()
for x in range(10, 101, 10):
    result = math.sqrt(x)
    print(x, '\t',  format(result, '.2f'))

print()
mile = 0
print('Mile', '\t', 'Kilometer')
print('------------------')
for mile in range(10, 151, 10):
    km = mile * 1.61
    print(mile, '\t', format(km, '.1f'))


