# GET data from servicenow
# Reading records from ServiceNow and saving them into local mongo database
from pymongo import MongoClient
import pymongo
from json import loads
from collections import OrderedDict

# Connection with Localhost
# Connecting with localhost type this URL = "'mongodb://localhost:27017"
client = MongoClient('localhost', 27017)
# creating DB call "Recipes_db" in MongoDB Compass after connecting to localhost
db = client['recipes_db']
# creating collection name "recipes"
collection_recipe = db['recipes']
# GET request w/ database table fields specified
# Need to install requests package for python
# easy_install requests
import requests, json, ast, itertools
# Set the request parameters
'''
Use sysparm_fields=field_name => field_name is the field you want to read
separate fields using commas in case you want to read more than one field from a table
'''
# URL for Recipe table in servicenow
url = 'https://emplkasperpsu1.service-now.com/api/now/table/x_snc_beer_brewing_recipe?sysparm_fields=sys_id%2Csys_updated_by%2Csys_created_on%2Csys_mod_count%2Crecipe_name%2Csys_updated_on%2Csys_tags%2Csys_created_by'
# Use IST440 for both user and pwd of serviceNow
user = ''
pwd = ''
# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}
# Do the HTTP request
# GET is the request to read data
response = requests.get(url, auth=(user, pwd), headers=headers)

# Decode the JSON response into a dictionary and use the data
data = response.json()
print(type(data))
print()
print("This is a json dictionary: ", data, "Type: ", type(data))

# No we need to get the list of key value pairs from our dict
print()

recipe_names_pairs = data['result']

print("This is a list: ", recipe_names_pairs)
print()
# Check type
print("Recipe_names_pairs is of the list type and can now be used to create documents in mongodb: ", type(recipe_names_pairs))
# Inserting Data to mongoDB in localhost and can be use for CrowPi
db.collection_recipe.insert(recipe_names_pairs)
print()

for doc in recipe_names_pairs:
    try:
        # insert into db collection
        print("Inserting ", doc, " into db...")
        message = "Inserting ", doc, " into db..."
        db.collection_recipe.insert_one(doc)
    except pymongo.errors.DuplicateKeyError:
        # skip document because it already exists in the local db collection
        continue
