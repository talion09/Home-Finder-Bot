from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)

confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Верно"),
            KeyboardButton(text="Отменить")

        ],
        [
            KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True
)
