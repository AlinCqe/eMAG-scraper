from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi 
from dotenv import load_dotenv

import os

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')

uri = MONGODB_URI


client = MongoClient(uri, server_api=ServerApi('1'))


try:
    client.admin.command('ping')
except Exception as e:
    print(e)


db = client['eMAG-scraper']
collection = db['items_data']

# CAREFUL - DELETES ALL THE DATA IN MONGODB
#collection.delete_many({})