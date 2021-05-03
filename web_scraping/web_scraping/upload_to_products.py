import json 
import os
from pymongo import MongoClient  
from datetime import datetime
  
# Making Connection 
myclient = MongoClient("mongodb://host:27017",username='user',password='password')   
   
# database  
db = myclient["webshops"] 
   
# Created or Switched to collection  
Collection = db["products"] 
  
# updated items file if it's not empty
if os.stat("products_update.json").st_size > 1:
	new_products = [json.loads(line) for line in open('products_update.json', 'r')]
	# save the updated item's id's
	products_ids = []
	for product in new_products:
		products_ids.append(product['id'])

	# remove the old items
	for ids in products_ids:
		db.products.remove( {"id":ids});

	# insert the updated items
	if isinstance(new_products, list): 
	    Collection.insert_many(new_products)   
	else: 
	    Collection.insert_one(new_products) 

# Loading the json file       
products = [json.loads(line) for line in open('products.json', 'r')]
# Inserting the loaded data in the Collection 
# if JSON contains data more than one entry 
# insert_many is used else inser_one is used 
if isinstance(products, list): 
    Collection.insert_many(products)   
else: 
    Collection.insert_one(products) 