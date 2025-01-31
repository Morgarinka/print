from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from bd_3 import Product


async def get_products(sesion: AsyncSession):
    result = await sesion.execute(select(Product))
    return result.scalar().all()  # Получаем все продукты


async def button(updete, context):
    query = updete.callback_query
    await query.answer()

    # Получение ссусии для работы с ДБ
    async with AsyncSession() as session:
        product = await get_products(session)

    if query.data == "start":
        await query.edit_message_text(
            text=f"Здравствуйте, {query.from_user.last_name} {query.from_user.first_name}! Вы находитесь в главном меню. Выберите действие:",
            reply_markup=query.message.reply_markup,
        )
    elif query.data == "buy":
        context.user_data["operation"] = "buy"
        await query.edit_message_text(
            text="Вы выбрали 'Купить'.",
            reply_markup=product_kb(
                products
            ),  # Обновите клавиатуру с новыми продуктами
        )
    elif query.data.startswith("prod"):
        product_id = query.data
        context.user_data["product_id"] = product_id

    # Находим продукт в базе
    for product in products:
        if product.id == product_id:
            name = product.name
            price = product.price
            img = product.img
            caption = product.caption
        chat_id = updete.effective_chat.id
        img_path = r"C:\Users\1\Desktop\Progammirov\print\Img\\" + img
        # Отправка фото с товаром
        with open(img_path, "rb") as photo:
            await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"Вы выбрали {name} за {price} руб. Укажите количество:",
            )


async def receive_quantity(update, context):
    user_input = update.message.text
    if user_input.isdigit():
        product_name = context.user_data.get("product_name")
        product_price = context.user_data.get("product_price")
        quantity = int(user_input)
        total_price = quantity * int(product_price)

        # Создаем клавиатуку для подтверждения
        keyboard = [
            [InlineKeyboardButton("Подтвердить", callback_data="confirm")],
            [InlineKeyboardButton("Отменить", callback_data="cancel")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"Вы собираетесь продать {quantity} {product_name}(ов) на сумму {total_price} руб.",
            reply_markup=reply_markup,
        )
    else:
        await update.message.reply_text("Пожалуйста, введите корректное количество.")
