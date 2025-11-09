from pymongo import MongoClient

MONGO_DB_URL = "mongodb://db:27017"

DATABASE_NAME = "mydatabase"

client = MongoClient(MONGO_DB_URL)

db = client[DATABASE_NAME]

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS IS MY DATABASE WHERE I COLLECT ALL PROJECTS
projects_collection = db["projects"]

#-------------------------------------------------------------------------------------------------------------------------------------------
#THIS IS MY DATABASE WHERE I COLLECT ALL DETAIL ABOUT MY EVERY PROJECT
projects_details = db["project_details"]