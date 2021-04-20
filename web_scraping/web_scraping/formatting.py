# formatting the newly scraped data

import pandas as pd, numpy as np, json
from datetime import date

# read the json files
df_emag=pd.read_json('emag_items.json', lines=True)
df_pc_garage=pd.read_json('pc_garage_items.json', lines=True)
df_cel=pd.read_json('cel_items.json', lines=True)
df_flanco=pd.read_json('flanco_items.json', lines=True)

# rename the columns
df_emag=df_emag.rename(columns={"price":"emag_price","url":"emag_url","review_score":"emag_review_score","review_count":"emag_review_count","provider_name":"emag"})
df_pc_garage=df_pc_garage.rename(columns={"price":"pc_garage_price","url":"pc_garage_url","review_score":"pc_garage_review_score","review_count":"pc_garage_review_count","provider_name":"pc_garage"})
df_cel=df_cel.rename(columns={"price":"cel_price","url":"cel_url","review_score":"cel_review_score","review_count":"cel_review_count","provider_name":"cel"})
df_flanco=df_flanco.rename(columns={"price":"flanco_price","url":"flanco_url","review_score":"flanco_review_score","review_count":"flanco_review_count","provider_name":"flanco"})

# name cleaning
# emag
emag_jav=pd.read_csv('emag_item_jav.csv')
emag_jav.drop_duplicates(subset ="emag_url",keep = False, inplace = True)
df_emag.drop_duplicates(subset ="emag_url",keep = False, inplace = True)
emag_jav=emag_jav.drop('Unnamed: 0', axis=1)
emag_jav=emag_jav.set_index('emag_url')
df_emag=df_emag.set_index('emag_url')
df_emag['name'].update(emag_jav['name'])
df_emag.reset_index(inplace=True)
df_emag=df_emag[['name','emag_price','emag_url','emag_review_score','emag_review_count','emag','color','display_type','display_resolution','display_size','chipset','internal_memory','ram','main_camera','selfie_camera','os','os_version','nfc_indicator','battery_type','battery_capacity','date']]

# pc_garage
pc_garage_jav=pd.read_csv('pc_garage_item_jav.csv')
pc_garage_jav=pc_garage_jav.drop('Unnamed: 0', axis=1)
pc_garage_jav=pc_garage_jav.set_index('pc_garage_url')
df_pc_garage=df_pc_garage.set_index('pc_garage_url')
df_pc_garage['name'].update(pc_garage_jav['name'])
df_pc_garage.reset_index(inplace=True)
df_pc_garage=df_pc_garage[['name','pc_garage_price','pc_garage_url','pc_garage_review_score','pc_garage_review_count','pc_garage','color','display_type','display_resolution','display_size','chipset','internal_memory','ram','main_camera','selfie_camera','os','os_version','nfc_indicator','battery_type','battery_capacity','date']]

# Flanco delete rows where price is none 
df_flanco=df_flanco[df_flanco['flanco_price'].notna()]

# rename the date column, to be different
df_emag=df_emag.rename(columns={"date":"date_1"})
df_pc_garage=df_pc_garage.rename(columns={"date":"date_2"})
df_cel=df_cel.rename(columns={"date":"date_3"})
df_flanco=df_flanco.rename(columns={"date":"date_4"})

# PC garage + emag + cel + flanco, all items
df_pc_emag = df_pc_garage.merge(df_emag.dropna(axis='columns'), how='outer', on='name')
df_pc_emag_cel = df_pc_emag.merge(df_cel.dropna(axis='columns'), how='left', on='name')
df_pc_emag_cel_flanco = df_pc_emag_cel.merge(df_flanco.dropna(axis='columns'), how='left', on='name')

# convert to date format, to get rid of NaT values
df_pc_emag_cel_flanco[['date_1']]=date.today().strftime("%m/%d/%Y")

# convert all missing data into NaN (in order to be the same format)
df_pc_emag_cel_flanco = df_pc_emag_cel_flanco.fillna(value=np.nan)

# add an ID column

np.random.seed(1)

# create a list of unique names from product names and urls
df_copy=df_pc_emag_cel_flanco.replace(np.nan, '', regex=True)
names = df_copy[['name', 'emag_url','pc_garage_url','cel_url','flanco_url']].agg(' '.join, 1).unique().tolist()

# generate ids
ids = np.random.randint(low=1e9, high=1e10, size = len(names))

# maps ids to names
maps = {k:v for k,v in zip(names, ids)}

# add new id column
df_pc_emag_cel_flanco['id'] = df_copy[['name', 'emag_url','pc_garage_url','cel_url','flanco_url']].agg(' '.join, 1).map(maps)

# products collection (without prices, dates and with provider name boolean list)
cols = ['pc_garage','emag','cel','flanco']
df_products=df_pc_emag_cel_flanco
df_products=df_products.drop(['date_1','date_2','date_3','date_4','emag_price','cel_price','flanco_price','pc_garage_price'],axis=1)

# creating the list with the provider names
def json_values_to_bool(col):
	col = json.loads(col)
	keys = ['pc_garage','emag','cel','flanco']
	for key in keys:
		if col[key]:
			col[key] = True
		else:
			col[key] = False
	return json.dumps(col)

# applying to products
df_products['sold_by'] = df_products[cols].apply(lambda x: x.to_json(), axis=1)
df_products['sold_by'] = df_products['sold_by'].apply(json_values_to_bool) 
df_products = df_products.drop(cols, axis=1)
df_products.to_json('products.json', orient='records', lines=True)  

# prices collection (without any product specification)
df_price=df_pc_emag_cel_flanco[['id','name','emag_price','pc_garage_price','cel_price','flanco_price','date_1']]
df_price=df_price.rename(columns={'date_1':'date'})
df_price.to_json('prices.json', orient='records', lines=True)
                                        