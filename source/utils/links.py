async def detect_link(text):
    _ = text.split()
    for word in _:
        if word.startswith('https://x.com') or word.startswith('https://twitter.com'):
            return 1
        elif word.startswith('https://www.pixiv.net'):
            return 2
    return 0
