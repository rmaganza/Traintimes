from pymongo import MongoClient

MONGO_PORT = '27017'
DB_NAME = 'trains'
COLL_NAME = 'streamtrains'

client = MongoClient('localhost:' + MONGO_PORT)
collection = client[DB_NAME][COLL_NAME]