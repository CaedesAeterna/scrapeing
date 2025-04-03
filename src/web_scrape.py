#!/usr/bin/python3

html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

import json, lz4.block, pathlib
import requests
from bs4 import BeautifulSoup

# import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service



#/home/caedes/.mozilla/firefox/fsaqzro1.default-esr/sessionstore-backups/recovery.jsonlz4

# Adjust the path to your Firefox profile's sessionstore file:
# profile = pathlib.Path.home() / ".mozilla/firefox" / "yourprofile.default-release" / "sessionstore-backups" / "recovery.jsonlz4"
profile = pathlib.Path.home() / ".mozilla/firefox" / "fsaqzro1.default-esr" / "sessionstore-backups" / "recovery.jsonlz4"



with open(profile, "rb") as f:
    f.read(8)  # skip the header
    data = json.loads(lz4.block.decompress(f.read()).decode("utf-8")) # decode the jsonlz4 data

# Get the active tab from the first window
window = data["windows"][0]
# The active tab is at index 0
active_index = window["selected"] - 1   # Firefox uses 1-indexed value
# Get the active tab
active_tab = window["tabs"][active_index]
# The current URL is in the latest entry of this tab's history:
url = active_tab["entries"][active_tab["index"] - 1]["url"]
print(url)

# Get the HTML of the current page
#url = "https://www.google.co.uk/"
response = requests.get(url)
html = response.text 

# Parse the HTML
soup = BeautifulSoup(html, 'lxml')

 
# i needed gecko driver to /usr/bin/ and to /usr/local/bin
#! install geckodriver
#* color
#? color

options = Options()
# (if you're using headless mode, set headless to True)
#options.headless = False
options.set_preference("javascript.enabled", True)
options.add_argument('-headless')


# redirection the log to /dev/null 
service = Service(log_path='/dev/null')

# start the browser, it creates a new session which is not logged into any account therefore it is in romanian
driver = webdriver.Firefox(options=options, service=service)

# navigate to the page 
driver.get(url)


#for i in soup.get_text().splitlines():
# print(i)


#! at times it just does not works
for text in soup.stripped_strings:
    print(text)


#print(soup.prettify())
#print(BeautifulSoup)
#print(soup.get_text())
