def Message_processor(msg):
    print(msg)
    if msg['e'] == 'executionReport':
        if msg['X'] == 'FILLED' and msg['S'] == 'BUY':
            purchase_price = msg['p']
            print("매수 주문이 체결되었습니다.")
            print("매도 주문을 요청하겠습니다.")
            client.create_order(
                symbol='XRPUSDT',
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=1100,
                price=set_decimal(1.003 * float(purchase_price), 5)
            )
        elif msg['X'] == 'FILLED' and msg['S'] == 'SELL':
            sale_price = msg['p']
            print("매도 주문이 체결되었습니다.")
            print("매수 주문을 요청하겠습니다.")
            client.create_order(
                symbol='XRPUSDT',
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=1100,
                price=set_decimal(0.999 * float(sale_price), 5)
            )

if __name__ == '__main__':
    init_price = set_decimal(1.002 * get_price_now('XRPUSDT'), 5)
    client.create_order(
        symbol='XRPUSDT',
        side=SIDE_SELL,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=1500,
        price=init_price
        )
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    result = request_client.post_order(symbol="BTCUSDT", side=OrderSide.SELL, positionSide="BOTH", timeInForce="GTC",
                                       ordertype=OrderType.LIMIT, quantity=3.499, price=10500, closePosition=False,
                                       reduceOnly=True)

    bm = BinanceSocketManager(client)
    # Message가 나오면 Message processor에 던져버리는 듯
    bm.start_user_socket(Message_processor)
    bm.start()
