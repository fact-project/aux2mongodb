

def bulk_insert_with_overwrite(data, collection):
    bulk = collection.initialize_unordered_bulk_op()

    for row in data:
        bulk.find({'timestamp': row['timestamp']}).upsert().replace_one(row)

    result = bulk.execute()

    return result


def bulk_insert(data, collection, overwrite=False):
    if overwrite is True:
        result = bulk_insert_with_overwrite(data, collection)
    else:
        result = collection.insert_many(data, ordered=False)
    return result
