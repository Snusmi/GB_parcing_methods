from pymongo import MongoClient
from pymongo import DESCENDING
from  pprint import pprint
client = MongoClient('localhost',27017)
db = client['group330']

users = db.users
books = db.books

# users.insert_many([{"author": "Peter",
#                "age" : 19,
#                "text": "is cool! Wildberry",
#                "tags": ['cool','hot','ice'],
#                "date": '14.06.1983'},
#
#                     {"author": "Smith",
#                "age" : 28,
#                "title": "Cold Cool!!!",
#                "text": "not too!",
#                "date": '13.03.1987'}])

doc = {"author": "John",
               "age" : 38,
               "title": "Books and text",
               "text": "Super cool",
               "date": '13.03.1987'}
# users.update_many({'author':'Peter'},{'$set':{'age':29}})
#users.update_one({'author':'Peter'},{'$set':doc})

# users.delete_one({})
#users.delete_many({})

for user in users.find():
    pprint(user)
# for user in users.find({},{'author':1,'date':1, '_id':0}).sort('author',-1):
#     pprint(user)

