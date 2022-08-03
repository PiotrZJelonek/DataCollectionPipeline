# import libraries
import time

# import classes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# from pathlib import Path

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
            print("WebCrawler: unknown website")
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
            self.contents = []

            # output
            print("")
            print("WebCrawler was successfully instantiated!")
            print("")

    def print(self):
        """
        Print (initialised) object
        """

        print("Printing WebCrawler's attributes:")
        print("")

        # print website
        print("  website: ")
        print(f"    {self.website}")  

        # print URL
        print("  URL: ")
        print(f"    {self.URL}") 

        # print waiting time
        print("  maximum waiting time:")
        print(f"    {self.maximum_delay}")
        print("") 

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
                print("Frame Ready!")

                try:

                    # select an element by Xpath
                    accept_cookies_button = WebDriverWait(self.driver, self.maximum_delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="save"]')))
                    print("Accept Cookies Button Ready!")

                except TimeoutException:

                    print("Loading a botton took too much time!")

            elif self.website == "righmove":

                pass

            # click the button
            accept_cookies_button.click()

            # wait a second
            time.sleep(1)

        except TimeoutException:

            # output
            print("Loading a frame took too much time!")

        # refresh HTML code, to fix communication error between geckodriver and marionette
        self.driver.refresh()

    def get_links(self) -> list:
        """
        
        """

        prop_container = self.driver.find_element(by=By.XPATH, value='//div[@class="css-1itfubx e5pbze00"]')
        prop_list = prop_container.find_elements(by=By.XPATH, value='./div')
        links_on_page = []

        for house_property in prop_list:
            a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            links_on_page.append(link)

        return links_on_page

#


# RUN THE CRAWLER

URL = "https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list"

crawler = WebCrawler(URL=URL)

crawler.print()

crawler.load_and_accept_cookies()

links_on_page = crawler.get_links()

print(links_on_page)