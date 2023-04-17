import telebot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# здесь нужно указать токен вашего бота, который можно получить у @BotFather в Telegram
bot = telebot.TeleBot('6084252834:AAGVcipUyC72I1PRsWStjAVXczhejpIZ5Uo')

# здесь нужно указать айди чата с администратором, куда будут отправляться фото
admin_chat_id = 798093480


@bot.message_handler(content_types=['photo'])
def handle_photo(message: Message):
    # отправляем фото в чат с администратором
    bot.send_photo(admin_chat_id, message.photo[-1].file_id,
                   caption=f'Новое фото от пользователя {message.from_user.id}',
                   reply_markup=create_payment_confirmation_keyboard(message.from_user.id))


def create_payment_confirmation_keyboard(user_id: int) -> InlineKeyboardMarkup:
    # создаем кнопку для подтверждения оплаты с айди пользователя в качестве параметра
    button = InlineKeyboardButton('Подтвердить оплату', callback_data=f'payment_confirmed:{user_id}')
    keyboard = InlineKeyboardMarkup().row(button)
    return keyboard


@bot.callback_query_handler(lambda query: query.data.startswith('payment_confirmed:'))
def handle_payment_confirmation(query):
    # извлекаем айди пользователя из колбэк данных и отправляем его в чат с администратором
    user_id = int(query.data.split(':')[1])
    bot.send_message(admin_chat_id, f'Пользователь {user_id} подтвердил оплату')


# запускаем бота
bot.polling()
