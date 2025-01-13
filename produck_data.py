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
    await start_button(update, context)


async def button(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "start":
        await query.edit_message_text(
            text=f"Здравствуйте, {query.from_user.last_name} {query.from_user.first_name}! Вы находитесь в главном меню. Выберите действие:",
            reply_markup=query.message.reply_markup,
        )
    elif query.data == "buy":
        context.user_data["operation"] = "buy"
        await query.edit_message_text(
            text="Вы выбрали 'Купить'.", reply_markup=product_kb()
        )
    elif query.data.startswith("prod"):
        product_id = query.data
        context.user_data["product_id"] = product_id
        for product in products:
            if product["id"] == product_id:
                name = product["name"]
                price = product["price"]
                img = product["caption"]
                chat_id = update.effective_chat.id
                
