import sys
import threading
from datetime import datetime
from time import sleep

import telebot
from dateutil import parser
from django.core.management.base import BaseCommand

from Bot.management.commands.fucn_trader import get_trader_1, open_position, order_close, debug, check_users
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
            sleep(10)
            traders = Traders.objects.filter(is_active=True)
            for trade in traders:
                try:
                    get_trader_1(
                        trade.link, trade.name, trade
                    )
                except Exception as e:
                    # The name of your app and dyno
                    app_name = 'aws copy-trade-leaderboard'
                    debug(
                        e, app_name
                    )

                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
            sleep(1)
            # получаем ордера со статусом Фолс
            signals = Signal.objects.filter(status=False)
            # получаем айди трейдеров и
            users = Users.objects.filter(subs_active=True)
            for signal in signals:
                sleep(0.3)
                try:
                    bots.send_message(
                        my_id, signal.message, parse_mode='HTML'
                    )
                except:
                    pass
                try:
                    t = threading.Thread(target=open_position, args=(signal, admin))
                    t.start()
                except Exception as e:
                    # The name of your app and dyno
                    app_name = 'aws copy-trade-leaderboard'
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
                        app_name = 'aws copy-trade-leaderboard'
                        debug(
                            e, app_name
                        )
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        print(str(e) + 'line = ' + str(exc_tb.tb_lineno))

            # обновляем статус сигналов
            signals.update(status=True)
            sleep(1)
            # получаем активные ордера
            sig_ord = Signal.objects.filter(is_active=True, status=True)

            # сравниваем истекли срок годности ордера
            try:
                for order_s in sig_ord:
                    date_end = order_s.upd

                    now = datetime.now()

                    a = now - parser.parse(date_end)
                    delta = a.seconds / 60
                    # если срок годности ордера больше 1 минут, то получаем информацию об открытой позиции
                    # и закрываем её
                    print('DELTA = ' + str(round(delta, 2)) + f' {order_s.symbol}/ trader {order_s.name_trader}')
                    if delta >= 1.5:
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
                        try:
                            t = threading.Thread(target=order_close, args=(order_s, admin))
                            t.start()
                        except Exception as e:
                            # The name of your app and dyno
                            app_name = 'aws copy-trade-leaderboard'
                            debug(
                                e, app_name
                            )
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
                        for user in users:
                            try:
                                t = threading.Thread(target=order_close, args=(order_s, user))
                                t.start()
                            except Exception as e:
                                # The name of your app and dyno
                                app_name = 'aws copy-trade-leaderboard'
                                debug(
                                    e, app_name
                                )
                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
                        Signal.objects.filter(symbol=order_s.symbol, is_active=True).update(is_active=False)

            except Exception as e:
                app_name = 'aws copy-trade-leaderboard'
                debug(
                    e, app_name
                )
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(e) + 'line = ' + str(exc_tb.tb_lineno))
            sleep(15)
            try:
                check_users()
            except:
                pass
            Signal.objects.filter(is_active=False).delete()
