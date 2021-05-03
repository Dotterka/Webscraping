from bson import json_util
from pymongo import MongoClient  

# Making Connection 
myclient = MongoClient("mongodb://host:27017",username='user',password='password')   
   
# database  
db = myclient["webshops"] 

# Created or Switched to collection  
Collection = db["prices"] 

# save the price collection from database to json file
cursor = Collection.find({})
with open('prices_old.json', 'w') as file:
    for document in cursor:
        file.write(json_util.dumps(document))
        file.write('\n')