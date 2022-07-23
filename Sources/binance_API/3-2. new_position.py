import sys
import logging
from binance_f import RequestClient
from binance_f import SubscriptionClient
from binance_f.constant.test import *
from binance_f.model import *
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.base.printobject import *
import time

def callback(data_type: 'SubscribeMessageType', event: 'any'):
    if data_type == SubscribeMessageType.RESPONSE:
        print("Event ID: ", event)
    elif data_type == SubscribeMessageType.PAYLOAD:
        if event.eventType == "ACCOUNT_UPDATE":
            print("Event Type: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("Transaction time: ", event.transactionTime)
            print("=== Balances ===")
            PrintMix.print_data(event.balances)
            print("================")
            print("=== Positions ===")
            PrintMix.print_data(event.positions)
            print("================")
        elif event.eventType == "ORDER_TRADE_UPDATE":
            print("Event Type: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("Transaction Time: ", event.transactionTime)
            print("Symbol: ", event.symbol)
            print("Client Order Id: ", event.clientOrderId)
            print("Side: ", event.side)
            print("Order Type: ", event.type)
            print("Time in Force: ", event.timeInForce)
            print("Original Quantity: ", event.origQty)
            print("Position Side: ", event.positionSide)
            print("Price: ", event.price)
            print("Average Price: ", event.avgPrice)
            print("Stop Price: ", event.stopPrice)
            print("Execution Type: ", event.executionType)
            print("Order Status: ", event.orderStatus)
            print("Order Id: ", event.orderId)
            print("Order Last Filled Quantity: ", event.lastFilledQty)
            print("Order Filled Accumulated Quantity: ", event.cumulativeFilledQty)
            print("Last Filled Price: ", event.lastFilledPrice)
            print("Commission Asset: ", event.commissionAsset)
            print("Commissions: ", event.commissionAmount)
            print("Order Trade Time: ", event.orderTradeTime)
            print("Trade Id: ", event.tradeID)
            print("Bids Notional: ", event.bidsNotional)
            print("Ask Notional: ", event.asksNotional)
            print("Is this trade the maker side?: ", event.isMarkerSide)
            print("Is this reduce only: ", event.isReduceOnly)
            print("stop price working type: ", event.workingType)
            print("Is this Close-All: ", event.isClosePosition)
            if event.activationPrice is not None:
                print("Activation Price for Trailing Stop: ", event.activationPrice)
            if event.callbackRate is not None:
                print("Callback Rate for Trailing Stop: ", event.callbackRate)

            if event.orderId == long.orderId and event.orderStatus == 'FILLED':
                print("롱 오더가 체결되었습니다. 숏 오더를 캔슬하겠습니다.")
                cancel_order(short)
                tp_order(long)
            elif event.orderId == short.orderId and event.orderStatus == 'FILLED':
                print("숏 오더가 체결되었습니다. 롱 오더를 취소하겠습니다.")
                cancel_order(long)
                tp_order(short)

        elif event.eventType == "listenKeyExpired":
            print("Event: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
            print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
            print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
    else:
        print("Unknown Data:")
    print()


def error(e: 'BinanceApiException'):
    print(e.error_code + e.error_message)


def cancel_order(order):
    request_client.cancel_order(symbol='BTCUSDT', orderId=order.orderId)
    return


def hedgemode_on():
    """
    DUAL SIDE(HEDGE) MODE 활성화
    :param:
    :return:
    """
    pos_mode = request_client.get_position_mode()
    pos_mode = pos_mode.dualSidePosition
    if pos_mode is not True:
        request_client.change_position_mode(dualSidePosition=True)
    return


def oco_order():
    long_order = request_client.post_order(symbol="BTCUSDT",
                                           timeInForce=TimeInForce.GTC,
                                           ordertype=OrderType.STOP,
                                           positionSide=PositionSide.LONG,
                                           side=OrderSide.BUY,
                                           quantity=oco_long_quantity,
                                           price=oco_long_price,
                                           stopPrice=oco_long_stop_price,
                                           )
    short_order = request_client.post_order(symbol="BTCUSDT",
                                            timeInForce=TimeInForce.GTC,
                                            ordertype=OrderType.STOP,
                                            positionSide=PositionSide.SHORT,
                                            side=OrderSide.SELL,
                                            quantity=oco_short_quantity,
                                            price=oco_short_price,
                                            stopPrice=oco_short_stop_price)
    return long_order, short_order


def tp_order(order):
    print("tp order가 실행되었는지 확인여부(1)")
    print(order.positionSide)
    if order.positionSide == "LONG":
        print("tp order가 실행되었는지 확인여부(2)")
        print("남아있는 LONG포지션에 대한 매도를 실행합니다.")
        request_client.post_order(symbol="BTCUSDT",
                                 timeInForce=TimeInForce.GTC,
                                 ordertype=OrderType.TAKE_PROFIT_MARKET,
                                 positionSide=PositionSide.LONG,
                                 side=OrderSide.SELL,
                                 quantity=oco_long_quantity,
                                 stopPrice=tp_long_top_price)
        request_client.post_order(symbol="BTCUSDT",
                                 timeInForce=TimeInForce.GTC,
                                 ordertype=OrderType.STOP_MARKET,
                                 positionSide=PositionSide.LONG,
                                 side=OrderSide.SELL,
                                 quantity=oco_long_quantity,
                                 stopPrice=tp_long_bottom_price)
    elif order.positionSide == "SHORT":
        print("tp order가 실행되었는지 확인여부(3)")
        print("남아있는 SHORT포지션에 대한 매도를 실행합니다.")
        request_client.post_order(symbol="BTCUSDT",
                                   timeInForce=TimeInForce.GTC,
                                   ordertype=OrderType.TAKE_PROFIT_MARKET,
                                   positionSide=PositionSide.SHORT,
                                   side=OrderSide.SELL,
                                   quantity=oco_short_quantity,
                                   stopPrice=tp_short_top_price)
        request_client.post_order(symbol="BTCUSDT",
                                   timeInForce=TimeInForce.GTC,
                                   ordertype=OrderType.STOP_MARKET,
                                   positionSide=PositionSide.SHORT,
                                   side=OrderSide.SELL,
                                   quantity=oco_short_quantity,
                                   stopPrice=tp_short_bottom_price)

    return




if __name__ == '__main__':
    request_client = RequestClient(api_key=g_api_key,
                                   secret_key=g_secret_key)

    # Start user data stream
    listen_key = request_client.start_user_data_stream()
    print("listenKey: ", listen_key)

    # Keep user data stream
    result = request_client.keep_user_data_stream()
    print("Result: ", result)

    # 데이터 스트림 닫기
    # result = request_client.close_user_data_stream()
    # print("Result: ", result)

    # 로깅 파트
    # binance-client라는 이름의 logger 생성
    logger = logging.getLogger("binance-client")
    # Info level부터 출력 할 수 있도록 셋팅
    logger.setLevel(level=logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    # 양방향 모드 ON
    hedgemode_on()
    # 기준 가격 생성
    mark_price = request_client.get_mark_price(symbol="BTCUSDT")
    mark_price = mark_price.markPrice
    # OCO 주문 가격
    oco_long_stop_price = f'{mark_price * 1.0005:0.2f}'
    oco_long_price = f'{mark_price * 1.001:0.2f}'
    oco_long_quantity = 0.001
    oco_short_stop_price = f'{mark_price * 0.9995:0.2f}'
    oco_short_price = f'{mark_price * 0.9990:0.2f}'
    oco_short_quantity = 0.001
    # OCO 주문 실행
    long, short = oco_order()
    # TP 주문 가격 > 수수료 고려 0.05% 기준에서 위아래 동일
    tp_long_top_price = f'{mark_price * 1.002:0.2f}'
    tp_long_bottom_price = f'{mark_price * 0.995:0.2f}'
    #tp_long_bottom_price = f'{mark_price * 0.9998007:0.2f}'
    #tp_short_top_price = f'{mark_price * 1.0001993:0.2f}'
    tp_short_top_price = f'{mark_price * 1.005:0.2f}'
    tp_short_bottom_price = f'{mark_price * 0.998:0.2f}'

    sub_client = SubscriptionClient(api_key=g_api_key, secret_key=g_secret_key)
    sub_client.subscribe_user_data_event(listen_key, callback, error)