from telegram.ext import (
    
    CommandHandler,
    MessageHandler,
  
    
    ConversationHandler,
)
from telegram.ext import Updater, filters, CallbackContext
from keyboards import text_button
(
    NAME,
    PHONE,
    ADRESS,
    EMAIL,
    AGE,
    GENDER,
    CITY,
) = range(7)


async def user_data(update, context):
    context.user_data["user_name"] = ""
    context.user_data["user_phone"] = ""
    context.user_data["user_adress"] = ""
    context.user_data["user_email"] = ""
    context.user_data["user_age"] = ""
    context.user_data["user_gender"] = ""
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
        f'Вот собранная информация:{context.user_data["user_name"]} {context.user_data["user_phone"]} {context.user_data["user_adress"]} {context.user_data["user_email"]} {context.user_data["user_age"]} {context.user_data["user_gender"]} { context.user_data["user_city"]}'
    )
    return ConversationHandler.END


async def cancel(update, context):
    """Cancels and ends the conversation."""
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("^Сбор данных о пользователе$"), text_button)
    ],
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
