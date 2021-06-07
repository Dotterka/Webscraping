from flask import Flask, jsonify, request, redirect, render_template
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.json_util import dumps
import pandas as pd, numpy as np

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://username:password@host:port/db_name?authSource=admin"
mongo = PyMongo(app)

prices_db = mongo.db.prices
products_db = mongo.db.products

prices_db = mongo.db.prices
products_db = mongo.db.products

prices = [doc for doc in prices_db.find()]
products = [doc for doc in products_db.find()]

df_price = pd.DataFrame(data=prices)
df_price=df_price.drop('_id',axis=1)
df_prod = pd.DataFrame(data=products)
df_prod=df_prod.drop('_id',axis=1)

df_all=df_price.merge(df_prod,on=['id','name'],how='left')

brand = df_all["name"].str.split(" ", n = 1, expand = True)

df_all['brand']=brand[0]
for i, row in df_all.iterrows():
    brand = row['brand']
    if brand=='Telefon' or brand=='Black' or brand=='rezistent':
        df_all=df_all.drop(i)
    
df_all.loc[df_all['brand']=='Iphone', ['brand']] = 'Apple'
df_all.loc[df_all['brand']=='Galaxy', ['brand']] = 'Samsung'
df_all.loc[df_all['brand']=='OPPO', ['brand']] = 'Oppo'
df_all.loc[df_all['brand']=='Oneplus7', ['brand']] = 'OnePlus'
df_all.loc[df_all['brand']=='Kruger', ['brand']] = 'Kruger&Matz'
df_all.loc[df_all['brand']=='Kruger-Matz', ['brand']] = 'Kruger&Matz'
df_all.loc[df_all['brand']=='CUBOT', ['brand']] = 'Cubot'
df_all.loc[df_all['brand']=='EVOLVEO', ['brand']] = 'Evolveo'
df_all.loc[df_all['brand']=='LEAGOO', ['brand']] = 'Leagoo'
df_all.loc[df_all['brand']=='OUKITEL', ['brand']] = 'Oukitel'
df_all.loc[df_all['brand']=='Redmi', ['brand']] = 'Xiaomi'
df_all.loc[df_all['brand']=='POCO', ['brand']] = 'Poco'
df_all.loc[df_all['brand']=='ROG', ['brand']] = 'Asus'


df_all.loc[df_all['color']=='Negru', ['color']] = 'Black'
df_all.loc[df_all['color']=='Albastru', ['color']] = 'Blue'
df_all.loc[df_all['color']=='Alb', ['color']] = 'White'
df_all.loc[df_all['color']=='Gri', ['color']] = 'Silver'
df_all.loc[df_all['color']=='Auriu', ['color']] = 'Gold'
df_all.loc[df_all['color']=='Verde', ['color']] = 'Green'
df_all.loc[df_all['color']=='Argintiu', ['color']] = 'Silver'
df_all.loc[df_all['color']=='Rosu', ['color']] = 'Red'
df_all.loc[df_all['color']=='Mov', ['color']] = 'Violet'
df_all.loc[df_all['color']=='Portocaliu', ['color']] = 'Orange'
df_all.loc[df_all['color']=='Roz', ['color']] = 'Pink'
df_all.loc[df_all['color']=='Galben', ['color']] = 'Gold'
df_all.loc[df_all['color']=='Bleumarin', ['color']] = 'Blue'
df_all.loc[df_all['color']=='Rose gold', ['color']] = 'Gold'
df_all.loc[df_all['color']=='Turcoaz', ['color']] = 'Blue'
df_all.loc[df_all['color']=='Twilight', ['color']] = 'Black'
df_all.loc[df_all['color']=='Portocaliu\nNegru', ['color']] = 'Black'
df_all.loc[df_all['color']=='Aura glow', ['color']] = 'Crystal'
df_all.loc[df_all['color']=='Negru mat', ['color']] = 'Black'
df_all.loc[df_all['color']=='Albastru inchis', ['color']] = 'Blue'
df_all.loc[df_all['color']=='Maro', ['color']] = 'Brown'
df_all.loc[df_all['color']=='Corai', ['color']] = 'Orange'
df_all.loc[df_all['color']=='Rosu\nNegru', ['color']] = 'Black'
df_all.loc[df_all['color']=='Albastru-Turcoaz', ['color']] = 'Blue'
df_all.loc[df_all['color']=='Coral', ['color']] = 'Orange'
df_all.loc[df_all['color']=='Bleu', ['color']] = 'Blue'
df_all.loc[df_all['color']=='Prism white', ['color']] = 'White'
df_all.loc[df_all['color']=='Gri lucios', ['color']] = 'Silver'
df_all.loc[df_all['color']=='Bej', ['color']] = 'Brown'
df_all.loc[df_all['color']=='Crystal\nAlbastru', ['color']] = 'Crystal'
df_all.loc[df_all['color']=='Alb\nAuriu', ['color']] = 'Gold'
df_all.loc[df_all['color']=='Visiniu', ['color']] = 'Red'
df_all.loc[df_all['color']=='Argintiu\nNegru', ['color']] = 'Silver'
df_all.loc[df_all['color']=='Gri inchis', ['color']] = 'Silver'

name = df_all["name"].str.split("GB", n = 1, expand = True) + " GB"
df_all['short_name']=name[0]

df_all.loc[df_all['os']=='Android OS', ['os']] = 'Android'
        
df_all.loc[df_all['display_type']=='LCD\nIPS', ['display_type']] = 'LCD IPS'
df_all.loc[df_all['display_type']=='PLS\nTFT', ['display_type']] = 'PLS TFT'
#df_all.loc[df_all['display_type']=='PLS TFT LCD', ['display_type']] = 'PLS\TFT\LCD'
df_all.loc[df_all['display_type']=='IPS\nPLS', ['display_type']] = 'IPS PLS'
df_all.loc[df_all['display_type']=='LCD\nIPS\nLTPS', ['display_type']] = 'LCD IPS LTPS'
df_all.loc[df_all['display_type']=='LCD\nTFT', ['display_type']] = 'LCD TFT'
df_all.loc[df_all['display_type']=='Super Retina XDR OLED', ['display_type']] = 'OLED'
df_all.loc[df_all['display_type']=='IPS\nLTPS', ['display_type']] = 'LCD IPS LTPS'
df_all.loc[df_all['display_type']=='AMOLED\nSuper AMOLED', ['display_type']] = 'Super AMOLED'

df_all.loc[df_all['ram']=='4096 MB', ['ram']] = '4 GB'

df_global= pd.DataFrame()

@app.route('/read_all', methods=['GET'])
def prices():
    return jsonify(list(json.loads(df_all.to_json(orient='records'))))
    
@app.route('/read_all/<brand>', methods=['GET'])
def spec_brand(brand):
    global df_global
    if "{" not in brand:
        df_brand=df_all[df_all['brand']==brand]
        df_global= pd.DataFrame()
        df_global=df_global.append(df_brand)
    else:
        param_list=brand.split(',')
        param_list[0]=param_list[0][1:]
        param_list[len(param_list)-1]=param_list[len(param_list)-1][:-1]
        frames = [ df_all[df_all['brand']==param_list[i]] for i in range(len(param_list)) ]
        df_brand = pd.concat(frames)
        df_global= pd.DataFrame()
        df_global=df_global.append(df_brand)
    return jsonify(list(json.loads(df_brand.to_json(orient='records'))))
    
@app.route('/read_all/<brand>/<color>', methods=['GET'])
def spec_color(brand,color):
    spec_brand(brand)
    if "{" not in color:
        df_color=df_global[df_global['color']==color]
    else:
        param_list=color.split(',')
        param_list[0]=param_list[0][1:]
        param_list[len(param_list)-1]=param_list[len(param_list)-1][:-1]
        frames = [ df_global[df_global['color']==param_list[i]] for i in range(len(param_list)) ]
        df_color = pd.concat(frames)
    return jsonify(list(json.loads(df_color.to_json(orient='records'))))
    
@app.route('/read_all/short_name/<short_name>', methods=['GET'])
def spec_short_name(short_name):
	df_short_name=df_all[df_all['short_name']==short_name]
	return jsonify(list(json.loads(df_short_name.to_json(orient='records'))))

@app.route('/read_all/name/<name>', methods=['GET'])
def spec_name(name):
	df_name=df_all[df_all['name']==name]
	return jsonify(list(json.loads(df_name.to_json(orient='records'))))
	
@app.route('/read_all/<os>', methods=['GET'])
def spec_os(os):
	df_os=df_all[df_all['os']==os]
	return df_os	
	
@app.route('/read_all/<os>/<ram>', methods=['GET'])
def spec_ram(os,ram):
    df_all=spec_os(os)
    if "{" not in ram:
        df_ram=df_all[df_all['ram']==ram]
    else:
        param_list=ram.split(',')
        param_list[0]=param_list[0][1:]
        param_list[len(param_list)-1]=param_list[len(param_list)-1][:-1]
        frames = [ df_all[df_all['ram']==param_list[i]] for i in range(len(param_list)) ]
        df_ram = pd.concat(frames)
    return df_ram
    
@app.route('/read_all/all/<os>/<ram>/<display_type>/<display_size>/<memory>', methods=['GET'])
def spec_memory(os,ram,display_type,display_size,memory):
    df_all=spec_display_size(os,ram,display_type,display_size)
    if "{" not in memory:
        df_memory=df_all[df_all['internal_memory']==memory]
    else:
        param_list=memory.split(',')
        param_list[0]=param_list[0][1:]
        param_list[len(param_list)-1]=param_list[len(param_list)-1][:-1]
        frames = [ df_all[df_all['internal_memory']==param_list[i]] for i in range(len(param_list)) ]
        df_memory = pd.concat(frames)
    return jsonify(list(json.loads(df_memory.to_json(orient='records'))))
    
@app.route('/read_all/<os>/<ram>/<display_type>', methods=['GET'])
def spec_display_type(os,ram,display_type):
    df_all=spec_ram(os,ram)
    if "{" not in display_type:
        df_display_type=df_all[df_all['display_type']==display_type]
    else:
        param_list=display_type.split(',')
        param_list[0]=param_list[0][1:]
        param_list[len(param_list)-1]=param_list[len(param_list)-1][:-1]
        frames = [ df_all[df_all['display_type']==param_list[i]] for i in range(len(param_list)) ]
        df_display_type = pd.concat(frames)
    return df_display_type
    
@app.route('/read_all/<os>/<ram>/<display_type>/<display_size>', methods=['GET'])
def spec_display_size(os,ram,display_type,display_size):
    df_all=spec_display_type(os,ram,display_type)
    if "{" not in display_size:
        df_display_size=df_all[df_all['display_size']==float(display_size)]
    else:
        param_list=display_size.split(',')
        param_list[0]=param_list[0][1:]
        param_list[len(param_list)-1]=param_list[len(param_list)-1][:-1]
        param_list = [i for i in param_list if i]
        frames = [ df_all[df_all['display_size']==float(param_list[i])] for i in range(len(param_list)) ]
        df_display_size = pd.concat(frames)
    return df_display_size
    
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)