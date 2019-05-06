import os
from pprint import pprint
from pymongo import MongoClient

conn = os.getenv("DB_CONNECTION_STRING")
client = MongoClient(conn)
db = client.plog

# posts = db.posts
# for document in posts.find():
#     pprint(document)

for document in db.users.find():
    pprint(document)
