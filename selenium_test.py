# selenium can 'drive' a browser

from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC 
import time

# Selenium 4.1: https://selenium-python.readthedocs.io/locating-elements.html 

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def load_and_accept_cookies() -> webdriver.Firefox:
    '''
    Open Zoopla and accept the cookies
    
    Returns
    -------
    driver: webdriver.Firefox
        This driver is already in the Zoopla webpage
    '''

    driver = webdriver.Firefox()
    URL =    "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
    driver.get(URL)
    time.sleep(3) # Wait a couple of seconds, so the website doesn't suspect you are a bot

    try: 

        # This is the id of the frame
        driver.switch_to.frame('gdpr-consent-notice') 

        # select an element by Xpath
        accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="save"]')

        # click the button
        accept_cookies_button.click()

        # wait a second
        time.sleep(1)

    except:

        # If there is no cookies button, we won't find it
        print('load_and_accept_cookies: Sorry - no cookies!')

    # refresh HTML code, to fix communication error between geckodriver and marionette
    driver.refresh()

    return driver 

# accept cookies
driver = load_and_accept_cookies()  

time.sleep(2)

# Note: below we have to change @id to a value that certainly is on THIS page 

# find a listing on a given page, scrap text
house_property = driver.find_element(by=By.XPATH, value='//*[@id="listing_62035485"]')
s = house_property.text

# output
print("\nhouse_property.text: ")
print(s)

# find a link on a given page, get 'href'
a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
link = a_tag.get_attribute('href')

print("\nlink:")
print(link)

time.sleep(2)

driver.get(link)

# create placeholder for scraped data
dict_properties = {'Price': [], 'Address': [], 'Bedrooms': [], 'Description': []}

# get price
price = driver.find_element(by=By.XPATH, value='//p[@data-testid="price"]').text
dict_properties['Price'].append(price)

# get address
address = driver.find_element(by=By.XPATH, value='//address[@data-testid="address-label"]').text
dict_properties['Address'].append(address)

# get bedrooms
bedrooms = driver.find_element(by=By.XPATH, value='//div[@class="c-PJLV c-PJLV-iiNveLf-css"]').text
dict_properties['Bedrooms'].append(bedrooms)

# get description
div_tag = driver.find_element(by=By.XPATH, value='//div[@data-testid="truncated_text_container"]')
span_tag = div_tag.find_element(by=By.XPATH, value='.//span')
description = span_tag.text
dict_properties['Description'] = description

# output
for key in dict_properties.keys():
    print(f"{key}:")
    if isinstance(dict_properties[key], list):
        print(" ", end = ' ')
        for idx, element in enumerate(dict_properties[key]):
            print(f"{element}", end= ' ')
        print("")
    else:
        print(f"  {dict_properties[key]}")


# close the browser
driver.quit()

print(type(URL))

# dict_properties['Price'].append(price)
# address = driver.find_element(by=By.XPATH, value='//address[@data-testid="address-label"]').text
# dict_properties['Address'].append(address)
# bedrooms = driver.find_element(by=By.XPATH, value='//div[@class="c-PJLV c-PJLV-iiNveLf-css"]').text
# dict_properties['Bedrooms'].append(bedrooms)
# div_tag = driver.find_element(by=By.XPATH, value='//div[@data-testid="truncated_text_container"]')
# span_tag = div_tag.find_element(by=By.XPATH, value='.//span')
# description = span_tag.text
# dict_properties['Description'] = description


# crawler == creating a list of links



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

# change encoding, write html code to a 'result.html' file, close
# page = driver.page_source.encode('utf-8')
# file_ = open('result.html', 'wb')
# file_.write(page)
# file_.close()
# driver.close()