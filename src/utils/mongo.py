from pymongo import MongoClient


def write_collection(dbname, coll, data, delete_existing=True):
    mc = MongoClient('localhost', 27017)
    db = mc[dbname]
    if delete_existing:
        if coll in db.collection_names():
            db.drop_collection(coll)
    collection = db[coll]
    collection.insert_many(data)


def write_doc(dbname, coll, doc):
    mc = MongoClient('localhost', 27017)
    db = mc[dbname]
    collection = db[coll]
    collection.insert_one(doc)
