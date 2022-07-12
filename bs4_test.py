import requests 
from bs4 import BeautifulSoup

# make a HTTP GET request to a website
page = requests.get('http://pythonscraping.com/pages/page3.html') 
html = page.text 

# convert to BeautifulSoup object that has methods to make tag search easier
soup = BeautifulSoup(html, 'html.parser') 

# output
print("\nParses HTML:")
print(soup.prettify())

# if it does not find anything it returns None
fish = soup.find(name='tr', attrs={'id': 'gift3', 'class':'gift'})

# output
print("\nGift 3:")
print(fish)

# a list where each item corresponds to each 'td' tag
fish_row = fish.find_all('td') 

# output
print(f"\nNumber of 'td' tags: {len(fish_row)}")
print("")


# extract info
title = fish_row[0].text
description = fish_row[1].text
price = fish_row[2].text

# output
print(title,end=" ")
print(description,end=" ")
print(price,end=" ")
print("")

# find siblings and children
parrot = fish.find_next_sibling()
parrot_children = parrot.findChildren()

# Try it out
page = requests.get('https://en.wikipedia.org/wiki/Python_(programming_language)') 
html = page.text 

# convert to BeautifulSoup object that has methods to make tag search easier
soup = BeautifulSoup(html, 'html.parser') 

# a list where each item corresponds to each 'td' tag
python_row = soup.find_all('p') 

# output - first 5 paragraphs
for i in range(min(5,len(python_row))):
    print(f"\nparagraph {i}: ")
    print("")
    print(python_row[i])
print("")


