from bs4 import BeautifulSoup
import bs4

# import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time, datetime, requests, re


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
    title = soup.title.string.strip() if soup.title else "No title"

    # Extract content from main content areas first
    main_content = soup.find(
        ["main", "article", '[role="main"]', ".content", "#content"]
    )

    if main_content:
        content_soup = main_content
    else:
        content_soup = soup

    # Extract readable text while preserving paragraph structure
    paragraphs = []
    for block in content_soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li"]):
        text = block.get_text(separator=" ", strip=True)
        if text:
            paragraphs.append(text)

    # Join paragraphs with double newlines to separate them
    formatted_text = "\n\n".join(paragraphs)

    # Add metadata
    ts = time.time()
    final_text = (
        f"Title: {title}\n"
        f"Source: {url}\n"
        f"Date scraped: {datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"{formatted_text}"
    )

    return final_text
