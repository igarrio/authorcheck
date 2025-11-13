import json
import re
import httpx
from bs4 import BeautifulSoup
from source.utils.social.base import PixivDataForParsing


async def process_pixiv(user_request):
    id_from_link = (re.search(r'\d+', user_request)).group()
    if 'bookmarks' in user_request:
        pixiv_obj = PixivDataForParsing(f'https://www.pixiv.net/en/users/{id_from_link}',
                                        15,
                                        'user',
                                        id_from_link,
                                        'name')
        return await extract_author_from_pixiv_url(pixiv_obj)
    elif 'artworks' in user_request:
        pixiv_obj = PixivDataForParsing(user_request,
                                        26,
                                        'illust',
                                        id_from_link,
                                        'userAccount')
        return await extract_author_from_pixiv_url(pixiv_obj)
    elif 'users' in user_request:
        pixiv_obj = PixivDataForParsing(user_request,
                                        15,
                                        'user',
                                        id_from_link,
                                        'name')
        return await extract_author_from_pixiv_url(pixiv_obj)
    elif 'illustrations':
        pixiv_obj = PixivDataForParsing(f'https://www.pixiv.net/en/users/{id_from_link}',
                                        15,
                                        'user',
                                        id_from_link,
                                        'name')
        return await extract_author_from_pixiv_url(pixiv_obj)


async def extract_author_from_pixiv_url(pixiv_obj):
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(pixiv_obj.url)
    page = BeautifulSoup(response.text, 'html.parser')

    _ = page.find_all('meta')
    meta_tag = (_[pixiv_obj.meta_count])['content']
    data = json.loads(meta_tag)
    return data[pixiv_obj.link_type][pixiv_obj.job_id][pixiv_obj.target]