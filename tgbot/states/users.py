from aiogram.dispatcher.filters.state import StatesGroup, State


class Sell(StatesGroup):
    Phone = State()
    Sell_obj = State()
    Rent_obj = State()


class Appeal(StatesGroup):
    Get = State()


class Add_obj(StatesGroup):
    Categ = State()
    Types = State()
    Room = State()
    Region = State()
    Quarter = State()

    New_url = State()
    New_url_uz = State()
    New_text = State()
    New_text_uz = State()
    New_desc = State()
    New_desc_uz = State()
    New_id = State()
    Confirm = State()


class New_room(StatesGroup):
    Room = State()
    Room_uz = State()
    Region = State()
    Region_uz = State()
    Quarter = State()
    Quarter_uz = State()

    New_url = State()
    New_url_uz = State()
    New_text = State()
    New_text_uz = State()
    New_desc = State()
    New_desc_uz = State()
    New_id = State()
    Confirm = State()


class New_region(StatesGroup):
    Region = State()
    Region_uz = State()
    Quarter = State()
    Quarter_uz = State()

    New_url = State()
    New_url_uz = State()
    New_text = State()
    New_text_uz = State()
    New_desc = State()
    New_desc_uz = State()
    New_id = State()
    Confirm = State()


class New_quarter(StatesGroup):
    Quarter = State()
    Quarter_uz = State()

    New_url = State()
    New_url_uz = State()
    New_text = State()
    New_text_uz = State()
    New_desc = State()
    New_desc_uz = State()
    New_id = State()
    Confirm = State()


class Edit_obj(StatesGroup):
    Categ = State()
    Types = State()
    Room = State()
    Region = State()
    Quarter = State()

    New_url = State()
    New_url_uz = State()
    New_text = State()
    New_text_uz = State()
    New_desc = State()
    New_desc_uz = State()
    New_id = State()
    Confirm = State()


class Edit_room(StatesGroup):
    Room = State()
    New_Room = State()
    Room_uz = State()


class Edit_region(StatesGroup):
    Region = State()
    New_Region = State()
    Region_uz = State()


class Edit_quarter(StatesGroup):
    Quarter = State()
    New_Quarter = State()
    Quarter_uz = State()


class Delete_obj(StatesGroup):
    Categ = State()
    Types = State()
    Room = State()
    Region = State()
    Quarter = State()


class Admin(StatesGroup):
    Delete_admin = State()
    Add_admin = State()


class Group(StatesGroup):
    Next = State()





