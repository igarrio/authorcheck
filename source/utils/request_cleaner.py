def user_request_cleaner(text):
    _ = text.replace('__', '')
    _ = ''.join(char for char in _ if not char.isdigit())

    return _.lower()