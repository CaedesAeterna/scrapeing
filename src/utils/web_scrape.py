from bs4 import BeautifulSoup


import time, datetime, requests, re, logging
from playwright.async_api import async_playwright

# Configure logging
logging.basicConfig(
    filename="src/logs/scrape.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def scrape_url(url: str):
    # Fetch webpage content
    # headers = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    # }
    # response = requests.get(url, headers=headers)
    # # response.raise_for_status()  # Check for HTTP errors

    # # Fetch webpage content with JS rendering
    # session = AsyncHTMLSession()
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    # }
    # response = await session.get(url, headers=headers)
    # response.html.arender(timeout=20)  # JS rendering

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        # Wait for the page to load some content (customize selector as needed)
        await page.wait_for_load_state("networkidle")
        html = await page.content()
        await browser.close()

    # Parse HTML content
    soup = BeautifulSoup(html, "html.parser")

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

    pattern = re.compile(
        r"""
    ( ↑
    | ^\s*[\w\s,]+   # lines of just words/spaces/commas
    ( : | , | \| )\s*$
    | doi
    | ISBN
    | ISSN
    | Retrieved
    | OCLC
    | pp\.
    | Vol\.
    | ed\.
    | Archived
    | http
    | www
    | \.com
    | \.org
    | \.gov
    | \.edu
    )
    """,
        re.IGNORECASE | re.VERBOSE,
    )

    for block in content_soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li"]):
        text = block.get_text(separator=" ", strip=True)

        # Filter out short or meaningless text
        if text and len(text.split()) > 5:  # Keep paragraphs with more than 5 words
            # Exclude text that appears to be lists, citations, or metadata
            if not re.match(r"^\s*[\w\s,]+(:|,|\|)\s*$", text):  # Avoid lists
                if not pattern.search(text):  # Avoid citations and URLs
                    if not re.match(r"^\^", text):  # Avoid footnote-style references
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
    logging.info(f"Scraping completed for URL: {url}")
    return final_text
