import json
import sys
from datetime import datetime, timedelta
from pprint import pprint
from time import sleep

import requests
from binance import Client
from ccxt import bybit
from ccxt.base.decimal_to_precision import DECIMAL_PLACES  # noqa F401
from ccxt.base.decimal_to_precision import NO_PADDING  # noqa F401
from ccxt.base.decimal_to_precision import PAD_WITH_ZERO  # noqa F401
from ccxt.base.decimal_to_precision import ROUND  # noqa F401
from ccxt.base.decimal_to_precision import SIGNIFICANT_DIGITS  # noqa F401
from ccxt.base.decimal_to_precision import TICK_SIZE  # noqa F401
from ccxt.base.decimal_to_precision import TRUNCATE  # noqa F401
from ccxt.base.decimal_to_precision import decimal_to_precision  # noqa F401

from Bot.models import Signal, Users

# from pybit import HTTP

api = '8df03c1906ff35c53203563774fa3b53'
id_url = 'https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getLeaderboardRank'
pos_url = 'https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getOtherPosition'


def debug(e, app_name):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    msg = f'{e} line = {str(exc_tb.tb_lineno)} = date: {datetime.now()}\n\n' \
          f'{app_name}'
    pprint(
        msg
    )
    # import telebot
    #
    # token_1 = '5757732495:AAFtW8efGFeLEBcgPaigTeHTJt2BGZl6aKQ'
    #
    # bots_1 = telebot.TeleBot(token_1)
    #
    # exc_type, exc_obj, exc_tb = sys.exc_info()
    # print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
    # bots_1.send_message(
    #     -1001596828475,
    #     f'{e} line = {str(exc_tb.tb_lineno)} = date: {datetime.now()}\n\n'
    #     f'{app_name}'
    # )


def get_count(number):
    s = str(number)
    if '.' in s:
        return abs(s.find('.') - len(s)) - 1
    else:
        return 0


# def follows_js():
#     follow_list = []
#     traders = Traders.objects.all()  # Retrieves all traders from the Traders model
#     for trader in traders:
#         followers = UserFollowing.objects.filter(trader_f=trader)  # Retrieves all users following the current trader
#         user_list = []
#         for follow in followers:
#             b = {
#                 'id': follow.user_f.id,
#                 'name': follow.user_f.user_name,
#             }
#             user_list.append(b)  # Adds user data to user_list
#         a = {
#             'Trader': trader.name,
#             'followers': user_list
#         }
#         follow_list.append(a)  # Adds trader and user data to follow_list
#     with open('follows.json', 'w') as f:
#         json.dump(follow_list, f)  # Writes follow_list to follows.json


# def pair_list_update():
#     api_url = "https://api.bybit.com"  # The API URL
#     session = HTTP(api_url)  # Activates the session
#
#     sym_list = []  # The list of symbols
#     symbols = session.query_symbol()  # Retrieves all symbols from the API
#     if "ret_msg" in symbols.keys():
#         if symbols["ret_msg"] == "OK":
#             symbols = symbols["result"]
#             for symbol in symbols:
#                 # Filters out symbols with a quote currency other than USDT and those that are not currently trading
#                 if symbol["quote_currency"] == "USDT" and symbol["status"] == "Trading":
#                     sym_list.append(symbol['name'])  # Adds symbol name to sym_list
#     with open('pair_list.json', 'w') as f:
#         json.dump(sym_list, f)  # Writes sym_list to pair_list.json


def check_users():
    # Iterates over all users in the Users model
    for user in Users.objects.filter(subs_active=True):
        date_end = user.subs_date_end  # Retrieves the subscription end date for the user
        now = datetime.now()  # Retrieves the current date and time
        try:
            a = datetime.strptime(date_end.strftime("%Y-%m-%d"), "%Y-%m-%d") - now  # Calculates the difference
            # between the subscription end date and the current date
        except AttributeError:
            date_end = '2022-02-24'  # Sets a default subscription end date if the user's subscription end date is
            # not set
            a = datetime.strptime(date_end, "%Y-%m-%d") - now  # Calculates the difference between the default
            # subscription end date and the current date
        if a.days >= 1:
            # Does nothing if the difference between the subscription end date and the current date is greater than
            # or equal to one day
            pass
        else:
            # Updates the subs_active field of the user to False if the difference between the subscription end date
            # and the current date is less than one day
            Users.objects.filter(user_name=user.user_name).update(subs_active=False)


def get_orders(name_trader, symbol, date, size, mark_price, pnl, roe):
    """Делает запрос в базу и проверяет есть ли пользователь в базе"""
    try:
        order = Signal.objects.get(  # name_trader=name_trader,
            symbol=symbol,
        )
        if order.name_trader.name == name_trader.name:
            # size_1 = abs(float(order.size))
            size_2 = abs(float(size))

            Signal.objects.filter(name_trader=name_trader,
                                  symbol=symbol).update(upd=datetime.now(),
                                                        mark_price=mark_price,
                                                        pnl=pnl,
                                                        roe=roe,
                                                        size=size_2
                                                        )
        #     try:
        #         if size_1 != size_2:
        #             print(
        #                 f'Symbol {symbol}\n'
        #                 f's1 > s2\n'
        #                 f'{size_1} > {size_2}'
        #             )
        #             place_reduce(
        #                 order, symbol, name_trader, size_1, size_2, client_ad
        #             )
        #     except:
        #         pass
        return True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
        return False


def order_close(signal, user):
    try:
        if user.subs_active:
            symbol = signal.symbol
            side = signal.side

            api_key = user.api_key
            api_secret = user.api_secret
            # percent_balance = user.percent_balance
            leverage = user.leverage
            exchange = user.exchange

            if exchange == 'Binance':
                session = Client(api_key, api_secret,
                                 # {'proxies': {'https':
                                 #                  'http://55atd49zx3h8g4:rqsdhwj89arjlv4637fna1qx220@eu-west-static-05.quotaguard.com:9293'}
                                 #  }
                                 )
                print(
                    f'User {user.user_name}\n'
                    f'Start close position\n'
                    f'Symbol {symbol}'
                )
                if side == 'BUY':
                    qty = abs(float(session.futures_position_information(symbol=symbol)[0]['positionAmt']))
                    print(
                        f'Position QTY = {qty}'
                    )
                    if qty > 0:
                        session.futures_create_order(
                            symbol=symbol,
                            side='SELL',
                            type='MARKET',
                            quantity=qty,
                            reduceOnly=True
                        )
                        print(
                            f'Position close Successful\n'
                            f'User {user.user_name}\n'
                            f'Symbol {symbol}'
                        )
                else:
                    qty = abs(float(session.futures_position_information(symbol=symbol)[0]['positionAmt']))
                    if qty > 0:
                        session.futures_create_order(
                            symbol=symbol,
                            side='BUY',
                            type='MARKET',
                            quantity=qty,
                            reduceOnly=True
                        )
                        print(
                            f'Position close Successful\n'
                            f'User {user.user_name}\n'
                            f'Symbol {symbol}'
                        )
            elif exchange == 'Bybit':
                session = bybit({
                    "apiKey": api_key,
                    "secret": api_secret,
                    "enableRateLimit": True,
                    'timeout': 30000,
                })
                print(
                    f'User {user.user_name}\n'
                    f'Start close position\n'
                    f'Symbol {symbol}'
                )
                if side == 'BUY':
                    contracts = float(session.fetch_positions(symbol)[0]['contracts'])
                    if contracts <= 0:
                        contracts = float(session.fetch_positions(symbol)[1]['contracts'])

                    print(
                        f'contracts = {contracts}'
                    )
                    if contracts > 0:
                        try:
                            try:
                                session.create_market_order(
                                    symbol=symbol,
                                    side='Sell',
                                    amount=contracts,
                                    params={
                                        'Leverage': leverage,
                                        'reduceOnly': True,
                                        'position_idx': 2
                                    }
                                )
                            except:
                                session.create_market_order(
                                    symbol=symbol,
                                    side='Sell',
                                    amount=contracts,
                                    params={
                                        'Leverage': leverage,
                                        'reduceOnly': True,
                                        'position_idx': 1
                                    }
                                )
                            print(
                                f'Position close Successful\n'
                                f'User {user.user_name}\n'
                                f'Symbol {symbol}'
                            )
                        except Exception as e:
                            # The name of your app and dyno
                            app_name = 'aws copy-trade-leaderboard'
                            debug(
                                e, app_name
                            )
                else:
                    contracts = float(session.fetch_positions(symbol)[0]['contracts'])
                    if contracts <= 0:
                        contracts = float(session.fetch_positions(symbol)[1]['contracts'])
                    print(
                        f'contracts = {contracts}'
                    )
                    if contracts > 0:
                        try:
                            try:
                                session.create_market_order(
                                    symbol=symbol,
                                    side='Buy',
                                    amount=contracts,
                                    params={
                                        'Leverage': leverage,
                                        'reduceOnly': True,
                                        'position_idx': 2
                                    }
                                )
                            except:
                                session.create_market_order(
                                    symbol=symbol,
                                    side='Buy',
                                    amount=contracts,
                                    params={
                                        'Leverage': leverage,
                                        'reduceOnly': True,
                                        'position_idx': 1
                                    }
                                )
                            print(
                                f'Position close Successful\n'
                                f'User {user.user_name}\n'
                                f'Symbol {symbol}'
                            )
                        except Exception as e:
                            # The name of your app and dyno
                            app_name = 'aws copy-trade-leaderboard'
                            debug(
                                e, app_name
                            )
            else:
                pass
    except Exception as e:
        # The name of your app and dyno
        app_name = 'aws copy-trade-leaderboard'
        debug(
            e, app_name
        )

        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")


def open_position(signal, user):
    try:
        if user.subs_active:
            symbol = signal.symbol
            side = signal.side

            api_key = user.api_key
            api_secret = user.api_secret
            percent_balance = user.percent_balance
            leverage = user.leverage
            exchange = user.exchange

            # шаг цены в торговой паре
            step_size = 0
            tickSize = 0
            minQty = 0
            maxQty = 0
            with open('pair_list.json') as f:
                templates = json.load(f)

            for temp in templates:
                if temp['Symbol'] == symbol:
                    step_size = float(temp['stepSize'])
                    tickSize = float(temp['tickSize'])
                    minQty = float(temp['minQty'])
                    maxQty = float(temp['maxQty'])
                    break
            round_size = get_count(step_size)

            if exchange == 'Binance':
                client = Client(
                    api_key,
                    api_secret,
                    # {'proxies': {'https':
                    #                  'http://55atd49zx3h8g4:rqsdhwj89arjlv4637fna1qx220@eu-west-static-05.quotaguard.com:9293'}
                    #  }
                )
                try:
                    client.futures_change_margin_type(symbol=symbol,
                                                      marginType='CROSSED')
                except Exception as e:
                    pass
                try:
                    client.futures_change_leverage(
                        symbol=symbol,
                        leverage=leverage
                    )
                except:
                    pass
                current_price = signal.entry_price

                quantity = 0
                try:
                    if 'USDT' in symbol:
                        # Получаем баланс счета по фьючерсам.
                        account_balance = client.futures_account_balance()
                        # Ищем баланс USDT в ответе от сервера.
                        balance = float((next(item for item in account_balance if item['asset'] == 'USDT')
                                         )['withdrawAvailable']) * leverage

                        wa = (float(balance) * float(percent_balance) / 100)
                        while True:
                            min_amount_m = float(wa) / float(current_price) // float(
                                step_size) * float(step_size)
                            if min_amount_m <= 0.001:
                                wa += 1
                            else:
                                break
                        # округляем через функцию сстх апи
                        if min_amount_m >= 10:
                            quantity = round(min_amount_m)
                        else:
                            quantity = float(decimal_to_precision(min_amount_m,
                                                                  ROUND,
                                                                  round_size,
                                                                  DECIMAL_PLACES))
                        if quantity <= 0:
                            quantity = float(decimal_to_precision(min_amount_m,
                                                                  ROUND,
                                                                  round_size + 1,
                                                                  DECIMAL_PLACES))
                        if quantity <= minQty:
                            quantity = minQty
                except ZeroDivisionError:
                    print('бабки кончились')
                    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                except Exception as e:
                    # The name of your app and dyno
                    app_name = 'aws copy-trade-leaderboard'
                    debug(
                        e, app_name
                    )
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
                    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                print(f'QTY = {quantity}')

                client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='MARKET',
                    quantity=quantity,
                )
                print(
                    f'Position open!\n'
                    f'User = {user}\n'
                    f'symbol: {symbol}'
                )
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

            elif exchange == 'Bybit':
                with open('bybit_pair_list.json', 'r') as f:
                    sym_list = json.load(f)

                matches = any([symbol == sym for sym in sym_list])
                if matches:
                    session = bybit({
                        "apiKey": api_key,
                        "secret": api_secret,
                        "enableRateLimit": True,
                        'timeout': 30000,
                    })
                    try:
                        session.set_position_mode(
                            hedged='BothSide', symbol=symbol
                        )
                    except:
                        pass
                    try:
                        session.set_leverage(
                            symbol=symbol,
                            leverage=leverage
                        )
                    except:
                        pass
                    try:
                        session.set_margin_mode(
                            symbol=symbol,
                            marginMode='CROSS',
                            params={
                                'sell_leverage': leverage,
                                'buy_leverage': leverage
                            }
                        )
                    except:
                        pass
                    current_price = float(signal.mark_price)
                    quantity = 0
                    try:
                        if 'USDT' in symbol:
                            # Получаем баланс счета по фьючерсам.
                            # Ищем баланс USDT в ответе от сервера.
                            balance = float(session.fetch_balance()['USDT']['free']) * leverage

                            wa = (float(balance) * float(percent_balance) / 100)
                            while True:
                                min_amount_m = float(wa) / float(current_price) // float(
                                    step_size) * float(step_size)
                                if min_amount_m <= 0.001:
                                    wa += 1
                                else:
                                    break
                            # округляем через функцию сстх апи
                            if min_amount_m >= 10:
                                quantity = round(min_amount_m)
                            else:
                                quantity = float(decimal_to_precision(min_amount_m,
                                                                      ROUND,
                                                                      round_size,
                                                                      DECIMAL_PLACES))
                            if quantity <= 0:
                                quantity = float(decimal_to_precision(min_amount_m,
                                                                      ROUND,
                                                                      round_size + 1,
                                                                      DECIMAL_PLACES))
                            if quantity <= minQty:
                                quantity = minQty
                    except ZeroDivisionError:
                        print('бабки кончились')
                        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                    except Exception as e:
                        # The name of your app and dyno
                        app_name = 'os.environ.get("app_name")'
                        debug(
                            e, app_name
                        )
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
                        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                    print(f'QTY = {quantity}')

                    if side == 'BUY':
                        try:
                            session.create_market_order(
                                symbol=symbol,
                                side='Buy',
                                amount=quantity,
                                params={
                                    'Leverage': leverage,
                                    # 'reduceOnly': True,
                                    'position_idx': 1
                                }
                            )
                        except:
                            session.create_market_order(
                                symbol=symbol,
                                side='Buy',
                                amount=quantity,
                                params={
                                    'Leverage': leverage,
                                    # 'reduceOnly': True,
                                    'position_idx': 2
                                }
                            )
                        print(
                            f'Position open!\n'
                            f'User = {user}\n'
                            f'symbol: {symbol}'
                        )
                        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

                    else:
                        try:
                            session.create_market_order(
                                symbol=symbol,
                                side='Sell',
                                amount=quantity,
                                params={
                                    'Leverage': leverage,
                                    # 'reduceOnly': True,
                                    'position_idx': 2
                                }
                            )
                        except:
                            session.create_market_order(
                                symbol=symbol,
                                side='Sell',
                                amount=quantity,
                                params={
                                    'Leverage': leverage,
                                    # 'reduceOnly': True,
                                    'position_idx': 1
                                }
                            )
                        print(
                            f'Position open!\n'
                            f'User = {user}\n'
                            f'symbol: {symbol}'
                        )
                        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            else:
                pass
    except Exception as e:
        # The name of your app and dyno
        app_name = 'aws copy-trade-leaderboard'
        debug(
            e, app_name
        )
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")


def get_trader_1(link, name, trade):
    if len(link) > 5:
        uid = link.split('encryptedUid=')[1]
        k = 0
        while True:
            sleep(1)
            payload = {'api_key': api, 'url': pos_url, "apiParams": {
                "country_code": "eu",  # // string, see: https://api.scraperapi.com/geo
                "device_type": "desktop",  # // desktop | mobile
                "premium": 'true',  # // boolean
            }, }

            pos_response = requests.post('http://api.scraperapi.com', params=payload, json={"encryptedUid": uid,
                                                                                            "tradeType": "PERPETUAL"})
            if pos_response.ok:
                break
        # Получаем текущее время
        now = datetime.now()

        # Форматируем и выводим время
        current_time = now.strftime("%H:%M:%S")
        print(
            f'Position get from {name} / {current_time}'
        )
        position = json.loads(pos_response.content)['data']['otherPositionRetList']
        if position is None:
            pass
            # # Получаем текущее время
            # now = datetime.now()
            #
            # # Отнимаем 10 минут
            # new_time = now - timedelta(minutes=10)
            # Signal.objects.filter(name_trader=trade,
            #                       ).update(upd=new_time,
            #                                )
        if len(position) > 0:
            try:
                for tex in position:
                    sleep(0.3)
                    data = tex
                    if data['symbol'].find('USDT') >= 0:
                        symbol = data['symbol']
                        size = (data['amount'])
                        entry_price = data['entryPrice']
                        mark_price = data['markPrice']
                        pnl = data['pnl']
                        roe = data['roe']

                        # leverage = data['leverage']

                        date_1 = data['updateTime']
                        timestamp = datetime(*date_1[:6]).timestamp() + date_1[6] / 10 ** 9
                        date = datetime.fromtimestamp(timestamp)
                        side = ''
                        if size < 0:
                            side = 'Sell'
                        elif size > 0:
                            side = 'Buy'

                        if not get_orders(trade, symbol, date, size, mark_price, pnl, roe):
                            if side == 'Sell':
                                msg = f'<b>🚨 NEW ALERT 🚨</b>\n\n' \
                                      f'🥷🏾Trader: <b>{name}</b>\n' \
                                      f'💎Crypto: <b>{symbol}</b>\n' \
                                      f'🔴Trade: <b>Sell</b> (SHORT)\n\n' \
                                      f'📊Entry price: <b>{entry_price}</b>\n' \
                                      f'💰Size: <b>{round(abs(size * entry_price))}$</b>\n'
                                # инициализируем дату и добавляем в базу
                                signal = Signal(
                                    name_trader=trade,
                                    symbol=symbol,
                                    side='SELL',
                                    size=abs(size),
                                    entry_price=entry_price,
                                    mark_price=mark_price,
                                    pnl=pnl,
                                    roe=roe,
                                    date=date,
                                    upd=datetime.now(),
                                    message=msg,
                                    # status=False,
                                )
                                signal.save()
                            else:
                                msg = f'<b>🚨 NEW ALERT 🚨</b>\n\n' \
                                      f'🥷🏾Trader: <b>{name}</b>\n' \
                                      f'💎Crypto: <b>{symbol}</b>\n' \
                                      f'🔵Trade: <b>BUY</b> (LONG)\n\n' \
                                      f'📊Entry price: <b>{entry_price}</b>\n' \
                                      f'💰Size: <b>{round(abs(size * entry_price))}$</b>\n'
                                signal = Signal(
                                    name_trader=trade,
                                    symbol=symbol,
                                    side='BUY',
                                    size=abs(size),
                                    entry_price=entry_price,
                                    mark_price=mark_price,
                                    pnl=pnl,
                                    roe=roe,
                                    date=date,
                                    upd=datetime.now(),
                                    message=msg,
                                    # status=False,
                                )
                                signal.save()

            except Exception as e:
                # The name of your app and dyno
                app_name = 'aws copy-trade-leaderboard'
                debug(
                    e, app_name
                )
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
