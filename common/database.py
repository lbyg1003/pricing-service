from typing import Dict
import pymongo


class Database:  # a static database class, nothing more than a wrapper, so we put less lines of code in item.py
    URI = "mongodb://127.0.0.1:27017/pricing"
    DATABASE = pymongo.MongoClient(URI).get_database()

    @staticmethod
    def insert(collection: str, data: Dict):
        Database.DATABASE[collection].insert(data)  # call this method directly on the class, instead of on the object

    @staticmethod                           # pymongo.cursor behaves like a list, so the return is like a list of dict
    def find(collection: str, query: Dict) -> pymongo.cursor:  # query used for mango db is something like {_id: xxx}.
        return Database.DATABASE[collection].find(query)

    @staticmethod  # pymongo.cursor behaves like a list, so the return is like a list of dict
    def find_one(collection: str, query: Dict) -> Dict:  # query used for mango db is something like {_id: xxx}.
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict):
        Database.DATABASE[collection].update(query, data, upsert=True)  # update or insert if not exist

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:  # return all the documents that have been removed
        return Database.DATABASE[collection].remove(query)