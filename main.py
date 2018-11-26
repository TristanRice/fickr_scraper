#!/usr/bin/env python3

import requests
import re 
import sys
import lxml
import datetime
from threading import ThreadPool
from bs4 import BeautifulSoup as BSoup

BASE_URL = "https://www.flickr.com"
DEFAULT_DIRECTORY = "images/"

def download_image(src, name, image_directory, chunk_size=1024):
	r = requests.get("https:"+src, stream=True)
	with open(image_directory+name+".jpg", "wb") as f:
		for chunk in r.iter_content(chunk_size=chunk_size):
			if chunk:
				f.write(chunk)
				f.flush( )

def get_back_href(request):
	soup = BSoup(request.text, "lxml")
	a_tags = soup.find_all("a", class_="page-back")
	return a_tags[0]["href"]

def run_program(directory):
	url = BASE_URL+"/explore"
	while True:
		print("Downloading images for url: {}".format(url))
		r = requests.get(url, verify=False)
		#because the links are in javascript, I have to use regex to get them
		images = re.findall("img.src='.*'", r.text)
		[download_image(image[9:len(image)-1], image[38:len(image)-1],directory) for image in images]
		url = BASE_URL+get_back_href(r)

def get_dates(numdays):
	base = datetime.datetime.today( )
	date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]

def main( ):
	directory = DEFAULT_DIRECTORY
	if len(sys.argv)==2:
		directory = sys.argv[1]
	run_program(directory)

	
if __name__=="__main__":
    main( )
