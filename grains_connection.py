import requests
global grain, grain_weight

def get():
        #Need to install requests package for python
        #easy_install requests

        # Set the request parameters
        url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_ingredients?sysparm_query=Active%20%3D%20true&sysparm_fields=grain_weight%2Cgrains&sysparm_limit=1'

        # Eg. User name="admin", Password="admin" for this code sample.
        user = 'Amp6826'
        pwd = 'Swami101'

        # Set proper headers
        headers = {"Content-Type":"application/json","Accept":"application/json"}

        # Do the HTTP request
        response = requests.get(url, auth=(user, pwd), headers=headers )

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        grain = response.json()['result'][0]['grain']
        grain_weight = response.json()['result'][0]['grain_weight']
        print('Grain: ' + grain)
        print('Grain weight: ' + grain_weight)
        return grain, grain_weight
get()