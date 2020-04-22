import requests
import subprocess
import datetime



# Set the request parameters
def main():
    url = "https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query" \
          "=rpi_to_execute%3DClosePi%&sysparm_limit=1"

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'ruc230'
    pwd = '1%mFMHKr8QE^'

    # Set proper headers
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    ready_for_beer = True
    # Do the HTTP request
    # while (ready_for_beer):
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()

        # Decode the JSON response into a dictionary and use the data
    current_close_task = response.json()['result'][0]
    short_description = current_close_task['short_description']
    short_description = str.lower(short_description)
    number = current_close_task['number']
    description = current_close_task['description']
    description = str.lower(description)
    if short_description.find('label') != -1 or description.find('receipt') != -1:
        print_label(number)
if __name__ == "__main__":
    main()
def print_label(number):
    #url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_mother_brewv2?sysparm_query=ORDERBYDESCsys_created_on%5Enumber%3D' + number + '&sysparm_limit=1'
    #response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    #if response.status_code != 200:
        #print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        #exit()

        # Decode the JSON response into a dictionary and use the data
    #mother_brew_record = response.json()['result'][0]
    #extract abv, keg_volume, beer_name
    #current_date = datetime.now().tostring()
    #text_for_label = 'text 190,490 "Cool Island Beer\n' + current_date + '\nABV: 8.3%\n15.5 Gal"'
    #subprocess.Popen(['/usr/bin/convert', '-pointsize', '14', '-draw', text_for_label, 'beer_label.png', 'beer_label_withtext.png'])
    #subprocess.Popen(['/usr/bin/lp', '-d', 'HP_DeskJet_2130_series', '-o', 'orientation-requested=3', 'beer_label_withtext.png'])
    #CRITICAL: match up number fields, inherit from mother brew, whatever but we need to be able to match tasks up to mother brew records
