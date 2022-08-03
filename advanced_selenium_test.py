# import libraries
import time

# import classes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# initialize
driver = webdriver.Firefox()

# If you can explain it in words - selenium probably can do it. Just google it -
# or check the documentation

# Selenium 4.1: https://selenium-python.readthedocs.io/locating-elements.html 

# go to python website
driver.get("http://www.python.org")

# scroll to the bottom of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# look for the search bar and click it
search_bar = driver.find_element(by=By.XPATH, value='//*[@id="id-search-field"]')
search_bar.click()

# type "method" into search bar
search_bar.send_keys("method")

# press enter
search_bar.send_keys(Keys.RETURN)

# Many websites are dynamic, their whole content is not available right after connecting to them. 
# In this case, Selenium will try to find elements before the whole page is loaded, 
# and the scraper will fail if the element is not ready.

def load_and_accept_cookies() -> webdriver.Firefox:
    '''
    Open Zoopla and accept the cookies
    
    Returns
    -------
    driver: webdriver.Firefox
        This driver is already in the Zoopla webpage
    '''
    
    driver = webdriver.Firefox() 
    URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"
    driver.get(URL)
    maximum_delay = 10

    try:
        WebDriverWait(driver, maximum_delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gdpr-consent-notice"]')))
        driver.switch_to.frame('gdpr-consent-notice')
        print("Frame Ready!")
        
        try:
            accept_cookies_button = WebDriverWait(driver, maximum_delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="save"]')))
            accept_cookies_button.click()
            print("Accept Cookies Button Ready!")

        except TimeoutException:

            print("Loading a botton took too much time!")
        
        time.sleep(1)

    except TimeoutException:
        print("Loading a frame took too much time!")

    return driver 

# the code
driver = load_and_accept_cookies()
