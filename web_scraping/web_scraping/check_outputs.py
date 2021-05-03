import subprocess, json, os
from datetime import date

save_dir = 'smoketests'
file_name = date.today().strftime("%d_%m_%Y") + '.txt'
completeName = os.path.join(save_dir, file_name)
file = open(completeName, "w")

files = ['pc_garage_revisit_items.json', 'emag_items.json', 'cel_items.json', 'flanco_items.json']
for json_file in files:
	items = [json.loads(line) for line in open(json_file, 'r')]
	if len(items) < 50:
		file.write(json_file + ":" + " failed\n")
file.close()
with open(completeName) as f:
    if 'failed' not in f.read():
        subprocess.call(['sh', './format.sh'])