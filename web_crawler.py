# import libraries
import time
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

            main_container = self.driver.find_element(by=By.XPATH, value='//div[@data-testid="modal-bg"]/div/div/button')
            sing_up_for_alerts = main_container.find_element(By.XPATH, "./*[name()='svg']")
            ActionChains(self.driver).move_to_element(sing_up_for_alerts).click().perform()

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

    crawler.exit()
