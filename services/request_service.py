from services.redis_services import set_redis_value
from typing import List
from utilities.utils import clean_markdown
import hrequests


async def send_requests(base_url: str, links: List[str]) -> List[dict]:
    markdowns = []
    reqs = []
    for link in links:
        reqs.append(hrequests.async_get(link))
    responses = hrequests.map(reqs, size=5)
    for response in responses:
        if response.status_code == 200:
            print(f"✅ SUCCESS: {response.url}")
            await set_redis_value(key=base_url, text=f"✅ SUCCESS: {response.url}")
            markdowns.append(
                {"markdown": clean_markdown(response.text), "url": response.url}
            )
        else:
            print(response.status_code, response.url)
            await set_redis_value(
                key=base_url,
                text=f"Not SUCCESS: {response.url} | {response.status_code}",
            )
    return markdowns


async def main(base_url: str, links: List[str]) -> List[dict]:
    results = await send_requests(base_url, links)
    return results
