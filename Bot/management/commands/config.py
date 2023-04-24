# Main network token to pay for a subscription t.me/CryptoBot?start=r-1268434
token_pay_main = '97754:AA9SleQI44sdE3AZONIQkgWMrm4HM4TzIYk'
# Test network token to pay for a subscription https://t.me/CryptoTestnetBot
token_test_pay = '97754:AA9SleQI44sdE3AZONIQkgWMrm4HM4TzIYk'

info_url = 'https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getOtherLeaderboardBaseInfo'
width = 2

test = False
if test:
    token_pay = token_test_pay
    # test telegram token
    token = '5817843241:AAH5B89odTTPwxnFGdqTfWGv8wzuD20_dP0'
else:
    token_pay = token_pay_main
    # Main telegram token
    token = '5817843241:AAH5B89odTTPwxnFGdqTfWGv8wzuD20_dP0'


# try:
#     ua = UserAgent()
#     user_agent = ua.random
# except FakeUserAgentError:
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/74.0.3729.169 Safari/537.36"

pos_headers = {
    'authority': 'www.binance.com',
    'x-trace-id': '',  # xtrace
    'csrftoken': '',  # csrf token
    'x-ui-request-trace': '',  # x-ui-request-trace
    'user-agent': f'{user_agent}',  # UA
    'content-type': 'application/json',
    'lang': 'en',
    'fvideo-id': '',  # fvideo id
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua': '"Google Chrome";v="109", " Not;A Brand";v="99", "Chromium";v="109"',
    'device-info': '',  # device info
    'bnc-uuid': '',  # bnc-uuid
    'clienttype': 'web',
    'sec-ch-ua-platform': '"macOS"',
    'accept': '*/*',
    'origin': 'https://www.binance.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.binance.com/en/futures-activity/leaderboard?type=filterResults&isShared=true&limit=200'
               '&periodType=MONTHLY&pnlGainType=LEVEL4&roiGainType=&sortType=ROI&symbol=&tradeType=PERPETUAL',
    'accept-language': 'en',
    'cookie': '',  # cookie
}
pay_adres = '0x6C08125Ac747eFbD907807FDa1128823D4Cf3dBb'
network = 'BUSD Bep20'
pay_adres_1 = 'TX9akUcQpKddzV5DE9kS8bVwNbzfEfUgDo'
network_1 = 'Usdt trc20'
cashback = 5
admin_name = 'Mazbojim'
# name your telegram bot
bot_name = 'TradewithAI_bot'
# subscription price
vip_cost = 25
# ordinary_cost = 25
# standard_cost = 35
# subscription discount
# discount = 0.2
