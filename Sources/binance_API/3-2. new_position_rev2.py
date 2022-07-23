import sys
import logging
from binance_f import RequestClient
from binance_f import SubscriptionClient
from binance_f.constant.test import *
from binance_f.model import *
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.base.printobject import *
import time
from queue import Queue
from threading import Thread


class OrderHandler:
    def __init__(self, client):
        self.client = client
        self.quantity = 0.01
        self.market_price = 0
        self.long = None
        self.short = None

    def init_order(self):
        self.market_price = self.client.get_mark_price(symbol="BTCUSDT")
        self.market_price = self.market_price.markPrice
        # TRIGGER / BUY PRICE
        long_stop_price = f'{self.market_price * 1.0015:0.2f}'
        short_stop_price = f'{self.market_price * 0.9985:0.2f}'
        # PLACE ORDER IN BOTH SIDE
        self.long = self.client.post_order(symbol="BTCUSDT", timeInForce=TimeInForce.GTC,
                                           ordertype=OrderType.STOP_MARKET,
                                           positionSide=PositionSide.LONG, side=OrderSide.BUY,
                                           quantity=self.quantity,
                                           stopPrice=long_stop_price)
        self.short = self.client.post_order(symbol="BTCUSDT", timeInForce=TimeInForce.GTC,
                                            ordertype=OrderType.STOP_MARKET,
                                            positionSide=PositionSide.SHORT, side=OrderSide.SELL,
                                            quantity=self.quantity,
                                            stopPrice=short_stop_price)
        return

    def close_pos_order(self, position_order):
        # 수수료 고려시 익절과 손절에서의 양 같음
        """
        long_tp_price = f'{self.market_price * 1.002:0.2f}'
        long_stop_price = f'{self.market_price * 0.9998007:0.2f}'
        short_tp_price = f'{self.market_price * 1.0001993:0.2f}'
        short_stop_price = f'{self.market_price * 0.998:0.2f}'
        """
        long_tp_price = f'{self.market_price * 1.0025:0.2f}'
        long_stop_price = f'{self.market_price * 0.993:0.2f}'
        short_tp_price = f'{self.market_price * 1.007:0.2f}'
        short_stop_price = f'{self.market_price * 0.9975:0.2f}'
        if position_order.positionSide == "LONG":
            print("남아있는 LONG포지션에 대한 매도를 실행합니다.")
            time.sleep(0.2)
            tp = self.client.post_order(symbol="BTCUSDT", timeInForce=TimeInForce.GTC,
                                        ordertype=OrderType.TAKE_PROFIT_MARKET,
                                        positionSide=PositionSide.LONG,
                                        side=OrderSide.SELL,
                                        quantity=self.quantity,
                                        stopPrice=long_tp_price)
            time.sleep(0.2)
            stop = self.client.post_order(symbol="BTCUSDT",
                                          timeInForce=TimeInForce.GTC,
                                          ordertype=OrderType.STOP_MARKET,
                                          positionSide=PositionSide.LONG,
                                          side=OrderSide.SELL,
                                          quantity=self.quantity,
                                          stopPrice=long_stop_price)
        elif position_order.positionSide == "SHORT":
            print("남아있는 SHORT포지션에 대한 매도를 실행합니다.")
            time.sleep(0.2)
            tp = self.client.post_order(symbol="BTCUSDT",
                                        timeInForce=TimeInForce.GTC,
                                        ordertype=OrderType.TAKE_PROFIT_MARKET,
                                        positionSide=PositionSide.SHORT,
                                        side=OrderSide.BUY,
                                        quantity=self.quantity,
                                        stopPrice=short_stop_price)
            time.sleep(0.2)
            stop = self.client.post_order(symbol="BTCUSDT",
                                          timeInForce=TimeInForce.GTC,
                                          ordertype=OrderType.STOP_MARKET,
                                          positionSide=PositionSide.SHORT,
                                          side=OrderSide.BUY,
                                          quantity=self.quantity,
                                          stopPrice=short_tp_price)

        return tp, stop


class EventHandler(Thread):
    def __init__(self, client, queue):
        super().__init__()
        self.order = OrderHandler(client)
        self.queue = queue
        self.close_order_list = list()
        self.position_filled = False
        self.close_order = False
        self.cycle_done = False

    def run(self) -> None:
        self.order.init_order()
        while True:
            if self.cycle_done is True:
                self.order.init_order()
                self.cycle_done = False
            data_type, event = self.queue.get()
            self.print_event(data_type, event)
            self.open_position(data_type, event)
            if self.close_order_list:
                stop = self.close_order_list.pop()
                tp = self.close_order_list.pop()
            if self.close_order is True:
                self.sell_position(data_type, event, stop, tp)
                time.sleep(0.2)

    def open_position(self, data_type, event):
        if data_type == SubscribeMessageType.PAYLOAD:
            if event.eventType == "ORDER_TRADE_UPDATE":
                if event.orderId == self.order.long.orderId and event.orderStatus == 'FILLED':
                    print("롱 오더가 체결되었습니다. 숏 오더를 취소하겠습니다.")
                    self.position_filled = True
                    cancel_order(self.order.short)
                    time.sleep(0.2)
                    tp, stop = self.order.close_pos_order(self.order.long)
                    self.close_order = True
                    self.close_order_list.append(tp)
                    self.close_order_list.append(stop)
                elif event.orderId == self.order.short.orderId and event.orderStatus == 'FILLED':
                    print("숏 오더가 체결되었습니다. 롱 오더를 취소하겠습니다.")
                    self.position_filled = True
                    cancel_order(self.order.long)
                    time.sleep(0.2)
                    tp, stop = self.order.close_pos_order(self.order.short)
                    self.close_order = True
                    self.close_order_list.append(tp)
                    self.close_order_list.append(stop)

    def sell_position(self, data_type, event, stop, tp):
        if data_type == SubscribeMessageType.PAYLOAD:
            if event.eventType == "ORDER_TRADE_UPDATE":
                if event.orderId == tp.orderId and event.orderStatus == 'FILLED':
                    print("Take profit 주문이 체결되었습니다. Stop loss주문을 Cancel합니다.")
                    cancel_order(stop)
                    self.close_order = False
                    self.cycle_done = True
                elif event.orderId == stop.orderId and event.orderStatus == 'FILLED':
                    print("Stop loss 주문이 체결되었습니다. Take profit 주문을 Cancel합니다.")
                    cancel_order(tp)
                    self.close_order = False
                    self.cycle_done = True

    def print_event(self, data_type, event):
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
            elif event.eventType == "listenKeyExpired":
                print("Event: ", event.eventType)
                print("Event time: ", event.eventTime)
                print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
                print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
                print("CAUTION: YOUR LISTEN-KEY HAS BEEN EXPIRED!!!")
        else:
            print("Unknown Data:")
        print()


def cancel_order(order):
    request_client.cancel_order(symbol='BTCUSDT', orderId=order.orderId)
    return


def callback(data_type: 'SubscribeMessageType', event: 'any'):
    response = data_type, event
    queue.put(response)


def error(e: 'BinanceApiException'):
    print(e.error_code + e.error_message)


def hedge_on():
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


def current_pos_check(client):
    positions = client.get_position()
    for pos in positions:
        if pos.symbol == 'BTCUSDT':
            if pos.positionAmt == 0:
                print("현재 포지션 없음.")
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
                    choice = input("현재 포지션이 존재합니다. CLOSE 하시겠습니까? (Y/N): ")
                    if choice == 'Y' or choice == 'y':
                        # 여기에 CLOSE POS
                        close = request_client.post_order(symbol="BTCUSDT", side=OrderSide.SELL,
                                                          positionSide=pos.positionSide,
                                                          ordertype=OrderType.LIMIT, timeInForce="GTC",
                                                          price=pos.entryPrice, quantity=pos.positionAmt)
                        PrintBasic.print_obj(close)
                        break
                    elif choice == 'N' or choice == 'n':
                        print("포지션을 유지하겠습니다. 프로그램을 종료합니다.")
                        sys.exit()


if __name__ == '__main__':
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

    # 유저 스트림 시작
    listen_key = request_client.start_user_data_stream()
    print("listenKey: ", listen_key)

    # 유저 스트림 유지
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
    hedge_on()
    # 현재 열려있는 포지션 확인 및 CLOSE
    current_pos_check(request_client)
    queue = Queue()
    sub_client = SubscriptionClient(api_key=g_api_key, secret_key=g_secret_key)
    sub_client.subscribe_user_data_event(listen_key, callback, error)
    handler = EventHandler(request_client, queue)
    handler.start()
    handler.join()
