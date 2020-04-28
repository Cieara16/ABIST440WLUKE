import requests
import subprocess
import datetime
import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO


# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDBackpack(address=0x21)
emptyList = []


def print_label(beer_name, abv, keg_volume, current_date):
    label_line_1 = 'text 190,490 "' + beer_name + ' ' + current_date
    label_line_2 = 'text 190,520 "' + 'ABV: ' + abv + '% ' + keg_volume + ' Gal"'
    label_write_line_1 = subprocess.Popen(['/usr/bin/convert', '-pointsize', '18', '-draw', label_line_1, 'beer_label.png', 'beer_label_withtext.png'])
    label_write_line_1.wait()
    label_write_line_2 = subprocess.Popen(['/usr/bin/convert', '-pointsize', '18', '-draw', label_line_2, 'beer_label_withtext.png', 'beer_label_finished.png'])
    label_write_line_2.wait()
    #printing i9s commented out atm to save paper
    lcd.message("label printing")
    #subprocess.Popen(['/usr/bin/lp', '-d', 'HP_DeskJet_2130_series', '-o', 'orientation-requested=3', 'beer_label_finished.png'])
    

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
        exit()

        # Decode the JSON response into a dictionary and use the data
    return response.json()['result']


def main():
    while (get_from_any_table("https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=ORDERBYDESCsys_created_on%5Erpi_to_execute%3DClosePi%5Estate%3D-5&sysparm_limit=1") != emptyList):
        current_close_task = get_from_any_table("https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_lkbrewtask?sysparm_query=ORDERBYDESCsys_created_on%5Erpi_to_execute%3DClosePi%5Estate%3D-5&sysparm_limit=1")[0]
        short_description = current_close_task['short_description']
        short_description = short_description.lower()
        description = current_close_task['description']
        description = description.lower()
        task_id = current_close_task['sys_id']
        try:
            mother_brew_record = get_from_any_table(current_close_task['mother_brew_task']['link'])
        except:
            print("The task is missing a reference to mother brew table, or there is no task.")
            break
        abv = mother_brew_record['abv']
        keg_volume = mother_brew_record['keg_volume']
        beer_name = mother_brew_record['beer_name']
        current_date = datetime.datetime.now().strftime("%b %d %Y")
        if short_description.startswith('print') != -1 or description.startswith('print') != -1:
            print_label(beer_name, abv, keg_volume, current_date)
            patch_brew_task(task_id)
            time.sleep(5)
        elif short_description.startswith('attach') != -1 or description.startswith('attach') != -1:
            input("Press enter when the label has been attached...")
            patch_brew_task(task_id)
            time.sleep(5)


    time.sleep(5)
    lcd.message("No tasks")
    time.sleep(2)
    lcd.message("refreshing...")
    main()


if __name__ == "__main__":
    main()
    
    



