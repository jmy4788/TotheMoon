from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
result = request_client.get_position()

for pos in result:
    if pos.symbol == 'BTCUSDT':
        print("pos.entryPrice:", pos.entryPrice)
        print("pos.isAutoAddMargin:", pos.isAutoAddMargin)
        print("pos.leverage:", pos.leverage)
        print("pos.maxNotionalValue:", pos.maxNotionalValue)
        print("pos.liquidationPrice:", pos.liquidationPrice)
        print("pos.markPrice:", pos.markPrice)
        print("pos.positionAmt:", pos.positionAmt)
        print("pos.symbol:", pos.symbol)
        print("pos.unrealizedProfit:", pos.unrealizedProfit)
        print("pos.isolatedMargin:", pos.isolatedMargin)
        print("pos.positionSide:", pos.positionSide)

