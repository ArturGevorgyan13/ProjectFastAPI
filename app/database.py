from pymongo import MongoClient

MONGO_DB_URL = "mongodb://db:27017"

DATABASE_NAME = "mydatabase"

client = MongoClient(MONGO_DB_URL)

db = client[DATABASE_NAME]

projects_collection = db["projects"]