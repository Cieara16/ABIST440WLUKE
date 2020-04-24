import requests
import subprocess
import datetime
emptyList = []

def print_label(beer_name, abv, keg_volume, current_date):
    text_for_label = 'text 190,490 "' + beer_name + ' ' + current_date + ' ABV: ' + abv + '% ' + keg_volume + ' Gal"'
    label_write = subprocess.Popen(['/usr/bin/convert', '-pointsize', '18', '-draw', text_for_label, 'beer_label.png', 'beer_label_withtext.png'])
    label_write.wait()
    #subprocess.Popen(['/usr/bin/lp', '-d', 'HP_DeskJet_2130_series', '-o', 'orientation-requested=3', 'beer_label_withtext.png'])
    

def patch_brew_task(task_id):
    user = 'kasper440'
    pwd = 'kasper440'

    # Set proper headers
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/' + task_id
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.patch(url, auth=(user, pwd), headers=headers, data="{\"state\":\"3\"}")
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()
        
        
# Set the request parameters
def get_from_any_table(url):

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'kasper440'
    pwd = 'kasper440'

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
    return response.json()['result']


def main():
    current_close_task = get_from_any_table("https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=ORDERBYDESCnumber%5Erpi_to_execute%3DClosePi%5Estate%3D-5&sysparm_limit=1")
    while (current_close_task != emptyList):
        short_description = current_close_task['short_description']
        short_description = str.lower(short_description)
        description = current_close_task['description']
        description = str.lower(description)
        task_id = current_close_task['sys_id']
        mother_brew_record = get_from_any_table(current_close_task['mother_brew_task']['link'])
        abv = mother_brew_record['abv']
        keg_volume = mother_brew_record['keg_volume']
        beer_name = mother_brew_record['beer_name']
        current_date = datetime.datetime.now().strftime("%b %d %Y")
        if short_description.find('label') != -1 or description.find('label') != -1:
            print_label(beer_name, abv, keg_volume, current_date)
            patch_brew_task(task_id)
        current_close_task = get_from_any_table("https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=ORDERBYDESCnumber%5Erpi_to_execute%3DClosePi%5Estate%3D-5&sysparm_limit=1")
            


if __name__ == "__main__":
    main()
    
    



