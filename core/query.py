from .db_config import MongoManager
db_manager = MongoManager()
collection = db_manager.collection

def get_items_by_ids(ids_list):

    data = collection.find({'_id': {'$in':ids_list}})
    return (list(data))
