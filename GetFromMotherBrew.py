# Justin Hill - Team Boil
# Ryan Carey - Team Close
import requests
import time

def Loop():
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=sys_created_onRELATIVEGT%40minute%40ago%401&sysparm_limit=1'
    user = 'kasper440'
    pwd = 'kasper440'
    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    result = response.json()['result']
    emptyList = []

    while (result == emptyList):
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=sys_created_onRELATIVEGT%40minute%40ago%401&sysparm_limit=1'
        user = 'kasper440'
        pwd = 'kasper440'
        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        result = response.json()['result']
        emptyList = []
        print(result)
        time.sleep(25)
    if (result != emptyList):
        #import Your Main Program name here. E.x. BoilPhase.py but do not include the .py

Loop()




