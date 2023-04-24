import datetime
import sys
from pprint import pprint
from time import sleep

import ccxt
import telebot
from crypto_pay_api_sdk import cryptopay
from django.core.management.base import BaseCommand
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from Bot.management.commands.config import token, width, bot_name, vip_cost, cashback, \
    admin_name, token_pay
from Bot.models import Users

Crypto = cryptopay.Crypto(token_pay)

bot = telebot.TeleBot(token)

bot.delete_webhook()
# admin_chat_id = 6291876932


def add_balance(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    language = Users.objects.get(user_id=user_id).language
    try:
        # user_name = message.from_user.username
        link = int(message.text)
        if link > 100:
            link = 100
        if link < 1:
            link = 1
        Users.objects.filter(user_id=user_id).update(
            percent_balance=int(link)
        )
        msg = f''

        if language == 'ru':
            msg = f'Процент от баланса успешно изменено'
        elif language == 'en':
            msg = f'Percentage of balance successfully changed'

        bot.send_message(chat_id, msg, parse_mode='html')
    except:
        msg = ''
        if language == 'ru':
            msg = f'Что-то пошло не так! Попробуйте позже или проверьте правильность ввода!'
        elif language == 'en':
            msg = f'Something went wrong! Try again later or make sure you entered it correctly!'

        bot.send_message(chat_id, msg, parse_mode='html')


def add_leverage(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    language = Users.objects.get(user_id=user_id).language
    try:
        # user_name = message.from_user.username
        link = str(message.text)
        Users.objects.filter(user_id=user_id).update(
            leverage=int(link)
        )
        msg = f'Кредитное плече успешно изменено'

        if language == 'ru':
            msg = f'Кредитное плече успешно изменено'
        elif language == 'en':
            msg = f'Leverage has been successfully changed'

        bot.send_message(chat_id, msg, parse_mode='html')
    except:
        msg = ''
        if language == 'ru':
            msg = f'Что-то пошло не так! Попробуйте позже или проверьте правильность ввода!'
        elif language == 'en':
            msg = f'Something went wrong! Try again later or make sure you entered it correctly!'

        bot.send_message(chat_id, msg, parse_mode='html')


def add_binance_api(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    language = Users.objects.get(user_id=user_id).language
    try:
        # user_name = message.from_user.username
        link = str(message.text).split(',')
        api_key = str(link[0]).replace(' ', '')
        api_secret = str(link[1]).replace(' ', '')
        session = ccxt.binance(
            {
                "apiKey": api_key,
                "secret": api_secret,
            }
        )
        # result = ''

        try:
            session.fetch_balance()
            result = 'success'
            Users.objects.filter(user_id=user_id).update(
                api_key=api_key,
                api_secret=api_secret,
                exchange='Binance'
            )
        except:
            result = 'error'

        messages = {
            'ru': {
                'success': 'Биржа успешно подключена',
                'error': 'Что-то пошло не так проверьте свои апи и попробуйте снова'
            },
            'en': {
                'success': 'Exchange successfully connected',
                'error': 'Something went wrong check your api and try again'
            }
        }

        msg = messages[language][result]
        bot.send_message(chat_id, msg, parse_mode='html', reply_markup=gen_markup())
    except:
        msg = ''
        if language == 'ru':
            msg = f'Что-то пошло не так! Попробуйте позже или проверьте правильность ввода!'
        elif language == 'en':
            msg = f'Something went wrong! Try again later or make sure you entered it correctly!'

        bot.send_message(chat_id, msg, parse_mode='html')


def add_bybit_api(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    user = Users.objects.get(user_id=user_id)
    language = user.language
    try:
        link = message.text.strip().split(',')
        api_key = str(link[0]).replace(' ', '')
        api_secret = str(link[1]).replace(' ', '')

        session = ccxt.bybit({
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,
            'timeout': 30000,
        })

        try:
            session.fetch_balance()
            msg = ''
            if language == 'ru':
                msg = 'Биржа успешно подключена'
            elif language == 'en':
                msg = 'Exchange successfully connected'
            user.api_key = api_key
            user.api_secret = api_secret
            user.exchange = 'Bybit'
            user.save()
        except:
            msg = ''
            if language == 'ru':
                msg = 'Что-то пошло не так проверьте свои апи и попробуйте снова'
            elif language == 'en':
                msg = 'Something went wrong check your api and try again'

        bot.send_message(chat_id, msg, parse_mode='html', reply_markup=gen_markup())
    except:
        msg = ''
        if language == 'ru':
            msg = f'Что-то пошло не так! Попробуйте позже или проверьте правильность ввода!'
        elif language == 'en':
            msg = f'Something went wrong! Try again later or make sure you entered it correctly!'

        bot.send_message(chat_id, msg, parse_mode='html')


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = width
    markup.add(InlineKeyboardButton("⚙️Trade Settings", callback_data="Settings"),
               InlineKeyboardButton("💰Subscription", callback_data="Subscription"),
               InlineKeyboardButton("🇬🇧Language", callback_data="Language"),
               InlineKeyboardButton("👥Referral URL", callback_data="Referral"),
               )

    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'Settings':
        user = Users.objects.get(user_id=call.message.chat.id)
        language = user.language
        exchange = user.exchange
        leverage = user.leverage
        balance = user.percent_balance

        msg = ''
        if language == 'ru':
            if exchange == 'Not_connect':
                msg = f'Выберите настройку для изменения:\n\n' \
                      f'Биржа: Не подключена!!!\n' \
                      f'Кредитное плече: {leverage}\n' \
                      f'Процент от баланса: {balance}'
            else:
                msg = f'Выберите настройку для изменения:\n\n' \
                      f'Биржа: {exchange}\n' \
                      f'Кредитное плече: {leverage}\n' \
                      f'Процент от баланса: {balance}'
        elif language == 'en':
            if exchange == 'Not_connect':
                msg = f'Select a setting to change:\n\n' \
                      f'Exchange: Not connected!!!\n' \
                      f'Leverage: {leverage}\n' \
                      f'Percentage of balance: {balance}'
            else:
                msg = f'Select a setting to change:\n\n' \
                      f'Exchange: {exchange}\n' \
                      f'Leverage: {leverage}\n' \
                      f'Percentage of balance: {balance}'

        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.row_width = 3
        reply_markup.add(
            types.InlineKeyboardButton("🏦Exchange", callback_data='Exchange'),
            types.InlineKeyboardButton("🔢Leverage", callback_data='Leverage'),
            types.InlineKeyboardButton("💳Balance", callback_data='Balance'),
            types.InlineKeyboardButton("🔙Back", callback_data='Back')
        )

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=reply_markup, parse_mode='html')
    if call.data == 'Subscription':
        user = Users.objects.get(user_id=call.message.chat.id)
        language = user.language
        msg = ''
        if language == 'ru':
            if user.subs_active:
                msg = f'Ваша подписка активна до {user.subs_date_end}:'
            else:
                msg = f'Ваша подписка не активна!! Обновите её скорее!!:'

        elif language == 'en':
            if user.subs_active:
                msg = f'Your is active until {user.subs_date_end}:'
            else:
                msg = f'Your subscription  is not active!!! Update it soon!!!:'

        reply_markup = types.InlineKeyboardMarkup(row_width=1)
        reply_markup.add(
            types.InlineKeyboardButton("🥇Buy Subscription", callback_data='VIP'),
            types.InlineKeyboardButton("🔙Back", callback_data='Back')
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=reply_markup, parse_mode='html')
    if call.data == 'Language':
        language = Users.objects.get(user_id=call.message.chat.id).language
        msg = ''
        if language == 'ru':
            msg = f'Выберите язык приложения:'
        elif language == 'en':
            msg = f'Select the application language:'

        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.row_width = width
        reply_markup.add(
            types.InlineKeyboardButton("EN", callback_data='EN'),
            types.InlineKeyboardButton("RU", callback_data='RU'),
            types.InlineKeyboardButton("🔙Back", callback_data='Back')
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=reply_markup, parse_mode='html')
    # создание и обработка рефералов
    if call.data == 'Referral':
        user = Users.objects.get(user_id=call.message.chat.id)
        language = user.language
        balance = user.balance
        msg = ''
        count_ref = len(Users.objects.filter(referral=user))

        link = f'https://t.me/{bot_name}?start={call.message.chat.id}'
        if language == 'ru':
            msg = f'У вас {count_ref} рефералов\n\n' \
                  f'Ваша реферальная ссылка {link}\n\n' \
                  f'За каждого активного реферала вы получаете {cashback} USD кэшбек от оплаты подписки!\n' \
                  f'Ваш баланс: {balance} USDT\n' \
                  f'Чтобы получить выплату напишите администратору @{admin_name}\n' \
                  f'Минимальная сумма выплаты от 10 долларов!'

        elif language == 'en':
            msg = f'You have {count_ref} referrals\n\n' \
                  f'Your referral link {link}\n\n' \
                  f'For each active referral you get {cashback} USD cashback on subscription fees!\n' \
                  f'Your Balance: {balance} USDT\n' \
                  f'To receive a payout write the administrator @{admin_name}\n' \
                  f'Minimum amount of payments from 10 dollars!'

        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.row_width = width
        reply_markup.add(
            types.InlineKeyboardButton("🔙Back", callback_data='Back')
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=reply_markup, parse_mode='html')

    # second call part
    # Меняем язык
    if call.data == 'EN':
        Users.objects.filter(user_id=call.message.chat.id).update(language='en')
        user = Users.objects.get(user_id=call.message.chat.id)
        msg = f'{user.language.capitalize()} language has been successfully changed:'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=gen_markup(), parse_mode='html')

    if call.data == 'RU':
        user_id = call.message.chat.id
        Users.objects.filter(user_id=user_id).update(language='ru')
        language = 'ru'  # язык уже обновлен в базе данных, можно сразу присвоить его переменной
        msg = f'Язык успешно изменен:' if language == 'ru' else f'The language has been successfully changed:'
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=msg,
                              reply_markup=gen_markup(), parse_mode='html')

    # настройки подписки выбор тарифа и строка
    if call.data == 'VIP':
        language = Users.objects.get(user_id=call.message.chat.id).language
        msg = ''
        if language == 'ru':
            msg = f'Стоимость подписки в месяц {vip_cost} USDT\n\n'
        elif language == 'en':
            msg = f'The cost of the subscription per month is {vip_cost} USDT\n\n'

        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.row_width = 3
        reply_markup.add(
            types.InlineKeyboardButton("📅1 month", callback_data='1vip'),
            types.InlineKeyboardButton("📅3 month", callback_data='3vip'),
            types.InlineKeyboardButton("📅6 month", callback_data='7vip'),
            types.InlineKeyboardButton("🔙Back", callback_data='Back')
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=reply_markup, parse_mode='html')
    # оплата подписок
    # оплата подписок вип
    if call.data == '1vip':
        language = Users.objects.get(user_id=call.message.chat.id).language
        subs_cost = vip_cost  # (vip_cost - (subs_discount * vip_cost / 100)) * 1
        msg = ''
        if language == 'ru':
            msg = f'К оплате {subs_cost} USDT:\n'
        elif language == 'en':
            msg = f'Price {subs_cost} USDT:\n'

        invoice = Crypto.createInvoice("USDT", f'{subs_cost}', params={"description": "1vip",
                                                                       "expires_in": 300,
                                                                       })
        invoice_id = invoice['result']['invoice_id']

        inline_keyboard = [
            [
                types.InlineKeyboardButton("Check Pay", callback_data=invoice_id),
                types.InlineKeyboardButton("Pay", url=invoice['result']['pay_url']),
                types.InlineKeyboardButton("Back", callback_data='Back')
            ]
        ]

        reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
        reply_markup.row_width = width

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=reply_markup, parse_mode='html')
    if call.data == '3vip':
        language = Users.objects.get(user_id=call.message.chat.id).language
        subs_cost = 70  # (vip_cost - (subs_discount * vip_cost / 100)) * 3
        msg = ''
        if language == 'ru':
            msg = f'К оплате {subs_cost} USDT:\n'
        elif language == 'en':
            msg = f'Price {subs_cost} USDT:\n'

        invoice = Crypto.createInvoice("USDT", f'{subs_cost}', params={"description": "3vip",
                                                                       "expires_in": 300,
                                                                       })
        invoice_id = invoice['result']['invoice_id']

        inline_keyboard = [
            [
                types.InlineKeyboardButton("Check Pay", callback_data=invoice_id),
                types.InlineKeyboardButton("Pay", url=invoice['result']['pay_url']),
                types.InlineKeyboardButton("Back", callback_data='Back')

            ]
        ]

        reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
        reply_markup.row_width = width

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=reply_markup, parse_mode='html')
    if call.data == '7vip':
        language = Users.objects.get(user_id=call.message.chat.id).language
        subs_cost = 125  # (vip_cost - (subs_discount * vip_cost / 100)) * 7
        msg = ''
        if language == 'ru':
            msg = f'К оплате {subs_cost} USDT:\n'
        elif language == 'en':
            msg = f'Price {subs_cost} USDT:\n'

        invoice = Crypto.createInvoice("USDT", f'{subs_cost}', params={"description": "7vip",
                                                                       "expires_in": 300,
                                                                       })
        invoice_id = invoice['result']['invoice_id']

        inline_keyboard = [
            [
                types.InlineKeyboardButton("Check Pay", callback_data=invoice_id),
                types.InlineKeyboardButton("Pay", url=invoice['result']['pay_url']),
                types.InlineKeyboardButton("Back", callback_data='Back')

            ]
        ]

        reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
        reply_markup.row_width = width

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=reply_markup, parse_mode='html')
    if call.data == 'Exchange':
        language = Users.objects.get(user_id=call.message.chat.id).language
        msg = ''
        if language == 'ru':
            msg = f'Выберите биржу для подключения:'
        elif language == 'en':
            msg = f'Choose an exchange to connect to:'

        inline_keyboard = [
            [
                types.InlineKeyboardButton("Binance", callback_data='Binance'),
                # types.InlineKeyboardButton("Bybit", callback_data='Bybit'),
                types.InlineKeyboardButton("Back", callback_data='Back')

            ]
        ]

        reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
        reply_markup.row_width = width

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=reply_markup, parse_mode='html')
        # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # Добавляем апи ключи от биржи Bybit
    if call.data == 'Bybit':
        language = Users.objects.get(user_id=call.message.chat.id).language
        msg = ''
        if language == 'ru':
            msg = f'Пришлите мне ваши апи ключ и секретный ключ через кому api_key, api_secret:'
        elif language == 'en':
            msg = f'Send me your api key and secret key via coma api_key, api_secret:'

        mesag = bot.send_message(chat_id=call.message.chat.id, text=msg)

        bot.register_next_step_handler(mesag, add_bybit_api)
    # Добавляем апи ключи от биржи Binance
    if call.data == 'Binance':
        language = Users.objects.get(user_id=call.message.chat.id).language
        msg = ''
        if language == 'ru':
            msg = f'Пришлите мне ваши апи ключ и секретный ключ через кому api_key, api_secret:'
        elif language == 'en':
            msg = f'Send me your api key and secret key via coma api_key, api_secret:'

        mesag = bot.send_message(chat_id=call.message.chat.id, text=msg)

        bot.register_next_step_handler(mesag, add_binance_api)
    # Меняем плече в каждой сделке
    if call.data == 'Leverage':
        language = Users.objects.get(user_id=call.message.chat.id).language
        msg = ''
        if language == 'ru':
            msg = f'Пришлите значение кредитного плеча:'
        elif language == 'en':
            msg = f'Send the value of leverage:'

        mesag = bot.send_message(chat_id=call.message.chat.id, text=msg)

        bot.register_next_step_handler(mesag, add_leverage)
    # Меняем баланс для каждой сделки
    if call.data == 'Balance':
        language = Users.objects.get(user_id=call.message.chat.id).language
        msg = ''
        if language == 'ru':
            msg = f'Пришлите мне процент от баланса который вы хотите использовать для сделки число от 1 до 100:'
        elif language == 'en':
            msg = f'Send me a percentage of the balance you want to use for the transaction number from 1 to 100:'

        mesag = bot.send_message(chat_id=call.message.chat.id, text=msg)

        bot.register_next_step_handler(mesag, add_balance)
    # Кнопка назад
    if call.data == 'Back':
        language = Users.objects.get(user_id=call.message.chat.id).language
        msg = ''
        if language == 'ru':
            msg = f'Меню:'
        elif language == 'en':
            msg = f'Menu:'

        # mesag = bot.send_message(chat_id=call.message.chat.id, text=msg)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=gen_markup())
    # проверка оплаты
    else:
        try:
            invo_id = int(call.data)
            message_id = call.message.message_id
            # print(message_id)
            for in_id in Crypto.getInvoices()['result']['items']:
                if int(in_id['invoice_id']) == invo_id and in_id['status'] == 'paid':
                    # вип оплата
                    if in_id['description'] == '1vip':
                        user = Users.objects.get(user_id=call.message.chat.id)
                        if user.subs_active:
                            try:
                                ref = Users.objects.get(user_id=user.reffrel.id)
                                ref_cashback = cashback
                                bal = ref.balance
                                Users.objects.filter(user_id=user.reffrel.id).update(
                                    balance=bal + ref_cashback
                                )
                            except Users.DoesNotExist:
                                print('User dont have referral')
                            # Получаем сегодняшнюю дату
                            today = user.subs_date_end

                            # Добавляем 30 дней
                            delta = datetime.timedelta(days=30)
                            future_date = today + delta

                            language = user.language
                            Users.objects.filter(user_id=call.message.chat.id).update(
                                subs_date_end=future_date,
                                subs_active=True,
                                subscription_type='VIP'
                            )
                        else:
                            try:
                                ref = Users.objects.get(user_id=user.reffrel.id)
                                ref_cashback = cashback
                                bal = ref.balance
                                Users.objects.filter(user_id=user.reffrel.id).update(
                                    balance=bal + ref_cashback
                                )
                            except Users.DoesNotExist:
                                print('User dont have referral')
                            # Получаем сегодняшнюю дату
                            today = datetime.date.today()

                            # Добавляем 30 дней
                            delta = datetime.timedelta(days=30)
                            future_date = today + delta

                            language = user.language
                            Users.objects.filter(user_id=call.message.chat.id).update(
                                subs_date_end=future_date,
                                subs_active=True,
                                subscription_type='VIP'
                            )
                        msg = ''
                        if language == 'ru':
                            msg = f'Поздравляем ваша подписка успешно оплачена\n'

                        elif language == 'en':
                            msg = f'Congratulations, your subscription has been successfully paid.\n'

                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text=msg,
                                              reply_markup=gen_markup())
                    if in_id['description'] == '3vip':
                        user = Users.objects.get(user_id=call.message.chat.id)
                        if user.subs_active:
                            # Получаем сегодняшнюю дату
                            today = user.subs_date_end
                        else:
                            # Получаем сегодняшнюю дату
                            today = datetime.date.today()
                        try:
                            ref = Users.objects.get(user_id=user.reffrel.id)
                            ref_cashback = cashback
                            bal = ref.balance
                            Users.objects.filter(user_id=user.reffrel.id).update(
                                balance=bal + ref_cashback
                            )
                        except Users.DoesNotExist:
                            print('User dont have referral')
                        # Добавляем 30 дней
                        delta = datetime.timedelta(days=90)
                        future_date = today + delta

                        language = user.language
                        Users.objects.filter(user_id=call.message.chat.id).update(
                            subs_date_end=future_date,
                            subs_active=True,
                            subscription_type='VIP'
                        )

                        msg = ''
                        if language == 'ru':
                            msg = f'Поздравляем ваша подписка успешно оплачена\n'

                        elif language == 'en':
                            msg = f'Congratulations, your subscription has been successfully paid.\n'

                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text=msg,
                                              reply_markup=gen_markup())
                    if in_id['description'] == '7vip':
                        user = Users.objects.get(user_id=call.message.chat.id)
                        if user.subs_active:
                            # Получаем сегодняшнюю дату
                            today = user.subs_date_end
                        else:
                            # Получаем сегодняшнюю дату
                            today = datetime.date.today()
                        try:
                            ref = Users.objects.get(user_id=user.reffrel.id)
                            ref_cashback = cashback
                            bal = ref.balance
                            Users.objects.filter(user_id=user.reffrel.id).update(
                                balance=bal + ref_cashback
                            )
                        except Users.DoesNotExist:
                            print('User dont have referral')
                        # Добавляем 30 дней
                        delta = datetime.timedelta(days=180)
                        future_date = today + delta

                        language = user.language
                        Users.objects.filter(user_id=call.message.chat.id).update(
                            subs_date_end=future_date,
                            subs_active=True,
                            subscription_type='VIP'
                        )

                        msg = ''
                        if language == 'ru':
                            msg = f'Поздравляем ваша подписка успешно оплачена\n'

                        elif language == 'en':
                            msg = f'Congratulations, your subscription has been successfully paid.\n'

                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text=msg,
                                              reply_markup=gen_markup())
        except ValueError as e:
            pprint(e)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_name = message.from_user.username
    # en = ''
    # ru = ''

    referral = str(message.text).replace('/start', '')

    try:
        Users.objects.get(
            user_name=user_name,
            user_id=user_id,
        )
        msg_2 = f'Hello {user_name}'
    except Users.DoesNotExist:
        if len(referral) > 1 and referral != user_id:
            ref = Users.objects.get(user_id=int(referral))
            user = Users(
                user_name=user_name,
                user_id=user_id,
                referral=ref
            )
        else:
            user = Users(
                user_name=user_name,
                user_id=user_id,
            )
        user.save()
        msg_2 = f'Hello {user_name}\n\n'

    bot.send_message(chat_id, msg_2, reply_markup=gen_markup(), parse_mode='html', disable_web_page_preview=True)


class Command(BaseCommand):
    help = 'бот'

    def handle(self, *args, **options):
        while True:
            try:
                sleep(1)
                bot.infinity_polling()
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(f'{e} line = {str(exc_tb.tb_lineno)}')
