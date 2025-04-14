
from bs4 import BeautifulSoup
import bs4
# import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time, datetime, requests


#import get_current_tab
#import get_cookies

async def scrape_url(url: str):
    # Fetch webpage content
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract and clean text content
    clean_lines = []
    for line in soup.stripped_strings:
        # Add proper spacing between sentences
        formatted_line = line.replace('.', '. ').replace('  ', ' ')
        clean_lines.append(formatted_line)
    
    # Join lines with newlines for readability
    formatted_text = '\n'.join(clean_lines)
    
    return formatted_text

    # redirection the log to /dev/null
    service = Service(log_path="/dev/null")
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


    #! trying to use logged in profile
    # start the browser, it creates a new session which is not logged into any account therefore it is in romanian
    driver = webdriver.Firefox(options=options, service=service)

    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    return soup


# i needed gecko driver to /usr/bin/ and to /usr/local/bin
#! install geckodriver
# * color
# ? color



# ? profile path implementation not really usable i killed my profile once
# profile_path = pathlib.Path.home() / ".mozilla/firefox" / "fsaqzro1.default-esr"
# options.add_argument(f"--profile={profile_path}")
# profile = webdriver.FirefoxProfile(profile_path)


#cookies = get_cookies.cookies
#url = get_current_tab.url

# navigate to the page
# driver.get(url)

'''
# Add each cookie. Make sure domain, path, and expiry (if any) are set appropriately.
for host, name, value, path, expiry in cookies:
    cookie = {"name": name, "value": value, "path": path, "domain": host}
    # Only add cookies that match the current URL’s domain.
    if url in host:
        # expiry may be None or an integer timestamp
        if expiry:
            cookie["expiry"] = expiry
        driver.add_cookie(cookie)

'''
'''
# current timestamp in second since the epoch 1970
ts = time.time()


# file name based upon current timespatmp
file_name = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d_%H:%M:%S")


# create the txt file
with open(file_name, mode="wt") as f:
    #! at times it just does not works
    for text in soup.stripped_strings:
        if text:
            print(text)
            f.write(text)
            f.write("\n")

# print(file_name)

'''

"""


for br in soup.find_all("<br>"):
    br.replace_with(" ")
for text in soup.get_text(separator=" ", strip=True).splitlines():
    print(text)


for text in soup.get_text().split():
    print(text)


"""
