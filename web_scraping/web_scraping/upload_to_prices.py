import json 
from pymongo import MongoClient  
from datetime import datetime 
  
# Making Connection 
myclient = MongoClient("mongodb://host:27017",username='user',password='password')  
   
# database  
db = myclient["webshops"] 
   
# Created or Switched to collection   
Collection = db["prices"] 
  
# Loading the json file 
file_data = [json.loads(line) for line in open('prices.json', 'r')]
# Inserting the loaded data in the Collection 
# if JSON contains data more than one entry 
# insert_many is used else inser_one is used 
if isinstance(file_data, list): 
    Collection.insert_many(file_data)   
else: 
    Collection.insert_one(file_data) 