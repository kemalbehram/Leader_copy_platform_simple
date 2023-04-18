import os
import sys
import threading
from datetime import datetime
from time import sleep

import telebot
from dateutil import parser
from django.core.management.base import BaseCommand

from Bot.management.commands.fucn_trader import get_trader_1, open_position, order_close, debug
from Bot.models import Signal, Traders, Users, Admin

admin = Admin.objects.get(subs_active=True)
try:
    token = admin.bot_token  # dev bot token
    my_id = admin.user_id

    bots = telebot.TeleBot(token)
except:
    pass


class Command(BaseCommand):
    help = 'бот'

    def handle(self, *args, **options):
        print(
            'Copy Bot Start'
        )
        while True:
            sleep(4)
            traders = Traders.objects.filter(is_active=True)

            for trade in traders:
                sleep(0.3)
                t = threading.Thread(target=get_trader_1, args=(trade.link, trade.name, trade))
                t.start()

            # получаем ордера со статусом Фолс
            signals = Signal.objects.filter(status=False)
            # получаем айди трейдеров и
            users = Users.objects.filter(subs_active=True)
            for signal in signals:
                sleep(0.3)
                try:
                    t = threading.Thread(target=open_position, args=(signal, admin))
                    t.start()
                except Exception as e:
                    # The name of your app and dyno
                    app_name = ''
                    debug(
                        e, app_name
                    )
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
                for user in users:
                    sleep(0.3)
                    try:
                        t = threading.Thread(target=open_position, args=(signal, user))
                        t.start()
                    except Exception as e:
                        # The name of your app and dyno
                        app_name = 'os.environ.get("app_name")'
                        debug(
                            e, app_name
                        )
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        print(str(e) + 'line = ' + str(exc_tb.tb_lineno))

            # # получаем айди трейдеров и
            # for signal in signals:
            #     # trader = Traders.objects.get(id=signal.name_trader.id)
            #     #
            #     # with open('follows.json') as f:
            #     #     templates = json.load(f)
            #     #
            #     # for temp in templates:
            #     #     if trader.name == temp['Trader']:
            #     #         for follow in temp['followers']:
            #     #             user = Users.objects.get(id=follow['id'])
            #                 t = threading.Thread(target=open_position, args=(signal, user))
            #                 t.start()
            for signal in signals:
                sleep(0.3)
                try:
                    bots.send_message(
                        my_id, signal.message, parse_mode='HTML'
                    )
                except:
                    pass
            # обновляем статус сигналов
            signals.update(status=True)
            sleep(2)
            # получаем активные ордера
            sig_ord = Signal.objects.filter(is_active=True, status=True)

            # сравниваем истекли срок годности ордера
            try:
                for order_s in sig_ord:
                    date_end = order_s.upd

                    now = datetime.now()

                    a = now - parser.parse(date_end)
                    delta = a.seconds / 60
                    # если срок годности ордера больше 2 минут, то получаем информацию об открытой позиции
                    # и закрываем её
                    print('DELTA = ' + str(round(delta, 2)) + f' {order_s.symbol}/ trader {order_s.name_trader}')
                    if delta >= 1.5:
                        try:
                            t = threading.Thread(target=order_close, args=(order_s, admin))
                            t.start()
                        except Exception as e:
                            # The name of your app and dyno
                            app_name = 'os.environ.get("app_name")'
                            debug(
                                e, app_name
                            )
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
                        # users = Users.objects.filter(subs_active=True)
                        for user in users:
                            sleep(0.5)
                            try:
                                t = threading.Thread(target=order_close, args=(order_s, user))
                                t.start()
                            except Exception as e:
                                # The name of your app and dyno
                                app_name = 'os.environ.get("app_name")'
                                debug(
                                    e, app_name
                                )
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
                        sleep(1)
                        if order_s.side == 'BUY':
                            msg = f'<b>📳 TRADE CLOSED 📳</b>\n\n' \
                                  f'🥷🏾Trader: <b>{order_s.name_trader}</b>\n' \
                                  f'💎Crypto: <b>{order_s.symbol}</b>\n' \
                                  f'🔵Trade: <b>BUY</b> (LONG)\n\n' \
                                  f'📊Marketprice: <b>{order_s.mark_price}</b>\n' \
                                  f'💹PNL: <b>{round(float(order_s.roe), 2)}%</b>\n\n'
                            try:
                                bots.send_message(my_id, msg, parse_mode='HTML')
                            except:
                                pass
                        else:
                            msg = f'<b>📳 TRADE CLOSED 📳</b>\n\n' \
                                  f'🥷🏾Trader: <b>{order_s.name_trader}</b>\n' \
                                  f'💎Crypto: <b>{order_s.symbol}</b>\n' \
                                  f'🔴Trade: <b>Sell</b> (SHORT)\n\n' \
                                  f'📊Marketprice: <b>{order_s.mark_price}</b>\n' \
                                  f'💹PNL: <b>{round(float(order_s.roe), 2)}%</b>\n\n'
                            try:
                                bots.send_message(my_id, msg, parse_mode='HTML')
                            except:
                                pass
                        sleep(0.5)
                        Signal.objects.filter(symbol=order_s.symbol, is_active=True).update(is_active=False)
                        # trader = Traders.objects.get(id=order_s.name_trader.id)
                        # # получаем подпищиков трейдеров
                        # with open('follows.json') as f:
                        #     templates = json.load(f)
                        #
                        # for temp in templates:
                        #     if trader.name == temp['Trader']:
                        #         for follow in temp['followers']:
                        #             sleep(0.3)
                        #             # получаем пользователя из базы и закрываем позицию
                        #             user = Users.objects.get(id=follow['id'])
                        #             t = threading.Thread(target=order_close, args=(order_s, user))
                        #             t.start()

            except Exception as e:
                # The name of your app and dyno
                app_name = 'os.environ.get("app_name")'
                debug(
                    e, app_name
                )
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(e) + 'line = ' + str(exc_tb.tb_lineno))

            Signal.objects.filter(is_active=False).delete()
            sleep(1)
            # try:
            #     check_users()
            #     sleep(1)
            #     pair_list_update()
            # except:
            #     pass
