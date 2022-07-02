import requests 
from bs4 import BeautifulSoup

# make a HTTP GET request to a website
page = requests.get('http://pythonscraping.com/pages/page3.html') 
html = page.text 

# contents of a website as HTML
# print(page.text) # ,- raw HTML

# convert to BeautifulSoup object that has methods to make tag search easier
soup = BeautifulSoup(html, 'html.parser') 
print(soup.prettify())
