from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, factory
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMedia, InputFile, \
    InputMediaPhoto, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from tgbot.handlers.users.start import ru_language, admins_list, bot_start
from tgbot.keyboards.inline.catalog import menu, categ, type_categ, room_clb, regions_next, regions_back, quarter_clb, \
    slider, regions_cmrc, quarter_cmrc, delete_cart, info_clb, info_lng
from tgbot.states.users import Sell


async def sell_obj(call: CallbackQuery, state: FSMContext):
    db = call.bot.get("db")
    _ = call.bot.get("lang")

    await call.answer()
    sell_text = _("Опишите Ваш объект. \nНапример: 2 комнатная, Юнусабад 13.")
    back = _("Назад")
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text=back))

    await call.bot.send_message(call.from_user.id, sell_text, reply_markup=markup)
    await Sell.Sell_obj.set()


# Sell.Sell_obj
async def sell_obj2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    _ = message.bot.get("lang")

    await state.reset_state()

    done = _("Готово. Мы скоро свяжемся с вами")
    back = _("Назад")
    main_menu = _("Главное Меню")
    if message.text == back:
        await message.answer(main_menu, reply_markup=ReplyKeyboardRemove())
        await bot_start(message, state)
    else:
        await message.answer(done, reply_markup=ReplyKeyboardRemove())
        await bot_start(message, state)
        groups = await db.select_group(type_group="sell_group")
        sell_group = groups.get("group_id")
        username = await get_name(message.from_user.id, message)
        text = f"{username} -- 💰 Продать объект\n\n{message.text}"
        await message.bot.send_message(chat_id=int(sell_group), text=text)


async def get_name(id, message):
    db = message.bot.get("db")
    user = await db.select_user(telegram_id=int(id))
    username = user.get("username")
    first_name = user.get("first_name")
    if username:
        player = f"@{username}"
    else:
        player = f"<a href='tg://user?id={id}'>{first_name}</a>"
    return player


async def rent_obj(call: CallbackQuery, state: FSMContext):
    db = call.bot.get("db")
    _ = call.bot.get("lang")

    await call.answer()
    sell_text = _("Опишите Ваш объект. \nНапример: 2 комнатная, Юнусабад 13.")
    back = _("Назад")
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text=back))

    await call.bot.send_message(call.from_user.id, sell_text, reply_markup=markup)
    await Sell.Rent_obj.set()


# Sell.Rent_obj
async def rent_obj2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    _ = message.bot.get("lang")

    await state.reset_state()

    done = _("Готово. Мы скоро свяжемся с вами")
    back = _("Назад")
    main_menu = _("Главное Меню")
    if message.text == back:
        await message.answer(main_menu, reply_markup=ReplyKeyboardRemove())
        await bot_start(message, state)
    else:
        await message.answer(done, reply_markup=ReplyKeyboardRemove())
        await bot_start(message, state)
        groups = await db.select_group(type_group="rent_group")
        rent_group = groups.get("group_id")
        username = await get_name(message.from_user.id, message)
        text = f"{username} -- 🧾 Сдать объект\n\n{message.text}"
        await message.bot.send_message(chat_id=int(rent_group), text=text)


async def info(call: CallbackQuery, state: FSMContext):
    db = call.bot.get("db")
    _ = call.bot.get("lang")

    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    site = f" <a href='https://orientiruzb.uz/'>orientiruzb.uz</a>"
    inst = f" <a href='https://www.instagram.com/orientir.uz/'>orientir.uz</a>"
    text = f"Наш сайт: {site}\nНаш инста: {inst}\n"
    change_lng = _("🔄 Изменить язык")
    main_menu = _("🎛 В главное меню")
    loc = "📍 Локация"

    inline = InlineKeyboardMarkup(row_width=1)
    inline.insert(InlineKeyboardButton(text=change_lng, callback_data=info_clb.new(action="change_lng")))
    inline.insert(InlineKeyboardButton(text=main_menu, callback_data=info_clb.new(action="main_menu")))
    inline.insert(InlineKeyboardButton(text=loc, callback_data=info_clb.new(action="location")))
    await call.bot.send_message(call.from_user.id, text, reply_markup=inline)


async def info_lang(call: CallbackQuery):
    db = call.bot.get("db")
    _ = call.bot.get("lang")

    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    text = "Перед использованием сервиса выберите язык.\n" \
           "----------------------------------------\nХизматдан фойдаланишдан олдин тилни танланг.\n"

    inline = InlineKeyboardMarkup(row_width=1)
    inline.insert(InlineKeyboardButton(text="Русский язык 🇷🇺", callback_data=info_lng.new(action="ru")))
    inline.insert(InlineKeyboardButton(text="Узбек тили 🇺🇿", callback_data=info_lng.new(action="uz")))
    await call.bot.send_message(call.from_user.id, text, reply_markup=inline)


async def info_lang2(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    action = callback_data.get("action")

    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await db.update_user(telegram_id=call.from_user.id, language=action)
    await admins_list(call)


async def info_lang3(call: CallbackQuery):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await admins_list(call)


async def locat(call: CallbackQuery, state: FSMContext):
    db = call.bot.get("db")
    _ = call.bot.get("lang")

    await call.answer()
    await call.bot.send_location(call.from_user.id, latitude=41.353247, longitude=69.386786)

def register_sell(dp: Dispatcher):
    dp.register_callback_query_handler(sell_obj, menu.filter(action="sell"))
    dp.register_message_handler(sell_obj2, state=Sell.Sell_obj)

    dp.register_callback_query_handler(rent_obj, menu.filter(action="rent"))
    dp.register_message_handler(rent_obj2, state=Sell.Rent_obj)

    dp.register_callback_query_handler(info, menu.filter(action="about"))
    dp.register_callback_query_handler(locat, info_clb.filter(action="location"))

    dp.register_callback_query_handler(info_lang, info_clb.filter(action="change_lng"))
    dp.register_callback_query_handler(info_lang2, info_lng.filter())
    dp.register_callback_query_handler(info_lang3, info_clb.filter(action="main_menu"))





