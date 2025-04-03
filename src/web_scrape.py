#!/usr/bin/python3


from bs4 import BeautifulSoup

# import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


import get_current_tab
import get_cookies

# Parse the HTML
soup = BeautifulSoup(get_current_tab.html, "lxml")
# print(soup.prettify())

# i needed gecko driver to /usr/bin/ and to /usr/local/bin
#! install geckodriver
# * color
# ? color


options = Options()
# (if you're using headless mode, set headless to True)
# options.headless = False
options.set_preference("javascript.enabled", True)

# using headless mode to hide the browser
options.add_argument("-headless")
# using useragent orverride to simulate a real browser
options.set_preference(
    "general.useragent.override",
    "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
)

# ? profile path implementation not really usable i killed my profile once
# profile_path = pathlib.Path.home() / ".mozilla/firefox" / "fsaqzro1.default-esr"
# options.add_argument(f"--profile={profile_path}")
# profile = webdriver.FirefoxProfile(profile_path)

# redirection the log to /dev/null
service = Service(log_path="/dev/null")


#! trying to use logged in profile
# start the browser, it creates a new session which is not logged into any account therefore it is in romanian
driver = webdriver.Firefox(options=options, service=service)


cookies = get_cookies.cookies
url = get_current_tab.url

# navigate to the page
driver.get(url)


# Add each cookie. Make sure domain, path, and expiry (if any) are set appropriately.
for host, name, value, path, expiry in cookies:
    cookie = {"name": name, "value": value, "path": path, "domain": host}
    # Only add cookies that match the current URL’s domain.
    if url in host:
        # expiry may be None or an integer timestamp
        if expiry:
            cookie["expiry"] = expiry
        driver.add_cookie(cookie)


driver.get(url)


#! at times it just does not works
for text in soup.get_text().splitlines():
    if text:
        print(text)


"""
for br in soup.find_all("<br>"):
    br.replace_with(" ")
for text in soup.get_text(separator=" ", strip=True).splitlines():
    print(text)


for text in soup.stripped_strings:
    print(text)


"""
