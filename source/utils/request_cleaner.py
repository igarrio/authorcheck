def user_request_cleaner(text: str) -> str:
    """
    Clean user request by removing double underscores, digits,
    and converting to lowercase.
    """
    cleaned = text.replace('__', '')
    cleaned = ''.join(char for char in cleaned if not char.isdigit())
    return cleaned.lower()