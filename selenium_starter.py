from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()

browser.get('http://www.yahoo.com')
sleep(5)
assert 'Yahoo' in browser.title

elem = browser.find_element(By.NAME, 'p')  # Find the search box
elem.send_keys('seleniumhq' + Keys.RETURN)
sleep(5)

browser.quit()
