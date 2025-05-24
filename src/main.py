from src.database import db
from src.utils.web_scrape import scrape_url
from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from pydantic import HttpUrl
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

import os, html

# print("CWD:", os.getcwd())


# Lifespan context manager for the FastAPI app
# This is used to manage the database connection lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup db
    await db.connect()
    yield
    # shutdown db
    await db.disconnect()

# create the FastAPI app instance
app = FastAPI(lifespan=lifespan, title="Web Scraper API", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")


# Serve the frontend
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open(os.path.join("src/static", "index.html")) as f:
        return f.read()


# define the routes for the app
@app.get("/")
async def read_root():
    # query = "SELECT * FROM scraped_text"
    # results = await db.fetch_all(query)

    return {"Hello": "World"}


# using path converter because of the slashes
@app.get("/scrape/{url:path}")
async def scrape(url: HttpUrl):
    text_result = await scrape_url(str(url))

    # Check if the URL is already in the database
    select_query = "SELECT time, url, text FROM scraped_text WHERE url = :url"
    result = await db.fetch_one(select_query, values={"url": str(url)})

    if result is not None:

        # print("URL already exists in the database")

        return {"already_scraped": True, "result": result}

        #! for some reason this doesn't work
        return Response(content=result, media_type="text/plain")

    else:

        # If not, insert into database
        query = "INSERT INTO scraped_text (url, text) VALUES (:url, :text)"
        insert_result = await db.execute(
            query=query, values={"url": str(url), "text": text_result}
        )

        # print(insert_result)

        """'
        if insert_result is not None:
            print("Scraped text inserted into the database")
        else:
            print("Failed to insert scraped text into the database")
        """
        # Return safely escaped text
        # safe_content = html.escape(result)  # HTML escape for security
        # return Response(content=safe_content, media_type="text/html")

        # print("Scraped text:", text_result)

        return {"already_scraped": False, "result": insert_result}

        #! for some reason this doesn't work
        return Response(content=result, media_type="text/plain")


@app.get("/search_url/{url:path}")
async def search(url: HttpUrl):
    query = "SELECT time, url, text FROM scraped_text WHERE url = :url"
    result = await db.fetch_one(query=query, values={"url": str(url)})
    # print(result)

    if result is not None:
        return {"already_scraped": True, "result": result}

    return {"already_scraped": False, "result": None}


@app.get("/search_keyword/{keyword:path}")
async def search(keyword: str):
    query = "SELECT id, time, url FROM scraped_text WHERE text LIKE :keyword"
    results = await db.fetch_all(query=query, values={"keyword": f"%{keyword}%"})

    if results is not None:
        # Add a link to view the full text for each result
        results_with_links = [
            {
                "id": result["id"],
                "time": result["time"],
                "url": result["url"],
                "view_text_link": f"/view_result/{result['id']}",
            }
            for result in results
        ]
        return {"already_scraped": True, "results": results_with_links}

    return {"already_scraped": False, "results": "No results found from backend during search"}


@app.get("/view_result/{id}")
async def view_result(id: int):
    query = "SELECT time, url, text FROM scraped_text WHERE id = :id"
    result = await db.fetch_one(query=query, values={"id": id})

    if result:
        return {
            "already_scraped": True,
            "id": id,
            "time": result["time"],
            "url": result["url"],
            "text": result["text"],
        }

    return {"already_scraped": False, "id": id, "result": "No result found for this ID"}


# ------------------using query parameters--------------------------


# using simple get parameter
@app.get("/scrape")
async def scrape(url: HttpUrl):
    result = await scrape_url(str(url))

    # Insert into database
    query = "INSERT INTO scraped_text (url, text) VALUES (%s, %s)"
    await db.execute(query=query, values=(str(url), result))

    # Return safely escaped text
    safe_content = html.escape(result)  # HTML escape for security
    return Response(content=safe_content, media_type="text/html")

    # return {"result": result}
    return Response(content=result, media_type="text/plain")
