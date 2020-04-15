import requests
test = '0.25 oz. (7 g) Cashmere hops, 8.3% a.a. (60 min) '
url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_ingredients?sysparm_limit=1'

# Eg. User name="admin", Password="admin" for this code sample.
user = 'ruc230'
pwd = '1%mFMHKr8QE^'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
response = requests.get(url, auth=(user, pwd), headers=headers )

# Check for HTTP codes other than 200
if response.status_code != 200:
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()

# Decode the JSON response into a dictionary and use the data
data = response.json()
data = data['result'][0]
hops = data['hops']
print(hops)
amountIndex = test.find(')')
testAmount = test[:amountIndex+1]
print(testAmount)

