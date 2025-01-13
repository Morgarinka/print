from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,ConversationHandler
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


def product_kb():
    buttons = []
    for product in products:
        button_name = (
            f"{product['name']} {product['decripton']} price: {product['price']}"
        )
        button = InlineKeyboardButton(button_name, callback_data=product["id"])
        buttons.append([button])
    my_kb = InlineKeyboardMarkup(buttons)
    return my_kb


async def start(update, context):
    context.user_data["operation"] = None
    my_kb = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Начать", callback_data="start")],
            [InlineKeyboardButton("Купить", callback_data="buy")],
        ]
    )
    await update.message.reply_text(
        f'Здравствуйте, {update.effective_user.last_name} {update.effective_user.first_name}! Нажмите "Начать" для продолжения:',
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
                img = product["img"]
                caption = product["caption"]

                chat_id = update.effective_chat.id

                img_path = r"C:\Users\1\Desktop\Progammirov\print\Img\\" + img
                # Отправка фото с товаром
                with open(img_path, "rb") as photo:
                    await context.bot.send_photo(
                        chat_id=chat_id, photo=photo, caption=caption
                    )
                context.bot.send_message(
                    f"Вы выбрали {name} за {price} руб. Укажите количество:",
                )


async def receive_quantity(update, context):
    user_input = update.message.text
    if user_input.isdigit():
        product_name = context.user_data.get("product_name")
        product_price = context.user_data.get("product_price")
        quantity = int(user_input)
        total_price = quantity * int(product_price)

        await update.message.reply_text(
            f"Вы собираетесь продать {quantity} {product_name}(ов) на сумму {total_price} руб."
        )

    else:
        await update.message.reply_text("Пожалуйста, введите корректное количество.")


async def products_query(update, context):
    print("ok")


async def start_button(update, context):
    my_kb_2 = ReplyKeyboardMarkup(
        [
            ["Время работы", "Информация о компании"],
            ["Условия доставки", "Контакты"],
            ["Способ оплаты"],
        ],
        resize_keyboard=True,
    )

    await update.message.reply_text(
        f"Привет {update.effective_user.first_name}", reply_markup=my_kb_2
    )


async def text_button(update, context):
    user_text = update.message.text
    # разметка с текстовыми кнопками и их действия
    if user_text == "Время работы":
        bot_message = "«City Sport». Адрес: ул. Советская, 25. Время работы: пн. — выходной, вт. — вс. 10:00–18:00"
    elif user_text == "Информация о компании":
        bot_message = (
            "Мы магазин спортивного белья, на рынке 10 лет радуем своих покупателей качественной одеждой из Турции, Китая и Европы. "
            "А также в нашем ассортименте спортивное питание, витамины и пищевые добавки."
        )
    elif user_text == "Условия доставки":
        bot_message = "Мы доставляем во все регионы страны всеми доступными перевозчиками. Возврат товара в течение 14 календарных дней."
    elif user_text == "Контакты":
        bot_message = "Наши контакты: т. +7959123123, наш сайт https://vk.com/guliett_city_sport_lg"
    elif user_text == "Способ оплаты":
        bot_message = 'Оплата производится при полной предоплате на номер карты "123345892489" или по номеру телефона в кнопке "Контакты".'
    else:
        bot_message = "Такой функции еще нет."

    await update.message.reply_text(bot_message)

NAME, PHONE, ADRESS, EMAIL, AGE, GENDER, CITY, DESCRIPTION = range(8)

async def user_data(update, context):
    context.user_data["user_name"] = ""
    context.user_data["user_phone"] = ""
    context.user_data["user_adress"] = ""
    context.user_data["user_email"] = ""
    context.user_data["user_age"] = ""
    context.user_data["user_gender"]= ""
    context.user_data["user_city"] = ""
    await update.message.reply_text("Введи свое имя")
    return NAME


async def name(update, context):
    context.user_data["user_name"] = update.message.text
    await update.message.reply_text("Введи свой номер телефона")
    return PHONE


async def phone(update, context):
    context.user_data["user_phone"] = update.message.text
    await update.message.reply_text("Введи свой адрес")
    return ADRESS

async def adress(update, context):
    context.user_data["user_adress"] = update.message.text
    await update.message.reply_text("Введи свою электронную почту")
    return EMAIL

async def email(update, context):
    context.user_data["user_email"] = update.message.text
    await update.message.reply_text("Сколько тебе лет?")
    return AGE

async def age(update, context):
    context.user_data["user_age"] = update.message.text
    await update.message.reply_text("Какой у тебя пол?")
    return GENDER

async def gender(update, context):
    context.user_data["user_gender"] = update.message.text
    await update.message.reply_text("В каком городе ты живешь?")
    return CITY

async def city(update, context):
    context.user_data["user_city"] = update.message.text
    await update.message.reply_text(
        f'Вот собранная информация:{context.user_data["user_name"]} {context.user_data["user_phone"]} {context.user_data["user_adress"]}{context.user_data["user_email"]}{context.user_data["user_age"]}{context.user_data["user_gender"]}{ context.user_data["user_city"]}'
    )
    return ConversationHandler.END


async def cancel(update, context):
    """Cancels and ends the conversation."""
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("user_data", user_data)],
    states={
        NAME: [MessageHandler(filters.TEXT, name)],
        PHONE: [MessageHandler(filters.TEXT, phone)],
        ADRESS: [MessageHandler(filters.TEXT, adress)],
        EMAIL: [MessageHandler(filters.TEXT, email)],
        AGE: [MessageHandler(filters.TEXT, age)],
        GENDER: [MessageHandler(filters.TEXT, gender)],
        CITY: [MessageHandler(filters.TEXT, city)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)




app = (
    ApplicationBuilder()
    .token("8194772213:AAEzbdm1wjIhW5uaR8P9NLb1cc3Gq__5gkU")
    .build()  # Убедитесь, что вы ввели правильный токен
)

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Regex(r"^\d+$"), receive_quantity))
app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_button))
app.add_handler(CallbackQueryHandler(button))

app.add_handler(
    CallbackQueryHandler(products_query, pattern="^(prod_1|prod_2|prod_3)$")
)

# Запуск бота
print("Бот запущен!")
app.run_polling()
