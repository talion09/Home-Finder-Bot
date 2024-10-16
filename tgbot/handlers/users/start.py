from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove, CallbackQuery

from tgbot.keyboards.default.phone import phonenumber, phonenumber_uz
from tgbot.keyboards.inline.catalog import menu, lang_clb
from tgbot.states.users import Sell


async def ru_language(message):
    db = message.bot.get("db")
    user_in_db = await db.select_user(telegram_id=int(message.from_user.id))
    if user_in_db.get("language") == "ru":
        return True


async def admins_list(message):
    db = message.bot.get("db")
    admins_list = []
    for id, telegram_id, name in await db.select_all_admins():
        admins_list.append(telegram_id)

    if await ru_language(message):
        texxt = "Вы находитесь в главном меню бота компании «orientir».\n" \
                "Выполняем обещания соблюдая честность и прозрачность процессов.\n" \
                "Наша компания оказывает комплексные услуги в сфере недвижимости."
        markup = InlineKeyboardMarkup(row_width=2)
        markup.insert(InlineKeyboardButton(text="🏘 Каталог недвижимости", callback_data=menu.new(action="catalog")))
        markup.row(InlineKeyboardButton(text="📃 Лист осмотра", callback_data=menu.new(action="basket")),
                   InlineKeyboardButton(text="💰 Продать", callback_data=menu.new(action="sell")))
        markup.insert(InlineKeyboardButton(text="🧾 Сдать", callback_data=menu.new(action="rent")))
        markup.insert(InlineKeyboardButton(text="ℹ️ О нас", callback_data=menu.new(action="about")))
        markup.insert(InlineKeyboardButton(text="📢 Обращения", callback_data=menu.new(action="appeal")))

        if message.from_user.id in admins_list:
            markup.add(InlineKeyboardButton(text="Администрация", callback_data=menu.new(action="admin")))
    else:
        texxt = "Вы находитесь в главном меню бота компании «orientir».\n" \
                "Выполняем обещания соблюдая честность и прозрачность процессов.\n" \
                "Наша компания оказывает комплексные услуги в сфере недвижимости."
        markup = InlineKeyboardMarkup(row_width=2)
        markup.insert(InlineKeyboardButton(text="🏘 Ko'chmas mulk katalogi", callback_data=menu.new(action="catalog")))
        markup.row(InlineKeyboardButton(text="📃 Tekshirish varaqasi", callback_data=menu.new(action="basket")),
                   InlineKeyboardButton(text="💰 Ob'ekt sotiladi", callback_data=menu.new(action="sell")))
        markup.insert(InlineKeyboardButton(text="🧾 Ob'ektni ijaraga oling", callback_data=menu.new(action="rent")))
        markup.insert(InlineKeyboardButton(text="ℹ️ Biz haqimizda", callback_data=menu.new(action="about")))
        markup.insert(InlineKeyboardButton(text="📢 Murojaatlar", callback_data=menu.new(action="appeal")))

        if message.from_user.id in admins_list:
            markup.add(InlineKeyboardButton(text="Администрация", callback_data=menu.new(action="admin")))
    msg = await message.bot.send_photo(message.from_user.id,
                                       photo="AgACAgIAAxkBAAMEZT5pePpU-8AwZ1WU3H6vsIBo-S8AAkfQMRv1QPhJU4u7bEu072MBAAMCAAN5AAMwBA",
                                       caption=texxt, reply_markup=markup)
    return msg
# AgACAgIAAxkBAAIG7WSO0XcwmM632gv-ObvGAAHeN0LIYgACQ8cxG5pIeEgm__-YTmJnZQEAAwIAA3kAAy8E

async def bot_start(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    await state.reset_state()
    try:
        user_in_db = await db.select_user(telegram_id=int(message.from_user.id))
        username = user_in_db.get("username")
        if username != message.from_user.username:
            await db.update_user(telegram_id=int(message.from_user.id), username=message.from_user.username)
        await admins_list(message)
    except AttributeError:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.insert(InlineKeyboardButton(text="Русский язык🇷🇺", callback_data=lang_clb.new(action="ru")))
        markup.insert(InlineKeyboardButton(text="O'zbek tili🇺🇿", callback_data=lang_clb.new(action="uz")))
        await message.answer(
            f"Здесь вы можете выбрать удобный для Вас язык.\n----------------------------"
            f"-----------\nBu erda Siz o'zingiz uchun qulay bo'lgan tilni tanlashingiz mumkin.",
            reply_markup=markup)


async def info_lang(call: CallbackQuery, callback_data: dict, state: FSMContext):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    action = callback_data.get("action")

    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)

    if action == "ru":
        await call.message.answer("Отправьте ваш номер телефона (9989xxxxxxxx):", reply_markup=phonenumber)
        language = "ru"
    else:
        await call.message.answer("Telefon raqamingizni yuboring (9989xxxxxxxx):", reply_markup=phonenumber_uz)
        language = "uz"

    await Sell.Phone.set()
    await state.update_data(language=language)


# Sell.Phone
async def info_phone(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    _ = message.bot.get("lang")
    data = await state.get_data()
    language = data.get("language")

    admins_list = []
    for id, telegram_id, name in await db.select_all_admins():
        admins_list.append(telegram_id)

    if language == "ru":
        await message.answer("Готово", reply_markup=ReplyKeyboardRemove())
        texxt = "Вы находитесь в главном меню бота компании «orientir».\nВыполняем обещания соблюдая честность и " \
                "прозрачность процессов.\nНаша компания оказывает комплексные услуги в сфере недвижимости."
        markup = InlineKeyboardMarkup(row_width=2)
        markup.insert(InlineKeyboardButton(text="🏘 Каталог недвижимости", callback_data=menu.new(action="catalog")))
        markup.row(InlineKeyboardButton(text="📃 Лист осмотра", callback_data=menu.new(action="basket")),
                   InlineKeyboardButton(text="💰 Продать", callback_data=menu.new(action="sell")))
        markup.insert(InlineKeyboardButton(text="🧾 Сдать", callback_data=menu.new(action="rent")))
        markup.insert(InlineKeyboardButton(text="ℹ️ О нас", callback_data=menu.new(action="about")))
        markup.insert(InlineKeyboardButton(text="📢 Обращения", callback_data=menu.new(action="appeal")))

        if message.from_user.id in admins_list:
            markup.add(InlineKeyboardButton(text="Администрация", callback_data=menu.new(action="admin")))
    else:
        await message.answer("Тайор", reply_markup=ReplyKeyboardRemove())
        texxt = "Вы находитесь в главном меню бота компании «orientir».\nВыполняем обещания соблюдая честность и " \
                "прозрачность процессов.\nНаша компания оказывает комплексные услуги в сфере недвижимости."
        markup = InlineKeyboardMarkup(row_width=2)
        markup.insert(InlineKeyboardButton(text="🏘 Ko'chmas mulk katalogi", callback_data=menu.new(action="catalog")))
        markup.row(InlineKeyboardButton(text="📃 Tekshirish varaqasi", callback_data=menu.new(action="basket")),
                   InlineKeyboardButton(text="💰 Ob'ekt sotiladi", callback_data=menu.new(action="sell")))
        markup.insert(InlineKeyboardButton(text="🧾 Ob'ektni ijaraga oling", callback_data=menu.new(action="rent")))
        markup.insert(InlineKeyboardButton(text="ℹ️ Biz haqimizda", callback_data=menu.new(action="about")))
        markup.insert(InlineKeyboardButton(text="📢 Murojaatlar", callback_data=menu.new(action="appeal")))

        if message.from_user.id in admins_list:
            markup.add(InlineKeyboardButton(text="Администрация", callback_data=menu.new(action="admin")))
    await message.bot.send_photo(message.from_user.id,
                                 photo="AgACAgIAAxkBAAMEZT5pePpU-8AwZ1WU3H6vsIBo-S8AAkfQMRv1QPhJU4u7bEu072MBAAMCAAN5AAMwBA",
                                 caption=texxt, reply_markup=markup)
    await db.add_user(
        first_name=message.from_user.first_name,
        username=message.from_user.username,
        telegram_id=message.from_user.id,
        language=language
    )


async def llalala(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    for i in range(1, 17):
        await db.add_user(
            first_name="fefefg",
            username="fefefg",
            telegram_id=13244 + i,
            language="ru"
        )


def register_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart(deep_link="connect_user"))
    dp.register_message_handler(bot_start, CommandStart(), state="*")
    dp.register_callback_query_handler(info_lang, lang_clb.filter())
    dp.register_message_handler(info_phone, state=Sell.Phone, content_types=types.ContentTypes.CONTACT)
    dp.register_message_handler(llalala, text="lflslfls")
    dp.register_message_handler(bot_start, Command("menu"), state="*")


