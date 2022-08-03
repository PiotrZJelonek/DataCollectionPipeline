from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

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