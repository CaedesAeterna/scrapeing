from src.database import db
from src.utils.web_scrape import scrape_url
from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from pydantic import HttpUrl

import os, html

# print("CWD:", os.getcwd())


# create the database instance
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup db
    await db.connect()
    yield
    # shutdown db
    await db.disconnect()


# if db.connection:
# print("Database is connected")
# else:
# print("Database is not connected")


# create the FastAPI app instance
app = FastAPI(lifespan=lifespan, title="Web Scraper API", version="1.0.0")


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

        print("URL already exists in the database")

        return {"already_scraped": True, "result": result}

        #! for some reason this doesn't work
        return Response(content=result, media_type="text/plain")

    else:

        # If not, insert into database
        query = "INSERT INTO scraped_text (url, text) VALUES (:url, :text)"
        insert_result = await db.execute(
            query=query, values={"url": str(url), "text": text_result}
        )

        print(insert_result)
        if insert_result is not None:
            print("Scraped text inserted into the database")
        else:
            print("Failed to insert scraped text into the database")

        # Return safely escaped text
        # safe_content = html.escape(result)  # HTML escape for security
        # return Response(content=safe_content, media_type="text/html")

        # print("Scraped text:", text_result)

        return {"already_scraped": False, "result": result}

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
    query = "SELECT time, url, text FROM scraped_text WHERE text LIKE :keyword"
    results = await db.fetch_all(query=query, values={"keyword": f"%\n{keyword}%"})

    # print (results)
    if results is not None:
        return {"already_scraped": True, "result": results}

    return {"already_scraped": False, "result": None}


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
