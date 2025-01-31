from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)

from telegram.ext import Updater, filters, CallbackContext
from data_collection import conv_handler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup



from keyboards import (
    product_kb,
    start,
    start_button,
    button,
    receive_quantity,
    text_button,
    
)




app = (
    ApplicationBuilder()
    .token("8194772213:AAEzbdm1wjIhW5uaR8P9NLb1cc3Gq__5gkU")
    .build()  # Убедитесь, что вы ввели правильный токен
)


app.add_handler(conv_handler)
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Regex(r"^\d+$"), receive_quantity))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_button))
app.add_handler(CallbackQueryHandler(button))



# Запуск бота
print("Бот запущен!")
app.run_polling()
