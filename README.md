# Data Collection Pipeline

In this project I first crawl through a two UK real estate websites: [zoopla](https://www.zoopla.co.uk/) and [rightmove](https://www.rightmove.co.uk/). From these I obtain links to adverts of houses for sale in [Greater London](https://en.wikipedia.org/wiki/Greater_London) in a pre-specified neighborhood. First, my crawler visits the links, fetches the property data, cleans it, and stores it in [pandas](https://pandas.pydata.org/) DataFrame object. Next, whenever available, I fetch the floor plans corresponding to these properties. 

## Environment

- Created new virtual environment <em>dp</em> with
```conda
conda create -n dp python=3.9.7
```
- Installed [opencv-python](https://pypi.org/project/opencv-python/), 
[tensorflow](https://www.tensorflow.org/learn),
and [ipykernel](https://pypi.org/project/ipykernel/)
- Added [black](https://pypi.org/project/black/) to the mix to *blacken* the code later via
```black
black web_crawler.py
```
- Checked the environment using
```pip
pip freeze > requirements.txt
```
**Note**: A great source for OpenCV tutorials can be found [here](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

## Installation

sudo apt-get install python-bs4

pip install beautifulsoup4

install geckodriver

[to be cleaned/improved/continued]

## Driving Firefox browser using Selenium

[Selenium](https://www.selenium.dev/documentation/webdriver/)

## Doownloading images from websites

## Implementing logging

Logging with [loguru](https://loguru.readthedocs.io/en/stable/) allows us to retain a detailed account of a web crawler run without redirecting output to screen. It will be helpful once the code is run in the cloud
within a [docker container](https://www.docker.com/resources/what-container/).

- Implementation of the logger
```python
"""
# import classes
from loguru import logger

# creating a new log
logger.remove()
logger.add("log/web_crawler_{time}.log")
logger.info("")
logger.info("--------------------------------------- WEB CRAWLER RUN --------------------------------------- ")
logger.info("")
"""
```
Note that <em>logger</em> object is accessible globally, both within an instance of a <em>WebCrawler</em> class object and within ```__main__``` function. 
- Basic logging
<p align="center" width="100%">
    <img width="66%" src="https://github.com/PiotrZJelonek/DataCollectionPipeline/blob/develop/pics/logging.png?raw=true">
</p> 
<p align = "center">
Fig. 1 - First <em>loguru</em> log 
</p>

## Mixin in WebCrawler class

- Implementation of the mixin
```python
"""
# Mixin class to log objects
class LogObjectMixin:

    def _is_protected(self, prop):
        ## check if attribute is protected
        return prop.startswith('_')

    def log(self, obj):
        ## Log (initialised) object
        # list attributes: non-callable, non-private, non-protected
        attribute_list = [a for a in dir(self) if not callable(getattr(self, a)) and not a.startswith('__') and not self._is_protected(a)]
        attribute_list = sorted(attribute_list)

        # log class name and attributes
        logger.info(f"Logging {obj.__class__.__name__} class object")
        logger.info("")
        logger.info("  Attributes:")

        # populate the dictionary
        d = defaultdict(lambda: "Not defined")
        for a in attribute_list :
            d[a] = self.__getattribute__(a)

        # print all the keys
        for key in d.keys():
            logger.info(f"    {key}:")
            logger.info(f"      {d[key]}")
        logger.info("")

        # list methods: callable, non-private, non-protected
        method_list = [a for a in dir(self) if callable(getattr(self, a)) and not a.startswith('__') and not self._is_protected(a)]
        method_list = sorted(method_list)

        # log methods
        logger.info("  Methods:")
        for m in method_list:
            logger.info(f"    {m}():")
        logger.info("")
"""
```
- Using the mixin as a parent to <em>WebCrawler</em> class. As a result, <em>WebCrawler</em> instances inherit a method which can log <em>any</em> object.
<p align="center" width="100%">
    <img width="66%" src="https://github.com/PiotrZJelonek/DataCollectionPipeline/blob/develop/pics/mixin.png?raw=true">
</p> 
<p align = "center">
Fig. 2 - Logging object <em>attributes</em> and <em>methods</em>  with loguru
</p>