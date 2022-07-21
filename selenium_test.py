# selenium can 'drive' a browser

from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC 
import time

# Selenium 4.1: https://selenium-python.readthedocs.io/locating-elements.html 

driver = webdriver.Firefox()
URL =    "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"

driver.get(URL)
time.sleep(2) # Wait a couple of seconds, so the website doesn't suspect you are a bot

try: 

    # This is the id of the frame
    driver.switch_to.frame('gdpr-consent-notice') 

    # select an element by Xpath
    accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="save"]')

    # click the button
    accept_cookies_button.click()

    # change encoding, write html code to a 'result.html' file, close
    # page = driver.page_source.encode('utf-8')
    # file_ = open('result.html', 'wb')
    # file_.write(page)
    # file_.close()
    # driver.close()

except:

    # If there is no cookies button, we won't find it
    print('Sorry - no cookies!')


time.sleep(2)

# refresh HTML code, to fix communication error between geckodriver and marionette
driver.refresh()

# Note: below we have to change @id to a value that certainly is on THIS page 

# find a listing on a given page, scrap text
house_property = driver.find_element(by=By.XPATH, value='//*[@id="listing_62010333"]')
s = house_property.text

# output
print("\nhouse_property.text: ")
print(s)

# find a link on a given page, get 'href'
a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
link = a_tag.get_attribute('href')

print("\nlink:")
print(link)

# # running a driver in headless mode

# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options

# options = Options()
# options.headless = True
# driver = webdriver.Firefox(options=options, executable_path=r'C:\Utility\BrowserDrivers\geckodriver.exe')
# driver.get("http://google.com/")
# print ("Headless Firefox Initialized")
# driver.quit()

# Questions:
# 1) How to run locally Colab files