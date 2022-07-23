from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
result = request_client.get_balance()
mark_price = request_client.get_mark_price(symbol="BTCUSDT")
mark_price = mark_price.markPrice
mark_price_998 = f'{mark_price*0.998:0.2f}'
print("type: ", type(mark_price_998))
print("value: ", mark_price_998)
for obj in result:
    if obj.asset == "USDT":
        print("USDT잔고:", obj.balance)