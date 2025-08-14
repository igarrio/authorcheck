import os
from fastapi import FastAPI, Request, HTTPException, Security, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from aiogram.types import Update
from contextlib import asynccontextmanager
from source.bot_init import dp, on_startup, on_shutdown, bot
from source.database.requests import author_check


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    yield
    await on_shutdown()

app = FastAPI(lifespan=lifespan)
bearer_scheme = HTTPBearer()
API_SECRET_KEYS = os.getenv('API_SECRET_KEYS', '')
VALID_TOKENS = {key.strip() for key in API_SECRET_KEYS.split(',') if key.strip()}

async def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    if credentials.credentials not in VALID_TOKENS:
        raise HTTPException(status_code=401, detail='Unauthorized')


@app.get('/api/healthcheck', dependencies=[Depends(verify_api_key)])
async def health_check():
    return JSONResponse('ok', 200)


@app.post('/webhook/{token}')
async def telegram_webhook(token: str, request: Request):
    from source.bot_init import BOT_TOKEN
    if token != BOT_TOKEN:
        raise HTTPException(status_code=403, detail='Invalid token')

    update = Update.model_validate(await request.json(), context={'bot': bot})
    await dp.feed_update(bot, update)

    return JSONResponse('ok', 200)

@app.get('/check', dependencies=[Depends(verify_api_key)])
async def api_check(author: str):
    return await author_check(author)
