from django.shortcuts import render
from graphs.models import Account
import requests
import json
from bs4 import BeautifulSoup
import csv
import os

# Код для запросов API что бы взять баланс
def getData(labels):
    # Реквесты по API
    apikey = "VG28ZKAJRRE4AJCQDWADQN22QJJRNFJT85"
    walletValue = []
    i = 0

    # Делаем по 10 запросов
    while i != 100:
        temp = ""
        for y in range(i, i+20):
            temp += labels[y] + ","

        l = len(temp)
        adres = temp[:l-1]

        response = requests.get("https://api.etherscan.io/api" +
                                "?module=account" +
                                "&action=balancemulti" +
                                "&address=" + adres +
                                "&tag=latest" +
                                "&apikey=" + apikey)
        

        response_dict = response.json()['result']
        for res in response_dict:
            bal = res['balance']
            walletValue.append(int(bal))

        i += 20

    return walletValue


# Код для взятия топ 100 Адресов
def topHundrend():
    # Ссылка для запроса
    url = "https://etherscan.io/accounts/1?ps=100"  

    # User agent что бы сервер ответил
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    response = requests.get(url,headers=headers)
    webpage = response.content
    soup = BeautifulSoup(webpage, "html.parser")

    # Проходимся по таблице сайта и берем текст там где есть тэг </a>
    result = []
    for tr in soup.find_all('tr'):
        tds = tr.find_all('td')
        for td in tds:
            if td.find('a'):
                result.append(td.find('a').text)

        

    return result

def writeToCsv(labels,data):
    with open('output.csv', 'w+', newline='') as f:
        wr = csv.writer(f)

        for i in range(0,100):
            rows = [labels[i],data[i]]
            try:
                wr.writerow(rows)
            except:
                pass

        
# Create your views here.
def home(request):
    # Если файл не существует то запращиваем API и записаваем данные
    # Записываем данные так как запросы занимают много времени
    if not os.path.exists('./output.csv'):
        labels = topHundrend()
        data = getData(labels)
        writeToCsv(labels=labels, data=data)

    labels = []
    data = []

    # Берем данные из csv
    with open('output.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            labels.append(row[0])
            data.append(int(row[1]))

        
    # Передаем данные index.html
    return render(request, 'index.html', {
        'labels': labels,
        'data': data,
    })

