import datetime
import sys
from pprint import pprint
from time import sleep

import ccxt
import telebot
from django.core.management.base import BaseCommand
from telebot import types
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Bot.management.commands.config import token, width, bot_name, vip_cost, pay_adres, network, cashback, \
    pay_adres_1, network_1
from Bot.models import Users


bot = telebot.TeleBot(token)

bot.delete_webhook()
admin_chat_id = 6291876932


def add_balance(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    language = Users.objects.get(user_id=user_id).language
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


def add_leverage(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    language = Users.objects.get(user_id=user_id).language
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


def add_binance_api(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    language = Users.objects.get(user_id=user_id).language
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
    msg = ''

    try:
        session.fetch_balance()
        if language == 'ru':
            msg = f'Биржа успешно подключена'
        elif language == 'en':
            msg = f'Exchange successfully connected'
        Users.objects.filter(user_id=user_id).update(
            api_key=api_key,
            api_secret=api_secret,
            exchange='Binance'
        )
    except:
        if language == 'ru':
            msg = f'Что-то пошло не так проверьте свои апи и попробуйте снова'
        elif language == 'en':
            msg = f'Something went wrong check your api and try again'

    bot.send_message(chat_id, msg, parse_mode='html', reply_markup=gen_markup())


def add_bybit_api(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    language = Users.objects.get(user_id=user_id).language
    # user_name = message.from_user.username
    link = str(message.text).split(',')
    api_key = str(link[0]).replace(' ', '')
    api_secret = str(link[1]).replace(' ', '')
    session = ccxt.bybit(
        {
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,
            'timeout': 30000,
        }
    )
    msg = ''

    try:
        session.fetch_balance()
        if language == 'ru':
            msg = f'Биржа успешно подключена'
        elif language == 'en':
            msg = f'Exchange successfully connected'
        Users.objects.filter(user_id=user_id).update(
            api_key=api_key,
            api_secret=api_secret,
            exchange='Bybit'
        )
    except:
        if language == 'ru':
            msg = f'Что-то пошло не так проверьте свои апи и попробуйте снова'
        elif language == 'en':
            msg = f'Something went wrong check your api and try again'

    bot.send_message(chat_id, msg, parse_mode='html', reply_markup=gen_markup())


# def remove_trader(message):
#     user_id = message.from_user.id
#     chat_id = message.chat.id
#     # user_name = message.from_user.username
#     link = str(message.text)
#     user = Users.objects.get(user_id=user_id)
#     while True:
#         sleep(2)
#         pos_response = requests.post(info_url, headers=pos_headers,
#                                      json={"encryptedUid": link.split('encryptedUid=')[1]},
#                                      timeout=2)
#         if pos_response.ok:
#             break
#
#     data = json.loads(pos_response.content)['data']
#
#     trader = Traders.objects.get(
#         name=data['nickName'],
#         link=link
#     )
#
#     follow = UserFollowing.objects.get(
#         trader_f=trader,
#         user_f=user
#     )
#     follow.delete()
#     Users.objects.filter(user_id=user_id).update(traders_count=user.traders_count - 1)
#     bot.send_message(chat_id=chat_id, text='Trader remove Successful', reply_markup=gen_markup())


# def add_trader(message):
#     user_id = message.from_user.id
#     chat_id = message.chat.id
#     link = str(message.text)
#     user = Users.objects.get(user_id=user_id)
#     subscription_type = user.subscription_type
#     traders_count = user.traders_count
#
#     def get_subscription_info():
#         if subscription_type == 'VIP':
#             return 'VIP', 10, '10', '10'
#         elif subscription_type == 'Standard':
#             return 'Standard', 5, '5', '5'
#         elif subscription_type == 'Basic':
#             return 'Ordinary', 2, '2', '2'
#         else:
#             return 'Free', 0, 'none', '0'
#
#     subscription_name, max_traders_count, count_word, count_digit = get_subscription_info()
#
#     if subscription_type == 'Free':
#         language = user.language
#         if language == 'ru':
#             msg = f'Вам нельзя добавлять трейдеров с Бесплатной подпиской!\n' \
#                   f'Для этого обновите подписку и копируйте торговлю трейдеров'
#         else:
#             msg = f'You are not allowed to add traders with Free Subscription!\n' \
#                   f'To do this, update your subscription and copy traders trades'
#
#         bot.send_message(chat_id=chat_id, text=msg, reply_markup=gen_markup())
#         return
#
#     if traders_count >= max_traders_count:
#         language = user.language
#         if language == 'ru':
#             msg = f'У вас достигнут лимит по копированию трейдеров одновременно ({count_word} штук)!!\n' \
#                   f'Для добавления нового трейдера, удалите одного из существующих'
#         else:
#             msg = f'You have reached the limit on copying traders at the same time ({count_word} {count_digit})!!!\n' \
#                   f'To add a new trader, remove one of the existing ones'
#         bot.send_message(chat_id=chat_id, text=msg, reply_markup=gen_markup())
#         return
#     else:
#         while True:
#             sleep(2)
#             pos_response = requests.post(info_url, headers=pos_headers,
#                                          json={"encryptedUid": link.split('encryptedUid=')[1]},
#                                          timeout=2)
#             if pos_response.ok:
#                 break
#         data = json.loads(pos_response.content)['data']
#
#         try:
#             trader = Traders.objects.get(
#                 name=data['nickName'],
#                 link=link
#             )
#         except Traders.DoesNotExist:
#             trader = Traders(
#                 name=data['nickName'],
#                 link=link
#             )
#             trader.save()
#
#         follow = UserFollowing(
#             trader_f=trader,
#             user_f=user
#         )
#         follow.save()
#
#         Users.objects.filter(user_id=user_id).update(traders_count=traders_count + 1)
#         language = user.language
#         if language == 'ru':
#             msg = f'Трейдер успешно добавлен!\n' \
#                   f'Вы можете добавить еще {traders_count - 1} трейдеров'
#         else:
#             msg = f'Trader successfully added!\n' \
#                   f'You can add more {traders_count - 1} traders'
#         bot.send_message(chat_id=chat_id, text=msg, reply_markup=gen_markup())


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = width
    markup.add(InlineKeyboardButton("⚙️Trade Settings", callback_data="Settings"),
               # InlineKeyboardButton("🙍Traders", callback_data="Traders"),
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
        # api_key = user.api_key
        # api_secret = user.api_secret
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
        # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # if call.data == 'Traders':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'Выберите настройки трейдера:'
    #     elif language == 'en':
    #         msg = f'Select the trader settings:'
    #
    #     reply_markup = types.InlineKeyboardMarkup()
    #     reply_markup.row_width = 3
    #     reply_markup.add(
    #         types.InlineKeyboardButton("👀My Trader", callback_data='View'),
    #         types.InlineKeyboardButton("➕Subscribe", callback_data='Subscribe'),
    #         types.InlineKeyboardButton("➖Unsubscribe", callback_data='Unsubscribe'),
    #         types.InlineKeyboardButton("🔙Back", callback_data='Back')
    #     )
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
    #                           reply_markup=reply_markup, parse_mode='html')
    #     # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    if call.data == 'Subscription':
        language = Users.objects.get(user_id=call.message.chat.id).language
        user = Users.objects.get(user_id=call.message.chat.id)
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

        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.row_width = 1
        reply_markup.add(
            # types.InlineKeyboardButton("🥉Basic", callback_data='Ordinary'),
            types.InlineKeyboardButton("🥇Buy Subscription", callback_data='VIP'),
            # types.InlineKeyboardButton("🥈Standard", callback_data='Standard'),
            types.InlineKeyboardButton("🔙Back", callback_data='Back')
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=reply_markup, parse_mode='html')
        # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
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
        # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # создание и обработка рефералов
    if call.data == 'Referral':
        language = Users.objects.get(user_id=call.message.chat.id).language
        user = Users.objects.get(user_id=call.message.chat.id)
        balance = user.balance
        msg = ''
        count_ref = len(Users.objects.filter(referral=user))

        link = f'https://t.me/{bot_name}?start={call.message.chat.id}'
        if language == 'ru':
            msg = f'У вас {count_ref} рефералов\n\n' \
                  f'Ваша реферальная ссылка {link}\n\n' \
                  f'За каждого активного реферала вы получаете {cashback} USD кэшбек от оплаты подписки!\n' \
                  f'Ваш баланс: {balance} USDT'

        elif language == 'en':
            msg = f'You have {count_ref} referrals\n\n' \
                  f'Your referral link {link}\n\n' \
                  f'For each active referral you get {cashback} USD cashback on subscription fees!\n' \
                  f'Your Balance: {balance} USDT'

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
        language = Users.objects.get(user_id=call.message.chat.id).language
        msg = ''
        if language == 'ru':
            msg = f'Язык успешно изменен:'
        elif language == 'en':
            msg = f'The language has been successfully changed:'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=gen_markup(), parse_mode='html')
        # bot.send_message(call.message.chat.id, msg, reply_markup=gen_markup(), parse_mode='html')
    if call.data == 'RU':
        Users.objects.filter(user_id=call.message.chat.id).update(language='ru')
        language = Users.objects.get(user_id=call.message.chat.id).language
        msg = ''
        if language == 'ru':
            msg = f'Язык успешно изменен:'
        elif language == 'en':
            msg = f'The language has been successfully changed:'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=gen_markup(), parse_mode='html')
        # bot.send_message(call.message.chat.id, msg, reply_markup=gen_markup(), parse_mode='html')
    # настройки подписки выбор тарифа и строка
    if call.data == 'VIP':
        language = Users.objects.get(user_id=call.message.chat.id).language
        # user = Users.objects.get(user_id=call.message.chat.id)
        msg = ''
        if language == 'ru':
            msg = f'Стоимость подписки в месяц {vip_cost} USDT\n\n'
        elif language == 'en':
            msg = f'The cost of the subscription per month is {vip_cost} USDT\n\n'

        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.row_width = 3
        reply_markup.add(
            types.InlineKeyboardButton("📅1 month", callback_data='1vip'),
            # types.InlineKeyboardButton("📅3 month", callback_data='3vip'),
            # types.InlineKeyboardButton("📅7 month", callback_data='7vip'),
            types.InlineKeyboardButton("🔙Back", callback_data='Back')
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=reply_markup, parse_mode='html')
        # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # if call.data == 'Ordinary':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     # user = Users.objects.get(user_id=call.message.chat.id)
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'Стоимость подписки Basic в месяц {ordinary_cost} USDT\n\n' \
    #               f'Её преимущество:\n' \
    #               f'- Возможность следить за 2 трейдерами одновременно\n' \
    #               f'Выберите строк оформления подписки:'
    #     elif language == 'en':
    #         msg = f'The cost of the Basic subscription per month is {ordinary_cost} USDT\n\n' \
    #               f'Its advantage:\n\n' \
    #               f'- Ability to follow 2 traders at a time\n'
    #
    #     reply_markup = types.InlineKeyboardMarkup()
    #     reply_markup.row_width = 3
    #     reply_markup.add(
    #         types.InlineKeyboardButton("📅1 month", callback_data='1ord'),
    #         types.InlineKeyboardButton("📅3 month", callback_data='3ord'),
    #         types.InlineKeyboardButton("📅7 month", callback_data='7ord'),
    #         types.InlineKeyboardButton("🔙Back", callback_data='Back')
    #     )
    #
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
    #                           reply_markup=reply_markup, parse_mode='html')
    #     # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # if call.data == 'Standard':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     # user = Users.objects.get(user_id=call.message.chat.id)
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'Стоимость подписки Standard в месяц {standard_cost} USDT\n\n' \
    #               f'Её преимущество:\n' \
    #               f'- Возможность следить за 5 трейдерами одновременно\n' \
    #               f'- Средняя скорость копирования\n' \
    #               f'Выберите строк оформления подписки:'
    #     elif language == 'en':
    #         msg = f'The cost of the Standard subscription per month is {standard_cost} USDT\n\n' \
    #               f'Its advantage:\n\n' \
    #               f'- Ability to follow 5 traders at a time\n'
    #
    #     reply_markup = types.InlineKeyboardMarkup()
    #     reply_markup.row_width = 3
    #     reply_markup.add(
    #         types.InlineKeyboardButton("📅1 month", callback_data='1st'),
    #         types.InlineKeyboardButton("📅3 month", callback_data='3st'),
    #         types.InlineKeyboardButton("📅7 month", callback_data='7st'),
    #         types.InlineKeyboardButton("🔙Back", callback_data='Back')
    #     )
    #
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
    #                           reply_markup=reply_markup, parse_mode='html')
    #     # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # оплата подписок
    # оплата подписок вип
    if call.data == '1vip':
        language = Users.objects.get(user_id=call.message.chat.id).language
        user = Users.objects.get(user_id=call.message.chat.id)
        # count_ref = len(Users.objects.filter(referral=user, subs_active=True))
        # subs_discount = count_ref * discount
        # if subs_discount > 15:
        #     subs_discount = 15
        subs_cost = vip_cost  # (vip_cost - (subs_discount * vip_cost / 100)) * 1
        msg = ''
        if language == 'ru':
            msg = f'К оплате {subs_cost} USDT or BUSD:\n' \
                  f'Произведите оплату на этот адрес <code>{pay_adres}</code>\n' \
                  f'СЕТЬ: {network}\n' \
                  f'Произведите оплату на этот адрес <code>{pay_adres_1}</code>\n' \
                  f'СЕТЬ: {network_1}\n' \
                  f'После оплаты пришлите скриншот сюда для подтверждения оплаты'
        elif language == 'en':
            msg = f'Price {subs_cost} USDT or BUSD:\n' \
                  f'Pay to this address <code>{pay_adres}</code>\n' \
                  f'Network: {network}\n' \
                  f'Pay to this address <code>{pay_adres_1}</code>\n' \
                  f'Network: {network_1}\n' \
                  f'After payment, send a screenshot here to confirm payment'

        # invoice = Crypto.createInvoice("USDT", f'{subs_cost}', params={"description": "1vip",
        #                                                                "expires_in": 300,
        #                                                                })
        # invoice_id = invoice['result']['invoice_id']

        inline_keyboard = [
            [
                # types.InlineKeyboardButton("Check Pay", callback_data='check'),
                # types.InlineKeyboardButton("Pay", url=invoice['result']['pay_url']),
                types.InlineKeyboardButton("Back", callback_data='Back')

            ]
        ]

        reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
        reply_markup.row_width = width

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
                              reply_markup=reply_markup, parse_mode='html')
        # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # if call.data == '3vip':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     user = Users.objects.get(user_id=call.message.chat.id)
    #     # count_ref = len(Users.objects.filter(referral=user, subs_active=True))
    #     # subs_discount = count_ref * discount
    #     # if subs_discount > 15:
    #     #     subs_discount = 15
    #     subs_cost = vip_cost * 3  # (vip_cost - (subs_discount * vip_cost / 100)) * 3
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'К оплате {subs_cost} USDT:\n' \
    #               f'Произведите оплату на этот адрес <code>{pay_adres}</code>\n' \
    #               f'СЕТЬ: {network}\n' \
    #               f'После оплаты пришлите скриншот сюда для подтверждения оплаты'
    #     elif language == 'en':
    #         msg = f'Price {subs_cost} USDT:\n' \
    #               f'Pay to this address <code>{pay_adres}</code>\n' \
    #               f'Network: {network}\n' \
    #               f'After payment, send a screenshot here to confirm payment'
    #
    #     # invoice = Crypto.createInvoice("USDT", f'{subs_cost}', params={"description": "3vip",
    #     #                                                                "expires_in": 300,
    #     #                                                                })
    #     # invoice_id = invoice['result']['invoice_id']
    #
    #     inline_keyboard = [
    #         [
    #             # types.InlineKeyboardButton("Check Pay", callback_data=invoice_id),
    #             # types.InlineKeyboardButton("Pay", url=invoice['result']['pay_url']),
    #             types.InlineKeyboardButton("Back", callback_data='Back')
    #
    #         ]
    #     ]
    #
    #     reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
    #     reply_markup.row_width = width
    #
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
    #                           reply_markup=reply_markup, parse_mode='html')
    #     # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # if call.data == '7vip':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     user = Users.objects.get(user_id=call.message.chat.id)
    #     # count_ref = len(Users.objects.filter(referral=user, subs_active=True))
    #     # subs_discount = count_ref * discount
    #     # if subs_discount > 15:
    #     #     subs_discount = 15
    #     subs_cost = vip_cost * 7  # (vip_cost - (subs_discount * vip_cost / 100)) * 7
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'К оплате {subs_cost} USDT:\n' \
    #               f'Произведите оплату на этот адрес <code>{pay_adres}</code>\n' \
    #               f'СЕТЬ: {network}\n' \
    #               f'После оплаты пришлите скриншот сюда для подтверждения оплаты'
    #     elif language == 'en':
    #         msg = f'Price {subs_cost} USDT:\n' \
    #               f'Pay to this address <code>{pay_adres}</code>\n' \
    #               f'Network: {network}\n' \
    #               f'After payment, send a screenshot here to confirm payment'
    #
    #     # invoice = Crypto.createInvoice("USDT", f'{subs_cost}', params={"description": "7vip",
    #     #                                                                "expires_in": 300,
    #     #                                                                })
    #     # invoice_id = invoice['result']['invoice_id']
    #
    #     inline_keyboard = [
    #         [
    #             # types.InlineKeyboardButton("Check Pay", callback_data=invoice_id),
    #             # types.InlineKeyboardButton("Pay", url=invoice['result']['pay_url']),
    #             types.InlineKeyboardButton("Back", callback_data='Back')
    #
    #         ]
    #     ]
    #
    #     reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
    #     reply_markup.row_width = width
    #
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
    #                           reply_markup=reply_markup, parse_mode='html')
    #     # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # # оплата подписок Ordinary
    # if call.data == '1ord':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     user = Users.objects.get(user_id=call.message.chat.id)
    #     count_ref = len(Users.objects.filter(referral=user, subs_active=True))
    #     subs_discount = count_ref * discount
    #     if subs_discount > 15:
    #         subs_discount = 15
    #     subs_cost = (ordinary_cost - (subs_discount * ordinary_cost / 100)) * 1
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'К оплате {subs_cost} USDT:'
    #     elif language == 'en':
    #         msg = f'Price {subs_cost} USDT:'
    #
    #     invoice = Crypto.createInvoice("USDT", f'{subs_cost}', params={"description": "1ord",
    #                                                                    "expires_in": 300,
    #                                                                    })
    #     invoice_id = invoice['result']['invoice_id']
    #
    #     inline_keyboard = [
    #         [
    #             types.InlineKeyboardButton("Check Pay", callback_data=invoice_id),
    #             types.InlineKeyboardButton("Pay", url=invoice['result']['pay_url']),
    #             types.InlineKeyboardButton("Back", callback_data='Back')
    #
    #         ]
    #     ]
    #
    #     reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
    #     reply_markup.row_width = width
    #
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
    #                           reply_markup=reply_markup, parse_mode='html')
    #     # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # if call.data == '3ord':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     user = Users.objects.get(user_id=call.message.chat.id)
    #     count_ref = len(Users.objects.filter(referral=user, subs_active=True))
    #     subs_discount = count_ref * discount
    #     if subs_discount > 15:
    #         subs_discount = 15
    #     subs_cost = (ordinary_cost - (subs_discount * ordinary_cost / 100)) * 3
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'К оплате {subs_cost} USDT:'
    #     elif language == 'en':
    #         msg = f'Price {subs_cost} USDT:'
    #
    #     invoice = Crypto.createInvoice("USDT", f'{subs_cost}', params={"description": "3ord",
    #                                                                    "expires_in": 300,
    #                                                                    })
    #     invoice_id = invoice['result']['invoice_id']
    #
    #     inline_keyboard = [
    #         [
    #             types.InlineKeyboardButton("Check Pay", callback_data=invoice_id),
    #             types.InlineKeyboardButton("Pay", url=invoice['result']['pay_url']),
    #             types.InlineKeyboardButton("Back", callback_data='Back')
    #
    #         ]
    #     ]
    #
    #     reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
    #     reply_markup.row_width = width
    #
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
    #                           reply_markup=reply_markup, parse_mode='html')
    #     # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # if call.data == '7ord':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     user = Users.objects.get(user_id=call.message.chat.id)
    #     count_ref = len(Users.objects.filter(referral=user, subs_active=True))
    #     subs_discount = count_ref * discount
    #     if subs_discount > 15:
    #         subs_discount = 15
    #     subs_cost = (ordinary_cost - (subs_discount * ordinary_cost / 100)) * 7
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'К оплате {subs_cost} USDT:'
    #     elif language == 'en':
    #         msg = f'Price {subs_cost} USDT:'
    #
    #     invoice = Crypto.createInvoice("USDT", f'{subs_cost}', params={"description": "7ord",
    #                                                                    "expires_in": 300,
    #                                                                    })
    #     invoice_id = invoice['result']['invoice_id']
    #
    #     inline_keyboard = [
    #         [
    #             types.InlineKeyboardButton("Check Pay", callback_data=invoice_id),
    #             types.InlineKeyboardButton("Pay", url=invoice['result']['pay_url']),
    #             types.InlineKeyboardButton("Back", callback_data='Back')
    #
    #         ]
    #     ]
    #
    #     reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
    #     reply_markup.row_width = width
    #
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
    #                           reply_markup=reply_markup, parse_mode='html')
    #     # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # # оплата подписок Standard
    # if call.data == '1st':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     user = Users.objects.get(user_id=call.message.chat.id)
    #     count_ref = len(Users.objects.filter(referral=user, subs_active=True))
    #     subs_discount = count_ref * discount
    #     if subs_discount > 15:
    #         subs_discount = 15
    #     subs_cost = (standard_cost - (subs_discount * standard_cost / 100)) * 1
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'К оплате {subs_cost} USDT:'
    #     elif language == 'en':
    #         msg = f'Price {subs_cost} USDT:'
    #
    #     invoice = Crypto.createInvoice("USDT", f'{subs_cost}', params={"description": "1st",
    #                                                                    "expires_in": 300,
    #                                                                    })
    #     invoice_id = invoice['result']['invoice_id']
    #
    #     inline_keyboard = [
    #         [
    #             types.InlineKeyboardButton("Check Pay", callback_data=invoice_id),
    #             types.InlineKeyboardButton("Pay", url=invoice['result']['pay_url']),
    #             types.InlineKeyboardButton("Back", callback_data='Back')
    #
    #         ]
    #     ]
    #
    #     reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
    #     reply_markup.row_width = width
    #
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
    #                           reply_markup=reply_markup, parse_mode='html')
    #     # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # if call.data == '3st':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     user = Users.objects.get(user_id=call.message.chat.id)
    #     count_ref = len(Users.objects.filter(referral=user, subs_active=True))
    #     subs_discount = count_ref * discount
    #     if subs_discount > 15:
    #         subs_discount = 15
    #     subs_cost = (standard_cost - (subs_discount * standard_cost / 100)) * 3
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'К оплате {subs_cost} USDT:'
    #     elif language == 'en':
    #         msg = f'Price {subs_cost} USDT:'
    #
    #     invoice = Crypto.createInvoice("USDT", f'{subs_cost}', params={"description": "3st",
    #                                                                    "expires_in": 300,
    #                                                                    })
    #     invoice_id = invoice['result']['invoice_id']
    #
    #     inline_keyboard = [
    #         [
    #             types.InlineKeyboardButton("Check Pay", callback_data=invoice_id),
    #             types.InlineKeyboardButton("Pay", url=invoice['result']['pay_url']),
    #             types.InlineKeyboardButton("Back", callback_data='Back')
    #
    #         ]
    #     ]
    #
    #     reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
    #     reply_markup.row_width = width
    #
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
    #                           reply_markup=reply_markup, parse_mode='html')
    #     # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # if call.data == '7st':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     user = Users.objects.get(user_id=call.message.chat.id)
    #     count_ref = len(Users.objects.filter(referral=user, subs_active=True))
    #     subs_discount = count_ref * discount
    #     if subs_discount > 15:
    #         subs_discount = 15
    #     subs_cost = (standard_cost - (subs_discount * standard_cost / 100)) * 7
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'К оплате {subs_cost} USDT:'
    #     elif language == 'en':
    #         msg = f'Price {subs_cost} USDT:'
    #
    #     invoice = Crypto.createInvoice("USDT", f'{subs_cost}', params={"description": "7st",
    #                                                                    "expires_in": 300,
    #                                                                    })
    #     invoice_id = invoice['result']['invoice_id']
    #
    #     inline_keyboard = [
    #         [
    #             types.InlineKeyboardButton("Check Pay", callback_data=invoice_id),
    #             types.InlineKeyboardButton("Pay", url=invoice['result']['pay_url']),
    #             types.InlineKeyboardButton("Back", callback_data='Back')
    #
    #         ]
    #     ]
    #
    #     reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
    #     reply_markup.row_width = width
    #
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
    #                           reply_markup=reply_markup, parse_mode='html')
    #     # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
    # функции с трейдерами
    # # получаем список трейдеров
    # if call.data == 'View':
    #     trader_list = []
    #     trd_list = []
    #     k = 1
    #
    #     user = Users.objects.get(user_id=call.message.chat.id)
    #     follow = UserFollowing.objects.filter(user_f=user.id)
    #     for trader in follow:
    #         # pprint(
    #         #     trader.trader_f.id
    #         # )
    #         trader_list.append(trader.trader_f.id)
    #     for tra in trader_list:
    #         trd = Traders.objects.get(id=tra)
    #         name = trd.name
    #         link = trd.link
    #
    #         mes_row = f'{k}) {name}, <a href="{link}">View Profile</a>\n\n'
    #         trd_list.append(mes_row)
    #         k += 1
    #
    #     msg = str(''.join(trd_list))
    #     # print(
    #     #     str(''.join(trd_list))
    #     # )
    #     reply_markup = types.InlineKeyboardMarkup()
    #     reply_markup.row_width = 3
    #     reply_markup.add(
    #         types.InlineKeyboardButton("👀View Subscriptions", callback_data='View'),
    #         types.InlineKeyboardButton("➕Subscribe", callback_data='Subscribe'),
    #         types.InlineKeyboardButton("➖Unsubscribe", callback_data='Unsubscribe'),
    #         types.InlineKeyboardButton("🔙Back", callback_data='Back')
    #     )
    #     if len(follow) > 0:
    #         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
    #                               parse_mode='html', disable_web_page_preview=True)
    #         # bot.send_message(chat_id=call.message.chat.id, text=msg, parse_mode='html', disable_web_page_preview=True)
    #         bot.send_message(chat_id=call.message.chat.id, text='Menu:', reply_markup=gen_markup(), parse_mode='html')
    #     else:
    #         language = Users.objects.get(user_id=call.message.chat.id).language
    #         msg = ''
    #         if language == 'ru':
    #             msg = f'Вы еще не копируюете ни одного трейдера!'
    #         elif language == 'en':
    #             msg = f'You havent copied any traders yet!'
    #
    #         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
    #                               text=msg, reply_markup=reply_markup, parse_mode='html')
    # # добавляем трейдера в список
    # if call.data == 'Subscribe':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'Пришлите мне ссылку на профиль трейдера:'
    #     elif language == 'en':
    #         msg = f'Send me name and link trader profile:'
    #     mesag = bot.send_message(chat_id=call.message.chat.id, text=msg)
    #
    #     bot.register_next_step_handler(mesag, add_trader)
    # # удаляем трейдера из списка
    # if call.data == 'Unsubscribe':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'Пришлите мне ссылку на профиль трейдера:'
    #     elif language == 'en':
    #         msg = f'Send me name and link trader profile:'
    #     mesag = bot.send_message(chat_id=call.message.chat.id, text=msg)
    #
    #     bot.register_next_step_handler(mesag, remove_trader)
    # Настройки аккаунта
    # Добавляем апи ключи от биржи
    # if call.data == 'check':
    #     language = Users.objects.get(user_id=call.message.chat.id).language
    #     msg = ''
    #     if language == 'ru':
    #         msg = f'Отправьте скриншот оплаты:'
    #     elif language == 'en':
    #         msg = f'Send a screenshot of the payment:'
    #
    #     # inline_keyboard = [
    #     #     [
    #     #         types.InlineKeyboardButton("Binance", callback_data='Binance'),
    #     #         types.InlineKeyboardButton("Bybit", callback_data='Bybit'),
    #     #         types.InlineKeyboardButton("Back", callback_data='Back')
    #     #
    #     #     ]
    #     # ]
    #     #
    #     # reply_markup = types.InlineKeyboardMarkup(inline_keyboard)
    #     # reply_markup.row_width = width
    #
    #     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg,
    #                           parse_mode='html')
    #     # bot.send_message(call.message.chat.id, msg, reply_markup=reply_markup, parse_mode='html')
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
                types.InlineKeyboardButton("Bybit", callback_data='Bybit'),
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
            print(message_id)
            # for in_id in Crypto.getInvoices()['result']['items']:
            #     if int(in_id['invoice_id']) == invo_id and in_id['status'] == 'paid':
            #         # вип оплата
            #         if in_id['description'] == '1vip':
            #             user = Users.objects.get(user_id=call.message.chat.id)
            #             if user.subs_active:
            #                 # Получаем сегодняшнюю дату
            #                 today = user.subs_date_end
            #
            #                 # Добавляем 30 дней
            #                 delta = datetime.timedelta(days=30)
            #                 future_date = today + delta
            #
            #                 language = Users.objects.get(user_id=call.message.chat.id).language
            #                 Users.objects.filter(user_id=call.message.chat.id).update(
            #                     subs_date_end=future_date,
            #                     subs_active=True,
            #                     subscription_type='VIP'
            #                 )
            #             else:
            #                 # Получаем сегодняшнюю дату
            #                 today = datetime.date.today()
            #
            #                 # Добавляем 30 дней
            #                 delta = datetime.timedelta(days=30)
            #                 future_date = today + delta
            #
            #                 language = Users.objects.get(user_id=call.message.chat.id).language
            #                 Users.objects.filter(user_id=call.message.chat.id).update(
            #                     subs_date_end=future_date,
            #                     subs_active=True,
            #                     subscription_type='VIP'
            #                 )
            #
            #             msg = ''
            #             if language == 'ru':
            #                 msg = f'Поздравляем ваша подписка успешно оплачена\n'
            #
            #             elif language == 'en':
            #                 msg = f'Congratulations, your subscription has been successfully paid.\n'
            #
            #             bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text=msg)
            #         if in_id['description'] == '3vip':
            #             user = Users.objects.get(user_id=call.message.chat.id)
            #             if user.subs_active:
            #                 # Получаем сегодняшнюю дату
            #                 today = user.subs_date_end
            #             else:
            #                 # Получаем сегодняшнюю дату
            #                 today = datetime.date.today()
            #
            #             # Добавляем 30 дней
            #             delta = datetime.timedelta(days=90)
            #             future_date = today + delta
            #
            #             language = Users.objects.get(user_id=call.message.chat.id).language
            #             Users.objects.filter(user_id=call.message.chat.id).update(
            #                 subs_date_end=future_date,
            #                 subs_active=True,
            #                 subscription_type='VIP'
            #             )
            #
            #             msg = ''
            #             if language == 'ru':
            #                 msg = f'Поздравляем ваша подписка успешно оплачена\n'
            #
            #             elif language == 'en':
            #                 msg = f'Congratulations, your subscription has been successfully paid.\n'
            #
            #             bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text=msg)
            #         if in_id['description'] == '7vip':
            #             user = Users.objects.get(user_id=call.message.chat.id)
            #             if user.subs_active:
            #                 # Получаем сегодняшнюю дату
            #                 today = user.subs_date_end
            #             else:
            #                 # Получаем сегодняшнюю дату
            #                 today = datetime.date.today()
            #
            #             # Добавляем 30 дней
            #             delta = datetime.timedelta(days=210)
            #             future_date = today + delta
            #
            #             language = Users.objects.get(user_id=call.message.chat.id).language
            #             Users.objects.filter(user_id=call.message.chat.id).update(
            #                 subs_date_end=future_date,
            #                 subs_active=True,
            #                 subscription_type='VIP'
            #             )
            #
            #             msg = ''
            #             if language == 'ru':
            #                 msg = f'Поздравляем ваша подписка успешно оплачена\n'
            #
            #             elif language == 'en':
            #                 msg = f'Congratulations, your subscription has been successfully paid.\n'
            #
            #             bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text=msg)
            #         # стандарт оплата
            #         if in_id['description'] == '1ord':
            #             user = Users.objects.get(user_id=call.message.chat.id)
            #             if user.subs_active:
            #                 # Получаем сегодняшнюю дату
            #                 today = user.subs_date_end
            #             else:
            #                 # Получаем сегодняшнюю дату
            #                 today = datetime.date.today()
            #
            #             # Добавляем 30 дней
            #             delta = datetime.timedelta(days=30)
            #             future_date = today + delta
            #
            #             language = Users.objects.get(user_id=call.message.chat.id).language
            #             Users.objects.filter(user_id=call.message.chat.id).update(
            #                 subs_date_end=future_date,
            #                 subs_active=True,
            #                 subscription_type='Basic'
            #             )
            #
            #             msg = ''
            #             if language == 'ru':
            #                 msg = f'Поздравляем ваша подписка успешно оплачена\n'
            #
            #             elif language == 'en':
            #                 msg = f'Congratulations, your subscription has been successfully paid.\n'
            #
            #             bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text=msg)
            #         if in_id['description'] == '3ord':
            #             user = Users.objects.get(user_id=call.message.chat.id)
            #             if user.subs_active:
            #                 # Получаем сегодняшнюю дату
            #                 today = user.subs_date_end
            #             else:
            #                 # Получаем сегодняшнюю дату
            #                 today = datetime.date.today()
            #
            #             # Добавляем 30 дней
            #             delta = datetime.timedelta(days=90)
            #             future_date = today + delta
            #
            #             language = Users.objects.get(user_id=call.message.chat.id).language
            #             Users.objects.filter(user_id=call.message.chat.id).update(
            #                 subs_date_end=future_date,
            #                 subs_active=True,
            #                 subscription_type='Basic'
            #             )
            #
            #             msg = ''
            #             if language == 'ru':
            #                 msg = f'Поздравляем ваша подписка успешно оплачена\n'
            #
            #             elif language == 'en':
            #                 msg = f'Congratulations, your subscription has been successfully paid.\n'
            #
            #             bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text=msg)
            #         if in_id['description'] == '7ord':
            #             user = Users.objects.get(user_id=call.message.chat.id)
            #             if user.subs_active:
            #                 # Получаем сегодняшнюю дату
            #                 today = user.subs_date_end
            #             else:
            #                 # Получаем сегодняшнюю дату
            #                 today = datetime.date.today()
            #
            #             # Добавляем 30 дней
            #             delta = datetime.timedelta(days=210)
            #             future_date = today + delta
            #
            #             language = Users.objects.get(user_id=call.message.chat.id).language
            #             Users.objects.filter(user_id=call.message.chat.id).update(
            #                 subs_date_end=future_date,
            #                 subs_active=True,
            #                 subscription_type='Basic'
            #             )
            #
            #             msg = ''
            #             if language == 'ru':
            #                 msg = f'Поздравляем ваша подписка успешно оплачена\n'
            #
            #             elif language == 'en':
            #                 msg = f'Congratulations, your subscription has been successfully paid.\n'
            #
            #             bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text=msg)
            #         # Ordinary оплата
            #         if in_id['description'] == '1st':
            #             user = Users.objects.get(user_id=call.message.chat.id)
            #             if user.subs_active:
            #                 # Получаем сегодняшнюю дату
            #                 today = user.subs_date_end
            #             else:
            #                 # Получаем сегодняшнюю дату
            #                 today = datetime.date.today()
            #
            #             # Добавляем 30 дней
            #             delta = datetime.timedelta(days=30)
            #             future_date = today + delta
            #
            #             language = Users.objects.get(user_id=call.message.chat.id).language
            #             Users.objects.filter(user_id=call.message.chat.id).update(
            #                 subs_date_end=future_date,
            #                 subs_active=True,
            #                 subscription_type='Standard'
            #             )
            #
            #             msg = ''
            #             if language == 'ru':
            #                 msg = f'Поздравляем ваша подписка успешно оплачена\n'
            #
            #             elif language == 'en':
            #                 msg = f'Congratulations, your subscription has been successfully paid.\n'
            #
            #             bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text=msg)
            #         if in_id['description'] == '3st':
            #             user = Users.objects.get(user_id=call.message.chat.id)
            #             if user.subs_active:
            #                 # Получаем сегодняшнюю дату
            #                 today = user.subs_date_end
            #             else:
            #                 # Получаем сегодняшнюю дату
            #                 today = datetime.date.today()
            #
            #             # Добавляем 30 дней
            #             delta = datetime.timedelta(days=90)
            #             future_date = today + delta
            #
            #             language = Users.objects.get(user_id=call.message.chat.id).language
            #             Users.objects.filter(user_id=call.message.chat.id).update(
            #                 subs_date_end=future_date,
            #                 subs_active=True,
            #                 subscription_type='Standard'
            #             )
            #
            #             msg = ''
            #             if language == 'ru':
            #                 msg = f'Поздравляем ваша подписка успешно оплачена\n'
            #
            #             elif language == 'en':
            #                 msg = f'Congratulations, your subscription has been successfully paid.\n'
            #
            #             bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text=msg)
            #         if in_id['description'] == '7st':
            #             user = Users.objects.get(user_id=call.message.chat.id)
            #             if user.subs_active:
            #                 # Получаем сегодняшнюю дату
            #                 today = user.subs_date_end
            #             else:
            #                 # Получаем сегодняшнюю дату
            #                 today = datetime.date.today()
            #
            #             # Добавляем 30 дней
            #             delta = datetime.timedelta(days=210)
            #             future_date = today + delta
            #
            #             language = Users.objects.get(user_id=call.message.chat.id).language
            #             Users.objects.filter(user_id=call.message.chat.id).update(
            #                 subs_date_end=future_date,
            #                 subs_active=True,
            #                 subscription_type='Standard'
            #             )
            #
            #             msg = ''
            #             if language == 'ru':
            #                 msg = f'Поздравляем ваша подписка успешно оплачена\n'
            #
            #             elif language == 'en':
            #                 msg = f'Congratulations, your subscription has been successfully paid.\n'
            #
            #             bot.edit_message_text(chat_id=call.message.chat.id, message_id=message_id, text=msg)
        except ValueError as e:
            pprint(e)


@bot.message_handler(content_types=['photo'])
def handle_photo(message: Message):
    # отправляем фото в чат с администратором
    bot.send_photo(admin_chat_id, message.photo[-1].file_id,
                   caption=f'Paying for a subscription from a user @{message.from_user.username}',
                   reply_markup=create_payment_confirmation_keyboard(message.from_user.id))


def create_payment_confirmation_keyboard(user_id: int) -> InlineKeyboardMarkup:
    # создаем кнопку для подтверждения оплаты с айди пользователя в качестве параметра
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 2
    keyboard.add(InlineKeyboardButton('Confirm payment', callback_data=f'payment_confirmed:{user_id}'),
                 InlineKeyboardButton("not paid", callback_data=f"payment_not_confirmed:{user_id}"),
                 )
    return keyboard


@bot.callback_query_handler(lambda query: query.data.startswith('payment_not_confirmed:'))
def handle_payment_confirmation(query):
    # извлекаем айди пользователя из колбэк данных и отправляем его в чат с администратором
    user_id = int(query.data.split(':')[1])
    bot.send_message(admin_chat_id, f'Subscription not verified for the user id {user_id}')
    bot.send_message(user_id, f'Your subscription is not paid check again')


@bot.callback_query_handler(lambda query: query.data.startswith('payment_confirmed:'))
def handle_payment_confirmation(query):
    # извлекаем айди пользователя из колбэк данных и отправляем его в чат с администратором
    user_id = int(query.data.split(':')[1])
    user = Users.objects.get(user_id=user_id)
    try:
        ref = Users.objects.get(user_id=user.reffrel.id)
        ref_cashback = cashback
        bal = ref.balance
        Users.objects.filter(user_id=user.reffrel.id).update(
            balance=bal + ref_cashback
        )
    except:
        print('User dont have referral')

    if user.subs_active:
        # Получаем сегодняшнюю дату
        today = user.subs_date_end

        # Добавляем 30 дней
        delta = datetime.timedelta(days=30)
        future_date = today + delta

        Users.objects.filter(user_id=user_id).update(
            subs_date_end=future_date,
            subs_active=True,
            subscription_type='VIP'
        )
    else:
        # Получаем сегодняшнюю дату
        today = datetime.date.today()

        # Добавляем 30 дней
        delta = datetime.timedelta(days=30)
        future_date = today + delta

        Users.objects.filter(user_id=user_id).update(
            subs_date_end=future_date,
            subs_active=True,
            subscription_type='VIP'
        )
    bot.send_message(admin_chat_id, f'Subscription verified for the user  {user_id}')
    bot.send_message(user_id, f'Your subscription has been successfully verified')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_name = message.from_user.username
    en = ''
    ru = ''

    referral = str(message.text).replace('/start', '')

    if len(referral) > 1 and referral != user_id:
        try:
            Users.objects.get(
                user_name=user_name,
                user_id=user_id,
            )
            msg_2 = f'Hello {user_name}'
        except:
            ref = Users.objects.get(user_id=int(referral))
            user = Users(
                user_name=user_name,
                user_id=user_id,
                referral=ref
            )
            user.save()
            msg_2 = f'Hello {user_name}\n\n' \
                    # f'I see you are new here, here are instructions on how to use the bot: <a href="{en}">EN</a>, ' \
                    # f'<a href="{ru}">RU</a>'

        bot.send_message(chat_id, msg_2, reply_markup=gen_markup(), parse_mode='html', disable_web_page_preview=True)
    else:
        try:
            Users.objects.get(
                user_name=user_name,
                user_id=user_id,
            )
            msg_2 = f'Hello {user_name}'
        except:
            user = Users(
                user_name=user_name,
                user_id=user_id,
            )
            user.save()
            msg_2 = f'Hello {user_name}\n\n' \
                    # f'I see you are new here, here are instructions on how to use the bot: <a href="{en}">EN</a>, ' \
                    # f'<a href="{ru}">RU</a>'

        bot.send_message(chat_id, msg_2, reply_markup=gen_markup(), parse_mode='html', disable_web_page_preview=True)


class Command(BaseCommand):
    help = 'бот'

    def handle(self, *args, **options):
        while True:
            try:
                sleep(1)
                bot.infinity_polling()
            except Exception as e:
                # # Your Heroku API key
                # api_key_heroku = os.environ.get("api_key_heroku")
                # # The name of your app and dyno
                # app_name = os.environ.get("app_name")
                # heroku_conn = heroku3.from_key(api_key_heroku)
                # app = heroku_conn.app(app_name)
                # app.restart()

                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(f'{e} line = {str(exc_tb.tb_lineno)}')
