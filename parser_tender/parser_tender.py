import requests
from bs4 import BeautifulSoup
import json
import lxml
from time import sleep
import random

headers = { "User-Agent": 
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.148 YaBrowser/22.7.2.899 Yowser/2.5 Safari/537.36",}


# all_url = []
# for i in range(0, 171, 1):
# 	url = f"https://www.tender.gov.mn/en/bidder/list?page={i}&perpage=100&sortField=&sortOrder=&get=1"
# 	req = requests.get(url=url, headers=headers)
# 	src = req.text
# 	sleep(random.randrange(0, 2))
# 	soup = BeautifulSoup(src, "lxml")
# 	url_of_tr = soup.find("table", class_="table sortable").find("tbody").find_all("tr")
# 	for bidder in url_of_tr:
# 		url_of_td = bidder.find_all("td")
# 		url_of_bidder = "https://www.tender.gov.mn" + url_of_td[0].find("a").get("href")
# 		all_url.append(url_of_bidder)
# with open("all_url_of_bidder.json", "w") as file:
# 	json.dump(all_url, file, indent=4, ensure_ascii=False)
with open("all_url_of_bidder.json") as file:
	src = json.load(file)

all_info_bidders = []
count = 0
for item in src:
	count += 1
	print(f"#Итерация: {count}")
	print(f"Всего итераций: {int(len(src))}")
	req = requests.get(url=item, headers=headers)
	soup = BeautifulSoup(req.text, "lxml")
	all_div = soup.find_all("div", class_="col-md-12 col-sm-12 col-xs-12 simple-row")
	all_info_bidder = {}
	for i in all_div:
		name_info = i.find("div", class_="col-md-3 col-sm-3 col-xs-12 simple-row-label").text.strip()
		info = i.find("div", class_="col-md-9 col-sm-9 col-xs-12 simple-row-value").text.strip()
		all_info_bidder[name_info] = info
	all_info_bidders.append(all_info_bidder)
with open("all_info_of_bidders.json", "w", encoding="utf-8") as file:
	json.dump(all_info_bidders, file, indent=4, ensure_ascii=False)