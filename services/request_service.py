import httpx
import asyncio
from typing import List
from utilities.utils import clean_markdown
import hrequests


async def fetch_html(link: str, client: httpx.AsyncClient) -> str:
    print(f"\n🔄 SCRAPING: {link}")
    try:
        response = await client.get(link, timeout=10.0, follow_redirects=True)
        if response.status_code == 200 and "text/html" in response.headers.get(
            "content-type", ""
        ):
            print(f"✅ SUCCESS: {link}")
            return response.text, link
    except httpx.RequestError as e:
        print(f"❌ ERROR: {link} -> {e}")
    return ""


async def send_requests(links: List[str]) -> List[dict]:
    markdowns = []
    reqs = []
    for link in links:
        reqs.append(hrequests.async_get(link))
    responses = hrequests.map(reqs, size=5)
    for response in responses:
        if response.status_code == 200:
            print(f"✅ SUCCESS: {link}")
            markdowns.append(
                {"markdown": clean_markdown(response.text), "url": response.url}
            )
        else:
            print(response.status_code, response.url)
    return markdowns


async def main(links: List[str]) -> List[dict]:
    results = await send_requests(links)
    return results
