from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from products_1 import products


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


async def start_button(update, context):
    my_kb_2 = ReplyKeyboardMarkup(
        [
            ["Время работы", "Информация о компании"],
            ["Условия доставки", "Контакты"],
            ["Способ оплаты"],
            ["Сбор данных от пользователя"],
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
    elif user_text == "Сбор данных о пользователе":
        await update.message.reply_text(
            "Начнем собирать данные о тебе. Напиши свое имя."
        )
        
    else:
        bot_message = "Такой функции еще нет."

    await update.message.reply_text(bot_message)



