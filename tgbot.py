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
        "caption": "Лосины Черные",
    },
    {
        "name": "Топы",
        "decripton": "Белые",
        "price": "1200",
        "id": "prod_2",
        "img": "r_1.jpg",
        "caption": "Топы Белые",
    },
    {
        "name": "Рашгарды",
        "decripton": "Красные",
        "price": "3000",
        "id": "prod_3",
        "img": "t_1.jpg",
        "caption": "Рашгарды Красные",
    },
]


