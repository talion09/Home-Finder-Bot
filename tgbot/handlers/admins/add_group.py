from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.filters.is_admin import IsAdmin, IsGroup
from tgbot.states.users import Group


async def groups(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Добавить группу"))
    markup.insert(KeyboardButton(text="Назад"))
    text = "Если вы хотите чтобы записи скидывались вам в группу, то отправьте в группу, в котором добавлен бот, команды:\n\n" \
           "для заказов - /add_orders_group\n" \
           "для обращений - /add_appeal_group\n" \
           "для продаж - /add_sell_group\n" \
           "для тех, кто хочет сдать объект - /add_rent_group\n\n" \
           "Что вы хотите сделать ?"
    await message.answer(text, reply_markup=markup)
    await Group.Next.set()


# Group.Next
async def add_group(message: types.Message, state: FSMContext):
    await state.reset_state()
    if message.text == "Добавить группу":
        bot_name = await message.bot.get_me()
        url = f"t.me/{bot_name.username}?startgroup=true"
        markup = InlineKeyboardMarkup(row_width=2)
        markup.insert(InlineKeyboardButton(text="Добавить", url=url))
        await message.answer("Добавьте бота в свою группу", reply_markup=markup)

        markup1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        markup1.insert(KeyboardButton(text="Админы"))
        markup1.insert(KeyboardButton(text="Квартиры"))
        markup1.insert(KeyboardButton(text="Группы"))
        markup1.add(KeyboardButton(text="Главное Меню"))
        await message.bot.send_message(message.from_user.id, "Что вы хотите сделать ?", reply_markup=markup1)
    elif message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        markup.insert(KeyboardButton(text="Админы"))
        markup.insert(KeyboardButton(text="Квартиры"))
        markup.insert(KeyboardButton(text="Группы"))
        markup.add(KeyboardButton(text="Главное Меню"))
        await message.bot.send_message(message.from_user.id, "Что вы хотите сделать ?", reply_markup=markup)
    else:
        pass


async def add_appeal_group(message: types.Message):
    db = message.bot.get("db")
    try:
        await db.add_group(type_group="appeal_group", name=message.chat.full_name, group_id=message.chat.id)
        await message.answer("Теперь в этой группе будут отображаться записи для обращений!")
    except:
        group = await db.select_group(group_id=int(message.chat.id))
        try:
            group.get("group_id")
            await message.answer("В этой группе уже отображаются записи!")
        except:
            await message.answer("Ошибка! Напишите разработчику!")


async def add_orders_group(message: types.Message):
    db = message.bot.get("db")
    try:
        await db.add_group(type_group="orders_group", name=message.chat.full_name, group_id=message.chat.id)
        await message.answer("Теперь в этой группе будут отображаться записи для заказов!")
    except:
        group = await db.select_group(group_id=int(message.chat.id))
        try:
            group.get("group_id")
            await message.answer("В этой группе уже отображаются записи!")
        except:
            await message.answer("Ошибка! Напишите разработчику!")


async def add_sell_group(message: types.Message):
    db = message.bot.get("db")
    try:
        await db.add_group(type_group="sell_group", name=message.chat.full_name, group_id=message.chat.id)
        await message.answer("Теперь в этой группе будут отображаться записи для продаж!")
    except:
        group = await db.select_group(group_id=int(message.chat.id))
        try:
            group.get("group_id")
            await message.answer("В этой группе уже отображаются записи!")
        except:
            await message.answer("Ошибка! Напишите разработчику!")


async def add_rent_group(message: types.Message):
    db = message.bot.get("db")
    try:
        await db.add_group(type_group="rent_group", name=message.chat.full_name, group_id=message.chat.id)
        await message.answer("Теперь в этой группе будут отображаться записи для тех, кто хочет сдать объект!")
    except:
        group = await db.select_group(group_id=int(message.chat.id))
        try:
            group.get("group_id")
            await message.answer("В этой группе уже отображаются записи!")
        except:
            await message.answer("Ошибка! Напишите разработчику!")


def register_add_group(dp: Dispatcher):
    dp.register_message_handler(groups, IsAdmin(), text="Группы")
    dp.register_message_handler(add_group, IsAdmin(), state=Group.Next)
    dp.register_message_handler(add_appeal_group, IsAdmin(), IsGroup(), Command("add_appeal_group"))
    dp.register_message_handler(add_orders_group, IsAdmin(), IsGroup(), Command("add_orders_group"))
    dp.register_message_handler(add_sell_group, IsAdmin(), IsGroup(), Command("add_sell_group"))
    dp.register_message_handler(add_rent_group, IsAdmin(), IsGroup(), Command("add_rent_group"))

