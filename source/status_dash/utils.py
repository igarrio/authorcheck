from urllib.parse import urlparse, urlunparse
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def keep_path_only(url: str) -> str:
    url = (url or '').strip()
    parsed = urlparse(url)
    if not parsed.scheme and not parsed.netloc:
        return url
    return urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, parsed.fragment))

def get_iso_kyiv_tz() -> str:
    iso = datetime.now(timezone.utc).isoformat()
    dt = datetime.fromisoformat(iso)
    kyiv_tz = ZoneInfo('Europe/Kyiv')
    dt_kyiv = dt.astimezone(kyiv_tz)
    return dt_kyiv.strftime('%Y-%m-%d %H:%M:%S')