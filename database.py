from pymongo import AsyncMongoClient
Mongo_url = "mongodb://localhost:27017"
client = AsyncMongoClient(Mongo_url)
db = client["farm_database"]
students_collection= db["students"]

