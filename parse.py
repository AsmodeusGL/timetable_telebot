import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def parse_numbers(url):
    arr = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    hrefs = driver.find_element(By.CLASS_NAME, 'hexagon-container')
    links = hrefs.find_elements(By.TAG_NAME, 'a')
    for el in links:
        arr.append(el.get_attribute('href'))
    return arr


def routes(url):
    dictionary = {}
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(1)
    for number in range(len(driver.find_elements(By.CLASS_NAME, 'direction'))):
        dictionary[driver.find_elements(By.CLASS_NAME, 'direction')[number].find_element(By.TAG_NAME, 'h2').text] = {item.text: item.get_attribute('href') for item in driver.find_elements(By.CLASS_NAME, 'stops')[number].find_elements(By.TAG_NAME, 'a')}
    return dictionary


def timetable(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url.split('_')[3])
    new_url = driver.find_elements(By.CLASS_NAME, 'stops')[int(url.split('_')[1])].find_elements(By.CLASS_NAME, 'stop')[int(url.split('_')[2])].find_element(By.TAG_NAME, 'a').get_attribute('href')
    driver.get(new_url)
    return {driver.find_element(By.CLASS_NAME, 'heading').text: [item.text for item in driver.find_elements(By.CLASS_NAME, 'timetable-ceil')]}
