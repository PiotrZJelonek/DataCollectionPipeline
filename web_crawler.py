# import libraries
import time
import numpy as np
import pandas as pd
from collections import defaultdict
from pathlib import Path
from math import log10, floor

# import classes
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# Selenium 4.1: https://selenium-python.readthedocs.io/locating-elements.html 

def scroll_to_element(driver, element_locator):
    actions = ActionChains(driver)
    try:
        actions.move_to_element(element_locator).click().perform()
    except:
        driver.execute_script("arguments[0].scrollIntoView(true);", element_locator) 
        

class WebCrawler:

    def __init__(self, URL: str, maximum_delay: float = 10.0, website: str = ""):
        """
        Initialise WebCrawler instance

        Args:
            URL:     a string, a URL e.g. "https://www.zoopla.co.uk/..."
            website: a string, indicating website: "zoopla" | "rightmove"
        """

        # initialize logger
        # ....

        if website not in ["rightmove", "zoopla",""]:
            logger.info("WebCrawler: unknown website")
        else:
        
            # website (default is "zoopla")
            self.website = "zoopla" if website == "" else website

            # initialize URL    
            self.URL = URL

            # initialize the driver
            self.driver = webdriver.Firefox()
            (self.driver).maximize_window()

            # maximum waiting time
            self.maximum_delay = maximum_delay

            # list of links
            self.link_list = []

            # placeholder for website contents
            self.contents = defaultdict(lambda: 0.0)

            # output
            logger.info("")
            logger.info("WebCrawler was successfully instantiated!")
            logger.info("")

    def print(self):
        """
        Print (initialised) object
        """

        logger.info("Printing WebCrawler's attributes:")
        logger.info("")

        # print website
        logger.info("  website: ")
        logger.info(f"    {self.website}")  

        # print URL
        logger.info("  URL: ")
        logger.info(f"    {self.URL}") 

        # print waiting time
        logger.info("  maximum waiting time:")
        logger.info(f"    {self.maximum_delay}")
        logger.info("") 

    def load_and_accept_cookies(self):
        '''
        Open Zoopla/Rightmove and accept the cookies
        '''

        # now the driver contains the information about the current page
        self.driver.get(self.URL)

        # sleep
        time.sleep(3) 

        try: 

            if self.website == "zoopla":

                # This is the id of the frame
                WebDriverWait(self.driver, self.maximum_delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gdpr-consent-notice"]')))
                self.driver.switch_to.frame('gdpr-consent-notice')
                logger.info("Frame Ready!")

                try:

                    # select an element by Xpath
                    accept_cookies_button = WebDriverWait(self.driver, self.maximum_delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="save"]')))
                    logger.info("Accept Cookies Button Ready!")

                except TimeoutException:

                    logger.info("Loading a botton took too much time!")

            elif self.website == "righmove":

                pass

            # click the button
            accept_cookies_button.click()

            # wait a second
            time.sleep(1)

        except TimeoutException:

            # output
            logger.info("Loading a frame took too much time!")

        # refresh HTML code, to fix communication error between geckodriver and marionette
        self.driver.refresh()

    def get_links(self) -> list:
        '''
        Appends to link_list all the links in the current page.
        '''

        prop_container = self.driver.find_element(by=By.XPATH, value='//div[@data-testid="regular-listings"]')
        prop_list = prop_container.find_elements(by=By.XPATH, value='./div')
        links_on_page = []

        # get a link for each property
        for house_property in prop_list:
            a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            links_on_page.append(link)

        # extend link list
        (self.link_list).extend(links_on_page)

    def scroll_down(self):
        '''
        Scrolls down the page.
        '''

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 

    def click_next(self):
        '''
        Go to next page.
        '''

        if self.website == "zoopla":

            button_container = self.driver.find_element(by=By.XPATH, value='//div[@data-testid="pagination"]')
            a_tags = button_container.find_elements(by=By.TAG_NAME, value='a')
            for links in a_tags:
                if links.text == "Next >":
                    # logger.info("\nFound it!")
                    next_page_button = links.get_attribute('href')
            self.driver.get(next_page_button)

        elif self.website == "righmove":

            logger.info("click-next: not implemented for 'rightmove'")

    def sign_up_for_alerts(self):
        '''
        Sign up for the alerts.
        '''

        if self.website == "zoopla":

            try: 
                main_container = self.driver.find_element(by=By.XPATH, value='//div[@data-testid="modal-bg"]/div/div/button')
                sing_up_for_alerts = main_container.find_element(By.XPATH, "./*[name()='svg']")
                ActionChains(self.driver).move_to_element(sing_up_for_alerts).click().perform()
            
            except:

                pass 

        elif self.website == "righmove":

            logger.info("sign_up_for_alerts: not implemented for 'rightmove'")

    def collect_links(self, nof_pages=1):
        '''
        Scrape the links from a specified number of pages.
        Store the links in the 'crawler' object as 'link_list'.
        '''

        # loop over pages
        for page_number in range(nof_pages): 

            # logger.info(f"i: {page_number}")

            time.sleep(2)
            self.get_links() 
            self.scroll_down()
            self.click_next()
            time.sleep(2)

            if page_number==0:
                self.sign_up_for_alerts()

    def print_links(self):
        '''
        Print all the scraped links.
        '''

        link_list = crawler.link_list

        # print the list
        nof_links = len(link_list)
        n = floor(log10(nof_links - 1))
        logger.info("")
        logger.info(f"Total number of links: {nof_links}")
        logger.info("")
        for i in range(nof_links):
            logger.info(f"  ({i:4.0f}) {link_list[i]}")
            if i == nof_links - 1: 
                logger.info("")

    def exit(self):
        '''
        Close the driver.
        '''

        self.driver.close()

    def fetch_contents(self):
        '''
        This function gets contents from a website
        '''

        link_list = crawler.link_list
        driver = self.driver

        # create placeholder for scraped data
        properties_dict = {'PRICE': [], 'ADDRESS': [], 'BEDROOMS': [], 'BATHROOMS': [], 'RECEPTIONS': [], 'TOTAL AREA': [], 'DESCRIPTION': []}

        # iterate thorugh property links    
        for link in link_list[3:4]:

            # get link
            driver.get(link) 

            # get price
            price = driver.find_element(by=By.XPATH, value='//p[@data-testid="price"]').text
            numeric_price = int(price[1:].replace(',',''))
            properties_dict['PRICE'].append(numeric_price)

            # get address
            address = driver.find_element(by=By.XPATH, value='//address[@data-testid="address-label"]').text
            properties_dict['ADDRESS'].append(address)

            # get all the rooms
            rooms = driver.find_element(by=By.XPATH, value='//div[@class="c-PJLV c-PJLV-iiNveLf-css"]').text
    
            # parse and read numbers
            rooms_list = rooms.split('\n')

            bed_count = 0
            bath_count = 0
            lounge_count = 0
            total_area = 0
            for room in rooms_list:

                room_parsed = room.split(' ')
                value = float(room_parsed[0].replace(',',''))
                tag = room_parsed[1].lower()

                if bed_count == 0:
                    if tag in ['bed','beds','bedroom','bedroom']:
                        bed_count = int(value)
                if bath_count == 0:
                    if tag in ['bath','baths','bathroom','bahrooms']:
                        bath_count = int(value)
                if lounge_count == 0:
                    if tag in ['lounge','lounges','reception','receptions']:
                        lounge_count = int(value)
                if total_area == 0:
                    if tag in ['sq.']:
                        total_area = value

            properties_dict['BEDROOMS'].append(bed_count)
            properties_dict['BATHROOMS'].append(bath_count)
            properties_dict['RECEPTIONS'].append(lounge_count)
            properties_dict['TOTAL AREA'].append(total_area)

            print("") 
            print(numeric_price)
            print(bed_count, bath_count, lounge_count, total_area)
            print("")

            # get description
            div_tag = driver.find_element(by=By.XPATH, value='//div[@data-testid="truncated_text_container"]')
            span_tag = div_tag.find_element(by=By.XPATH, value='.//span')
            description = span_tag.text
            properties_dict['DESCRIPTION'].append(description)

            # sleep
            time.sleep(1)

            # 
            
            floorplan_button_container = driver.find_element(by=By.XPATH, value='//button[@data-testid="floorplans-label"]')
            time.sleep(1)

            driver.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, '//button[@data-testid="floorplans-label"]'))))

            # scroll_to_element(driver,floorplan_button_container)

            ActionChains(driver).move_to_element(floorplan_button_container).click().perform()

            # ActionChains(driver).move_to_element(floorplan_button_container).click().perform()
            


        return properties_dict


# RUN THE CRAWLER
if __name__ == "__main__":

    # creating a new log
    logger.remove()
    logger.add("log/web_crawler_{time}.log")
    logger.info("")
    logger.info("--------------------------------------- WEB CRAWLER RUN --------------------------------------- ")

    URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"

    nof_pages = 2

    crawler = WebCrawler(URL=URL)

    crawler.print()

    crawler.load_and_accept_cookies()

    crawler.collect_links(nof_pages=nof_pages)

    crawler.print_links()

    properties_dict = crawler.fetch_contents()

    df = pd.DataFrame.from_dict(properties_dict)
    df['TOTAL AREA'] = df['TOTAL AREA'].apply(lambda x: x if x!=0 else np.nan)

    df.to_csv('output/df.csv')

    print(df)

    # crawler.exit()

    # https://postcodes.io

    # def scroll_to_element(driver, element_locator):
    # actions = ActionChains(driver)
    # try:
    # actions.move_to_element(element_locator).perform()
    # except MoveTargetOutOfBoundsException as e:
    # print(e)
    # driver.execute_script("arguments[0].scrollIntoView(true);", element_locator) 

    # drvier.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xxxxx))) 
