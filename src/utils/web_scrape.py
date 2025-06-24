from bs4 import BeautifulSoup
import time, datetime, requests, re, logging
from playwright.async_api import async_playwright
from transformers import pipeline

# --- Add these imports ---
import spacy

# Load spaCy model (run: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

# Initialize zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
labels = ["News", "Research", "Tutorial", "History", "Unknown"]


def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]


def classify_topic(text):
    lowered = text.lower()
    news_keywords = [
        "news",
        "breaking",
        "report",
        "journalist",
        "press",
        "headline",
        "update",
        "coverage",
        "article",
        "media",
        "reuters",
        "bbc",
        "cnn",
        "nytimes",
        "guardian",
        "al jazeera",
        "fox news",
        "ap news",
        "newsweek",
        "washington post",
        "associated press",
        "bloomberg",
        "financial times",
        "the economist",
        "politico",
        "huffpost",
        "buzzfeed",
        "vox",
        "vice",
        "the verge",
        "techcrunch",
        "wired",
        "cnet",
        "engadget",
        "mashable",
        "the atlantic",
        "the new yorker",
        "the times",
        "the sun" "the daily mail",
        "the independent",
        "the telegraph",
        "the mirror",
        "the spectator",
        "the observer",
        "the herald",
        "the age",
        "the guardian",
        "the australian",
        "the courier mail",
        "the sydney morning herald",
        "the financial review",
        "the australian financial review",
        "war report",
        "political news",
        "international news",
        "local news",
        "breaking news",
        "current affairs",
        "world news",
        "local news",
        "sports news",
        "entertainment news",
        "business news",
        "technology news",
        "health news",
        "science news",
        "environment news",
        "education news",
        "lifestyle news",
        "opinion",
        "editorial",
        "commentary" "investigation",
    ]
    research_keywords = [
        "research",
        "study",
        "journal",
        "paper",
        "doi",
        "experiment",
        "findings",
        "results",
        "analysis",
        "methodology",
        "hypothesis",
        "theory",
        "scholar",
        "academic",
        "peer-reviewed",
        "conference",
        "publication",
        "citation",
        "literature review",
        "systematic review",
        "meta-analysis",
        "case study",
        "field study",
        "longitudinal study",
        "cross-sectional study",
        "qualitative research",
        "quantitative research",
        "mixed methods",
        "data collection",
        "data analysis",
        "statistical analysis",
    ]
    tutorial_keywords = [
        "tutorial",
        "how to",
        "guide",
        "step by step",
        "lesson",
        "instruction",
        "training",
        "course",
        "workshop",
        "webinar",
        "video tutorial",
        "online course",
        "e-learning",
        "self-paced",
        "hands-on",
        "practical",
    ]

    history_keywords = [
        "history",
        "historical",
        "historian",
        "ancient",
        "medieval",
        "modern",
        "timeline",
        "chronology",
        "archaeology",
        "artifact",
        "civilization",
        "empire",
        "dynasty",
        "revolution",
        "war",
        "battle",
        "conflict",
        "treaty",
        "diplomacy",
        "colonialism",
        "imperialism",
        "decolonization",
        "renaissance",
        "enlightenment",
        "industrial revolution",
        "world war",
        "cold war",
        "historical event",
        "historical figure",
        "historical period",
        "historical context",
        "historical narrative",
        "historical analysis",
        "historical interpretation",
        "historical research",
        "historical methodology",
        "nationalism",
        "totalitarianism",
        "dictatorship",
        "ideology",
        "irredentism",
        "expansionism",
        "corporatism",
        "racism",
        "antisemitism",
        "resistance",
        "monarchy",
        "republic",
        "syndicalism",
        "militarism",
        "propaganda",
        "civil war",
        "alliance",
        "occupation",
        "annexation",
        "unification",
        "constitution",
        "political movement",
        "economic policy",
        "social change",
        "cultural change",
        "religious change",
        "historical document",
        "historical source",
        "historical evidence",
        "historical account",
        "historical narrative",
    ]

    if any(word in lowered for word in research_keywords):
        return "Research"
    if any(word in lowered for word in news_keywords):
        return "News"
    if any(word in lowered for word in tutorial_keywords):
        return "Tutorial"
    if any(word in lowered for word in history_keywords):
        return "History"
    return "Unknown"


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

    # Regex pattern to filter out unwanted text
    # This pattern matches common citation formats, URLs, and metadata
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

    # --- Advanced categorisation ---
    # Extract entities using spaCy and zero-shot classifications
    entities = extract_entities(formatted_text)
    # Classify topic using spaCy and zero-shot classification
    result = classifier(formatted_text, candidate_labels=labels)
    # Use the highest scoring label as the topic
    topic = result["labels"][0]

    # Return structured result
    return {
        "text": final_text,
        "entities": entities,
        "topic": topic,
    }
