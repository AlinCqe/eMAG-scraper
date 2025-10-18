from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi 
from datetime import datetime
from dotenv import load_dotenv
import os


class MongoManager:
    def __init__(self):

        load_dotenv()
        uri = os.getenv('MONGO_URI')
        self.today = datetime.now().strftime("%Y-%m-%dS") 
        
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['eMAG-scraper']
        self.collection = self.db[self.today]

    def collection_setter(self, date=None):
        """
        
        Change the active collection to anohter date.
        Defatul date being current day
        
        """
        if date:
            self.collection = self.db[date]
        else:
            self.collection = self.db[self.today]
            
    def get_all_collections(self):
        """
        
        Returns list of all collections in the DB

        """
        collections = self.db.list_collection_names()
        collections.sort()
        return collections


    def get_data(self):
        """

        Return data from the current collection
        
        """
        return list(self.collection.find({}))


    def ping_server(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            return True
        except Exception as e:
            print(e)
            return False