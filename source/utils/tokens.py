import os
import secrets
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import hmac
import hashlib
import base64
from source.utils.logger_init import logger


bearer_scheme = HTTPBearer(auto_error=False)
API_USER_KEYS = os.getenv('API_SECRET_KEYS', '')
API_ADMIN_KEYS = os.getenv('API_ADMIN_KEYS', '')
USER_TOKENS = {key.strip() for key in API_USER_KEYS.split(',') if key.strip()}
ADMIN_TOKENS = {key.strip() for key in API_ADMIN_KEYS.split(',') if key.strip()}
SERVER_SECRET = secrets.token_bytes(32)
XTBAST = secrets.token_urlsafe(16)

logger.warning(f'Bearer_scheme.auto_error = {bearer_scheme.auto_error}')


def make_wh_token(bot_token: str, trunc: int = 16) -> str:
    mac = hmac.new(SERVER_SECRET, bot_token.encode("utf-8"), hashlib.sha256).digest()
    short = mac[:trunc]
    return base64.urlsafe_b64encode(short).rstrip(b"=").decode("ascii")


async def user_verify_api_key(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = credentials.credentials
    logger.info(f'Verifying token: {token}')
    if token not in USER_TOKENS and token not in ADMIN_TOKENS:
        raise HTTPException(status_code=401, detail='Invalid API token')

async def admin_verify_api_key(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = credentials.credentials
    logger.info(f'Verifying token: {token}')
    if token not in ADMIN_TOKENS:
        raise HTTPException(status_code=401, detail='Invalid API token')
