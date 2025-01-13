from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from produck_data import products


products = [
    {
        "name": "Лосины",
        "decripton": "Черные",
        "price": "4500",
        "id": "prod_1",
        "img": "l_1.jpg",
    },
    {
        "name": "Топы",
        "decripton": "Белые",
        "price": "1200",
        "id": "prod_2",
        "img": "r_1.jpg",
    },
    {
        "name": "Рашгарды",
        "decripton": "Красные",
        "price": "3000",
        "id": "prod_3",
        "img": "t_1.jpg",
    },
]


def product_kb():
    buttons = []
    for product in products:
        button_name = (
            f"{product['name']} {product['decripton']} price:{product['price']}"
        )
        button = InlineKeyboardButton(button_name, callback_data=product["id"])
        button.append([button])
    my_kb = InlineKeyboardMarkup(buttons)
    return my_kb


async def start(update, context):
    context.user_data["operation"] = None
    my_kb = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Начать", callback_data="start")],
            [InlineKeyboardButton("Купить", callback_data="buy")],
        ],
    )
    await update.message.reply_text(
        f'Здраствуйте,{update.effective_user.last_name} {update.effective_user.first_name}! Нажмите "Начать" для продолжения:',
        reply_markup=my_kb,
    )
