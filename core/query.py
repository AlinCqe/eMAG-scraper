from .db_config import collection



def get_items_by_ids(ids_list):

    data = collection.find({'_id': {'$in':ids_list}})
    return (list(data))
