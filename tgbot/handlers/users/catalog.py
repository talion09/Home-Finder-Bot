from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


from tgbot.handlers.users.start import ru_language, admins_list
from tgbot.keyboards.inline.catalog import menu, categ, type_categ, room_clb, regions_next, regions_back, quarter_clb, \
    slider, regions_cmrc, quarter_cmrc, delete_cart


async def catalog(call: CallbackQuery):
    db = call.bot.get("db")
    _ = call.bot.get("lang")

    await call.answer()
    text = _("Сделали для Вас удобный каталог недвижимости. \n\nЧто Вас интересует?:")
    take = _("Снять")
    buy = _("Купить")
    back = _("Назад")

    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text=take, callback_data=categ.new(categ_code=2, action="next")))
    markup.insert(InlineKeyboardButton(text=buy, callback_data=categ.new(categ_code=1, action="next")))
    markup.add(InlineKeyboardButton(text=back, callback_data=categ.new(categ_code=0, action="back")))
    await call.bot.send_photo(call.from_user.id,
                              photo="AgACAgIAAxkBAAMGZT5pjzGnkQE0OgwEs2YrNE-2PK8AAknQMRv1QPhJjpucO7z7XvUBAAMCAAN5AAMwBA",
                              caption=text, reply_markup=markup)
# AgACAgIAAxkBAAIG72SO0ZGaS2a9TETUy5O7lWmi0C_FAAJQxzEbmkh4SLMGuF2NjryKAQADAgADeQADLwQ

async def back_menu(call: CallbackQuery):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await admins_list(call)


async def types_catg(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    categ_code = callback_data.get("categ_code")

    await call.answer()
    text = _("Какой тип недвижимости Вас интересует:")
    flat = _("Квартира")
    commerc = _("Коммерческое")
    back = _("Назад")

    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text=flat, callback_data=type_categ.new(categ_code=categ_code, type_code=1, action="next")))
    markup.insert(InlineKeyboardButton(text=commerc, callback_data=type_categ.new(categ_code=categ_code, type_code=2, action="next_cmrc")))
    markup.add(InlineKeyboardButton(text=back, callback_data=type_categ.new(categ_code=categ_code, type_code=0, action="back")))
    await call.bot.send_photo(call.from_user.id,
                              photo="AgACAgIAAxkBAAMGZT5pjzGnkQE0OgwEs2YrNE-2PK8AAknQMRv1QPhJjpucO7z7XvUBAAMCAAN5AAMwBA",
                              caption=text, reply_markup=markup)


async def rooms(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    categ_code = int(callback_data.get("categ_code"))
    type_code = int(callback_data.get("type_code"))

    await call.answer()
    send_text = _("Выберите категорию:")
    back = _("Назад")

    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    markup = InlineKeyboardMarkup(row_width=1)
    room_lst = []
    room_lst_uz = []
    if await ru_language(call):
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_in_types(
                catg_code=categ_code, type_code=type_code):
            if room:
                if room not in room_lst:
                    room_lst.append(room)
                    markup.insert(InlineKeyboardButton(text=room, callback_data=room_clb.new(categ_code=categ_code,
                                                                                             type_code=type_code,
                                                                                             room_code=room_code,
                                                                                             action="next")))
            else:
                pass
    else:
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_in_types(
                catg_code=categ_code, type_code=type_code):
            if room_uz:
                if room_uz not in room_lst_uz:
                    room_lst_uz.append(room_uz)
                    markup.insert(InlineKeyboardButton(text=room_uz, callback_data=room_clb.new(categ_code=categ_code,
                                                                                                type_code=type_code,
                                                                                                room_code=room_code,
                                                                                                action="next")))
            else:
                pass
    markup.add(InlineKeyboardButton(text=back, callback_data=room_clb.new(categ_code=categ_code, type_code=type_code, room_code=0, action="back")))
    await call.bot.send_message(call.from_user.id, text=send_text, reply_markup=markup)


async def regions(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    categ_code = int(callback_data.get("categ_code"))
    type_code = int(callback_data.get("type_code"))
    room_code = int(callback_data.get("room_code"))


    await call.answer()
    send_text = _("Выберите район:")
    back = _("Назад")

    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    markup = InlineKeyboardMarkup(row_width=1)
    region_lst = []
    region_lst_uz = []
    if await ru_language(call):
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_in_rooms(
                catg_code=categ_code, type_code=type_code, room_code=room_code):
            if sub1category not in region_lst:
                region_lst.append(sub1category)
                markup.insert(
                    InlineKeyboardButton(text=sub1category, callback_data=regions_next.new(categ_code=categ_code,
                                                                                           type_code=type_code,
                                                                                           room_code=room_code,
                                                                                           sub1_code=sub1_code)))
    else:
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_in_rooms(
                catg_code=categ_code, type_code=type_code, room_code=room_code):
            if sub1category_uz not in region_lst_uz:
                region_lst_uz.append(sub1category_uz)
                markup.insert(
                    InlineKeyboardButton(text=sub1category_uz, callback_data=regions_next.new(categ_code=categ_code,
                                                                                              type_code=type_code,
                                                                                              room_code=room_code,
                                                                                              sub1_code=sub1_code)))

    markup.add(InlineKeyboardButton(text=back,
                                    callback_data=regions_back.new(categ_code=categ_code, type_code=type_code,
                                                                   room_code=room_code, sub1_code=0)))
    await call.bot.send_message(call.from_user.id, text=send_text, reply_markup=markup)


async def quarter(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    categ_code = int(callback_data.get("categ_code"))
    type_code = int(callback_data.get("type_code"))
    room_code = int(callback_data.get("room_code"))
    sub1_code = int(callback_data.get("sub1_code"))

    await call.answer()
    send_text = _("Выберите квартал:")
    send_text2 = _("Все объекты")
    back = _("Назад")

    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(InlineKeyboardButton(text=send_text2, callback_data=quarter_clb.new(categ_code=categ_code,
                                                                                      type_code=type_code,
                                                                                      room_code=room_code,
                                                                                      sub1_code=sub1_code,
                                                                                      sub2_code=999,
                                                                                      action="all")))
    quarter_lst = []
    quarter_lst_uz = []
    if await ru_language(call):
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_in_regions(
                catg_code=categ_code, type_code=type_code, room_code=room_code, sub1_code=sub1_code):
            if sub2category not in quarter_lst:
                quarter_lst.append(sub2category)
                markup.insert(InlineKeyboardButton(text=sub2category, callback_data=quarter_clb.new(categ_code=categ_code,
                                                                                         type_code=type_code, room_code=room_code,
                                                                                         sub1_code=sub1_code, sub2_code=sub2_code,
                                                                                         action="next")))
    else:
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_in_regions(
                catg_code=categ_code, type_code=type_code, room_code=room_code, sub1_code=sub1_code):
            if sub2category_uz not in quarter_lst_uz:
                quarter_lst_uz.append(sub2category_uz)
                markup.insert(InlineKeyboardButton(text=sub2category_uz, callback_data=quarter_clb.new(categ_code=categ_code,
                                                                                         type_code=type_code, room_code=room_code,
                                                                                         sub1_code=sub1_code, sub2_code=sub2_code,
                                                                                         action="next")))

    markup.add(InlineKeyboardButton(text=back, callback_data=quarter_clb.new(categ_code=categ_code, type_code=type_code, room_code=room_code, sub1_code=sub1_code, sub2_code=0, action="back")))
    await call.bot.send_message(call.from_user.id, text=send_text, reply_markup=markup)


async def quarter_back(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")

    flat_id = int(callback_data.get("id"))
    flat = await db.select_flat(id=flat_id)
    categ_code = int(flat.get("catg_code"))
    type_code = int(flat.get("type_code"))
    room_code = int(flat.get("room_code"))
    sub1_code = int(flat.get("sub1_code"))

    await call.answer()
    send_text = _("Выберите квартал:")
    send_text2 = _("Все объекты")
    back = _("Назад")

    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(InlineKeyboardButton(text=send_text2, callback_data=quarter_clb.new(categ_code=categ_code,
                                                                                      type_code=type_code,
                                                                                      room_code=room_code,
                                                                                      sub1_code=sub1_code,
                                                                                      sub2_code=999,
                                                                                      action="all")))
    quarter_lst = []
    quarter_lst_uz = []
    if await ru_language(call):
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_in_regions(
                catg_code=categ_code, type_code=type_code, room_code=room_code, sub1_code=sub1_code):
            if sub2category not in quarter_lst:
                quarter_lst.append(sub2category)
                markup.insert(InlineKeyboardButton(text=sub2category, callback_data=quarter_clb.new(categ_code=categ_code,
                                                                                         type_code=type_code, room_code=room_code,
                                                                                         sub1_code=sub1_code, sub2_code=sub2_code,
                                                                                         action="next")))
    else:
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_in_regions(
                catg_code=categ_code, type_code=type_code, room_code=room_code, sub1_code=sub1_code):
            if sub2category_uz not in quarter_lst_uz:
                quarter_lst_uz.append(sub2category_uz)
                markup.insert(InlineKeyboardButton(text=sub2category_uz, callback_data=quarter_clb.new(categ_code=categ_code,
                                                                                         type_code=type_code, room_code=room_code,
                                                                                         sub1_code=sub1_code, sub2_code=sub2_code,
                                                                                         action="next")))

    markup.add(InlineKeyboardButton(text=back, callback_data=quarter_clb.new(categ_code=categ_code, type_code=type_code, room_code=room_code, sub1_code=sub1_code, sub2_code=0, action="back")))
    await call.bot.send_message(call.from_user.id, text=send_text, reply_markup=markup)


async def all_flats(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    categ_code = int(callback_data.get("categ_code"))
    room_code = int(callback_data.get("room_code"))
    sub1_code = int(callback_data.get("sub1_code"))
    sub2_codee = int(callback_data.get("sub2_code"))

    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    order_txt = _("В лист осмотра 📃")
    backk = _("Назад")
    basket = _("📃 Лист осмотра")

    ids = []
    for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in sorted(
            await db.ids_in_flats_sub1(sub1_code=sub1_code, room_code=room_code, catg_code=categ_code)):
        if id not in ids:
            ids.append(id)
    flat = await db.select_flat(id=int(ids[0]))
    flat_id = int(flat.get("id"))
    flat_index = ids.index(flat_id)
    if await ru_language(call):
        msg_url = flat.get("url")
        msg_text = flat.get("text")
        # msg_descrip = flat.get("descrip")
    else:
        msg_url = flat.get("url_uz")
        msg_text = flat.get("text_uz")

    user_cart = await db.select_cart(telegram_id=call.from_user.id, object_id=flat_id)
    if user_cart:
        order_txt = "✅ " + order_txt
    else:
        pass

    markup = InlineKeyboardMarkup(row_width=1)
    next = InlineKeyboardButton(text="⬅️", callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_codee, action="back_slide"))
    page = InlineKeyboardButton(text=f"1/{len(ids)}", callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_codee, action="none"))
    back = InlineKeyboardButton(text="➡️", callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_codee, action="next_slide"))
    markup.row(next, page, back)
    markup.insert(InlineKeyboardButton(text=order_txt, callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_codee, action="order")))
    markup.insert(InlineKeyboardButton(text=backk, callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_codee, action="back")))
    markup.insert(InlineKeyboardButton(text=basket, callback_data=menu.new(action="basket")))
    await call.bot.send_message(call.from_user.id, text=f" <a href='{msg_url}'>{msg_text}</a>", reply_markup=markup)


async def flats(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    categ_code = int(callback_data.get("categ_code"))
    type_code = int(callback_data.get("type_code"))
    room_code = int(callback_data.get("room_code"))
    sub1_code = int(callback_data.get("sub1_code"))
    sub2_code = int(callback_data.get("sub2_code"))

    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    order_txt = _("В лист осмотра 📃")
    backk = _("Назад")
    basket = _("📃 Лист осмотра")

    ids = []
    for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in sorted(await db.select_flats(catg_code=categ_code, type_code=type_code, room_code=room_code, sub1_code=sub1_code, sub2_code=sub2_code)):
        if id not in ids:
            ids.append(id)
    flat = await db.select_flat(id=int(ids[0]))
    flat_id = int(flat.get("id"))
    flat_index = ids.index(flat_id)
    if await ru_language(call):
        msg_url = flat.get("url")
        msg_text = flat.get("text")
        # msg_descrip = flat.get("descrip")
    else:
        msg_url = flat.get("url_uz")
        msg_text = flat.get("text_uz")

    user_cart = await db.select_cart(telegram_id=call.from_user.id, object_id=flat_id)
    if user_cart:
        order_txt = "✅ " + order_txt
    else:
        pass

    markup = InlineKeyboardMarkup(row_width=1)
    next = InlineKeyboardButton(text="⬅️", callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code, action="back_slide"))
    page = InlineKeyboardButton(text=f"1/{len(ids)}", callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code, action="none"))
    back = InlineKeyboardButton(text="➡️", callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code, action="next_slide"))
    markup.row(next, page, back)
    markup.insert(InlineKeyboardButton(text=order_txt, callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code, action="order")))
    markup.insert(InlineKeyboardButton(text=backk, callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code, action="back")))
    markup.insert(InlineKeyboardButton(text=basket, callback_data=menu.new(action="basket")))
    await call.bot.send_message(call.from_user.id, text=f" <a href='{msg_url}'>{msg_text}</a>", reply_markup=markup)


async def slider_func(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    flat_id = int(callback_data.get("id"))
    flat_index = int(callback_data.get("index"))
    sub2_codee = int(callback_data.get("sub2_code"))

    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    order_txt = _("В лист осмотра 📃")
    backk = _("Назад")
    basket = _("📃 Лист осмотра")


    flat = await db.select_flat(id=flat_id)
    catg_code = int(flat.get("catg_code"))
    room_code = int(flat.get("room_code"))
    sub1_code = int(flat.get("sub1_code"))

    id_list = []
    if sub2_codee == 999:
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in sorted(
                await db.ids_in_flats_sub1(sub1_code=sub1_code, room_code=room_code, catg_code=catg_code)):
            if id not in id_list:
                id_list.append(id)
    else:
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in sorted(
                await db.ids_in_flats_sub2(sub2_code=sub2_codee, room_code=room_code, catg_code=catg_code)):
            if id not in id_list:
                id_list.append(id)

    user_cart = await db.select_cart(telegram_id=call.from_user.id, object_id=flat_id)
    if callback_data.get("action") == 'back_slide':
        flat_index -= 1
    elif callback_data.get("action") == 'next_slide':
        flat_index += 1
    elif callback_data.get("action") == 'order':
        await call.answer(text="Занесен в Лист осмотра 📃", show_alert=True)
        if user_cart:
            pass
        else:
            await db.add_to_cart(telegram_id=call.from_user.id, object_id=flat_id)
        order_txt = "✅ " + order_txt
    else:
        pass

    current_index = flat_index
    if flat_index < 0:
        current_index = len(id_list) - 1
    elif flat_index >= len(id_list):
        current_index = 0

    flat_id = id_list[current_index]
    flat = await db.select_flat(id=int(flat_id))
    if await ru_language(call):
        msg_url = flat.get("url")
        msg_text = flat.get("text")
        # msg_descrip = flat.get("descrip")
    else:
        msg_url = flat.get("url_uz")
        msg_text = flat.get("text_uz")

    user_cart2 = await db.select_cart(telegram_id=call.from_user.id, object_id=flat_id)
    if user_cart2:
        if "✅" in order_txt:
            pass
        else:
            order_txt = "✅ " + order_txt
    else:
        pass


    markup = InlineKeyboardMarkup(row_width=1)
    next = InlineKeyboardButton(text="⬅️", callback_data=slider.new(id=flat_id, index=current_index, sub2_code=sub2_codee, action="back_slide"))
    page = InlineKeyboardButton(text=f"{current_index + 1}/{len(id_list)}", callback_data=slider.new(id=flat_id, index=current_index, sub2_code=sub2_codee, action="none"))
    back = InlineKeyboardButton(text="➡️", callback_data=slider.new(id=flat_id, index=current_index, sub2_code=sub2_codee, action="next_slide"))
    markup.row(next, page, back)
    markup.insert(InlineKeyboardButton(text=order_txt, callback_data=slider.new(id=flat_id, index=current_index, sub2_code=sub2_codee, action="order")))
    markup.insert(InlineKeyboardButton(text=backk, callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_codee, action="back")))
    markup.insert(InlineKeyboardButton(text=basket, callback_data=menu.new(action="basket")))
    await call.bot.send_message(call.from_user.id, text=f" <a href='{msg_url}'>{msg_text}</a>", reply_markup=markup)


async def commerc(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    categ_code = int(callback_data.get("categ_code"))
    type_code = int(callback_data.get("type_code"))

    await call.answer()
    send_text = _("Выберите район:")
    back = _("Назад")

    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    markup = InlineKeyboardMarkup(row_width=1)
    regions_lst = []
    regions_lst_uz = []
    if await ru_language(call):
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_in_types(
                catg_code=categ_code, type_code=type_code):
            if sub1category not in regions_lst:
                regions_lst.append(sub1category)
                markup.insert(InlineKeyboardButton(text=sub1category, callback_data=regions_cmrc.new(categ_code=categ_code,
                                                                                         type_code=type_code,
                                                                                         sub1_code=sub1_code,
                                                                                         action="next")))
    else:
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_in_types(
                catg_code=categ_code, type_code=type_code):
            if sub1category_uz not in regions_lst_uz:
                regions_lst_uz.append(sub1category_uz)
                markup.insert(InlineKeyboardButton(text=sub1category_uz, callback_data=regions_cmrc.new(categ_code=categ_code,
                                                                                         type_code=type_code,
                                                                                         sub1_code=sub1_code,
                                                                                         action="next")))
    markup.add(InlineKeyboardButton(text=back, callback_data=regions_cmrc.new(categ_code=categ_code, type_code=type_code, sub1_code=0, action="back")))
    await call.bot.send_message(call.from_user.id, text=send_text, reply_markup=markup)


async def commerc_quarter(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    categ_code = int(callback_data.get("categ_code"))
    type_code = int(callback_data.get("type_code"))
    sub1_code = int(callback_data.get("sub1_code"))

    await call.answer()
    send_text = _("Выберите район:")
    send_text2 = _("Все объекты")
    back = _("Назад")

    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(InlineKeyboardButton(text=send_text2, callback_data=quarter_cmrc.new(categ_code=categ_code,
                                                                                      type_code=type_code,
                                                                                      sub1_code=sub1_code,
                                                                                      sub2_code=999,
                                                                                      action="all")))
    quarter_lst = []
    quarter_lst_uz = []
    if await ru_language(call):
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_quarter(
                catg_code=categ_code, type_code=type_code, sub1_code=sub1_code):
            if sub2category not in quarter_lst:
                quarter_lst.append(sub2category)
                markup.insert(InlineKeyboardButton(text=sub2category, callback_data=quarter_cmrc.new(categ_code=categ_code,
                                                                                         type_code=type_code,
                                                                                         sub1_code=sub1_code, sub2_code=sub2_code,
                                                                                         action="next")))
    else:
        for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in await db.select_quarter(
                catg_code=categ_code, type_code=type_code, sub1_code=sub1_code):
            if sub2category_uz not in quarter_lst_uz:
                quarter_lst_uz.append(sub2category_uz)
                markup.insert(InlineKeyboardButton(text=sub2category_uz, callback_data=quarter_cmrc.new(categ_code=categ_code,
                                                                                         type_code=type_code,
                                                                                         sub1_code=sub1_code, sub2_code=sub2_code,
                                                                                         action="next")))
    markup.add(InlineKeyboardButton(text=back, callback_data=quarter_cmrc.new(categ_code=categ_code, type_code=type_code, sub1_code=sub1_code, sub2_code=0, action="back")))
    await call.bot.send_message(call.from_user.id, text=send_text, reply_markup=markup)


async def all_houses(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    categ_code = int(callback_data.get("categ_code"))
    type_code = int(callback_data.get("type_code"))
    sub1_code = int(callback_data.get("sub1_code"))
    sub2_codee = int(callback_data.get("sub2_code"))

    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    order_txt = _("В лист осмотра 📃")
    backk = _("Назад")
    basket = _("📃 Лист осмотра")

    ids = []
    for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in sorted(
            await db.select_flats(sub1_code=sub1_code, catg_code=categ_code, type_code=type_code)):
        if id not in ids:
            ids.append(id)
    flat = await db.select_flat(id=int(ids[0]))
    flat_id = int(flat.get("id"))
    flat_index = ids.index(flat_id)
    if await ru_language(call):
        msg_url = flat.get("url")
        msg_text = flat.get("text")
        # msg_descrip = flat.get("descrip")
    else:
        msg_url = flat.get("url_uz")
        msg_text = flat.get("text_uz")

    markup = InlineKeyboardMarkup(row_width=1)
    next = InlineKeyboardButton(text="⬅️", callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_codee, action="back_slide"))
    page = InlineKeyboardButton(text=f"1/{len(ids)}", callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_codee, action="none"))
    back = InlineKeyboardButton(text="➡️", callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_codee, action="next_slide"))
    markup.row(next, page, back)
    markup.insert(InlineKeyboardButton(text=order_txt, callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_codee, action="order")))
    markup.insert(InlineKeyboardButton(text=backk, callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_codee, action="back")))
    markup.insert(InlineKeyboardButton(text=basket, callback_data=menu.new(action="basket")))
    await call.bot.send_message(call.from_user.id, text=f" <a href='{msg_url}'>{msg_text}</a>", reply_markup=markup)


async def houses(call: CallbackQuery, callback_data: dict):
    db = call.bot.get("db")
    _ = call.bot.get("lang")
    categ_code = int(callback_data.get("categ_code"))
    type_code = int(callback_data.get("type_code"))
    sub1_code = int(callback_data.get("sub1_code"))
    sub2_code = int(callback_data.get("sub2_code"))

    await call.answer()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    order_txt = _("В лист осмотра 📃")
    backk = _("Назад")
    basket = _("📃 Лист осмотра")

    ids = []
    for key_id, id, catg_code, category, type_code, type, room_code, room, room_uz, sub1_code, sub1category, sub1category_uz, sub2_code, sub2category, sub2category_uz, url, url_uz, text, text_uz, descrip, desc_uz in sorted(await db.select_flats(catg_code=categ_code, type_code=type_code, sub1_code=sub1_code, sub2_code=sub2_code)):
        if id not in ids:
            ids.append(id)
    flat = await db.select_flat(id=int(ids[0]))
    flat_id = int(flat.get("id"))
    flat_index = ids.index(flat_id)
    if await ru_language(call):
        msg_url = flat.get("url")
        msg_text = flat.get("text")
        # msg_descrip = flat.get("descrip")
    else:
        msg_url = flat.get("url_uz")
        msg_text = flat.get("text_uz")

    markup = InlineKeyboardMarkup(row_width=1)
    next = InlineKeyboardButton(text="⬅️", callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code, action="back_slide"))
    page = InlineKeyboardButton(text=f"1/{len(ids)}", callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code, action="none"))
    back = InlineKeyboardButton(text="➡️", callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code, action="next_slide"))
    markup.row(next, page, back)
    markup.insert(InlineKeyboardButton(text=order_txt, callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code, action="order")))
    markup.insert(InlineKeyboardButton(text=backk, callback_data=slider.new(id=flat_id, index=flat_index, sub2_code=sub2_code, action="back")))
    markup.insert(InlineKeyboardButton(text=basket, callback_data=menu.new(action="basket")))
    await call.bot.send_message(call.from_user.id, text=f" <a href='{msg_url}'>{msg_text}</a>", reply_markup=markup)


def register_catalog(dp: Dispatcher):
    dp.register_callback_query_handler(catalog, delete_cart.filter(action="add"))
    dp.register_callback_query_handler(catalog, menu.filter(action="catalog"))
    dp.register_callback_query_handler(catalog, type_categ.filter(action="back"))
    dp.register_callback_query_handler(back_menu, categ.filter(action="back"))


    dp.register_callback_query_handler(types_catg, categ.filter(action="next"))
    dp.register_callback_query_handler(types_catg, room_clb.filter(action="back"))
    dp.register_callback_query_handler(types_catg, regions_cmrc.filter(action="back"))

    dp.register_callback_query_handler(rooms, type_categ.filter(action="next"))
    dp.register_callback_query_handler(rooms, regions_back.filter())

    dp.register_callback_query_handler(regions, room_clb.filter(action="next"))
    dp.register_callback_query_handler(regions, quarter_clb.filter(action="back"))

    dp.register_callback_query_handler(quarter, regions_next.filter())
    dp.register_callback_query_handler(quarter_back, slider.filter(action="back"))

    dp.register_callback_query_handler(all_flats, quarter_clb.filter(action="all"))
    dp.register_callback_query_handler(flats, quarter_clb.filter(action="next"))
    dp.register_callback_query_handler(slider_func, slider.filter())

    # ____________________________________________________________________________________________________________________

    dp.register_callback_query_handler(commerc, type_categ.filter(action="next_cmrc"))
    dp.register_callback_query_handler(commerc, quarter_cmrc.filter(action="back"))

    dp.register_callback_query_handler(commerc_quarter, regions_cmrc.filter(action="next"))

    dp.register_callback_query_handler(all_houses, quarter_cmrc.filter(action="all"))
    dp.register_callback_query_handler(houses, quarter_cmrc.filter(action="next"))





