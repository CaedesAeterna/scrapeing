from bs4 import BeautifulSoup
import bs4

# import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time, datetime, requests, re


# import get_current_tab
# import get_cookies


async def scrape_url(url: str):
    # Fetch webpage content
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for HTTP errors

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unwanted elements
    for element in soup(
        ["script", "style", "nav", "footer", "iframe", '[class*="ads"]']
    ):
        element.decompose()

    # Get title
    title = soup.title.string if soup.title else "No title"

    # Extract content from main content areas first
    main_content = soup.find(
        ["main", "article", '[role="main"]', ".content", "#content"]
    )

    if main_content:
        content_soup = main_content
    else:
        content_soup = soup

    formatted_text = ""

    for line in content_soup.get_text().splitlines():
        # Skip very short lines
        if len(line) < 4:
            continue

        if len(line) < 40:
            # Add the line to formatted_text with a newline before and after
            formatted_text += "\n" + line + "\n"
        else:
            # Add the line to formatted_text witg a double  newline after
            formatted_text += line + "\n \n"

    ts = time.time()

    # Add metadata
    final_text = f"Title: {title}\nSource: {url}\nDate scraped: {datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')}\n\n{formatted_text}"

    return final_text

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


# cookies = get_cookies.cookies
# url = get_current_tab.url

# navigate to the page
# driver.get(url)

"""
# Add each cookie. Make sure domain, path, and expiry (if any) are set appropriately.
for host, name, value, path, expiry in cookies:
    cookie = {"name": name, "value": value, "path": path, "domain": host}
    # Only add cookies that match the current URL’s domain.
    if url in host:
        # expiry may be None or an integer timestamp
        if expiry:
            cookie["expiry"] = expiry
        driver.add_cookie(cookie)

"""
"""
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

"""

"""


for br in soup.find_all("<br>"):
    br.replace_with(" ")
for text in soup.get_text(separator=" ", strip=True).splitlines():
    print(text)


for text in soup.get_text().split():
    print(text)


"""
