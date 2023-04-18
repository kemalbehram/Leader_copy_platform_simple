import json
import sys
from datetime import datetime
from time import sleep

import requests
from ccxt.base.decimal_to_precision import DECIMAL_PLACES  # noqa F401
from ccxt.base.decimal_to_precision import NO_PADDING  # noqa F401
from ccxt.base.decimal_to_precision import PAD_WITH_ZERO  # noqa F401
from ccxt.base.decimal_to_precision import ROUND  # noqa F401
from ccxt.base.decimal_to_precision import SIGNIFICANT_DIGITS  # noqa F401
from ccxt.base.decimal_to_precision import TICK_SIZE  # noqa F401
from ccxt.base.decimal_to_precision import TRUNCATE  # noqa F401
from ccxt.base.decimal_to_precision import decimal_to_precision  # noqa F401
from django.core.management import BaseCommand

from Bot.management.commands.config import pos_headers
from Bot.management.commands.fucn_trader import pos_url, get_orders
from Bot.models import Traders, Signal


def get_trader_2(trade):
    link = trade.link
    name = trade.name
    if len(link) > 5:

        uid = link.split('encryptedUid=')[1]
        while True:
            sleep(2)
            pos_response = requests.post(pos_url, headers=pos_headers,
                                         json={"encryptedUid": uid,
                                               "tradeType": "PERPETUAL"},
                                         timeout=2)
            if pos_response.ok:
                break
        position = json.loads(pos_response.content)['data']['otherPositionRetList']
        print(
            f'Position get from {name}'
        )
        if len(position) > 0:
            try:
                for tex in position:
                    sleep(0.3)
                    data = tex
                    if data['symbol'].find('USDT') >= 0:
                        symbol = data['symbol']
                        size = data['amount']
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
                        # # шаг цены в торговой паре
                        # step_size = 1
                        # pprint(data)
                        # with open('data_file.json') as f:
                        #     templates = json.load(f)
                        #
                        # for temp in templates:
                        #     if temp['symbol'] == symbol:
                        #         step_size = float(temp['stepSize'])
                        #         break

                        # matches = any([symbol == sym for sym in sym_list])
                        # if matches:
                        #     session = ''
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
                                    status=True
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
                                    status=True
                                )
                                signal.save()

            except Exception as e:
                #     # Your Heroku API key
                #     api_key_heroku = os.environ.get("api_key_heroku")
                #
                #     # The name of your app and dyno
                #     app_name = os.environ.get("app_name")
                #     # debug(
                #     #     e, app_name
                #     # )
                #     heroku_conn = heroku3.from_key(api_key_heroku)
                #     app = heroku_conn.app(app_name)
                #     app.restart()
                #
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(str(e) + 'line = ' + str(exc_tb.tb_lineno))


class Command(BaseCommand):
    help = 'бот'

    def handle(self, *args, **options):
        traders = Traders.objects.all()

        for trade in traders:
            try:
                get_trader_2(trade)
            except TypeError as e:
                print(e)
