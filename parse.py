from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def start_bus():
    arr = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://minsk.btrans.by/avtobus')
    hrefs = driver.find_element(By.CLASS_NAME, 'hexagon-container')
    links = hrefs.find_elements(By.TAG_NAME, 'a')
    for el in links:
        arr.append(el.get_attribute('href'))
    return arr


def start_trolleybus():
    arr = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://minsk.btrans.by/trollejbus')
    hrefs = driver.find_element(By.CLASS_NAME, 'hexagon-container')
    links = hrefs.find_elements(By.TAG_NAME, 'a')
    for el in links:
        arr.append(el.get_attribute('href'))
    return arr


def start_tram():
    arr = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://minsk.btrans.by/tramvaj')
    hrefs = driver.find_element(By.CLASS_NAME, 'hexagon-container')
    links = hrefs.find_elements(By.TAG_NAME, 'a')
    for el in links:
        arr.append(el.get_attribute('href'))
    return arr

