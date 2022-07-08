from msilib import Table
from operator import index
import re
from bs4 import BeautifulSoup
from numpy import number
import requests
import time
import pandas as pd

Commune_Info = {"NumCommune": [], "CommuneAr": [],
                "Fax": [], "CommuneFr": [], "Willaya": []}


def GrabbingData(url):
    global df
    global Commune_Info
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    contenttable = soup.find("div", {"class": "p-body-content"})
    blocklist = contenttable.find_all("div", {"class": "block"})
    body = blocklist[1].find("div", {"class": "block-body"})
    Table = body.find("table", {"class": "dataList-table"})
    tr = Table.find_all("tr")
    listtr = list(tr)
    del listtr[0]
    for i in listtr:
        td = i.find_all("td")
        NumCommune = td[0].text
        CommuneAr = td[1].text
        CommuneFr = td[2].text
        Fax = td[3].text
        Willaya = td[4].text
        Commune_Info["NumCommune"].append(NumCommune)
        Commune_Info["CommuneAr"].append(CommuneAr)
        Commune_Info["CommuneFr"].append(CommuneFr)
        Commune_Info["Fax"].append(Fax)
        Commune_Info["Willaya"].append(Willaya)


for i in range(42):
    url = "https://apcsali-adrar.dz/communes/?page="+str(i+1)
    GrabbingData(url)
    print(Commune_Info)
df = pd.DataFrame(Commune_Info)
with open('Communes.json', 'w', encoding='utf-8') as file:
    df.to_json(file, force_ascii=False)
df.to_excel('Communes.xlsx' ,  encoding='utf8')
