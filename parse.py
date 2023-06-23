from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import json

from selenium.webdriver.chrome.service import Service

url = "https://www.personality-database.com/profile?pid=2&cid=27&sub_cat_id=39&sort=alphabet"

options = webdriver.ChromeOptions()
service = Service(executable_path="C:\\Users\\aksen\\Documents\\chromedriver.exe",
                              chrome_options=options)
driver = webdriver.Chrome(service=service)

try:
    from selenium.webdriver.common.by import By
    driver.get(url)
    time.sleep(10)

    driver.execute_script("window.scrollBy(0 , 10000 );")
    time.sleep(5)

    page_click1 = driver.find_element(by=By.CLASS_NAME, value="rc-pagination-options")
    page_click1.click()
    time.sleep(5)

    page_click2 = driver.find_element(by=By.XPATH, value="//div [contains( text(), '500 Profiles / Page')]")
    page_click2.click()
    time.sleep(5)

    driver.execute_script("window.scrollBy(0 , -10000 );")

    for i in range(1000): #scroll
        driver.execute_script("window.scrollBy(0 , 10 );")

    page = bs(driver.page_source, 'html.parser')
    print("Done")

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

def swap(name_string):
    name = list(name_string)
    for i in range(len(name)):
        if name[i] == '"':
            name[i] = ""
    name = ''.join(name)
    return name

def parse(page):

    result_list = []
    characters = page.find_all(class_='profile-card')

    for character in characters:
        char = {}
        char['name'] = swap(character.find(class_='info-name').text)
        char['category'] = character.find('div', class_='info-subcategory').label.text
        char['personality type'] = character.find('div', class_='personality').text
        char['personality subtype'] = character.find('div', class_='subtype').text
        char['avatar'] = character.find('img')["src"]
        result_list.append(char)
    return result_list

with open('json_mcu.json', 'w') as outfile:
    json.dump(parse(page), outfile)

with open('mcu.js', 'w') as outfile:
    outfile.write('var mcu =`')
    json.dump(parse(page), outfile)
    outfile.write('`;')