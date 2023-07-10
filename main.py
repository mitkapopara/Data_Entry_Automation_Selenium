from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


import time

CHROME_DRIVER_PATH = "C:/Users/meet/Desktop/Development/chromedriver.exe"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                               "like Gecko) Chrome/114.0.0.0 Safari/537.36",
                                 "Accept-Language": "en-US,en;q=0.5"
}
response = requests.get(url="https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D"
                        "%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C"
                        "%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37"
                        ".857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B"
                        "%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22"
                        "%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D"
                        "%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf"
                        "%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B"
                        "%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1"
                        "%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D", headers=headers)


webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")

#Property Addresses
property_addresses = []
all_addresses_element = soup.select(".gZUDVm address")
for address in all_addresses_element:
    address = address.get_text().split(" | ")[-1]
    property_addresses.append(address)
print(property_addresses)

#Property Prices
property_prices = []
all_prices = soup.find_all(name="span", class_="iMKTKr")
for price in all_prices:
    price = price.getText().split("+")[0]
    property_prices.append(price)
print(property_prices)

#Property Prices Links
property_links = []
all_links = soup.select(".bdwyNr a")
for link in all_links:
    href = link["href"]
    if "http" not in href:
        property_links.append(f"https://www.zillow.com{href}")
    else:
        property_links.append(href)
print(property_links)


service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdPHCxzSWXfQmrGRE14HuEWzV4hoaqRNl6PQpaQ2Z5RbEkeww/viewform?usp=sf_link")
time.sleep(1)
for n in range(0, len(property_prices)):
    q_1 = driver.find_element(by="xpath", value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    q_1.send_keys(property_addresses[n])

    q_2 = driver.find_element(by="xpath", value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    q_2.send_keys(property_prices[n])

    q_3 = driver.find_element(by="xpath", value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    q_3.send_keys(property_links[n])

    submit = driver.find_element(by="xpath", value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit.click()
    time.sleep(1)

    reload = driver.find_element(by="xpath", value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    reload.click()
    time.sleep(2)