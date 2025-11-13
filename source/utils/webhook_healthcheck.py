import logging
import asyncio
from source.utils.tokens import XTBAST

wh_logger = logging.getLogger('WH.Health')

WEBHOOK_CHECK_INTERVAL = 900.0  # seconds between regular checks
WEBHOOK_REPAIR_MAX_ATTEMPTS = 5
WEBHOOK_REPAIR_BASE_DELAY = 10.0  # base for exponential backoff

_webhook_monitor_task: asyncio.Task | None = None
_webhook_monitor_stop = asyncio.Event()
_webhook_monitor_lock = asyncio.Lock()

bot = None


async def ensure_webhook(_wh_url):
    async with _webhook_monitor_lock:
        try:
            info = await bot.get_webhook_info()
        except Exception as e:
            wh_logger.warning(f'Could not get webhook info: {e}')
            raise

        # Check the webhook info
        current_url = getattr(info, 'url')
        last_error = getattr(info, 'last_error_message')

        if not current_url:
            wh_logger.warning('Webhook not configured. Starting recovery.')
            # Recovery attempts
            attempt = 0
            while attempt < WEBHOOK_REPAIR_MAX_ATTEMPTS:
                attempt += 1
                try:
                    await bot.set_webhook(_wh_url, secret_token=XTBAST, max_connections=100)
                    wh_logger.warning(f'Webhook successfully installed on {_wh_url} (attempt {attempt})')
                    return True
                except Exception as e:
                    delay = WEBHOOK_REPAIR_BASE_DELAY * (2 ** (attempt - 1))
                    wh_logger.warning(f'Error while setting_webhook (attempt {attempt}): {e}. Retrying in %.1f s', delay)
                    await asyncio.sleep(delay)
            wh_logger.error(f'Failed to set webhook after {WEBHOOK_REPAIR_MAX_ATTEMPTS} attempts')
            return False

        # If the URL is set but errors occur — log and optional reinstall
        if last_error:
            wh_logger.warning(f'Webhook has a problem: {last_error}; URL={current_url}')
            try:
                await bot.delete_webhook(drop_pending_updates=False)
                await bot.set_webhook(_wh_url, secret_token=XTBAST, max_connections=100)
                wh_logger.warning('Webhook reloaded due to errors')
                return True
            except Exception as e:
                wh_logger.exception(f'Error reloading webhook: {e}')
                return False

        # Webhook ok
        wh_logger.warning(f'Webhook OK: {current_url}')
        return True


async def _webhook_monitor_loop(_wh_url):
    """WebHook Monitor"""
    while not _webhook_monitor_stop.is_set():
        try:
            try:
                ok = await ensure_webhook(_wh_url)
            except Exception as e:
                wh_logger.warning(f'Failed to verify or restore webhook: {e}')
                ok = False

            await asyncio.sleep(WEBHOOK_CHECK_INTERVAL if ok else min(30.0, WEBHOOK_CHECK_INTERVAL))
        except asyncio.CancelledError:
            wh_logger.warning('Webhook monitor cancelled')
            break
        except Exception as e:
            wh_logger.exception(f'Unexpected error in webhook monitor: {e}')
            await asyncio.sleep(5.0)


async def start_webhook_monitor(_bot, _wh_url):
    global _webhook_monitor_task, _webhook_monitor_stop, bot
    bot = _bot
    _webhook_monitor_stop.clear()
    if _webhook_monitor_task is None or _webhook_monitor_task.done():
        _webhook_monitor_task = asyncio.create_task(_webhook_monitor_loop(_wh_url))
        wh_logger.warning('Webhook monitor started')


async def stop_webhook_monitor():
    global _webhook_monitor_task, _webhook_monitor_stop
    _webhook_monitor_stop.set()
    if _webhook_monitor_task is not None:
        _webhook_monitor_task.cancel()
        try:
            await _webhook_monitor_task
        except asyncio.CancelledError:
            pass
    wh_logger.warning('Webhook monitor stopped')
