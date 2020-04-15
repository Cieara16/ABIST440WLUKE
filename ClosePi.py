import requests
import subprocess
# Set the request parameters
url = "https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query" \
      "=rpi_to_execute%3DClosePi%5Estate%3D-5&sysparm_limit=1"

# Eg. User name="admin", Password="admin" for this code sample.
user = 'ruc230'
pwd = '1%mFMHKr8QE^'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}
ready_for_beer = True
# Do the HTTP request
#while (ready_for_beer):
response = requests.get(url, auth=(user, pwd), headers=headers )

# Check for HTTP codes other than 200
if response.status_code != 200:
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()

    # Decode the JSON response into a dictionary and use the data
current_close_task = response.json()['result'][0]
short_description = current_close_task['short_description']
short_description = str.lower(short_description)
description = current_close_task['description']
description = str.lower(description)

print(description + '\n' + short_description)
#if (short_description.find('receipt') != -1 or description.find('receipt') != -1):

