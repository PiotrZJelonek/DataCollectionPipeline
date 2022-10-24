# selenium can 'drive' a browser

from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC 
import time

# Selenium 4.1: https://selenium-python.readthedocs.io/locating-elements.html 


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


def get_links(driver: webdriver.Chrome) -> list:
    '''
    Returns a list with all the links in the current page
    Parameters
    ----------
    driver: webdriver.Chrome
        The driver that contains information about the current page
    
    Returns
    -------
    link_list: list
        A list with all the links in the page
    '''

    prop_container = driver.find_element(by=By.XPATH, value='//div[@class="css-1itfubx e3tdh350"]')
    prop_list = prop_container.find_elements(by=By.XPATH, value='./div')
    link_list = []

    for house_property in prop_list:
        a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
        link = a_tag.get_attribute('href')
        link_list.append(link)

    return link_list  

big_list = []
driver = load_and_accept_cookies()

nof_pages = 1

for i in range(nof_pages): # The first 5 pages only

    big_list.extend(get_links(driver)) # Call the function we just created and extend the big list with the returned list
    next_page_button = driver.find_element(by=By.CLASS_NAME, value='eaoxhr15 css-xtzp5a-ButtonLink-Button-StyledPaginationLink eaqu47p1')
    next_page_button.click()

    ## TODO: Click the next button. Don't forget to use sleeps, so the website doesn't suspect
    pass # This pass should be removed once the code is complete


# print(big_list)

nof_links = len(big_list)
print("")
print(f"Total number of links: {nof_links}")
print("")
for i in range(nof_links):
    print(f"  ({i:3.0f}) {big_list[i]}")
    if i == nof_links - 1: 
        print("")

# for link in big_list:
#     ## TODO: Visit all the links, and extract the data. Don't forget to use sleeps, so the website doesn't suspect
#     pass # This pass should be removed once the code is complete

# driver.quit() # Close the browser when you finish












# # accept cookies
# driver = load_and_accept_cookies()  

# time.sleep(2)

# # try: 

# prop_container = driver.find_element(by=By.XPATH, value='//div[@class="css-1itfubx e3tdh350"]') # XPath corresponding to the Container

# prop_list = prop_container.find_elements(by=By.XPATH, value='./div')
# link_list = []

# for house_property in prop_list:
#     a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
#     link = a_tag.get_attribute('href')
#     link_list.append(link)
    
# print(f'There are {len(link_list)} properties in this page')

# for link in link_list:
#     print(f"  {link}") 



# # except:

# #     print('duupa')


# # Note: below we have to change @id to a value that certainly is on THIS page 

# # find a listing on a given page, scrap text
# house_property = driver.find_element(by=By.XPATH, value='//*[@id="listing_62721271"]')
# s = house_property.text

# # output
# print("\nhouse_property.text: ")
# print(s)

# # find a link on a given page, get 'href'
# a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
# link = a_tag.get_attribute('href')

# print("\nlink:")
# print(link)

# time.sleep(2)

# driver.get(link)

# # create placeholder for scraped data
# dict_properties = {'Price': [], 'Address': [], 'Bedrooms': [], 'Description': []}

# # get price
# price = driver.find_element(by=By.XPATH, value='//p[@data-testid="price"]').text
# dict_properties['Price'].append(price)

# # get address
# address = driver.find_element(by=By.XPATH, value='//address[@data-testid="address-label"]').text
# dict_properties['Address'].append(address)

# # get bedrooms
# bedrooms = driver.find_element(by=By.XPATH, value='//div[@class="c-PJLV c-PJLV-iiNveLf-css"]').text
# dict_properties['Bedrooms'].append(bedrooms)

# # get description
# div_tag = driver.find_element(by=By.XPATH, value='//div[@data-testid="truncated_text_container"]')
# span_tag = div_tag.find_element(by=By.XPATH, value='.//span')
# description = span_tag.text
# dict_properties['Description'] = description

# # output
# for key in dict_properties.keys():
#     print(f"{key}:")
#     if isinstance(dict_properties[key], list):
#         print(" ", end = ' ')
#         for idx, element in enumerate(dict_properties[key]):
#             print(f"{element}", end= ' ')
#         print("")
#     else:
#         print(f"  {dict_properties[key]}")


# # close the browser
# driver.quit()

# # dict_properties['Price'].append(price)
# # address = driver.find_element(by=By.XPATH, value='//address[@data-testid="address-label"]').text
# # dict_properties['Address'].append(address)
# # bedrooms = driver.find_element(by=By.XPATH, value='//div[@class="c-PJLV c-PJLV-iiNveLf-css"]').text
# # dict_properties['Bedrooms'].append(bedrooms)
# # div_tag = driver.find_element(by=By.XPATH, value='//div[@data-testid="truncated_text_container"]')
# # span_tag = div_tag.find_element(by=By.XPATH, value='.//span')
# # description = span_tag.text
# # dict_properties['Description'] = description


# # crawler == creating a list of links



# # # running a driver in headless mode

# # from selenium import webdriver
# # from selenium.webdriver.firefox.options import Options

# # options = Options()
# # options.headless = True
# # driver = webdriver.Firefox(options=options, executable_path=r'C:\Utility\BrowserDrivers\geckodriver.exe')
# # driver.get("http://google.com/")
# # print ("Headless Firefox Initialized")
# # driver.quit()

# # Note:
# # geckodriver is located at : /usr/local/bin

# # Questions:
# # 1) How to run locally Colab files

# # change encoding, write html code to a 'result.html' file, close
# # page = driver.page_source.encode('utf-8')
# # file_ = open('result.html', 'wb')
# # file_.write(page)
# # file_.close()
# # driver.close()