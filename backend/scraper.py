from typing import List
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup, Tag

async def scrape_images(url: str) -> List[str]:
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            html = response.text
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"Failed to scrape: {e.response.status_code} {e.response.reason_phrase} for url '{url}'\nRedirect location: '{e.response.headers.get('location', 'N/A')}'") from e
    except Exception as e:
        raise RuntimeError(f"Failed to scrape: {str(e)} for url '{url}'") from e

    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')

    image_urls = []
    for img in img_tags:
        if isinstance(img, Tag):
            src = img.get('src')
            if src and isinstance(src, str):
                absolute_url = urljoin(url, src)
                image_urls.append(absolute_url)

    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for u in image_urls:
        if u not in seen:
            unique_urls.append(u)
            seen.add(u)

    return unique_urls