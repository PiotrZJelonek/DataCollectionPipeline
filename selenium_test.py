# # selenium can 'drive' a browser


## Does not do enything useful - just opens the browser
# from selenium import webdriver 

# driver = webdriver.Firefox()
# my_path1 = driver.find_element_by_xpath('//button')
# my_path2 = driver.find_element_by_xpath('//*[@id="__next"]')
# print(my_path1)

# new_path = my_path.find_element_by_xpath('./div')

# from selenium import webdriver
# from time import sleep

# driver = webdriver.Firefox()
# # driver.get("https://zoopla.co.uk")

# URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
# driver.get(URL)


from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()
URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
driver.get(URL)
time.sleep(2) # Wait a couple of seconds, so the website doesn't suspect you are a bot

try: 

    # This is the id of the frame
    driver.switch_to.frame('gdpr-consent-notice') 

    # select an element by Xpath
    accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="save"]')

    # click the button
    accept_cookies_button.click()

    # page = driver.page_source.encode('utf-8')
    # page = driver.page_source.encode('utf-8')

    # # open result.html
    # file_ = open('result.html', 'wb')
  
    # # Write the entire page content in result.html
    # file_.write(page)
  
    # # Closing the file
    # file_.close()
  
    # # Closing the driver
    # driver.close()


except:

    # If there is no cookies button, we won't find it
    print('Sorry - no cookies!')

# try:
#     driver.switch_to_frame('gdpr-consent-notice') # This is the id of the frame
#     accept_cookies_button = driver.find_element_by_xpath('//*[@id="save"]')
#     accept_cookies_button.click()
#     print('a')

# except AttributeError: # If you have the latest version of Selenium, the code above won't run because the "switch_to_frame" is deprecated
#     driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
#     accept_cookies_button = driver.find_element_by_xpath('//*[@id="save"]')
#     accept_cookies_button.click()

#     print('b')

# except:

#     print('duupa')
#     pass # If there is no cookies button, we won't find it, so we can pass


