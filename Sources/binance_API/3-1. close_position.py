import logging
from binance_f import RequestClient
from binance_f import SubscriptionClient
from binance_f.constant.test import *
from binance_f.model import *
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.base.printobject import *


def position_check(client):
    positions = client.get_position()
    for pos in positions:
        if pos.symbol == 'BTCUSDT':
            if pos.positionAmt == 0:
                print("Position does not exist.")
            else:
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
                while True:
                    choice = input("Position already exist, do you want to close the position? (Y/N): ")
                    if choice == 'Y' or choice == 'y':
                        # ClosePosition True = Can not be sent with non zero quanitity
                        # Positionside = LONG OR SHORT for hedge mode
                        # side = BUY or SELL
                        close = request_client.post_order(symbol="BTCUSDT", side=OrderSide.SELL,
                                                          positionSide=pos.positionSide,
                                                          ordertype=OrderType.LIMIT, timeInForce="GTC",
                                                          price=pos.entryPrice, quantity=pos.positionAmt)
                        PrintBasic.print_obj(close)
                        break
                    elif choice == 'N' or choice == 'n':
                        print("You let the position open, program terminating.")
                        sys.exit()


if __name__ == '__main__':
