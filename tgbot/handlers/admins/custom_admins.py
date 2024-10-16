from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, ReplyKeyboardRemove

from tgbot.handlers.users.start import admins_list
from tgbot.keyboards.inline.catalog import menu


async def admin(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await state.reset_state()

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.insert(KeyboardButton(text="Админы"))
    markup.insert(KeyboardButton(text="Квартиры"))
    markup.insert(KeyboardButton(text="Группы"))
    markup.add(KeyboardButton(text="Главное Меню"))
    await call.bot.send_message(call.from_user.id, "Что вы хотите сделать ?", reply_markup=markup)


async def admin_back(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer("🎛 Главное Меню", reply_markup=ReplyKeyboardRemove())
    await admins_list(message)


def register_custom_admins(dp: Dispatcher):
    dp.register_callback_query_handler(admin, menu.filter(action="admin"))
    dp.register_message_handler(admin_back, text="Главное Меню")