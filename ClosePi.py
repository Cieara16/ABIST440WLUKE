import requests
import subprocess
import datetime
import time
emptyList = []
user = 'kasper440'
pwd = 'kasper440'
headers = {"Content-Type": "application/json", "Accept": "application/json"}


def print_label(beer_name, abv, keg_volume, current_date):
    label_line_1 = 'text 190,490 "' + beer_name + ' ' + current_date
    label_line_2 = 'text 190,520 "' + 'ABV: ' + abv + '% ' + keg_volume + ' Gal"'
    label_write_line_1 = subprocess.Popen(['/usr/bin/convert', '-pointsize', '18', '-draw', label_line_1, 'beer_label.png', 'beer_label_withtext.png'])
    label_write_line_1.wait()
    label_write_line_2 = subprocess.Popen(['/usr/bin/convert', '-pointsize', '18', '-draw', label_line_2, 'beer_label_withtext.png', 'beer_label_finished.png'])
    label_write_line_2.wait()
    #printing is now live
    print("label printing")
    #subprocess.Popen(['/usr/bin/lp', '-d', 'HP_DeskJet_2130_series', '-o', 'orientation-requested=3', 'beer_label_finished.png'])


def post_start_time(mother_brew_number, start_time):
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table'

    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd), headers=headers,
                             data="{\"number\":\"" + mother_brew_number + "\",\"close_start_time\":\"" + str(start_time) + "\"}")
    if response.status_code != 201:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()
    return response.json()['result']['sys_id']


def patch_end_time(log_post_sys_id, end_time):
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_log_table/' + log_post_sys_id
    response = requests.patch(url, auth=(user, pwd), headers=headers, data="{\"close_end_time\":\"" + str(end_time) + "\"}")
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()


def patch_brew_task(task_id):
    # Set proper headers
    url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask/' + task_id
    response = requests.patch(url, auth=(user, pwd), headers=headers, data="{\"state\":\"3\"}")
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
        exit()
        
        
# Set the request parameters
def get_from_any_table(url):
    # Set proper headers    ready_for_beer = True
    # Do the HTTP request
    # while (ready_for_beer):
    response = requests.get(url, auth=(user, pwd), headers=headers)
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        exit()
    # Decode the JSON response into a dictionary and use the data
    return response.json()['result']


def main():
    while (get_from_any_table("https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=ORDERBYDESCsys_created_on%5Erpi_to_execute%3DClosePi%5Estate%3D-5&sysparm_limit=1") != emptyList):
        current_close_task = get_from_any_table("https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=ORDERBYDESCsys_created_on%5Erpi_to_execute%3DClosePi%5Estate%3D-5&sysparm_limit=1")[0]
        start_time = datetime.datetime.now()
        short_description = current_close_task['short_description']
        short_description = short_description.lower()
        description = current_close_task['description']
        description = description.lower()
        task_id = current_close_task['sys_id']
        try:
            mother_brew_record = get_from_any_table(current_close_task['mother_brew_task']['link'])
            print('Task Found')
        except: 
            print('No Task')
            break
        mother_brew_number = mother_brew_record['number']
        log_post_sys_id = post_start_time(mother_brew_number, start_time)
        abv = mother_brew_record['abv']
        keg_volume = mother_brew_record['keg_volume']
        beer_name = mother_brew_record['beer_name']
        current_date = datetime.datetime.now().strftime("%b %d %Y")
        if short_description.startswith('print') or description.startswith('print'):
            print_label(beer_name, abv, keg_volume, current_date)
            patch_brew_task(task_id)
            time.sleep(5)
        elif short_description.startswith('attach') or description.startswith('attach'):
            input("Press enter when the label has been attached...")
            patch_brew_task(task_id)
            end_time = datetime.datetime.now()
            patch_end_time(log_post_sys_id, end_time)
            time.sleep(5)
    time.sleep(2)
    print('Refreshing...')
    time.sleep(5)
    main()


if __name__ == "__main__":
    main()
    
    



