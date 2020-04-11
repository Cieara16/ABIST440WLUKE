#Need to install requests package for python
#easy_install requests
import requests
from AlcCont import alcohol_input
# Set the request parameters
url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_recipe?sysparm_fields=alcohol_content'

# Eg. User name="admin", Password="admin" for this code sample.
user = 'mak6311'
pwd = 'Mak77433'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
response = requests.post(url, auth=(user, pwd), headers=headers ,data="{\"alcohol_content\":\""+str(alcohol_input)+"\"}")

# Check for HTTP codes other than 200
if response.status_code != 200:
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()

# Decode the JSON response into a dictionary and use the data
data = response.json()
print(data)