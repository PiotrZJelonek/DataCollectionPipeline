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
# URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"

URL = "https://www.zoopla.co.uk/new-homes/houses/sw12/?beds_max=4&is_auction=false&is_retirement_home=false&page_size=25&price_max=700000&property_sub_type=terraced&property_sub_type=detached&property_sub_type=bungalow&property_sub_type=semi_detached&view_type=list&q=SW12&radius=3&results_sort=newest_listings&search_source=refine"

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


time.sleep(2)


try:

    # house_property = driver.find_element(by=By.XPATH, value='//div[starts-with(@id,”listing_”)]') 

    house_property = driver.find_element(by=By.XPATH, value='//*[@id="listing_60800810"]') 

except:

    print('noo!')

# prop_container = driver.find_element(by=By.XPATH, value='//div[@class="css-1itfubx e11mabic0"]') 


# house_property = driver.find_element(by=By.XPATH, value='//*[@id="listing_60800810]') # Change this xpath with the xpath the current page has in their properties
# a_tag = house_property.find_element_by_tag_name('a')
# link = a_tag.get_attribute('href')
# print(link)

# Questions:
# 1) how to run locally Colab files
# 2) this shit does not run
