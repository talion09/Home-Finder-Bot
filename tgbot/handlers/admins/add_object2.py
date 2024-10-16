from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from tgbot.handlers.admins.add_object import custom_flats
from tgbot.handlers.admins.functions import rooms_admin, regions_admin, quarters_admin
from tgbot.handlers.users.start import bot_start, admins_list
from tgbot.keyboards.default.cancel import back, confirm
from tgbot.states.users import Add_obj, New_region, New_quarter


# New_region.Region
async def new_region(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("room")
    region = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Добавить новый район"))
        lst = await regions_admin(message, categ, types, roomm)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите район или добавьте новый", reply_markup=markup)
        await Add_obj.Region.set()
    else:
        await message.answer("Введите название нового района для узбекоязычных пользователей", reply_markup=back)
        print("New_region.Region", message.text)
        sub1_codes = await db.select_sub1()
        print(sub1_codes)
        max_sub1_code = max(sub1_codes, key=lambda x: x)
        print(max_sub1_code)
        new_sub1 = 1 + int(max_sub1_code.get("sub1_code"))
        print(new_sub1)
        await state.update_data(sub1_code=new_sub1)
        await state.update_data(region=region)
        await New_region.Region_uz.set()


# New_region.Region_uz
async def new_region_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    region_uz = message.text
    if message.text == "Назад":
        await message.answer("Введите название нового района для рускоязычных пользователей", reply_markup=back)
        await New_region.Region.set()
    else:
        await message.answer("Введите название нового квартала для рускоязычных пользователей", reply_markup=back)
        await state.update_data(sub1category_uz=region_uz)
        await New_region.Quarter.set()


# New_region.Quarter
async def new_quarter(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    quarter = message.text
    if message.text == "Назад":
        await message.answer("Введите название нового района для узбекоязычных пользователей", reply_markup=back)
        await New_region.Region_uz.set()
    else:
        await message.answer("Введите название нового квартала для узбекоязычных пользователей", reply_markup=back)
        sub2_codes = await db.select_sub2()
        max_sub2_code = max(sub2_codes, key=lambda x: x)
        new_sub2 = 1 + int(max_sub2_code.get("sub2_code"))
        await state.update_data(sub2_code=new_sub2)
        await state.update_data(quarter=quarter)
        await New_region.Quarter_uz.set()


# New_region.Quarter_uz
async def new_quarter_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    quarter_uz = message.text
    if message.text == "Назад":
        await message.answer("Введите название нового квартала для рускоязычных пользователей", reply_markup=back)
        await New_region.Quarter.set()
    else:
        await state.update_data(sub2category_uz=quarter_uz)
        await message.answer("Отправьте ссылку на объект для рускоязычных пользователей", reply_markup=back)
        await New_region.New_url.set()


# New_region.New_url
async def new_url1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_url = message.text
    if message.text == "Назад":
        await message.answer("Введите название нового квартала для узбекоязычных пользователей", reply_markup=back)
        await New_region.Quarter_uz.set()
    else:
        await message.answer("Отправьте ссылку на объект для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_url=msq_url)
        await New_region.New_url_uz.set()


# New_region.New_url_uz
async def new_url_uz1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_url_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте ссылку на объект для рускоязычных пользователей", reply_markup=back)
        await New_region.New_url.set()
    else:
        await message.answer("Отправьте текст ссылки для рускоязычных пользователей", reply_markup=back)
        await state.update_data(msq_url_uz=msq_url_uz)
        await New_region.New_text.set()


# New_region.New_text
async def new_text1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_text = message.text
    if message.text == "Назад":
        await message.answer("Отправьте ссылку на объект для узбекоязычных пользователей", reply_markup=back)
        await New_region.New_url_uz.set()
    else:
        await message.answer("Отправьте текст ссылки для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_text=msq_text)
        await New_region.New_text_uz.set()


# New_region.New_text_uz
async def new_text_uz1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_text_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте текст ссылки для рускоязычных пользователей", reply_markup=back)
        await New_region.New_text.set()
    else:
        await message.answer("Отправьте описание для рускоязычных пользователей", reply_markup=back)
        await state.update_data(msq_text_uz=msq_text_uz)
        await New_region.New_desc.set()


# New_region.New_desc
async def new_desc1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_desc = message.text
    if message.text == "Назад":
        await message.answer("Отправьте текст ссылки для узбекоязычных пользователей", reply_markup=back)
        await New_region.New_text.set()
    else:
        await message.answer("Отправьте описание для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_desc=msq_desc)
        await New_region.New_desc_uz.set()


# New_region.New_desc_uz
async def new_desc_uz1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_desc_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте описание для рускоязычных пользователей", reply_markup=back)
        await New_region.New_desc.set()
    else:
        await message.answer("Отправьте айди объекта", reply_markup=back)
        await state.update_data(msq_desc_uz=msq_desc_uz)
        await New_region.New_id.set()


# New_region.New_id
async def new_id1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("roomm")
    region = data.get("region")
    quarter = data.get("quarter")

    msq_url = data.get("msq_url")
    msq_url_uz = data.get("msq_url_uz")
    msq_text = data.get("msq_text")
    msq_text_uz = data.get("msq_text_uz")
    msq_desc = data.get("msq_desc")
    msq_desc_uz = data.get("msq_desc_uz")
    id_obj = message.text
    if message.text == "Назад":
        await message.answer("Отправьте описание для узбекоязычных пользователей", reply_markup=back)
        await New_region.New_desc_uz.set()
    else:
        try:
            id_obj = int(id_obj)
            text = f"Все верно? \n\n" \
                   f"Категория: {categ}\n" \
                   f"Категория: {types}\n" \
                   f"Комната: {roomm}\n" \
                   f"Район: {region}\n" \
                   f"Квартал {quarter}\n\n" \
                   f"Ссылка (ru/uz): {msq_url} / {msq_url_uz}\n" \
                   f"Текст (ru/uz): {msq_text} / {msq_text_uz}\n" \
                   f"Описание (ru/uz): {msq_desc} / {msq_desc_uz}\n" \
                   f"Айди: {id_obj}\n\n" \
                   f" <a href='{msq_url}'>{msq_text}</a>\n" \
                   f" <a href='{msq_url_uz}'>{msq_text_uz}</a>"
            await message.answer(text, reply_markup=confirm)
            await state.update_data(id_obj=id_obj)
            await New_region.Confirm.set()
        except:
            await message.answer("Отправьте айди объекта", reply_markup=back)
            await New_region.New_id.set()


# New_region.Confirm
async def new_confirm1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("roomm")
    region = data.get("region")
    quarter = data.get("quarter")
    sub1_code = int(data.get("sub1_code"))
    sub2_code = int(data.get("sub2_code"))
    id_obj = int(data.get("id_obj"))

    catg_code = int(data.get("catg_code"))
    type_code = int(data.get("type_code"))
    region_uz = data.get("sub1category_uz")
    quarter_uz = data.get("sub2category_uz")

    msq_url = data.get("msq_url")
    msq_url_uz = data.get("msq_url_uz")
    msq_text = data.get("msq_text")
    msq_text_uz = data.get("msq_text_uz")
    msq_desc = data.get("msq_desc")
    msq_desc_uz = data.get("msq_desc_uz")
    if roomm == "0":
        room_code = 0
        roomm_uz = "0"
    else:
        room_code = int(data.get("room_code"))
        roomm_uz = data.get("room_uz")
    if message.text == "Назад":
        await message.answer("Отправьте айди объекта", reply_markup=back)
        await New_region.New_id.set()
    elif message.text == "Верно":
        await db.add_flat(id=id_obj, catg_code=catg_code, category=categ, type_code=type_code, type=types,
                          room_code=room_code, room=str(roomm), room_uz=str(roomm_uz), sub1_code=sub1_code, sub1category=region,
                          sub1category_uz=region_uz,
                          sub2_code=sub2_code, sub2category=quarter, sub2category_uz=quarter_uz, url=msq_url,
                          url_uz=msq_url_uz, text=msq_text, text_uz=msq_text_uz, descrip=msq_desc, desc_uz=msq_desc_uz)
        await state.reset_state()
        await message.answer("Объект был добавлен в базу данных!", reply_markup=ReplyKeyboardRemove())
        await admins_list(message)
    else:
        await state.reset_state()
        await custom_flats(message)


# New_quarter.Quarter
async def new_quarter1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("roomm")
    region = data.get("region")
    quarter = message.text
    print(roomm)
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Добавить новый квартал"))
        lst = await quarters_admin(message, categ, types, roomm, region)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите квартал или добавьте новый", reply_markup=markup)
        await Add_obj.Quarter.set()
    else:
        print("New_quarter.Quarter", message.text)
        await message.answer("Введите название нового квартала для узбекоязычных пользователей", reply_markup=back)
        sub2_codes = await db.select_sub2()
        print(sub2_codes)
        max_sub2_code = max(sub2_codes, key=lambda x: x)
        print(max_sub2_code)
        new_sub2 = 1 + int(max_sub2_code.get("sub2_code"))
        print(new_sub2)
        await state.update_data(sub2_code=new_sub2)
        await state.update_data(quarter=quarter)
        await New_quarter.Quarter_uz.set()


# New_quarter.Quarter_uz
async def new_quarter_uz1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    quarter_uz = message.text
    if message.text == "Назад":
        await message.answer("Введите название нового квартала для рускоязычных пользователей", reply_markup=back)
        await New_quarter.Quarter.set()
    else:
        await state.update_data(sub2category_uz=quarter_uz)
        await message.answer("Отправьте ссылку на объект для рускоязычных пользователей", reply_markup=back)
        await New_quarter.New_url.set()


# New_quarter.New_url
async def new_url2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_url = message.text
    if message.text == "Назад":
        await message.answer("Введите название нового квартала для узбекоязычных пользователей", reply_markup=back)
        await New_quarter.Quarter_uz.set()
    else:
        await message.answer("Отправьте ссылку на объект для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_url=msq_url)
        await New_quarter.New_url_uz.set()


# New_quarter.New_url_uz
async def new_url_uz2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_url_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте ссылку на объект для рускоязычных пользователей", reply_markup=back)
        await New_quarter.New_url.set()
    else:
        await message.answer("Отправьте текст ссылки для рускоязычных пользователей", reply_markup=back)
        await state.update_data(msq_url_uz=msq_url_uz)
        await New_quarter.New_text.set()


# New_quarter.New_text
async def new_text2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_text = message.text
    if message.text == "Назад":
        await message.answer("Отправьте ссылку на объект для узбекоязычных пользователей", reply_markup=back)
        await New_quarter.New_url_uz.set()
    else:
        await message.answer("Отправьте текст ссылки для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_text=msq_text)
        await New_quarter.New_text_uz.set()


# New_quarter.New_text_uz
async def new_text_uz2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_text_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте текст ссылки для рускоязычных пользователей", reply_markup=back)
        await New_quarter.New_text.set()
    else:
        await message.answer("Отправьте описание для рускоязычных пользователей", reply_markup=back)
        await state.update_data(msq_text_uz=msq_text_uz)
        await New_quarter.New_desc.set()


# New_quarter.New_desc
async def new_desc2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_desc = message.text
    if message.text == "Назад":
        await message.answer("Отправьте текст ссылки для узбекоязычных пользователей", reply_markup=back)
        await New_quarter.New_text.set()
    else:
        await message.answer("Отправьте описание для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_desc=msq_desc)
        await New_quarter.New_desc_uz.set()


# New_quarter.New_desc_uz
async def new_desc_uz2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_desc_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте описание для рускоязычных пользователей", reply_markup=back)
        await New_quarter.New_desc.set()
    else:
        await message.answer("Отправьте айди объекта", reply_markup=back)
        await state.update_data(msq_desc_uz=msq_desc_uz)
        await New_quarter.New_id.set()


# New_quarter.New_id
async def new_id2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("roomm")
    region = data.get("region")
    quarter = data.get("quarter")

    msq_url = data.get("msq_url")
    msq_url_uz = data.get("msq_url_uz")
    msq_text = data.get("msq_text")
    msq_text_uz = data.get("msq_text_uz")
    msq_desc = data.get("msq_desc")
    msq_desc_uz = data.get("msq_desc_uz")
    id_obj = message.text
    if message.text == "Назад":
        await message.answer("Отправьте описание для узбекоязычных пользователей", reply_markup=back)
        await New_quarter.New_desc_uz.set()
    else:
        try:
            id_obj = int(id_obj)
            text = f"Все верно? \n\n" \
                   f"Категория: {categ}\n" \
                   f"Категория: {types}\n" \
                   f"Комната: {roomm}\n" \
                   f"Район: {region}\n" \
                   f"Квартал {quarter}\n\n" \
                   f"Ссылка (ru/uz): {msq_url} / {msq_url_uz}\n" \
                   f"Текст (ru/uz): {msq_text} / {msq_text_uz}\n" \
                   f"Описание (ru/uz): {msq_desc} / {msq_desc_uz}\n" \
                   f"Айди: {id_obj}\n\n" \
                   f" <a href='{msq_url}'>{msq_text}</a>\n" \
                   f" <a href='{msq_url_uz}'>{msq_text_uz}</a>"
            await message.answer(text, reply_markup=confirm)
            await state.update_data(id_obj=id_obj)
            await New_quarter.Confirm.set()
        except:
            await message.answer("Отправьте айди объекта", reply_markup=back)
            await New_quarter.New_id.set()


# New_quarter.Confirm
async def new_confirm2(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("roomm")
    region = data.get("region")
    quarter = data.get("quarter")
    sub1_code = int(data.get("sub1_code"))
    sub2_code = int(data.get("sub2_code"))
    id_obj = int(data.get("id_obj"))

    catg_code = int(data.get("catg_code"))
    type_code = int(data.get("type_code"))
    region_uz = data.get("sub1category_uz")
    quarter_uz = data.get("sub2category_uz")

    msq_url = data.get("msq_url")
    msq_url_uz = data.get("msq_url_uz")
    msq_text = data.get("msq_text")
    msq_text_uz = data.get("msq_text_uz")
    msq_desc = data.get("msq_desc")
    msq_desc_uz = data.get("msq_desc_uz")
    if roomm == "0":
        room_code = 0
        roomm_uz = "0"
    else:
        room_code = int(data.get("room_code"))
        roomm_uz = data.get("room_uz")
    if message.text == "Назад":
        await message.answer("Отправьте айди объекта", reply_markup=back)
        await New_quarter.New_id.set()
    elif message.text == "Верно":
        await db.add_flat(id=id_obj, catg_code=catg_code, category=categ, type_code=type_code, type=types,
                          room_code=room_code, room=str(roomm), room_uz=str(roomm_uz), sub1_code=sub1_code, sub1category=region,
                          sub1category_uz=region_uz,
                          sub2_code=sub2_code, sub2category=quarter, sub2category_uz=quarter_uz, url=msq_url,
                          url_uz=msq_url_uz, text=msq_text, text_uz=msq_text_uz, descrip=msq_desc, desc_uz=msq_desc_uz)
        await state.reset_state()
        await message.answer("Объект был добавлен в базу данных!", reply_markup=ReplyKeyboardRemove())
        await admins_list(message)
    else:
        await state.reset_state()
        await custom_flats(message)


def register_add_object2(dp: Dispatcher):
    dp.register_message_handler(new_region, state=New_region.Region)
    dp.register_message_handler(new_region_uz, state=New_region.Region_uz)
    dp.register_message_handler(new_quarter, state=New_region.Quarter)
    dp.register_message_handler(new_quarter_uz, state=New_region.Quarter_uz)

    dp.register_message_handler(new_url1, state=New_region.New_url)
    dp.register_message_handler(new_url_uz1, state=New_region.New_url_uz)
    dp.register_message_handler(new_text1, state=New_region.New_text)
    dp.register_message_handler(new_text_uz1, state=New_region.New_text_uz)
    dp.register_message_handler(new_desc1, state=New_region.New_desc)
    dp.register_message_handler(new_desc_uz1, state=New_region.New_desc_uz)
    dp.register_message_handler(new_id1, state=New_region.New_id)
    dp.register_message_handler(new_confirm1, state=New_region.Confirm)

    dp.register_message_handler(new_quarter1, state=New_quarter.Quarter)
    dp.register_message_handler(new_quarter_uz1, state=New_quarter.Quarter_uz)

    dp.register_message_handler(new_url2, state=New_quarter.New_url)
    dp.register_message_handler(new_url_uz2, state=New_quarter.New_url_uz)
    dp.register_message_handler(new_text2, state=New_quarter.New_text)
    dp.register_message_handler(new_text_uz2, state=New_quarter.New_text_uz)
    dp.register_message_handler(new_desc2, state=New_quarter.New_desc)
    dp.register_message_handler(new_desc_uz2, state=New_quarter.New_desc_uz)
    dp.register_message_handler(new_id2, state=New_quarter.New_id)
    dp.register_message_handler(new_confirm2, state=New_quarter.Confirm)