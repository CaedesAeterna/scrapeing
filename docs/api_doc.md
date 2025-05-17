# Web Scraper Project Documentation

## Project Structure

```
root/
├── docs/
│   └── api_doc.md
├── src/
│   ├── main.py
│   ├── database.py
│   ├── requirements.txt
│   └── utils/
│       └── web_scrape.py
│   └── static/
│       ├── index.html
│       ├── styles.css
│       ├── script.js
│       └── view_result.html
│   └── extension/
│       └── firefox-ext/
│           ├── manifest.json
│           └── background.js
├── venv/
├── .gitignore
└── README.md
```

---

## API Endpoints

### `/scrape/{url}`

- **Description:**  
  Scrapes the given URL and returns the extracted text content.  
  If the URL was already scraped, returns the cached result.

- **Response:**  
  ```json
  {
    "already_scraped": true | false,
    "result": {
      "time": "YYYY-MM-DD HH:MM:SS",
      "url": "https://example.com",
      "text": "Extracted text content..."
    }
  }
  ```
  - If not previously scraped, `result` may be an integer (insert id).

---

### `/search_url/{url}`

- **Description:**  
  Searches for a previously scraped URL (case sensitive).

- **Response:**  
  ```json
  {
    "already_scraped": true | false,
    "result": {
      "time": "YYYY-MM-DD HH:MM:SS",
      "url": "https://example.com",
      "text": "Extracted text content..."
    } | null
  }
  ```

---

### `/search_keyword/{keyword}`

- **Description:**  
  Searches for a keyword (case sensitive) in all scraped texts.

- **Response:**  
  ```json
  {
    "already_scraped": true | false,
    "results": [
      {
        "id": 1,
        "time": "YYYY-MM-DD HH:MM:SS",
        "url": "https://example.com",
        "view_text_link": "/view_result/1"
      },
      ...
    ] | "No results found from backend during search"
  }
  ```

---

### `/view_result/{id}`

- **Description:**  
  Returns the full scraped text for a given result ID.

- **Response:**  
  ```json
  {
    "already_scraped": true | false,
    "id": 1,
    "time": "YYYY-MM-DD HH:MM:SS",
    "url": "https://example.com",
    "text": "Extracted text content..."
  }
  ```

---

## Notes

- All endpoints use HTTP GET and expect/return JSON unless otherwise specified.
- The `/scrape` endpoint also supports query parameters: `/scrape?url=https://example.com`
- The API is case sensitive for both URLs and keywords.
- The `already_scraped` flag indicates whether the data was fetched from cache or newly scraped.
- Timestamps are in `YYYY-MM-DD HH:MM:SS` format.
- The frontend is served at `/` and static files are under `/static/`.

---

## Example Usage

### Scrape a URL

```
GET /scrape/https://example.com
```

### Search by URL

```
GET /search_url/https://example.com
```

### Search by Keyword

```
GET /search_keyword/someKeyword
```

### View Full Result

```
GET /view_result/1
```

---

## Frontend

- Main page: `/static/index.html`
- View result: `/static/view_result.html?id={id}`

---

## Dependencies

See [`src/requirements.txt`](../src/requirements.txt):

- fastapi
- uvicorn
- databases
- aiomysql
- beautifulsoup4
- selenium
- requests

---

## Environment Variables

Set in `.env` (not tracked in git):

- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_NAME`
- `DB_PORT`

---

## Logging

- Scraping logs are written to `src/logs/scrape.log`.

---

## Extension

- Firefox extension in `src/extension/firefox-ext/` allows sending the current tab URL to the backend for scraping.

---
---



