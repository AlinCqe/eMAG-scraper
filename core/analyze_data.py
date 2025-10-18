from .db_config import MongoManager

db_manager = MongoManager()

saved_days = db_manager.get_all_collections()

current_data = {}
for date in saved_days:

    db_manager.collection_setter(date=date)
    data = db_manager.get_data()
    current_data[date] = data



def main():
    print(saved_days)
    print(saved_days[-1])
    print(saved_days[-2])
    db_manager.collection_setter(saved_days[-1])
    day_one_data = db_manager.get_data()
    db_manager.collection_setter(saved_days[-2])
    day_two_data = db_manager.get_data()

    day_one_ids = [item["_id"] for item in day_one_data]
    day_two_ids = [item["_id"] for item in day_two_data]

    ids_common_set = set(day_one_ids).intersection(set(day_two_ids))
    print(ids_common_set)
    day_one_data_dict = {item["_id"]: item for item in day_one_data}
    day_two_data_dict = {item["_id"]: item for item in day_two_data}
    price_changes = []

    for _id in ids_common_set:
        day_one_price = day_one_data_dict[_id]["item_price"]
        day_two_price = day_two_data_dict[_id]["item_price"]
        print(day_one_price, day_two_price)

        if day_one_price != day_two_price:
            price_changes.append({
            "item_name":day_one_data_dict[_id]["item_name"],
            saved_days[-1]: day_one_price,
            saved_days[-2]: day_two_price
            })
    print(price_changes)


main()
#intersection