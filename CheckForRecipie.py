# Team Ferment - James Bee, Virginia Hoffman, Michaela Fox, and Samantha Scheer
# IST 440 - Luke Kasper

# Justin Hill - Team Boil
# Ryan Carey - Team Close

import requests
import json
import time

#main code
def TeamFerment():
    import TeamFerment

def CheckForRecipies():
    # Set the request parameters
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=state%3D-5%5Erpi_to_execute%3DFermentPi&sysparm_limit=1'
    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'kasper440'
    pwd = 'kasper440'
    
    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    
    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers )
    
    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    
    # Decode the JSON response into a dictionary and use the data
    result = response.json()['result']
    list = []
    
    while (result == list):
        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=state%3D-5%5Erpi_to_execute%3DFermentPi&sysparm_limit=1'
        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'kasper440'
        pwd = 'kasper440'
        
        # Set proper headers
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        
        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers )
        
        # Check for HTTP codes other than 200
        if response.status_code != 200: 
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()
            
       # Decode the JSON response into a dictionary and use the data
        result = response.json()['result']
        list = []
        print(result)
        time.sleep(25)
        if (result != list):
            TeamFerment()
            
CheckForRecipies()
