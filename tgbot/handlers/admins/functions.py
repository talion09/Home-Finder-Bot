from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def rooms_admin(message, categ, types):
    db = message.bot.get("db")
    rooms = []
    # markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # markup.insert(KeyboardButton(text="Добавить кол-во комнат"))
    lst = []
    lst.append(KeyboardButton(text="Назад"))
    for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_flats(
            category=categ, type=types):
        if room:
            if room not in rooms:
                rooms.append(room)
                lst.append(KeyboardButton(text=room))
        else:
            pass
    return lst


async def regions_admin(message, categ, types, roomm):
    db = message.bot.get("db")
    if roomm == 0:
        try:
            select = await db.select_flat(category=categ, type=types)
            select.get("sub1_code")
            sub1categories = []
            # markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            # markup.insert(KeyboardButton(text="Добавить новый район"))
            lst = []
            lst.append(KeyboardButton(text="Назад"))
            for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_flats(
                    category=categ, type=types):
                if sub1category not in sub1categories:
                    sub1categories.append(sub1category)
            for region in sorted(sub1categories):
                lst.append(KeyboardButton(text=region))
                return lst

        except:
            pass
    else:
        try:
            select = await db.select_flat(category=categ, type=types, room=roomm)
            select.get("sub1_code")
            sub1categories = []
            lst = []
            lst.append(KeyboardButton(text="Назад"))
            for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_flats(
                    category=categ, type=types, room=roomm):
                if sub1category not in sub1categories:
                    sub1categories.append(sub1category)
            for region in sorted(sub1categories):
                lst.append(KeyboardButton(text=region))
            return lst

        except:
            pass


async def quarters_admin(message, categ, types, roomm, sub1):
    db = message.bot.get("db")
    if roomm == 0:
        try:
            select = await db.select_flat(category=categ, type=types, sub1category=sub1)
            select.get("sub2_code")
            sub2categories = []
            # markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            # markup.insert(KeyboardButton(text="Добавить новый квартал"))
            lst = []
            lst.append(KeyboardButton(text="Назад"))
            for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_flats(
                    category=categ, type=types, sub1category=sub1):
                if sub2category not in sub2categories:
                    sub2categories.append(sub2category)
            for quarter in sorted(sub2categories):
                lst.append(KeyboardButton(text=quarter))
            return lst
        except:
            pass
    else:
        try:
            select = await db.select_flat(category=categ, type=types, room=roomm)
            print("select", select)
            select.get("sub1_code")
            sub2categories = []
            # markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            # markup.insert(KeyboardButton(text="Добавить новый квартал"))
            lst = []
            lst.append(KeyboardButton(text="Назад"))
            for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_flats(
                    category=categ, type=types, room=roomm, sub1category=sub1):
                if sub2category not in sub2categories:
                    sub2categories.append(sub2category)
            for quarter in sorted(sub2categories):
                lst.append(KeyboardButton(text=quarter))
            print("sub2categories", sub2categories)
            print("lst", lst)
            return lst
        except:
            pass