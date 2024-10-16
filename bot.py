import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.db_api.postgresql import Database
from tgbot.config import load_config
from tgbot.filters.is_admin import IsAdmin, IsGroup
from tgbot.handlers.admins.add_admin import register_add_admin
from tgbot.handlers.admins.add_group import register_add_group
from tgbot.handlers.admins.add_object import register_add_object
from tgbot.handlers.admins.add_object2 import register_add_object2
from tgbot.handlers.admins.custom_admins import register_custom_admins

from tgbot.handlers.admins.delete_obj import register_delete_obj
from tgbot.handlers.admins.edit_obj import register_edit_obj
from tgbot.handlers.users.appeals import register_appeals
from tgbot.handlers.users.cart import register_cart
from tgbot.handlers.users.catalog import register_catalog
from tgbot.handlers.users.inline_mode import register_inline_mode
from tgbot.handlers.users.sell import register_sell
from tgbot.handlers.users.start import register_start
from tgbot.middlewares.language_mid import setup_middleware
from tgbot.misc.notify_admins import on_startup_notify
from tgbot.misc.set_bot_commands import set_default_commands

logger = logging.getLogger(__name__)


def register_all_filters(dp):
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsGroup)


def register_all_handlers(dp):
    register_start(dp)

    register_custom_admins(dp)
    register_add_admin(dp)
    register_add_group(dp)
    register_add_object(dp)
    register_add_object2(dp)
    register_edit_obj(dp)
    register_delete_obj(dp)

    register_cart(dp)
    register_catalog(dp)
    register_inline_mode(dp)
    register_sell(dp)
    register_appeals(dp)


async def main():
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    db = Database()
    i18n = setup_middleware(dp)
    lang = i18n.gettext

    bot['config'] = config
    bot['lang'] = lang

    register_all_filters(dp)
    register_all_handlers(dp)

    await db.create()

    # await db.drop_users()
    # await db.drop_admins()
    # await db.drop_flats()
    # await db.drop_cart()
    # await db.drop_groups()

    await db.create_table_users()
    await db.create_table_flats()
    await db.create_table_admins()
    await db.create_table_cart()
    await db.create_table_groups()

    bot['db'] = db

    await set_default_commands(dp)
    await on_startup_notify(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        # asyncio.run(main())
        asyncio.get_event_loop().run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
