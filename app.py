import asyncio
from fastapi import FastAPI, Request, HTTPException, Security, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from aiogram.types import Update
from contextlib import asynccontextmanager
from secrets import compare_digest
from a2wsgi import WSGIMiddleware
from starlette.types import ASGIApp
from typing import cast
from source.bot_init import dp, on_startup, on_shutdown, bot, BOT_TOKEN, get_webhook_info
from source.database.requests import author_check, author_add
from source.utils.tokens import user_verify_api_key, admin_verify_api_key, make_wh_token, XTBAST
from source.utils.custom_feed_update import _feed_update
from source.states.base import APIAddAuthor
from source.status_dash.main import status_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    yield
    await on_shutdown()

app = FastAPI(lifespan=lifespan)

app.mount('/status', cast(ASGIApp, WSGIMiddleware(status_app.server)))


@app.get('/api/healthcheck', dependencies=[Depends(admin_verify_api_key)], include_in_schema=False)
async def health_check():
    return JSONResponse('ok', 200)

@app.get('/')
async def welcome():
    return RedirectResponse(url='/status')


@app.post('/authorcheck/{token}', include_in_schema=False)
async def telegram_webhook(token: str, request: Request):
    secret_from_tg = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    expected = make_wh_token(BOT_TOKEN)
    if not compare_digest(token, expected):
        raise HTTPException(status_code=403, detail='Invalid URL token')

    if not secret_from_tg == XTBAST:
        raise HTTPException(status_code=403, detail='Invalid Webhook secret')

    update = Update.model_validate(await request.json(), context={'bot': bot})
    asyncio.create_task(_feed_update(dp, bot, update))

    return JSONResponse(status_code=200, content={'ok': True})


@app.get('/check', dependencies=[Depends(user_verify_api_key)])
async def api_check(author: str):
    return await author_check(author)

@app.get('/get_webhook_info', dependencies=[Depends(admin_verify_api_key)])
async def api_get_wh_info():
    return await get_webhook_info()

@app.post('/add_author',
          dependencies=[Depends(admin_verify_api_key)],
          status_code=200,
          summary='Add Author',
          description='Adding an author with accompanying content;\n'
                      'Author Type: add_bad/add_good;\n'
                      "Name: Artist's nickname;\n"
                      'Content:\n'
                      '\t\t - add_bad: reason for being blacklisted;\n'
                      '\t\t - add_good: link to one of the social networks.'
          )
async def add_author(payload: APIAddAuthor):
    try:
        await author_add(
            payload.author_type,
            payload.name,
            payload.content)
        return JSONResponse(status_code=200, content='ok')
    except Exception as e:
        return JSONResponse(status_code=400, content=e)
