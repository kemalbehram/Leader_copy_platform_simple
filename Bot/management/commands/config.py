from fake_useragent import UserAgent, FakeUserAgentError
# Main network token to pay for a subscription t.me/CryptoBot?start=r-1268434
token_pay_main = ''
# Test network token to pay for a subscription https://t.me/CryptoTestnetBot
token_test_pay = ''

info_url = 'https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getOtherLeaderboardBaseInfo'
width = 2

test = True
if test:
    token_pay = token_test_pay
    # test telegram token
    token = '6084252834'
else:
    token_pay = token_pay_main
    # Main telegram token
    token = '5850680399'


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
pay_adres = ''
network = ''
cashback = 0.02
# name your telegram bot
bot_name = 'asdhiahsdaihs_bot'
# subscription price
vip_cost = 75
# ordinary_cost = 25
# standard_cost = 35
# subscription discount
# discount = 0.2