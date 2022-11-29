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