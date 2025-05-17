import sys
from typing import List

sys.path.append(".")


from services.redis_services import flush_redis_db, get_redis_values, set_redis_value
from services.database import add_data
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from urllib.parse import urlparse
from models import detail_page
from utilities.utils import clean_markdown
from models.listing_page import Multi_ListingPage_Article
from constants.prompts import DETAIL_PAGE_PROMPT, LISTING_PAGE_PROMPT
from services import llm_service, request_service
from asyncio import to_thread


app = FastAPI(title="Archive Parser")


async def start_processing(
    html: str, base_url: str, primary_keywords: list[str], secondary_keywords: list[str]
) -> None:
    cleaned_markdown = clean_markdown(html)
    await set_redis_value(
        key=base_url, text="HTML cleaned; Getting links from the listing"
    )
    articles = await to_thread(
        llm_service.model_parser,
        LISTING_PAGE_PROMPT,
        Multi_ListingPage_Article,
        cleaned_markdown,
    )
    await set_redis_value(
        key=base_url, text=f"Article links extracted; got {len(articles.data)}"
    )
    article_links = []
    for article in articles.data:
        article_links.append(article.url)

    # parse the article htmls
    results: List[dict] = await request_service.main(article_links)
    print(f"Total articles: {len(results)}")
    for result in results:
        markdown = result.get("markdown")
        url = result.get("url")
        is_valid = True

        await set_redis_value(key=base_url, text=f"Parsing artcle - {url}")

        # check if all primary keywords are present
        for primary_keyword in primary_keywords:
            if primary_keyword.lower() not in markdown.lower():
                is_valid = False

        # check if atleast one secondary keyword is present
        if is_valid:
            present_keywords = []
            for secondary_keyword in secondary_keywords:
                if secondary_keyword.lower() in markdown.lower():
                    present_keywords.append(secondary_keyword)
        if (secondary_keywords) and (not present_keywords):
            is_valid = False

        # if all condition is valid parse the data
        if is_valid:
            await set_redis_value(
                key=base_url, text="Converting article into structured format"
            )
            structured_article: detail_page.DetailPage = await to_thread(
                llm_service.model_parser,
                DETAIL_PAGE_PROMPT,
                detail_page.DetailPage,
                markdown,
            )
            # save the article to baserow
            await set_redis_value(key=base_url, text="Saving article")
            await add_data(
                urlparse(base_url).netloc,
                {
                    "Date Scraped": datetime.now().isoformat(),
                    "Date Of Article": structured_article.date,
                    "News Article": structured_article.title,
                    "Link": url,
                    "Suspect Name": structured_article.suspect_name,
                    "Charges": structured_article.charge,
                    "Primary Keywords": ";".join(primary_keywords),
                    "Secondary Keywords": ";".join(present_keywords),
                },
            )
            await set_redis_value(key=base_url, text="Article parsing done")


@app.post("/api/start-process")
async def index(
    background_task: BackgroundTasks,
    base_url: str,
    payload: dict,
) -> dict:
    await set_redis_value(key=base_url, text="Starting the bot")
    html = payload.get("html")
    primary_keywords = payload.get("primary_keywords", [])
    secondary_keywords = payload.get("secondary_keywords", [])
    background_task.add_task(
        start_processing, html, base_url, primary_keywords, secondary_keywords
    )
    return {"details": "Hello World"}


@app.get("/get-log")
async def get_log(key: str) -> str | None:
    log = await get_redis_values(key)
    return log


@app.get("/clear-log")
async def clear_log(key: str) -> str | None:
    await flush_redis_db()
