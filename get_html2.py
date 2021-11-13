import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import os

#names = pd.read_csv("data/IMDb_names.csv").dropna(how='all', subset=['spouses_string']).reset_index(drop=True)
names = pd.read_csv("data/names2.csv")

url_prefix = "https://www.imdb.com/name/"
url_postfix = "/bio"

donezo = os.listdir("html")
donezo = set(donezo)

print(f"Total, {len(names.index)}")

start = time.time()
total_time = 0
pcent = 0
err_log = open("logs/err_log", 'w+')
out_log = open("logs/out_log", 'w+')
skp_log = open("logs/skp_log", 'w+')
size = len(names.index)
inc = int(size * 0.01)
num_skipped = 0

for i in range(size):

	nameID = names['imdb_name_id'][i]
	url = url_prefix + nameID + url_postfix

	if nameID+".html" in donezo:
		num_skipped += 1
		skp_log.write(nameID + "\n")
		continue

	try:
		src = requests.get(url).text
		soup = BeautifulSoup(src, 'lxml')
		fam = soup.find("table", {"id": "tableFamily"}).prettify()

		fout = open("html/"+nameID+".html", 'w+')
		fout.write(str(fam))
		fout.close()

		if i % inc == 0:
			end = time.time()
			dt = end - start
			total_time += dt
			pcent = int(100 * i / size)
			print(f"{pcent}% -- {i}/{size} -- Elapsed: {total_time/60:.3f} mins -- Delta: {dt/60:.3f} mins -- Remaining: {((100-pcent) * dt / 60):.3f} mins -- Skipped {num_skipped}")
			start = time.time()

	except:
		err_log.write(nameID + "\n")


err_log.close()
out_log.close()
skp_log.close()