import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"}


def parse_numbers(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    return ['https://minsk.btrans.by' + item.find('a').get('href') for item in soup.find_all('li', class_='hexagon')]


def routes(url):
    dictionary = {}
    response = requests.get(url, headers=headers, allow_redirects=False)
    soup = BeautifulSoup(response.text, 'lxml')
    for number in range(len(soup.find_all('div', class_='direction'))):
        dictionary[soup.find_all('div', class_='direction')[number].find('h2').text] = {item.text: 'https://minsk.btrans.by' + item.get('href') for item in soup.find_all('ul', class_='stops')[number].find_all_next('a') if item.text not in ('Вверх', '')}
    return dictionary


def timetable(url):
    response = requests.get(url.split('_')[3], headers=headers, allow_redirects=False)
    soup = BeautifulSoup(response.text, 'lxml')
    new_url = soup.find_all('ul', class_='stops')[int(url.split('_')[1])].find_all_next(class_='stop')[int(url.split('_')[2])].find('a').get('href')
    response = requests.get('https://minsk.btrans.by' + new_url, headers=headers, allow_redirects=False)
    soup = BeautifulSoup(response.text, 'lxml')
    return {soup.find(class_='heading').text: [item.text for item in soup.find_all(class_='timetable-ceil')]}
