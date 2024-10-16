from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery

from tgbot.handlers.users.start import ru_language


async def empty(query: types.InlineQuery):
    await query.answer(results=[], cache_time=2)


async def empty_query(query: types.InlineQuery):
    db = query.bot.get('db')
    user = await db.select_user(telegram_id=int(query.from_user.id))
    # "@test_10_10_bot 1-комнатная"
    room = f"%{query.query}%"
    try:
        user.get("first_name")
        inline = InlineKeyboardMarkup()
        flats = await db.select_inline(room=room)
        resultss = []
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in sorted(
                flats):
            if await ru_language(query):
                msg_url = url
                msg_text = text
                msg_descrip = descrip
            else:
                msg_url = url_uz
                msg_text = text_uz
                msg_descrip = desc_uz
            resultss.append(types.InlineQueryResultArticle(
                id=id,
                title=msg_text,
                description=msg_descrip,
                input_message_content=types.InputTextMessageContent(
                    message_text=f" <a href='{msg_url}'>{msg_text}</a>")))
        await query.answer(results=resultss, cache_time=4)
    except:
        await query.answer(results=[],
                           switch_pm_text="Бот недоступен. Подключить бота",
                           switch_pm_parameter="connect_user",
                           cache_time=5)


def register_inline_mode(dp: Dispatcher):
    dp.register_inline_handler(empty, text="")
    dp.register_inline_handler(empty_query)




