from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove

from tgbot.filters.is_admin import IsAdmin
from tgbot.handlers.admins.add_object import custom_flats
from tgbot.handlers.admins.functions import rooms_admin, regions_admin, quarters_admin
from tgbot.handlers.users.start import admins_list
from tgbot.keyboards.default.cancel import back, confirm
from tgbot.keyboards.inline.catalog import edit_slider
from tgbot.states.users import Edit_obj, Edit_room, Edit_region, Edit_quarter


async def edit_flat(message: types.Message):
    db = message.bot.get("db")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Купить"))
    markup.insert(KeyboardButton(text="Снять"))
    markup.insert(KeyboardButton(text="Главное Меню"))
    markup.insert(KeyboardButton(text="Назад"))
    await message.answer("Выберите категорию:", reply_markup=markup)
    await Edit_obj.Categ.set()


# Edit_obj.Categ
async def edit_in_categ(message: types.Message, state: FSMContext):
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
        await Edit_obj.Types.set()


# Edit_obj.Types
async def edit_in_types(message: types.Message, state: FSMContext):
    data = await state.get_data()
    categ = data.get("categ")
    types = message.text
    if message.text == "Назад":
        await state.reset_state()
        await edit_flat(message)
    elif message.text == "Квартира":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Продолжить"))
        lst = await rooms_admin(message, categ, types)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите количество комнат для редактирования или продолжите дальше", reply_markup=markup)
        await state.update_data(types=types)
        await Edit_obj.Room.set()
    else:
        roomm = 0
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Продолжить"))
        lst = await regions_admin(message, categ, types, roomm)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите район для редактирования или продолжите дальше", reply_markup=markup)
        await state.update_data(types=types)
        await state.update_data(roomm=roomm)
        await Edit_obj.Region.set()


# Edit_obj.Room
async def edit_in_room(message: types.Message, state: FSMContext):
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
        await Edit_obj.Types.set()
    elif message.text == "Продолжить":
        await state.reset_state()
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        lst = await rooms_admin(message, categ, types)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите количество комнат для редактирования", reply_markup=markup)
        await Edit_room.Room.set()
        await state.update_data(categ=categ)
        await state.update_data(types=types)
    else:
        select = await db.select_flat(room=roomm)
        room_code = select.get("room_code")
        await state.update_data(roomm=roomm)
        await state.update_data(room_code=room_code)
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Продолжить"))
        lst = await regions_admin(message, categ, types, roomm)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите район для редактирования или продолжите дальше", reply_markup=markup)
        await Edit_obj.Region.set()


# Edit_obj.Region
async def edit_in_regions(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("roomm")
    region = message.text
    if message.text == "Назад":
        if types == "Квартира":
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.insert(KeyboardButton(text="Продолжить"))
            lst = await rooms_admin(message, categ, types)
            for button in lst:
                markup.insert(button)
            await message.answer("Выберите количество комнат для редактирования или продолжите дальше", reply_markup=markup)
            await Edit_obj.Room.set()
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.insert(KeyboardButton(text="Квартира"))
            markup.insert(KeyboardButton(text="Коммерческое"))
            markup.insert(KeyboardButton(text="Назад"))
            await message.answer("Выберите категорию:", reply_markup=markup)
            await Edit_obj.Types.set()
    elif message.text == "Продолжить":
        await state.reset_state()
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        lst = await regions_admin(message, categ, types, roomm)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите район для редактирования", reply_markup=markup)
        await Edit_region.Region.set()
        await state.update_data(categ=categ)
        await state.update_data(types=types)
        await state.update_data(roomm=roomm)
    else:
        select = await db.select_flat(sub1category=region)
        sub1_code = select.get("sub1_code")
        await state.update_data(region=region)
        await state.update_data(sub1_code=sub1_code)
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Продолжить"))
        lst = await quarters_admin(message, categ, types, roomm, region)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите квартал для редактирования или продолжите дальше", reply_markup=markup)
        await Edit_obj.Quarter.set()


# Edit_obj.Quarter
async def edit_in_quarter(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("roomm")
    region = data.get("region")
    quarter = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Продолжить"))
        lst = await regions_admin(message, categ, types, roomm)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите район для редактирования или продолжите дальше", reply_markup=markup)
        await Edit_obj.Region.set()
    elif message.text == "Продолжить":
        await state.reset_state()
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        lst = await regions_admin(message, categ, types, roomm)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите квартал для редактирования", reply_markup=markup)
        await Edit_quarter.Quarter.set()
        await state.update_data(categ=categ)
        await state.update_data(types=types)
        await state.update_data(roomm=roomm)
        await state.update_data(region=region)
    else:
        select = await db.select_flat(category=categ, type=types, room=roomm, sub1category=region, sub2category=quarter)
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

        markup = InlineKeyboardMarkup(row_width=1)
        next = InlineKeyboardButton(text="⬅️",
                                    callback_data=edit_slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code,
                                                             action="back_slide"))
        page = InlineKeyboardButton(text=f"1/{len(ids)}",
                                    callback_data=edit_slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code,
                                                             action="none"))
        back = InlineKeyboardButton(text="➡️",
                                    callback_data=edit_slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code,
                                                             action="next_slide"))
        markup.row(next, page, back)
        markup.insert(InlineKeyboardButton(text="Изменить",
                                           callback_data=edit_slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code,
                                                                    action="edit")))
        await message.bot.send_message(message.from_user.id, text=f" <a href='{msg_url}'>{msg_text}</a>\n\n{msg_descrip}",
                                    reply_markup=markup)


async def edit_sliderr(call: CallbackQuery, callback_data: dict, state: FSMContext):
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

    if callback_data.get("action") == 'edit':
        await call.bot.send_message(call.from_user.id,
                                    text=f"Отправьте ссылку на объект для рускоязычных пользователей")
        await Edit_obj.New_url.set()
        await state.update_data(flat_id=flat_id)
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
                                    callback_data=edit_slider.new(id=flat_id, index=current_index, sub2_code=sub2_codee,
                                                                  action="back_slide"))
        page = InlineKeyboardButton(text=f"{current_index + 1}/{len(id_list)}",
                                    callback_data=edit_slider.new(id=flat_id, index=current_index, sub2_code=sub2_codee,
                                                                  action="none"))
        backk = InlineKeyboardButton(text="➡️", callback_data=edit_slider.new(id=flat_id, index=current_index,
                                                                              sub2_code=sub2_codee,
                                                                              action="next_slide"))
        markup.row(next, page, backk)
        markup.insert(InlineKeyboardButton(text="Изменить",
                                           callback_data=edit_slider.new(id=flat_id, index=current_index,
                                                                         sub2_code=sub2_codee, action="edit")))
        await call.bot.send_message(call.from_user.id, text=f" <a href='{msg_url}'>{msg_text}</a>\n\n{msg_descrip}",
                                    reply_markup=markup)


# Edit_obj.New_url
async def new_url(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    flat_id = data.get("flat_id")

    msq_url = message.text
    if message.text == "Назад":
        select = await db.select_flat(id=int(flat_id))
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

        markup = InlineKeyboardMarkup(row_width=1)
        next = InlineKeyboardButton(text="⬅️",
                                    callback_data=edit_slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code,
                                                                  action="back_slide"))
        page = InlineKeyboardButton(text=f"1/{len(ids)}",
                                    callback_data=edit_slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code,
                                                                  action="none"))
        backk = InlineKeyboardButton(text="➡️",
                                    callback_data=edit_slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code,
                                                                  action="next_slide"))
        markup.row(next, page, backk)
        markup.insert(InlineKeyboardButton(text="Изменить",
                                           callback_data=edit_slider.new(id=flat_id, index=flat_index,
                                                                         sub2_code=sub2_code,
                                                                         action="edit")))
        await message.bot.send_message(message.from_user.id,
                                       text=f" <a href='{msg_url}'>{msg_text}</a>\n\n{msg_descrip}",
                                       reply_markup=markup)
    else:
        await message.answer("Отправьте ссылку на объект для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_url=msq_url)
        await Edit_obj.New_url_uz.set()


# Edit_obj.New_url_uz
async def new_url_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_url_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте ссылку на объект для рускоязычных пользователей", reply_markup=back)
        await Edit_obj.New_url.set()
    else:
        await message.answer("Отправьте текст ссылки для рускоязычных пользователей", reply_markup=back)
        await state.update_data(msq_url_uz=msq_url_uz)
        await Edit_obj.New_text.set()


# Edit_obj.New_text
async def new_text(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_text = message.text
    if message.text == "Назад":
        await message.answer("Отправьте ссылку на объект для узбекоязычных пользователей", reply_markup=back)
        await Edit_obj.New_url_uz.set()
    else:
        await message.answer("Отправьте текст ссылки для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_text=msq_text)
        await Edit_obj.New_text_uz.set()


# Edit_obj.New_text_uz
async def new_text_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_text_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте текст ссылки для рускоязычных пользователей", reply_markup=back)
        await Edit_obj.New_text.set()
    else:
        await message.answer("Отправьте описание для рускоязычных пользователей", reply_markup=back)
        await state.update_data(msq_text_uz=msq_text_uz)
        await Edit_obj.New_desc.set()


# Edit_obj.New_desc
async def new_desc(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_desc = message.text
    if message.text == "Назад":
        await message.answer("Отправьте текст ссылки для узбекоязычных пользователей", reply_markup=back)
        await Edit_obj.New_text.set()
    else:
        await message.answer("Отправьте описание для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_desc=msq_desc)
        await Edit_obj.New_desc_uz.set()


# Edit_obj.New_desc_uz
async def new_desc_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    flat_id = data.get("flat_id")

    msq_url = data.get("msq_url")
    msq_url_uz = data.get("msq_url_uz")
    msq_text = data.get("msq_text")
    msq_text_uz = data.get("msq_text_uz")
    msq_desc = data.get("msq_desc")
    msq_desc_uz = data.get("msq_desc_uz")
    if message.text == "Назад":
        await message.answer("Отправьте описание для узбекоязычных пользователей", reply_markup=back)
        await Edit_obj.New_desc_uz.set()
    else:
        text = f"Все верно? \n\n" \
               f"Ссылка (ru/uz): {msq_url} / {msq_url_uz}\n" \
               f"Текст (ru/uz): {msq_text} / {msq_text_uz}\n" \
               f"Описание (ru/uz): {msq_desc} / {msq_desc_uz}\n" \
               f" <a href='{msq_url}'>{msq_text}</a>\n" \
               f" <a href='{msq_url_uz}'>{msq_text_uz}</a>"
        await message.answer(text, reply_markup=confirm)
        await state.update_data(msq_desc_uz=msq_desc_uz)
        await Edit_obj.Confirm.set()


# Add_obj.Confirm
async def new_confirm(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    flat_id = data.get("flat_id")

    msq_url = data.get("msq_url")
    msq_url_uz = data.get("msq_url_uz")
    msq_text = data.get("msq_text")
    msq_text_uz = data.get("msq_text_uz")
    msq_desc = data.get("msq_desc")
    msq_desc_uz = data.get("msq_desc_uz")
    if message.text == "Назад":
        await message.answer("Отправьте айди объекта", reply_markup=back)
        await Edit_obj.New_id.set()
    elif message.text == "Верно":
        await db.update_flat(id=int(flat_id), url=msq_url)
        await db.update_flat(id=int(flat_id), url_uz=msq_url_uz)
        await db.update_flat(id=int(flat_id), text=msq_text)
        await db.update_flat(id=int(flat_id), text_uz=msq_text_uz)
        await db.update_flat(id=int(flat_id), descrip=msq_desc)
        await db.update_flat(id=int(flat_id), desc_uz=msq_desc_uz)
        await state.reset_state()
        await message.answer("Объект был добавлен в базу данных!", reply_markup=ReplyKeyboardRemove())
        await admins_list(message)
    else:
        await state.reset_state()
        await custom_flats(message)


# Edit_room.Room
async def edit_room(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    room = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Продолжить"))
        lst = await rooms_admin(message, categ, types)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите количество комнат редактирования или продолжите дальше", reply_markup=markup)
        await state.update_data(types=types)
        await Edit_obj.Room.set()
    else:
        select = await db.select_flat(room=room)
        room_code = select.get("room_code")
        await state.update_data(room_code=room_code)
        await state.update_data(room=room)
        await message.answer(f"Введите измененное название {room}", reply_markup=back)
        await Edit_room.New_Room.set()


# Edit_room.New_Room
async def edit_room_new(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    room = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        lst = await rooms_admin(message, categ, types)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите количество комнат для редактирования", reply_markup=markup)
        await Edit_room.Room.set()
    else:
        await message.answer("Введите измененное название для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(new_room=room)
        await Edit_room.Room_uz.set()


# Edit_room.Room_uz
async def edit_room_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    room = data.get("room")
    new_room = data.get("new_room")
    room_uz = message.text
    if message.text == "Назад":
        await message.answer(f"Введите измененное название", reply_markup=back)
        await Edit_room.New_Room.set()
    else:
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_flats(room=room):
            await db.update_flat(id=id, romm=new_room)
            await db.update_flat(id=id, room_uz=message.text)
        await state.reset_state()
        await message.answer(f"Изменения внесены!"
                             f"Новое название: {new_room}\n"
                             f"Новое название (узб): {room_uz}", reply_markup=ReplyKeyboardRemove())
        await admins_list(message)


# Edit_region.Region
async def edit_region(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    room = data.get("room")
    region = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Продолжить"))
        lst = await regions_admin(message, categ, types, room)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите район для редактирования или продолжите дальше", reply_markup=markup)
        await Edit_obj.Region.set()
    else:
        select = await db.select_flat(sub1category=region)
        sub1_code = select.get("sub1_code")
        await state.update_data(sub1_code=sub1_code)
        await state.update_data(region=region)
        await message.answer(f"Введите измененное название {region}", reply_markup=back)
        await Edit_region.New_Region.set()


# Edit_region.New_Region
async def edit_region_new(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    room = data.get("room")
    region = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        lst = await regions_admin(message, categ, types, room)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите район для редактирования", reply_markup=markup)
        await Edit_region.Region.set()
    else:
        await message.answer("Введите измененное название для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(new_region=region)
        await Edit_region.Region_uz.set()


# Edit_region.Region_uz
async def edit_region_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    region = data.get("region")
    new_region = data.get("new_region")
    region_uz = message.text
    if message.text == "Назад":
        select = await db.select_flat(region=region)
        sub1_code = select.get("sub1_code")
        await state.update_data(sub1_code=sub1_code)
        await state.update_data(region=region)
        await message.answer(f"Введите измененное название {region}", reply_markup=back)
        await Edit_region.New_Region.set()
    else:
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_flats(
                sub1category=region):
            await db.update_flat(id=id, sub1category=new_region)
            await db.update_flat(id=id, sub1category_uz=message.text)
        await state.reset_state()
        await message.answer(f"Изменения внесены!"
                             f"Новое название: {new_region}\n"
                             f"Новое название (узб): {region_uz}", reply_markup=ReplyKeyboardRemove())
        await admins_list(message)


# Edit_quarter.Quarter
async def edit_quarter(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    room = data.get("room")
    region = data.get("region")
    quarter = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Продолжить"))
        lst = await quarters_admin(message, categ, types, room, region)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите квартал для редактирования или продолжите дальше", reply_markup=markup)
        await Edit_obj.Quarter.set()
    else:
        select = await db.select_flat(sub2category=quarter)
        sub2_code = select.get("sub2_code")
        await state.update_data(sub2_code=sub2_code)
        await state.update_data(quarter=quarter)
        await message.answer(f"Введите измененное название {quarter}", reply_markup=back)
        await Edit_quarter.New_Quarter.set()


# Edit_quarter.New_Quarter
async def edit_quarter_new(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    room = data.get("room")
    region = data.get("region")
    quarter = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        lst = await regions_admin(message, categ, types, room)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите квартал для редактирования", reply_markup=markup)
        await Edit_quarter.Quarter.set()
    else:
        await message.answer("Введите измененное название для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(new_quarter=quarter)
        await Edit_region.Region_uz.set()


# Edit_quarter.Quarter_uz
async def edit_quarter_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    quarter = data.get("quarter")
    new_quarter = data.get("new_quarter")
    quarter_uz = message.text
    if message.text == "Назад":
        select = await db.select_flat(sub2category=quarter)
        sub2_code = select.get("sub2_code")
        await state.update_data(sub2_code=sub2_code)
        await state.update_data(quarter=quarter)
        await message.answer(f"Введите измененное название {quarter}", reply_markup=back)
        await Edit_quarter.New_Quarter.set()
    else:
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_flats(
                sub2category=quarter):
            await db.update_flat(id=id, sub2category=new_quarter)
            await db.update_flat(id=id, sub2category_uz=message.text)
        await state.reset_state()
        await message.answer(f"Изменения внесены!"
                             f"Новое название: {new_quarter}\n"
                             f"Новое название (узб): {quarter_uz}", reply_markup=ReplyKeyboardRemove())
        await admins_list(message)


def register_edit_obj(dp: Dispatcher):
    dp.register_message_handler(edit_flat, IsAdmin(), text="Редактировать Квартиру")
    dp.register_message_handler(edit_in_categ, IsAdmin(), state=Edit_obj.Categ, text=["Купить", "Снять", "Назад"])
    dp.register_message_handler(edit_in_types, IsAdmin(), state=Edit_obj.Types, text=["Квартира", "Коммерческое", "Назад"])
    dp.register_message_handler(edit_in_room, IsAdmin(), state=Edit_obj.Room)
    dp.register_message_handler(edit_in_regions, IsAdmin(), state=Edit_obj.Region)
    dp.register_message_handler(edit_in_quarter, IsAdmin(), state=Edit_obj.Quarter)
    dp.register_callback_query_handler(edit_sliderr, edit_slider.filter())

    dp.register_message_handler(new_url, state=Edit_obj.New_url)
    dp.register_message_handler(new_url_uz, state=Edit_obj.New_url_uz)
    dp.register_message_handler(new_text, state=Edit_obj.New_text)
    dp.register_message_handler(new_text_uz, state=Edit_obj.New_text_uz)
    dp.register_message_handler(new_desc, state=Edit_obj.New_desc)
    dp.register_message_handler(new_desc_uz, state=Edit_obj.New_desc_uz)
    dp.register_message_handler(new_confirm, state=Edit_obj.Confirm)

    dp.register_message_handler(edit_room, state=Edit_room.Room)
    dp.register_message_handler(edit_room_new, state=Edit_room.New_Room)
    dp.register_message_handler(edit_room_uz, state=Edit_room.Room_uz)

    dp.register_message_handler(edit_region, state=Edit_region.Region)
    dp.register_message_handler(edit_region_new, state=Edit_region.New_Region)
    dp.register_message_handler(edit_region_uz, state=Edit_region.Region_uz)

    dp.register_message_handler(edit_quarter, state=Edit_quarter.Quarter)
    dp.register_message_handler(edit_quarter_new, state=Edit_quarter.Quarter)
    dp.register_message_handler(edit_quarter_uz, state=Edit_quarter.Quarter_uz)

