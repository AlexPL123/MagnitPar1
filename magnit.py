from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("start-maximized")

driver = webdriver.Chrome(
    options=options
)
page = 0
data = []

url = f"https://magnit.ru/catalog/?categoryId=4884&pageNumber=1"
driver.get(url)
time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
while soup.find_all('li', class_='arrow next') :
    page += 1
    url = f"https://magnit.ru/catalog/?categoryId=4884&pageNumber={page}"
    # driver.switch_to.new_window('tab')

    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    cards_all = soup.find_all('a', class_='new-card-product')
    for card in cards_all:
        cards_title = card.find('div', class_='new-card-product__title').text.strip().replace('₽', '')
        cards_price = card.find('div', class_='new-card-product__price-regular').text.strip().replace('₽', '')
        price = f'{cards_title}:{cards_price}'
        print(price)
        data.append(
            [cards_title, cards_price]

        )
    time.sleep(7)
driver.quit()

with open('Catalog.csv', 'w') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(
        [
            'Продукт',
            'Цена'
        ]
    )

    writer.writerows(
        data
    )
