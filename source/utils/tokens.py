import base64
import hashlib
import hmac
import os
import secrets

from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from source.utils.logger_init import logger


bearer_scheme: HTTPBearer = HTTPBearer(auto_error=False)

API_USER_KEYS: str = os.getenv('API_SECRET_KEYS', '')
API_ADMIN_KEYS: str = os.getenv('API_ADMIN_KEYS', '')

USER_TOKENS: set[str] = {key.strip() for key in API_USER_KEYS.split(',') if key.strip()}
ADMIN_TOKENS: set[str] = {key.strip() for key in API_ADMIN_KEYS.split(',') if key.strip()}

SERVER_SECRET: bytes = secrets.token_bytes(32)
XTBAST: str = secrets.token_urlsafe(16)

logger.warning(f'Bearer_scheme.auto_error = {bearer_scheme.auto_error}')


def make_wh_token(bot_token: str, trunc: int = 16) -> str:
    """Generate webhook URL token from bot token using HMAC-SHA256."""
    mac = hmac.new(SERVER_SECRET, bot_token.encode("utf-8"), hashlib.sha256).digest()
    short = mac[:trunc]
    return base64.urlsafe_b64encode(short).rstrip(b"=").decode("ascii")


async def user_verify_api_key(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme)
) -> None:
    """Verify user or admin API key from Authorization header."""
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = credentials.credentials
    logger.debug(f'Verifying token: {token[:8]}...')
    if token not in USER_TOKENS and token not in ADMIN_TOKENS:
        raise HTTPException(status_code=401, detail='Invalid API token')


async def admin_verify_api_key(
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme)
) -> None:
    """Verify admin API key from Authorization header."""
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = credentials.credentials
    logger.debug(f'Verifying token: {token[:8]}...')
    if token not in ADMIN_TOKENS:
        raise HTTPException(status_code=401, detail='Invalid API token')
