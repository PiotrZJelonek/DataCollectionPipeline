# selenium can 'drive' a browser

# from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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

    # driver = webdriver.Chrome(ChromeDriverManager().install())
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


def get_link_list(driver: webdriver.Firefox) -> list:
    '''
    Returns a list with all the links in the current page
    Parameters
    ----------
    driver: webdriver.Firefox
        The driver that contains information about the current page
    
    Returns
    -------
    link_list: list
        A list with all the links in the page css-1itfubx ebjry2p0
    '''

    prop_container = driver.find_element(by=By.XPATH, value='//div[@data-testid="regular-listings"]')
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
s_next = '//div[@data-testid="pagination"]/ul//li/a[@aria-label="Page 1"]'

for page_number in range(nof_pages): # The first 5 pages only

    print(f"i: {page_number}")

    time.sleep(2)

    big_list.extend(get_link_list(driver)) # Call the function we just created and extend the big list with the returned list
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 

    button_container = driver.find_element(by=By.XPATH, value='//div[@data-testid="pagination"]')
    a_tags = button_container.find_elements(by=By.TAG_NAME, value='a')
    for links in a_tags:
        if links.text == "Next >":
            print("\nFound it")
            next_page_button = links.get_attribute('href')
    driver.get(next_page_button)
    
    time.sleep(2)

    if page_number==0:
        main_container = driver.find_element(by=By.XPATH, value='//div[@data-testid="modal-bg"]/div/div/button')
        sing_up_for_alerts = main_container.find_element(By.XPATH, "./*[name()='svg']")
        ActionChains(driver).move_to_element(sing_up_for_alerts).click().perform()

# print the list
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

# create placeholder for scraped data
dict_properties = {'Price': [], 'Address': [], 'Bedrooms': [], 'Bathrooms': [], 'Receptions': [], 'Description': []}

nof_properties = 10
for i in range(nof_properties):

    print(f"i: {i}")
    driver.get(big_list[i]) 

    # get price
    price = driver.find_element(by=By.XPATH, value='//p[@data-testid="price"]').text
    
    numeric_price = int(price[1:].replace(',',''))
    dict_properties['Price'].append(numeric_price )

    # get address
    address = driver.find_element(by=By.XPATH, value='//address[@data-testid="address-label"]').text
    dict_properties['Address'].append(address)

    # get all the rooms
    rooms = driver.find_element(by=By.XPATH, value='//div[@class="c-PJLV c-PJLV-iiNveLf-css"]').text
    
    # parse and read numbers
    rooms_list = rooms.split('\n')

    bed_count = 0
    bath_count = 0
    lounge_count = 0
    for room in rooms_list:
        room_parsed = room.split(' ')
        count = int(room_parsed[0])
        tag = room_parsed[1].lower()
        if bed_count == 0:
            if tag in ['bed','beds','bedroom','bedroom']:
                bed_count = count
        if bath_count == 0:
            if tag in ['bath','baths','bathroom','bahrooms']:
                bath_count = count
        if lounge_count == 0:
            if tag in ['lounge','lounges','reception','receptions']:
                lounge_count = count

        #print(room)

    dict_properties['Bedrooms'].append(bed_count)
    dict_properties['Bathrooms'].append(bath_count)
    dict_properties['Receptions'].append(lounge_count)

    print("") 
    print(numeric_price)
    print(bed_count, bath_count, lounge_count)
    print("")

    # print(rooms_list,'\n')

    # bedrooms = int(rooms_list[0])
    # bathrooms = int(rooms_list[2])
    # receptions= int(rooms_list[4])

    # print(bedrooms, bathrooms, receptions)
    # print("")


    # dict_properties['Bedrooms'].append(bedrooms)

    # print(bedrooms)

    # get description
    div_tag = driver.find_element(by=By.XPATH, value='//div[@data-testid="truncated_text_container"]')
    span_tag = div_tag.find_element(by=By.XPATH, value='.//span')
    description = span_tag.text
    dict_properties['Description'] = description

    # sleep
    time.sleep(1)

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


# # running a driver in headless mode

# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options

# options = Options()
# options.headless = True
# driver = webdriver.Firefox(options=options, executable_path=r'C:\Utility\BrowserDrivers\geckodriver.exe')
# driver.get("http://google.com/")
# print ("Headless Firefox Initialized")
# driver.quit()

# Note:
# geckodriver is located at : /usr/local/bin

# Questions:
# 1) How to run locally Colab files

# change encoding, write html code to a 'result.html' file, close
# page = driver.page_source.encode('utf-8')
# file_ = open('result.html', 'wb')
# file_.write(page)
# file_.close()
# driver.close()