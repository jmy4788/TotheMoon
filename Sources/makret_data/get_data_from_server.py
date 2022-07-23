from binance_f import RequestClient
from binance_f.constant.test import *
from datetime import datetime
import time
import csv

"""
Mission :
1. Get same interval feature data (e.g. market price, depth)
2. Get maximum data in same interval (target = 500ms interval)
3. Save the data in
"""

CSV_TITLE = datetime.now().strftime('%m%d %H%M')
print(CSV_TITLE)
#헬퍼 함수를 몇 개 만들어야 할 듯
if __name__ == '__main__':
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    head_exist = False
    while time.perf_counter() < 20:
        price_sum, depth_sum = 0, 0
        for i in range(9):
            start_time = time.perf_counter()
            mark_price = request_client.get_mark_price(symbol="BTCUSDT")
            mark_depth = request_client.get_order_book(symbol="BTCUSDT", limit=50)
            cnt, bid = 0, 0

            #여기서 generator expression 적용해보기
            for bids in mark_depth.bids:
                # bid : 매수벽
                # print(cnt, i.price, i.qty)
                cnt += 1
                bid += float(bids.qty)
            cnt, ask = 0, 0
            for asks in mark_depth.asks:
                # ask : 매도벽
                # print(cnt, i.price, i.qty)
                cnt += 1
                ask += float(asks.qty)
            price = mark_price.markPrice
            depth = bid-ask
            price_sum += price
            depth_sum += depth
            end_time = time.perf_counter()
            time.sleep(0.992 - (end_time - start_time))
        start_time2 = time.perf_counter()
        mark_price = request_client.get_mark_price(symbol="BTCUSDT")
        mark_depth = request_client.get_order_book(symbol="BTCUSDT", limit=50)
        cnt, bid = 0, 0
        for bids in mark_depth.bids:
            # bid : 매수벽
            # print(cnt, i.price, i.qty)
            cnt += 1
            bid += float(bids.qty)
        cnt, ask = 0, 0
        for asks in mark_depth.asks:
            # ask : 매도벽
            # print(cnt, i.price, i.qty)
            cnt += 1
            ask += float(asks.qty)
        price = mark_price.markPrice
        depth = bid - ask
        price_sum += price
        depth_sum += depth
        price_avg = (price_sum/10)
        depth_avg = (depth_sum/10)
        t_price = (mark_price.time / 1000)
        t_depth = (mark_depth.time / 1000)
        print('마커')
        with open(('꺼져.csv'), 'a', encoding='utf-8', newline='') as csvfile:
        #with open((fr'C:\코인\imsi{CSV_TITLE}.csv'), 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # header 없으면 header 기록해줍니다.

            print(['price', 'price_time', 'depth', 'depth_time'])
            if head_exist is False:
                writer.writerow(['price', 'price_time', 'depth', 'depth_time'])
                head_exist = True
            # 이 부분 round함수 이용하는 것에서 f 포매팅으로 소수점 첫째자리까지만 표현하는 것으로 바꿨습니다.
            writer.writerow([f'{price_avg:0.1f}', f'{t_price:0.1f}', f'{depth_avg:0.1f}',
                             f'{t_depth:0.1f}'])
        end_time2 = time.perf_counter()
        time.sleep(0.992 - (end_time2 - start_time2))


#좋은 아이디어 반복은 9까지만 하고 10은 따로 뺀다?!