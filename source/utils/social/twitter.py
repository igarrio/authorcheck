import re

async def extract_author_from_twitter_url(url):
    pattern = r'https?://(?:twitter\.com|x\.com)/([^/]+)(?:/status/\d+)?'
    matches = re.findall(pattern, url)

    if matches:
        return matches[0]
    else:
        return None