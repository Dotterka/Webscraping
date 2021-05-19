# for updating the products collection, if anything changed

import pandas as pd, numpy as np, json

# products_old.json is from the database products collection
df_old=pd.read_json("products_old.json", lines=True)
df_new=pd.read_json("products.json", lines=True)

# dropping the id generated by mongodb
df_old=df_old.drop('_id',axis=1)

# rename the column that could changed
df_new=df_new.rename(columns={"sold_by":"sold_by_new","pc_garage_url":"pc_garage_url_new","emag_url":"emag_url_new","cel_url":"cel_url_new","flanco_url":"flanco_url_new"})

# checking if the new data's sold_by column has changed (if the item appeared on a site or disappeared)
df_final=pd.merge(df_old, df_new[['sold_by_new','pc_garage_url_new','emag_url_new','cel_url_new','flanco_url_new','id','name']], on=['id','name'], how="inner")
df_filtered=df_final[(df_final.sold_by != df_final.sold_by_new)]

pc_garage=0
cel=0
flanco=0
emag=0
for i, row in df_filtered.iterrows():
  sold_by = row['sold_by']
  a=json.loads(sold_by)
  sold_by_new = row['sold_by_new']
  b=json.loads(sold_by_new)
  diff = {k: b[k] for k in b if k in a and b[k] != a[k]}
  true = {k: diff[k] for k in diff if diff[k]==True}
  for i in true:
    if i == 'pc_garage':
      pc_garage=1
    else:
      if i == 'cel':
        cel=1
      else:
        if i == 'flanco':
          flanco=1
        else:
          if i == 'emag':
            emag=1

if pc_garage:
  df_filtered['pc_garage_url']= np.where(df_filtered['pc_garage_url'].isnull(), df_filtered['pc_garage_url_new'],df_filtered['pc_garage_url'])
  df_filtered=df_filtered.drop(columns={'pc_garage_url_new'})
if cel:
  df_filtered['cel_url']= np.where(df_filtered['cel_url'].isnull(), df_filtered['cel_url_new'],df_filtered['cel_url'])
  df_filtered=df_filtered.drop(columns={'cel_url_new'})
if flanco:
  df_filtered['flanco_url']= np.where(df_filtered['flanco_url'].isnull(), df_filtered['flanco_url_new'],df_filtered['flanco_url'])
  df_filtered=df_filtered.drop(columns={'flanco_url_new'})
if emag:
  df_filtered['emag_url']= np.where(df_filtered['emag_url'].isnull(), df_filtered['emag_url_new'],df_filtered['emag_url'])
  df_filtered=df_filtered.drop(columns={'emag_url_new'})
if set(['pc_garage_url_new']).issubset(df_filtered.columns):
  df_filtered=df_filtered.drop(columns={'pc_garage_url_new'})
if set(['cel_url_new']).issubset(df_filtered.columns):
  df_filtered=df_filtered.drop(columns={'cel_url_new'})
if set(['flanco_url_new']).issubset(df_filtered.columns):
  df_filtered=df_filtered.drop(columns={'flanco_url_new'})
if set(['emag_url_new']).issubset(df_filtered.columns):
  df_filtered=df_filtered.drop(columns={'emag_url_new'})

# if changed keeping the new data
df_filtered=df_filtered.drop(columns={'sold_by'})
df_filtered=df_filtered.rename(columns={'sold_by_new':'sold_by'})
df_filtered.to_json('products_update.json', orient='records', lines=True)

# collecting the new data's url, in order to scrape it's specifications later
df_new=pd.read_json('products.json',lines=True)
df_old = df_old.fillna(value=np.nan)

# keep only what's new (items only in the new dataframe)
df_products_new=pd.merge(df_old[['name']],df_new,on=['name'],how="right", indicator=True).query('_merge=="right_only"')
df_products_new=df_products_new.drop(columns={"_merge"})
df_products_new.to_json('new_items.json', orient='records', lines=True)

df_links=df_products_new['emag_url'].dropna()
df_links=df_links.to_frame()
# keep only those links which are not in old links
df_links_old=pd.read_json("emag_revisit_links.json", lines=True)
df_links_old=df_links_old.T
df_links_old=df_links_old.rename(columns={0:'emag_url'})
df_links_final=pd.merge(df_links_old[['emag_url']],df_links,on=['emag_url'],how="right", indicator=True).query('_merge=="right_only"')
df_links_final=df_links_final.drop(columns={"_merge"})
links_final=df_links_final['emag_url']

# save the links
links_final.to_json('emag_revisit_links.json', orient='records')