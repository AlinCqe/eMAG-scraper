from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi 
from datetime import datetime
from dotenv import load_dotenv
import os

now = datetime.now()
today = now.strftime("%Y-%m-%dS") 

load_dotenv()

uri = os.getenv('MONGO_URI')

print(uri)
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['eMAG-scraper']
collection = db[today]

# CAREFUL - DELETES ALL THE DATA IN MONGODB
#collection.delete_many({})


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)