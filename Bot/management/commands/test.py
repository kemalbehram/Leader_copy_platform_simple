import json
from pprint import pprint
from scraper_api import ScraperAPIClient

import requests

link = 'https://www.binance.com/en/futures-activity/leaderboard/user/um?encryptedUid=802118EDADBFD330E6635220BE0A7821'
uid = link.split('encryptedUid=')[1]
api = '8df03c1906ff35c53203563774fa3b53'
# pos_response = requests.post(pos_url, headers=pos_headers,
#                                          json={"encryptedUid": uid,
#                                                "tradeType": "PERPETUAL"},
#                                          timeout=10,
#                                          proxies=choice(proxies))
# payload = {'api_key': '',
#            'url': f'{uid}', 'country_code': 'us'}
# client = ScraperAPIClient(api)
# result = client.get(url='http://httpbin.org/ip')
# print(result)
# r = requests.post('http://api.scraperapi.com', params=payload, json={"encryptedUid": uid,
#                                                                      "tradeType": "PERPETUAL"})
# # print(r.text)

pos_url = 'https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getOtherPosition'

payload = {'api_key': api, 'url': pos_url}


r = requests.post('http://api.scraperapi.com', params=payload, json={"encryptedUid": uid,
                                                                     "tradeType": "PERPETUAL"})
# print(r)
pprint(
    json.loads(r.content)
)
