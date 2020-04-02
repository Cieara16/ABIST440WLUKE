# Need to install requests package for python
# easy_install requests
import requests
# URL for Recipe table in servicenow
# Set the request parameters, and you need to add "sys_id" where "undefined" to update that specific data
url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_recipe/undefined?sysparm_fields=sys_id%2Csys_updated_by%2Csys_created_on%2Csys_mod_count%2Crecipe_name%2Csys_updated_on%2Csys_tags%2Csys_created_by'

# Eg. User name="admin", Password="admin" for this code sample.
user = ''
pwd = ''

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}
#
#
# TO Update record by add back of header e.g.data="{\"Recipes\":\"RikenTest\"}"
#
#

# Do the HTTP request
response = requests.patch(url, auth=(user, pwd), headers=headers ,data="{\"recipe_name\":\"Riken_Test\"}")

# Check for HTTP codes other than 200
if response.status_code != 200:
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()

# Decode the JSON response into a dictionary and use the data
data = response.json()
print(data)