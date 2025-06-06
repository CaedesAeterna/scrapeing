from bs4 import BeautifulSoup


import time, datetime, requests, re, logging

# Configure logging
logging.basicConfig(
    filename="src/logs/scrape.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


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

        # Filter out short or meaningless text
        if text and len(text.split()) > 5:  # Keep paragraphs with more than 5 words
            # Exclude text that appears to be lists, citations, or metadata
            if not re.match(r"^\s*[\w\s,]+(:|,|\|)\s*$", text):  # Avoid lists
                if not re.search(
                    r"(↑|^\s*[\w\s,]+(:|,|\|)\s*$|doi|ISBN|ISSN|Retrieved|OCLC|pp\.|Vol\.|ed\.|Archived|http|www|\.com|\.org|\.gov|\.edu)",
                    text,
                    re.IGNORECASE,
                ):  # Avoid citations and URLs
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
