from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, factory
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMedia, InputFile, \
    InputMediaPhoto
from aiogram.utils.callback_data import CallbackData

from tgbot.handlers.users.sell import get_name
from tgbot.handlers.users.start import ru_language, admins_list
from tgbot.keyboards.inline.catalog import menu, categ, type_categ, room_clb, regions_next, regions_back, quarter_clb, \
    slider, regions_cmrc, quarter_cmrc, delete_cart


async def user_cart(call: CallbackQuery):
    db = call.bot.get("db")
    _ = call.bot.get("lang")

    await call.answer()
    null_cart = _("Добавьте из каталога недвижимости объекты, которые Вам понравятся. Осмотр объектов совершенно"
                  " бесплатный! Мы понимаем, что выбор недвижимости сложный и тонкий вопрос. Мы готовы помочь!"
                  " И конечно будем рады познакомится лично!)")
    text_cart = _("Вы можете добавить в «Лист осмотра» все понравившиеся объекты и оформить их осмотр. "
                 "Осмотр объектов совершенно бесплатный! Мы понимаем, что выбор недвижимости сложный "
                 "и тонкий вопрос. Мы готовы помочь! И конечно будем рады познакомится лично!)\n\n")
    add = _("Добавить объекты")
    back = _("Назад")
    order = _("Оформить осмотр")

    user_cart = await db.select_cart(telegram_id=call.from_user.id)
    if user_cart:
        await call.bot.delete_message(call.from_user.id, call.message.message_id)
        markup = InlineKeyboardMarkup(row_width=3)
        objects = []
        for id, telegram_id, object_id in await db.select_all_objects(telegram_id=call.from_user.id):
            if object_id not in objects:
                objects.append(object_id)
                object = await db.select_flat(id=int(object_id))
                url = object.get("url")
                room = object.get("room")
                url_uz = object.get("url_uz")
                room_uz = object.get("room_uz")
                text = object.get("text")
                text_uz = object.get("text_uz")


                if await ru_language(call):
                    text_cart += f" <a href='{url}'>{room}</a>\n"
                    msg_text = text
                else:
                    text_cart += f" <a href='{url_uz}'>{room_uz}</a>\n"
                    msg_text = text_uz

                markup.insert(InlineKeyboardButton(text=f"{msg_text} ❌",
                                                   callback_data=delete_cart.new(object_id=object_id, action="delete")))
        markup.row(InlineKeyboardButton(text=add, callback_data=delete_cart.new(object_id=0, action="add")))
        markup.row(InlineKeyboardButton(text=back, callback_data=delete_cart.new(object_id=0, action="back")))
        markup.row(InlineKeyboardButton(text=order, callback_data=delete_cart.new(object_id=0, action="order")))
        await call.bot.send_message(call.from_user.id, text=text_cart, reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup(row_width=3)
        markup.row(InlineKeyboardButton(text=add, callback_data=delete_cart.new(object_id=0, action="add")))
        await call.bot.delete_message(call.from_user.id, call.message.message_id)
        await call.bot.send_message(call.from_user.id, text=null_cart, reply_markup=markup)


async def delete_from_cart(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    object_id = int(callback_data.get("object_id"))

    await call.answer()
    count = await db.count_cart(telegram_id=call.from_user.id)
    if int(count) > 1:
        pass
    else:
        await call.bot.delete_message(call.from_user.id, call.message.message_id)
        await admins_list(call)
    await db.delete_cart(telegram_id=call.from_user.id, object_id=object_id)
    await user_cart(call)


async def back_from_cart(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await admins_list(call)


async def order_cart(call: CallbackQuery):
    db = call.bot.get("db")
    _ = call.bot.get("lang")

    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)

    username = await get_name(call.from_user.id, call)
    text_cart = _("Корзина ")
    text_cart += f"{username}:\n\n"
    done = _("Готово. Мы скоро свяжемся с вами")

    objects = []
    for id, telegram_id, object_id in await db.select_all_objects(telegram_id=call.from_user.id):
        if object_id not in objects:
            objects.append(object_id)
            object = await db.select_flat(id=int(object_id))
            url = object.get("url")
            room = object.get("room")
            id = object.get("id")
            text_cart += f" <a href='{url}'>{room}</a> - {id}\n"

    await db.delete_whole_cart(telegram_id=call.from_user.id)
    await call.bot.send_message(call.from_user.id, text=done)

    groups = await db.select_group(type_group="orders_group")
    orders_group = groups.get("group_id")
    await call.bot.send_message(chat_id=int(orders_group), text=text_cart)
    await admins_list(call)


async def add_owner(message: types.Message):
    db = message.bot.get('db')
    await db.add_administrator(telegram_id=int(153479611), name="Мухаммад")


async def msg_photo_id(message: types.Message):
    await message.answer(message.photo[-1].file_id)


def register_cart(dp: Dispatcher):
    dp.register_callback_query_handler(user_cart, menu.filter(action="basket"))
    dp.register_callback_query_handler(delete_from_cart, delete_cart.filter(action="delete"))
    dp.register_callback_query_handler(back_from_cart, delete_cart.filter(action="back"))
    dp.register_callback_query_handler(order_cart, delete_cart.filter(action="order"))
    dp.register_message_handler(add_owner, Command("add_owner"))
    dp.register_message_handler(msg_photo_id, content_types=types.ContentTypes.PHOTO)



