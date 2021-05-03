# for updating the products collection, if there are any new items

import pandas as pd, numpy as np, json

# new_items.json is from the update_products.py file, it contains the new products
df_new_items=pd.read_json('new_items.json',lines=True)

# emag_revisit_items.json contains the new products and it's specifications (it's from the emag_revisit spider)
df_emag_revisit=pd.read_json('emag_revisit_items.json',lines=True)

# update the dataframe, to store the specifications
df_emag_revisit=df_emag_revisit.rename(columns={'price':'emag_price','url':'emag_url','review_score':'emag_review_score','review_count':'emag_review_count','provider_name':'emag'})
df_new_items=df_new_items.set_index('emag_url')
df_emag_revisit=df_emag_revisit.set_index('emag_url')
df_new_items.update(df_emag_revisit)
df_new_items.reset_index(inplace=True)
df_new_items=df_new_items[["name", "pc_garage_url", "pc_garage_review_score", "pc_garage_review_count", "color", "display_type", "display_resolution", "display_size", "chipset", "internal_memory", "ram", "main_camera", "selfie_camera", "os", "os_version", "nfc_indicator", "battery_type", "battery_capacity", "emag_url", "emag_review_score", "emag_review_count", "cel_url", "flanco_url", "flanco_review_score", "flanco_review_count", "id", "sold_by"]]

# keep only the items where the display_size column is not null
# if the display_size column is empty, than the emag_revisit_items.json doesn't have that product
# (because of an attribute of the emag_revisit spider), so all the specificcations are empty 
df_new_items = df_new_items[df_new_items['display_size'].notna()]
df_new_items = df_new_items.fillna(value=np.nan)
df_new_items=df_new_items.drop_duplicates()
df_new_items.to_json('products.json', orient='records', lines=True)