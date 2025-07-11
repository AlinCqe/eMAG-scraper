from .db_config import collection
from flask import jsonify



def get_items_by_ids(ids_list):
    data = collection.find({'_id': {'$in':ids_list}}, {'_id':0})
    return (list(data), ['First', 'second'])
