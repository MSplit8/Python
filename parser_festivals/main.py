import requests
from bs4 import BeautifulSoup
import lxml
import json
from time import sleep
import random


headers = { "User-Agent": 
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.148 YaBrowser/22.7.2.899 Yowser/2.5 Safari/537.36",}

all_cards_href = []
for i in range(0, 192, 24):
	sleep(random.randrange(2,4))
	url = "https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o={i}&bannertitle=August"
	
	req = requests.get(url=url, headers=headers)
	json_data = json.loads(req.text)
	html_response = json_data["html"]

	with open(f"data/index_{i}.html", "w") as file:
		file.write(html_response)

	with open(f"data/index_{i}.html") as file:
		src = file.read()

	soup = BeautifulSoup(src, "lxml")
	cards = soup.find_all("a", class_="card-img-link")

	for item in cards:
		card_href = "https://www.skiddle.com" + item.get("href")
		all_cards_href.append(card_href)

fest_information = []
count = 0
for url in all_cards_href:
	count += 1
	print(f"Данные фестиваля №{count} записаны...: {url}")
	req = requests.get(url=url, headers=headers)

	try:
		soup = BeautifulSoup(req.text, "lxml")
		fest_name = soup.find("div", class_="MuiContainer-root MuiContainer-maxWidthFalse css-1krljt2").find("h1").text.strip()
		fest_info = soup.find("div", class_="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-1ik2gjq").find_all("div", class_="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol")

		fest_date_all = fest_info[0].find_all("span")
		fest_date = fest_date_all[0].text.strip() + ". " + fest_date_all[1].text.strip()
		if int(len(fest_info)) == 1:
			fest_price = "no info"
			fest_local = "no info"
			continue
		if int(len(fest_info)) == 2:
			fest_price_all = fest_info[1].find_all("span")
			simbol = "£"
			if simbol in fest_price_all[0].text:
				if int(len(fest_price_all)) == 2:
					fest_price = fest_price_all[0].text.strip() + fest_price_all[1].text
				else:
					fest_price = fest_price_all[0].text
				fest_local = "no info"
			else:
				fest_local = fest_price_all[0].text.strip()
				fest_price = "no info"
		else:
			fest_local = fest_info[1].find("span").text.strip()
			fest_price_all = fest_info[2].find_all("span")
			fest_price = fest_price_all[0].text.strip() + fest_price_all[1].text

		fest_information.append(
			{
				"Fest name": fest_name,
				"Date": fest_date,
				"Local": fest_local,
				"Price": fest_price
			}
		)
	except Exception as ex:
		print(ex)
		print("Damn... There was some erorr...")
with open("fest_list_result.json", "w", encoding="utf-8") as file:
	json.dump(fest_information, file, indent=4, ensure_ascii=False)