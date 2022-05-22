from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def start():
    arr = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://minsk.btrans.by/avtobus')
    hrefs = driver.find_element(By.CLASS_NAME, 'hexagon-container')
    links = hrefs.find_elements(By.TAG_NAME, 'a')
    for el in links:
        arr.append(el.get_attribute('href'))
    return arr[:10]
