import json
import re
from typing import Any

import httpx
from bs4 import BeautifulSoup

from source.utils.social.base import PixivDataForParsing


async def process_pixiv(user_request: str) -> str | None:
    """Extract author name from Pixiv URL."""
    match = re.search(r'\d+', user_request)
    if not match:
        return None

    id_from_link = match.group()

    if 'bookmarks' in user_request:
        pixiv_obj = PixivDataForParsing(
            url=f'https://www.pixiv.net/en/users/{id_from_link}',
            meta_count=15,
            link_type='user',
            job_id=id_from_link,
            target='name'
        )
        return await extract_author_from_pixiv_url(pixiv_obj)
    elif 'artworks' in user_request:
        pixiv_obj = PixivDataForParsing(
            url=user_request,
            meta_count=26,
            link_type='illust',
            job_id=id_from_link,
            target='userAccount'
        )
        return await extract_author_from_pixiv_url(pixiv_obj)
    elif 'users' in user_request:
        pixiv_obj = PixivDataForParsing(
            url=user_request,
            meta_count=15,
            link_type='user',
            job_id=id_from_link,
            target='name'
        )
        return await extract_author_from_pixiv_url(pixiv_obj)
    elif 'illustrations' in user_request:
        pixiv_obj = PixivDataForParsing(
            url=f'https://www.pixiv.net/en/users/{id_from_link}',
            meta_count=15,
            link_type='user',
            job_id=id_from_link,
            target='name'
        )
        return await extract_author_from_pixiv_url(pixiv_obj)

    return None


async def extract_author_from_pixiv_url(pixiv_obj: PixivDataForParsing) -> Any:
    """Fetch and parse author data from Pixiv page metadata."""
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(pixiv_obj.url)

    page = BeautifulSoup(response.text, 'html.parser')
    meta_tags = page.find_all('meta')
    meta_tag = meta_tags[pixiv_obj.meta_count]['content']
    data = json.loads(meta_tag)

    return data[pixiv_obj.link_type][pixiv_obj.job_id][pixiv_obj.target]