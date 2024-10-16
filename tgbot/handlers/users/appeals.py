from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, factory
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMedia, InputFile, \
    InputMediaPhoto, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

from tgbot.handlers.users.sell import get_name
from tgbot.handlers.users.start import ru_language, admins_list, bot_start
from tgbot.keyboards.inline.catalog import menu, categ, type_categ, room_clb, regions_next, regions_back, quarter_clb, \
    slider, regions_cmrc, quarter_cmrc, delete_cart, info_clb, info_lng, appeal_clb
from tgbot.states.users import Sell, Appeal


async def appeals(call: CallbackQuery):
    db = call.bot.get("db")
    _ = call.bot.get("lang")

    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)

    send_text = _("Выберите тип обращения:")
    claim = _("🔔 Жалоба")
    comment = _("🗣 Отзыв")
    partner = _("👥 Партнёр")
    main_menu = _("🎛 В главное меню")

    inline = InlineKeyboardMarkup(row_width=3)
    inline.insert(InlineKeyboardButton(text=claim, callback_data=appeal_clb.new(action="claim")))
    inline.insert(InlineKeyboardButton(text=comment, callback_data=appeal_clb.new(action="comment")))
    inline.insert(InlineKeyboardButton(text=partner, callback_data=appeal_clb.new(action="partner")))
    inline.row(InlineKeyboardButton(text=main_menu, callback_data=appeal_clb.new(action="main_menu")))

    await call.bot.send_message(call.from_user.id, send_text, reply_markup=inline)


async def appeals2(call: CallbackQuery, callback_data: dict, state: FSMContext):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    action = callback_data.get("action")

    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    send_text = _("Опишите суть вопроса.")
    back = _("Назад")
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton(text=back))
    if action == "claim":
        await Appeal.Get.set()
        await call.bot.send_message(call.from_user.id, send_text, reply_markup=markup)
        await state.update_data(action="claim")
    elif action == "comment":
        await Appeal.Get.set()
        await call.bot.send_message(call.from_user.id, send_text, reply_markup=markup)
        await state.update_data(action="comment")
    elif action == "partner":
        await Appeal.Get.set()
        await call.bot.send_message(call.from_user.id, send_text, reply_markup=markup)
        await state.update_data(action="partner")
    else:
        await admins_list(call)


# Appeal.Get
async def get_appeal(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    _ = message.bot.get("lang")
    data = await state.get_data()
    action = data.get("action")

    await state.reset_state()
    await message.bot.delete_message(message.from_user.id, message.message_id)

    if action == "claim":
        appeal_txt = "🔔 Жалоба"
    elif action == "comment":
        appeal_txt = "🗣 Отзыв"
    else:
        appeal_txt = "👥 Партнёр"

    done = _("Готово")
    back = _("Назад")
    send_appeal = _("📢 Обращения")
    if message.text == back:
        await message.answer(send_appeal, reply_markup=ReplyKeyboardRemove())
        send_text = _("Выберите тип обращения:")
        claim = _("🔔 Жалоба")
        comment = _("🗣 Отзыв")
        partner = _("👥 Партнёр")
        main_menu = _("🎛 В главное меню")

        inline = InlineKeyboardMarkup(row_width=3)
        inline.insert(InlineKeyboardButton(text=claim, callback_data=appeal_clb.new(action="claim")))
        inline.insert(InlineKeyboardButton(text=comment, callback_data=appeal_clb.new(action="comment")))
        inline.insert(InlineKeyboardButton(text=partner, callback_data=appeal_clb.new(action="partner")))
        inline.row(InlineKeyboardButton(text=main_menu, callback_data=appeal_clb.new(action="main_menu")))

        await message.bot.send_message(message.from_user.id, send_text, reply_markup=inline)
    else:
        await message.answer(done, reply_markup=ReplyKeyboardRemove())
        await admins_list(message)
        groups = await db.select_group(type_group="appeal_group")
        appeal_group = groups.get("group_id")
        username = await get_name(message.from_user.id, message)
        text = f"{username} -- {appeal_txt}\n\n{message.text}"
        await message.bot.send_message(chat_id=int(appeal_group), text=text)


def register_appeals(dp: Dispatcher):
    dp.register_callback_query_handler(appeals, menu.filter(action="appeal"))
    dp.register_callback_query_handler(appeals2, appeal_clb.filter())
    dp.register_message_handler(get_appeal, state=Appeal.Get)

