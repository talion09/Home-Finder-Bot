from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from tgbot.filters.is_admin import IsAdmin
from tgbot.handlers.admins.functions import rooms_admin, regions_admin, quarters_admin
from tgbot.handlers.users.start import bot_start, admins_list
from tgbot.keyboards.default.cancel import back, confirm
from tgbot.keyboards.default.cust_flat import flat_customize_adm
from tgbot.states.users import Admin, Add_obj, New_room, New_region, New_quarter


async def custom_flats(message: types.Message):
    await message.answer("Что вы хотите сделать ?", reply_markup=flat_customize_adm)


async def add_flat(message: types.Message):
    db = message.bot.get("db")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.insert(KeyboardButton(text="Купить"))
    markup.insert(KeyboardButton(text="Снять"))
    markup.insert(KeyboardButton(text="Главное Меню"))
    markup.insert(KeyboardButton(text="Назад"))
    await message.answer("Выберите категорию:", reply_markup=markup)
    await Add_obj.Categ.set()


# Add_obj.Categ
async def select_in_categ(message: types.Message, state: FSMContext):
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
        await Add_obj.Types.set()


# Add_obj.Types
async def select_in_types(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = message.text
    if message.text == "Назад":
        await state.reset_state()
        await add_flat(message)
    elif message.text == "Квартира":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Добавить кол-во комнат"))
        lst = await rooms_admin(message, categ, types)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите кол-во комнат или добавьте новый", reply_markup=markup)
        select = await db.select_flat(category=categ, type=types)

        catg_code = select.get("catg_code")
        type_code = select.get("type_code")
        await state.update_data(catg_code=catg_code)
        await state.update_data(type_code=type_code)
        await state.update_data(types=types)
        await Add_obj.Room.set()
    else:
        roomm = 0
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Добавить новый район"))
        lst = await regions_admin(message, categ, types, roomm)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите район или добавьте новый", reply_markup=markup)
        select = await db.select_flat(category=categ, type=types)
        catg_code = select.get("catg_code")
        type_code = select.get("type_code")
        await state.update_data(catg_code=catg_code)
        await state.update_data(type_code=type_code)
        await state.update_data(types=types)
        await state.update_data(roomm=roomm)
        await Add_obj.Region.set()


# Add_obj.Room
async def select_in_room(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    catg_code = data.get("catg_code")
    type_code = data.get("type_code")
    roomm = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Квартира"))
        markup.insert(KeyboardButton(text="Коммерческое"))
        markup.insert(KeyboardButton(text="Назад"))
        await message.answer("Выберите категорию:", reply_markup=markup)
        await Add_obj.Types.set()
    elif message.text == "Добавить кол-во комнат":
        await state.reset_state()
        await message.answer("Введите новое кол-во комнат", reply_markup=back)
        await New_room.Room.set()
        await state.update_data(categ=categ)
        await state.update_data(types=types)
        await state.update_data(catg_code=catg_code)
        await state.update_data(type_code=type_code)
    else:
        select = await db.select_flat(room=roomm)
        room_code = select.get("room_code")
        room_uz = select.get("room_uz")
        await state.update_data(roomm=roomm)
        await state.update_data(room_uz=room_uz)
        await state.update_data(room_code=room_code)
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Добавить новый район"))
        lst = await regions_admin(message, categ, types, roomm)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите район или добавьте новый", reply_markup=markup)
        await Add_obj.Region.set()


# Add_obj.Region
async def select_in_regions(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("roomm")
    catg_code = data.get("catg_code")
    type_code = data.get("type_code")
    region = message.text
    if message.text == "Назад":
        if types == "Квартира":
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.insert(KeyboardButton(text="Добавить кол-во комнат"))
            lst = await rooms_admin(message, categ, types)
            for button in lst:
                markup.insert(button)
            await message.answer("Выберите кол-во комнат или добавьте новый", reply_markup=markup)
            await Add_obj.Room.set()
        else:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.insert(KeyboardButton(text="Квартира"))
            markup.insert(KeyboardButton(text="Коммерческое"))
            markup.insert(KeyboardButton(text="Назад"))
            await message.answer("Выберите категорию:", reply_markup=markup)
            await Add_obj.Types.set()
    elif message.text == "Добавить новый район":
        await state.reset_state()
        await message.answer("Введите название нового района", reply_markup=back)
        await New_region.Region.set()
        await state.update_data(categ=categ)
        await state.update_data(types=types)
        await state.update_data(catg_code=catg_code)
        await state.update_data(type_code=type_code)
        await state.update_data(roomm=roomm)
        if roomm == 0:
            await state.update_data(room_code=0)
            await state.update_data(room_uz=0)
        else:
            room_code = data.get("room_code")
            room_uz = data.get("room_uz")
            await state.update_data(room_code=room_code)
            await state.update_data(room_uz=room_uz)
    else:
        select = await db.select_flat(sub1category=region)
        sub1_code = select.get("sub1_code")
        region_uz = select.get("sub1category_uz")
        await state.update_data(region=region)
        await state.update_data(sub1_code=sub1_code)
        await state.update_data(sub1category_uz=region_uz)
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Добавить новый квартал"))
        lst = await quarters_admin(message, categ, types, roomm, region)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите квартал или добавьте новый", reply_markup=markup)
        await Add_obj.Quarter.set()


# Add_obj.Quarter
async def select_in_quarter(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("roomm")
    room_code = data.get("room_code")
    room_uz = data.get("room_uz")
    catg_code = data.get("catg_code")
    type_code = data.get("type_code")
    region = data.get("region")
    sub1category_uz = data.get("sub1category_uz")
    sub1_code = data.get("sub1_code")
    quarter = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Добавить новый район"))
        lst = await regions_admin(message, categ, types, roomm)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите район или добавьте новый", reply_markup=markup)
        await Add_obj.Region.set()
    elif message.text == "Добавить новый квартал":
        await state.reset_state()
        await message.answer("Введите название нового квартала", reply_markup=back)
        await New_quarter.Quarter.set()
        await state.update_data(categ=categ)
        await state.update_data(types=types)
        await state.update_data(catg_code=catg_code)
        await state.update_data(type_code=type_code)
        await state.update_data(roomm=roomm)
        await state.update_data(room_code=room_code)
        await state.update_data(room_uz=room_uz)
        await state.update_data(region=region)
        await state.update_data(sub1_code=sub1_code)
        await state.update_data(sub1category_uz=sub1category_uz)

    else:
        select = await db.select_flat(sub2category=quarter)
        quarter_uz = select.get("sub2category_uz")
        sub2_code = select.get("sub2_code")
        await state.update_data(quarter=quarter)
        await state.update_data(sub2category_uz=quarter_uz)
        await state.update_data(sub2_code=sub2_code)
        await message.answer("Отправьте ссылку на объект для рускоязычных пользователей", reply_markup=back)
        await Add_obj.New_url.set()


# Add_obj.New_url
async def new_url(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("roomm")
    region = data.get("region")
    msq_url = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Добавить новый квартал"))
        lst = await quarters_admin(message, categ, types, roomm, region)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите квартал или добавьте новый", reply_markup=markup)
        await Add_obj.Quarter.set()
    else:
        await message.answer("Отправьте ссылку на объект для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_url=msq_url)
        await Add_obj.New_url_uz.set()


# Add_obj.New_url_uz
async def new_url_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_url_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте ссылку на объект для рускоязычных пользователей", reply_markup=back)
        await Add_obj.New_url.set()
    else:
        await message.answer("Отправьте текст ссылки для рускоязычных пользователей", reply_markup=back)
        await state.update_data(msq_url_uz=msq_url_uz)
        await Add_obj.New_text.set()


# Add_obj.New_text
async def new_text(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_text = message.text
    if message.text == "Назад":
        await message.answer("Отправьте ссылку на объект для узбекоязычных пользователей", reply_markup=back)
        await Add_obj.New_url_uz.set()
    else:
        await message.answer("Отправьте текст ссылки для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_text=msq_text)
        await Add_obj.New_text_uz.set()


# Add_obj.New_text_uz
async def new_text_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_text_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте текст ссылки для рускоязычных пользователей", reply_markup=back)
        await Add_obj.New_text.set()
    else:
        await message.answer("Отправьте описание для рускоязычных пользователей", reply_markup=back)
        await state.update_data(msq_text_uz=msq_text_uz)
        await Add_obj.New_desc.set()


# Add_obj.New_desc
async def new_desc(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_desc = message.text
    if message.text == "Назад":
        await message.answer("Отправьте текст ссылки для узбекоязычных пользователей", reply_markup=back)
        await Add_obj.New_text.set()
    else:
        await message.answer("Отправьте описание для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_desc=msq_desc)
        await Add_obj.New_desc_uz.set()


# Add_obj.New_desc_uz
async def new_desc_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_desc_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте описание для рускоязычных пользователей", reply_markup=back)
        await Add_obj.New_desc.set()
    else:
        await message.answer("Отправьте айди объекта", reply_markup=back)
        await state.update_data(msq_desc_uz=msq_desc_uz)
        await Add_obj.New_id.set()


# Add_obj.New_id
async def new_id(message: types.Message, state: FSMContext):
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
        await Add_obj.New_desc_uz.set()
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
            await Add_obj.Confirm.set()
        except:
            await message.answer("Отправьте айди объекта", reply_markup=back)
            await Add_obj.New_id.set()


# Add_obj.Confirm
async def new_confirm(message: types.Message, state: FSMContext):
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
        await Add_obj.New_id.set()
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


# New_room.Room
async def new_room(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    room = message.text
    if message.text == "Назад":
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.insert(KeyboardButton(text="Добавить кол-во комнат"))
        lst = await rooms_admin(message, categ, types)
        for button in lst:
            markup.insert(button)
        await message.answer("Выберите кол-во комнат или добавьте новый", reply_markup=markup)
        await Add_obj.Room.set()
    else:
        print("New_room.Room", message.text)
        await message.answer("Отправьте новое кол-во комнат узбекоязычных пользователей", reply_markup=back)
        room_codes = await db.select_room_code()
        print(room_codes)
        max_room_code = max(room_codes, key=lambda x: x)
        print(max_room_code)
        new_room_code = 1 + int(max_room_code.get("room_code"))
        print(max_room_code)
        await state.update_data(room_code=new_room_code)
        await state.update_data(room=room)
        await New_room.Room_uz.set()


# New_room.Room_uz
async def new_room_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    room_uz = message.text
    if message.text == "Назад":
        await message.answer("Введите новое кол-во комнат", reply_markup=back)
        await New_room.Room.set()
    else:
        await message.answer("Введите название нового района для рускоязычных пользователей", reply_markup=back)
        await state.update_data(room_uz=room_uz)
        await New_room.Region.set()


# New_room.Region
async def new_region(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    region = message.text
    if message.text == "Назад":
        await message.answer("Отправьте новое кол-во комнат узбекоязычных пользователей", reply_markup=back)
        await New_room.Room_uz.set()
    else:
        await message.answer("Введите название нового района для узбекоязычных пользователей", reply_markup=back)
        sub1_codes = await db.select_sub1()
        max_sub1_code = max(sub1_codes, key=lambda x: x)
        new_sub1 = 1 + int(max_sub1_code.get("sub1_code"))
        await state.update_data(sub1_code=new_sub1)
        await state.update_data(region=region)
        await New_room.Region_uz.set()


# New_room.Region_uz
async def new_region_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    region_uz = message.text
    if message.text == "Назад":
        await message.answer("Введите название нового района для рускоязычных пользователей", reply_markup=back)
        await New_room.Region.set()
    else:
        await message.answer("Введите название нового квартала для рускоязычных пользователей", reply_markup=back)
        await state.update_data(sub1category_uz=region_uz)
        await New_room.Quarter.set()


# New_room.Quarter
async def new_quarter(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    quarter = message.text
    if message.text == "Назад":
        await message.answer("Введите название нового района для узбекоязычных пользователей", reply_markup=back)
        await New_room.Region_uz.set()
    else:
        await message.answer("Введите название нового квартала для узбекоязычных пользователей", reply_markup=back)
        sub2_codes = await db.select_sub2()
        max_sub2_code = max(sub2_codes, key=lambda x: x)
        new_sub2 = 1 + int(max_sub2_code.get("sub2_code"))
        await state.update_data(sub2_code=new_sub2)
        await state.update_data(quarter=quarter)
        await New_room.Quarter_uz.set()


# New_room.Quarter_uz
async def new_quarter_uz(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    quarter_uz = message.text
    if message.text == "Назад":
        await message.answer("Введите название нового квартала для рускоязычных пользователей", reply_markup=back)
        await New_room.Quarter.set()
    else:
        await state.update_data(sub2category_uz=quarter_uz)
        await message.answer("Отправьте ссылку на объект для рускоязычных пользователей", reply_markup=back)
        await New_room.New_url.set()


# New_room.New_url
async def new_url1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_url = message.text
    if message.text == "Назад":
        await message.answer("Введите название нового квартала для узбекоязычных пользователей", reply_markup=back)
        await New_room.Quarter_uz.set()
    else:
        await message.answer("Отправьте ссылку на объект для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_url=msq_url)
        await New_room.New_url_uz.set()


# New_room.New_url_uz
async def new_url_uz1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_url_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте ссылку на объект для рускоязычных пользователей", reply_markup=back)
        await New_room.New_url.set()
    else:
        await message.answer("Отправьте текст ссылки для рускоязычных пользователей", reply_markup=back)
        await state.update_data(msq_url_uz=msq_url_uz)
        await New_room.New_text.set()


# New_room.New_text
async def new_text1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_text = message.text
    if message.text == "Назад":
        await message.answer("Отправьте ссылку на объект для узбекоязычных пользователей", reply_markup=back)
        await New_room.New_url_uz.set()
    else:
        await message.answer("Отправьте текст ссылки для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_text=msq_text)
        await New_room.New_text_uz.set()


# New_room.New_text_uz
async def new_text_uz1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_text_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте текст ссылки для рускоязычных пользователей", reply_markup=back)
        await New_room.New_text.set()
    else:
        await message.answer("Отправьте описание для рускоязычных пользователей", reply_markup=back)
        await state.update_data(msq_text_uz=msq_text_uz)
        await New_room.New_desc.set()


# New_room.New_desc
async def new_desc1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_desc = message.text
    if message.text == "Назад":
        await message.answer("Отправьте текст ссылки для узбекоязычных пользователей", reply_markup=back)
        await New_room.New_text.set()
    else:
        await message.answer("Отправьте описание для узбекоязычных пользователей", reply_markup=back)
        await state.update_data(msq_desc=msq_desc)
        await New_room.New_desc_uz.set()


# New_room.New_desc_uz
async def new_desc_uz1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    msq_desc_uz = message.text
    if message.text == "Назад":
        await message.answer("Отправьте описание для рускоязычных пользователей", reply_markup=back)
        await New_room.New_desc.set()
    else:
        await message.answer("Отправьте айди объекта", reply_markup=back)
        await state.update_data(msq_desc_uz=msq_desc_uz)
        await New_room.New_id.set()


# New_room.New_id
async def new_id1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("room")
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
        await New_room.New_desc_uz.set()
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
            await New_room.Confirm.set()
        except:
            await message.answer("Отправьте айди объекта", reply_markup=back)
            await New_room.New_id.set()


# New_room.Confirm
async def new_confirm1(message: types.Message, state: FSMContext):
    db = message.bot.get("db")
    data = await state.get_data()
    categ = data.get("categ")
    types = data.get("types")
    roomm = data.get("room")
    region = data.get("region")
    quarter = data.get("quarter")
    room_code = int(data.get("room_code"))
    sub1_code = int(data.get("sub1_code"))
    sub2_code = int(data.get("sub2_code"))
    id_obj = int(data.get("id_obj"))

    catg_code = int(data.get("catg_code"))
    type_code = int(data.get("type_code"))
    roomm_uz = data.get("room_uz")
    region_uz = data.get("sub1category_uz")
    quarter_uz = data.get("sub2category_uz")

    msq_url = data.get("msq_url")
    msq_url_uz = data.get("msq_url_uz")
    msq_text = data.get("msq_text")
    msq_text_uz = data.get("msq_text_uz")
    msq_desc = data.get("msq_desc")
    msq_desc_uz = data.get("msq_desc_uz")
    if message.text == "Назад":
        await message.answer("Отправьте айди объекта", reply_markup=back)
        await New_room.New_id.set()
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


def register_add_object(dp: Dispatcher):
    dp.register_message_handler(custom_flats, IsAdmin(), text="Квартиры")
    dp.register_message_handler(add_flat, IsAdmin(), text="Добавить Квартиру")
    dp.register_message_handler(select_in_categ, IsAdmin(), state=Add_obj.Categ, text=["Купить", "Снять", "Назад"])
    dp.register_message_handler(select_in_types, IsAdmin(), state=Add_obj.Types, text=["Квартира", "Коммерческое", "Назад"])
    dp.register_message_handler(select_in_room, IsAdmin(), state=Add_obj.Room)
    dp.register_message_handler(select_in_regions, IsAdmin(), state=Add_obj.Region)
    dp.register_message_handler(select_in_quarter, IsAdmin(), state=Add_obj.Quarter)

    dp.register_message_handler(new_url, state=Add_obj.New_url)
    dp.register_message_handler(new_url_uz, state=Add_obj.New_url_uz)
    dp.register_message_handler(new_text, state=Add_obj.New_text)
    dp.register_message_handler(new_text_uz, state=Add_obj.New_text_uz)
    dp.register_message_handler(new_desc, state=Add_obj.New_desc)
    dp.register_message_handler(new_desc_uz, state=Add_obj.New_desc_uz)
    dp.register_message_handler(new_id, state=Add_obj.New_id)
    dp.register_message_handler(new_confirm, state=Add_obj.Confirm)

    dp.register_message_handler(new_room, state=New_room.Room)
    dp.register_message_handler(new_room_uz, state=New_room.Room_uz)
    dp.register_message_handler(new_region, state=New_room.Region)
    dp.register_message_handler(new_region_uz, state=New_room.Region_uz)
    dp.register_message_handler(new_quarter, state=New_room.Quarter)
    dp.register_message_handler(new_quarter_uz, state=New_room.Quarter_uz)

    dp.register_message_handler(new_url1, state=New_room.New_url)
    dp.register_message_handler(new_url_uz1, state=New_room.New_url_uz)
    dp.register_message_handler(new_text1, state=New_room.New_text)
    dp.register_message_handler(new_text_uz1, state=New_room.New_text_uz)
    dp.register_message_handler(new_desc1, state=New_room.New_desc)
    dp.register_message_handler(new_desc_uz1, state=New_room.New_desc_uz)
    dp.register_message_handler(new_id1, state=New_room.New_id)
    dp.register_message_handler(new_confirm1, state=New_room.Confirm)



