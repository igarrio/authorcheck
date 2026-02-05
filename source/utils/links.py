async def detect_link(text: str) -> int:
    """
    Detect social media link type in text.

    Returns:
        1 - Twitter/X link
        2 - Pixiv link
        0 - No recognized link
    """
    words = text.split()
    for word in words:
        if word.startswith('https://x.com') or word.startswith('https://twitter.com'):
            return 1
        elif word.startswith('https://www.pixiv.net'):
            return 2
    return 0
