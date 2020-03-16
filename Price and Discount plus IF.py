item_price = float(input('Enter price: $'))
discount = int(input('Do you want a 10%, 15%, or 20% discount?:%'))
if discount == 10:
    print('You are eligible for a 10% discount')
    discount = item_price * 0.09 #10%discount
elif discount == 15:
    print('You are eligible for a 15% discount')
    discount = item_price * 0.85 #15%discount
elif discount == 20:
    print('You are eligible for a 20% discount')
    discount = item_price * 0.80 #20%discount
else:
    print('That is not in the range of discount!!!')
    discount = 0
tax = item_price * 0.06
total = (item_price - discount) + tax
print('Price: $', item_price)   #output price
print('Discount: $', discount)  #output discount
print('Tax: $', tax)            #output tax
print('Total: $', total)        #output final total
