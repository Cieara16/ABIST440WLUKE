# Team Ferment - James Bee, Virginia Hoffman, Michaela Fox, and Samantha Scheer
# IST 440 - Luke Kasper

import requests
import json
import time

def CheckForRecipies():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=sys_created_onRELATIVEGT%40minute%40ago%401&sysparm_limit=1'
    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'mmf5571'
    pwd = 'Werewolf00'

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)
    
    startTask = response.json()['result'][0]['rpi_to_execute']
    FermentPi = startTask['FermentPi']
    
    list = {}
    
    while (data == list):
         # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=sys_created_onRELATIVEGT%40minute%40ago%401&sysparm_limit=1'
        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'mmf5571'
        pwd = 'Werewolf00'

        # Set proper headers
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers)
         # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()
    
        # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)
        list = {}
        time.sleep(25)
        
        if(data != list):
            import TeamFerment
            
CheckForRecipies()