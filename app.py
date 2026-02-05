import asyncio
from contextlib import asynccontextmanager
from secrets import compare_digest
from typing import AsyncGenerator, cast

from a2wsgi import WSGIMiddleware
from aiogram.types import Update
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.types import ASGIApp

from source.bot_init import dp, bot, BOT_TOKEN
from source.database.requests import author_check, author_add
from source.lifespan import on_startup, on_shutdown
from source.states.base import APIAddAuthor
from source.status_dash.checking import schedule_run_checks
from source.status_dash.main import status_app
from source.utils.bot import get_wh_info
from source.utils.custom_feed_update import _feed_update
from source.utils.tokens import user_verify_api_key, admin_verify_api_key, make_wh_token, XTBAST


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager."""
    await on_startup()
    yield
    await on_shutdown()


app = FastAPI(lifespan=lifespan)

app.mount('/status', cast(ASGIApp, WSGIMiddleware(status_app.server)))


@app.get('/api/healthcheck',
         dependencies=[Depends(admin_verify_api_key)],
         include_in_schema=False)
async def health_check() -> JSONResponse:
    """Admin health check endpoint."""
    return JSONResponse('ok', 200)


@app.get('/',
         include_in_schema=False)
async def welcome() -> RedirectResponse:
    """Redirect root to status dashboard."""
    return RedirectResponse(url='/status')


@app.post('/authorcheck/{token}',
          include_in_schema=False)
async def telegram_webhook(token: str, request: Request) -> JSONResponse:
    """Telegram webhook endpoint - receives bot updates."""
    secret_from_tg = request.headers.get('X-Telegram-Bot-Api-Secret-Token')
    expected = make_wh_token(BOT_TOKEN)

    if not compare_digest(token, expected):
        raise HTTPException(status_code=403, detail='Invalid URL token')

    if secret_from_tg != XTBAST:
        raise HTTPException(status_code=403, detail='Invalid Webhook secret')

    update = Update.model_validate(await request.json(), context={'bot': bot})
    asyncio.create_task(_feed_update(dp, bot, update))

    return JSONResponse(status_code=200, content={'ok': True})


@app.get('/check',
         dependencies=[Depends(user_verify_api_key)])
async def api_check(author: str) -> list | None:
    """Public API endpoint to check author in blacklist."""
    return await author_check(author)


@app.get('/get_webhook_info',
         dependencies=[Depends(admin_verify_api_key)])
async def api_get_wh_info():
    """Admin endpoint to get webhook configuration info."""
    return await get_wh_info()


@app.post('/add_author',
          dependencies=[Depends(admin_verify_api_key)],
          status_code=200,
          summary='Add Author',
          description='Adding an author with accompanying content;\n'
                      'Author Type: add_bad/add_good;\n'
                      "Name: Artist's nickname;\n"
                      'Content:\n'
                      '\t\t - add_bad: reason for being blacklisted;\n'
                      '\t\t - add_good: link to one of the social networks.')
async def add_author(payload: APIAddAuthor) -> JSONResponse:
    """Admin endpoint to add author to database."""
    try:
        await author_add(
            payload.author_type,
            payload.name,
            payload.content
        )
        return JSONResponse(status_code=200, content='ok')
    except Exception as e:
        return JSONResponse(status_code=400, content={'error': str(e)})


@app.post('/dash/update_cache',
          dependencies=[Depends(admin_verify_api_key)])
async def update_monitor_cache() -> JSONResponse:
    """Admin endpoint to trigger status dashboard cache refresh."""
    try:
        schedule_run_checks()
        return JSONResponse(status_code=202, content='Monitor cache update started')
    except Exception as e:
        return JSONResponse(status_code=400, content={'error': str(e)})
