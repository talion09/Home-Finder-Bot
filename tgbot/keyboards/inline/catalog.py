
from aiogram.utils.callback_data import CallbackData


flat = CallbackData("flat", "action", "id", "likes", "dislikes", "views", "categ", "sub1")

delete_id = CallbackData("delete_id", "id", "action", "categ")
# _______________________________________________________________________________________________________________________

menu = CallbackData("menu", "action")

categ = CallbackData("categ", "categ_code", "action")

type_categ = CallbackData("type_categ", "categ_code", "type_code", "action")

room_clb = CallbackData("room_clb", "categ_code", "type_code", "room_code", "action")

regions_next = CallbackData("regions_next", "categ_code", "type_code", "room_code", "sub1_code")

regions_back = CallbackData("regions_back", "categ_code", "type_code", "room_code", "sub1_code")

quarter_clb = CallbackData("quarter_clb", "categ_code", "type_code", "room_code", "sub1_code", "sub2_code", "action")

slider = CallbackData("slider", "id", "index", "sub2_code", "action")

regions_cmrc = CallbackData("regions_cmrc", "categ_code", "type_code", "sub1_code", "action")

quarter_cmrc = CallbackData("quarter_cmrc", "categ_code", "type_code", "sub1_code", "sub2_code", "action")

delete_cart = CallbackData("delete_cart", "object_id", "action")

info_clb = CallbackData("info_clb", "action")

info_lng = CallbackData("info_lng", "action")

appeal_clb = CallbackData("appeal_clb", "action")

edit_slider = CallbackData("edit_slider", "id", "index", "sub2_code", "action")

del_slider = CallbackData("del_slider", "id", "index", "sub2_code", "action")

lang_clb = CallbackData("lang_clb", "action")





