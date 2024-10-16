from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove

from tgbot.filters.is_admin import IsAdmin
from tgbot.handlers.admins.add_object import custom_flats
from tgbot.handlers.admins.functions import rooms_admin, regions_admin, quarters_admin
from tgbot.handlers.users.start import admins_list
from tgbot.keyboards.inline.catalog import edit_slider, del_slider
from tgbot.states.users import Edit_obj, Edit_room, Edit_region, Edit_quarter, Delete_obj


async def delete_flat(message: types.Message):
    db = message.bot.get("db")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Купить"))
    markup.insert(KeyboardButton(text="Снять"))
    markup.insert(KeyboardButton(text="Главное Меню"))
    markup.insert(KeyboardButton(text="Назад"))
    await message.answer("Выберите категорию:", reply_markup=markup)
    await Delete_obj.Categ.set()


# Delete_obj.Categ
async def delete_in_categ(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.reset_state()
        await custom_flats(message)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Квартира"))
        markup.insert(KeyboardButton(text="Коммерческое"))
        markup.insert(KeyboardButton(text="Назад"))
        await message.answer("Выберите категорию:", reply_markup=markup)
        await state.update_data(categ=message.text)
        await Delete_obj.Types.set()


# Delete_obj.Types
async def delete_in_types(message: types.Message, state: FSMContext):
    data = await state.get_data()
    categ = data.get("categ")
    types = message.text
    if message.text == "Назад":
        await state.reset_state()
        await delete_flat(message)
    elif message.text == "Квартира":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        lst = await rooms_admin(message, categ, types)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите количество комнат", reply_markup=markup)
        await state.update_data(types=types)
        await Delete_obj.Room.set()
    else:
        roomm = 0
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        lst = await regions_admin(message, categ, types, roomm)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите район", reply_markup=markup)
        await state.update_data(types=types)
        await state.update_data(roomm=roomm)
        await Delete_obj.Region.set()


# Delete_obj.Room
async def delete_in_room(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Квартира"))
        markup.insert(KeyboardButton(text="Коммерческое"))
        markup.insert(KeyboardButton(text="Назад"))
        await message.answer("Выберите категорию:", reply_markup=markup)
        await Delete_obj.Types.set()
    else:
        select = await db.select_flat(room=roomm)
        room_code = select.get("room_code")
        await state.update_data(roomm=roomm)
        await state.update_data(room_code=room_code)
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        lst = await regions_admin(message, categ, types, roomm)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите район", reply_markup=markup)
        await Delete_obj.Region.set()


# Delete_obj.Region
async def delete_in_regions(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("roomm")
    region = message.text
    if message.text == "Назад":
        if types == "Квартира":
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            lst = await rooms_admin(message, categ, types)
            for button in lst:
                markup.insert(button)
            await message.answer("Выберите количество комнат", reply_markup=markup)
            await Delete_obj.Room.set()
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.insert(KeyboardButton(text="Квартира"))
            markup.insert(KeyboardButton(text="Коммерческое"))
            markup.insert(KeyboardButton(text="Назад"))
            await message.answer("Выберите категорию:", reply_markup=markup)
            await Delete_obj.Types.set()
    else:
        select = await db.select_flat(sub1category=region)
        sub1_code = select.get("sub1_code")
        await state.update_data(region=region)
        await state.update_data(sub1_code=sub1_code)
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        lst = await quarters_admin(message, categ, types, roomm, region)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите квартал", reply_markup=markup)
        await Delete_obj.Quarter.set()


# Delete_obj.Quarter
async def delete_in_quarter(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("roomm")
    region = data.get("region")
    quarter = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        lst = await regions_admin(message, categ, types, roomm)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите район", reply_markup=markup)
        await Edit_obj.Region.set()
    else:
        await message.answer("Выберите квартиру", reply_markup=ReplyKeyboardRemove())
        select = await db.select_flat(category=categ, type=types, room=str(roomm), sub1category=region, sub2category=quarter)
        categ_code = int(select.get("catg_code"))
        type_code = int(select.get("type_code"))
        room_code = int(select.get("room_code"))
        sub1_code = int(select.get("sub1_code"))
        sub2_code = int(select.get("sub2_code"))

        ids = []
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in sorted(
                await db.select_flats(catg_code=categ_code, type_code=type_code, room_code=room_code,
                                      sub1_code=sub1_code, sub2_code=sub2_code)):
            if id not in ids:
                ids.append(id)
        flat = await db.select_flat(id=int(ids[0]))
        flat_id = int(flat.get("id"))
        flat_index = ids.index(flat_id)
        msg_url = flat.get("url")
        msg_text = flat.get("text")
        msg_descrip = flat.get("descrip")
        await state.reset_state()

        markup = InlineKeyboardMarkup(row_width=1)
        next = InlineKeyboardButton(text="⬅️",
                                    callback_data=del_slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code,
                                                             action="back_slide"))
        page = InlineKeyboardButton(text=f"1/{len(ids)}",
                                    callback_data=del_slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code,
                                                             action="none"))
        back = InlineKeyboardButton(text="➡️",
                                    callback_data=del_slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code,
                                                             action="next_slide"))
        markup.row(next, page, back)
        markup.insert(InlineKeyboardButton(text="Удалить",
                                           callback_data=del_slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code,
                                                                    action="delete")))
        markup.insert(InlineKeyboardButton(text="Назад",
                                           callback_data=del_slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code,
                                                                    action="back")))
        await message.bot.send_message(message.from_user.id, text=f" <a href='{msg_url}'>{msg_text}</a>\n\n{msg_descrip}",
                                    reply_markup=markup)


async def del_sliderr(call: CallbackQuery, callback_data: dict, state: FSMContext):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    flat_id = int(callback_data.get("id"))
    flat_index = int(callback_data.get("index"))
    sub2_codee = int(callback_data.get("sub2_code"))

    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)

    flat = await db.select_flat(id=flat_id)
    catg_code = int(flat.get("catg_code"))
    room_code = int(flat.get("room_code"))

    id_list = []
    for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in sorted(
            await db.ids_in_flats_sub2(sub2_code=sub2_codee, room_code=room_code, catg_code=catg_code)):
        if id not in id_list:
            id_list.append(id)

    if callback_data.get("action") == 'delete':
        await call.bot.send_message(call.from_user.id,
                                    text=f"Объект успешно удален из базы данных")
        await db.delete_flat(id=flat_id)
    elif callback_data.get("action") == 'back':
        flat = await db.select_flat(id=flat_id)
        categ = flat.get("category")
        typess = flat.get("type")
        roomm = flat.get("room")
        region = flat.get("sub1category")
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        lst = await quarters_admin(call, categ, typess, roomm, region)
        for button in lst:
            markup.insert(button)
        await call.bot.send_message(call.from_user.id, "Выберите квартал", reply_markup=markup)
        await Delete_obj.Quarter.set()
        await state.update_data(categ=categ)
        await state.update_data(types=typess)
        await state.update_data(roomm=roomm)
        await state.update_data(region=region)
    else:
        if callback_data.get("action") == 'back_slide':
            flat_index -= 1
        elif callback_data.get("action") == 'next_slide':
            flat_index += 1
        else:
            pass

        current_index = flat_index
        if flat_index < 0:
            current_index = len(id_list) - 1
        elif flat_index >= len(id_list):
            current_index = 0

        flat_id = id_list[current_index]
        flat = await db.select_flat(id=int(flat_id))
        msg_url = flat.get("url")
        msg_text = flat.get("text")
        msg_descrip = flat.get("descrip")

        markup = InlineKeyboardMarkup(row_width=1)
        next = InlineKeyboardButton(text="⬅️",
                                    callback_data=del_slider.new(id=flat_id, index=current_index, sub2_code=sub2_codee,
                                                                  action="back_slide"))
        page = InlineKeyboardButton(text=f"{current_index + 1}/{len(id_list)}",
                                    callback_data=del_slider.new(id=flat_id, index=current_index, sub2_code=sub2_codee,
                                                                  action="none"))
        backk = InlineKeyboardButton(text="➡️", callback_data=del_slider.new(id=flat_id, index=current_index,
                                                                              sub2_code=sub2_codee,
                                                                              action="next_slide"))
        markup.row(next, page, backk)
        markup.insert(InlineKeyboardButton(text="Удалить",
                                           callback_data=del_slider.new(id=flat_id, index=current_index,
                                                                         sub2_code=sub2_codee, action="delete")))
        markup.insert(InlineKeyboardButton(text="Назад",
                                           callback_data=del_slider.new(id=flat_id, index=flat_index, sub2_code=sub2_codee,
                                                                    action="back")))
        await call.bot.send_message(call.from_user.id, text=f" <a href='{msg_url}'>{msg_text}</a>\n\n{msg_descrip}",
                                    reply_markup=markup)


def register_delete_obj(dp: Dispatcher):
    dp.register_message_handler(delete_flat, IsAdmin(), text="Удалить Квартиру")
    dp.register_message_handler(delete_in_categ, IsAdmin(), state=Delete_obj.Categ, text=["Купить", "Снять", "Назад"])
    dp.register_message_handler(delete_in_types, IsAdmin(), state=Delete_obj.Types, text=["Квартира", "Коммерческое", "Назад"])
    dp.register_message_handler(delete_in_room, IsAdmin(), state=Delete_obj.Room)
    dp.register_message_handler(delete_in_regions, IsAdmin(), state=Delete_obj.Region)
    dp.register_message_handler(delete_in_quarter, IsAdmin(), state=Delete_obj.Quarter)
    dp.register_callback_query_handler(del_sliderr, del_slider.filter())