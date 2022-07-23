from datetime import datetime
import pandas as pd
from binance_f import RequestClient
from binance_f.constant.test import *

def save_candle_csv(request_cleint):
    __file_path = r"C:\\Programming\\python\\TotheMoon\\Storage\\"
    __time = datetime.now().strftime('%m%d %H%M')
    __file_name = __file_path+__time+'.csv'
    result = request_client.get_candlestick_data(symbol='BTCUSDT', interval='5m')
    
    candle_col = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'CloseTime']
    df = pd.DataFrame(columns=candle_col)
    for i in result:
        i.openTime = datetime.fromtimestamp(i.openTime/1000)
        print('OpenTime : ', i.openTime)
        print('Open : ', i.open)
        print('High : ', i.high)
        print('Low : ', i.low)
        print('Close : ', i.close)
        print('CloseTime : ', i.closeTime)
        print('Volume : ', i.volume)
        one_candle = {'OpenTime': i.openTime, 'Open': i.open, 'High': i.high, 'Low': i.low, 'Close': i.close,
                      'CloseTime': i.closeTime, 'Volume': i.volume}
        df = df.append(one_candle, ignore_index=True)
    df.to_csv(__file_name, index=False)
    print("result 의 타입은 ", type(result))
    return

if __name__ == '__main__':
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    save_candle_csv(request_client)
# interval = 1m 3m 5m 15m 30m 1h 2h 4h 6h 8h 12h 1d 3d 1w 1M
# object 안에 어떤 속성들이 있는지 알아내는 함수 : dir
# candle을 DF화 시키기

#datetime.fromtimestamp()
#1. Timestamp시간을 UTC시간으로 변경하기
#2. matplotlib으로 candle 그리기
#3. 5분봉 500개 나옴
#'close', 'closeTime', 'high', 'ignore', 'json_parse', 'low', 'numTrades',
# 'open', 'openTime', 'quoteAssetVolume', 'takerBuyBaseAssetVolume', 'takerBuyQuoteAssetVolume', 'volume'

"""
Response
[
  [
    1607444700000,          // Open time
    "18879.99",             // Open
    "18900.00",             // High
    "18878.98",             // Low
    "18896.13",             // Close (or latest price)
    "492.363",              // Volume
    1607444759999,          // Close time
    "9302145.66080",        // Quote asset volume
    1874,                   // Number of trades
    "385.983",              // Taker buy volume
    "7292402.33267",        // Taker buy quote asset volume
    "0"                     // Ignore.
  ]
]
"""
