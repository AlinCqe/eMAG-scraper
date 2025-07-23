from .db_config import collection
from flask import jsonify



def get_items_by_ids(ids_list):
    data = collection.find({'_id': {'$in':ids_list}})
    return (list(data))
