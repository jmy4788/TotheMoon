import sys
sys.path.append('../')
from qt_core import *
from api_key import *
import datetime
import time
import pandas as pd
import os

"""
2023.10.31 마지막 업데이트
바이낸스에서 데이터 다운로드 받아서 Download 폴더에 저장하는 코드
이거 한 다음에 formatting하면 PTST model에 입력 할 수 있는 코드로 바뀜
"""
futures_client = UMFutures(home_key, home_secret)

class GetDatafromServer:
    INTERVAL_TIME_DELTA = {
        '15m': 15 * 60 * 1000,
        '1h': 3600 * 1000,
        '4h': 4 * 3600 * 1000,
        '1d': 24 * 3600 * 1000
    }
    
    def __init__(self, start_time="2020-01-19 12:00:00", end_time=None, dist="15m", symbol="BTCUSDT", path=""):
        self.server_time = futures_client.time()
        self.set_time_attributes(start_time, end_time)
        self.dist = dist
        self.symbol = symbol
        self.path = os.path.join(path, symbol)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        print(f"The current server time of Binance API is: {self.server_time}")

    def set_time_attributes(self, start_time, end_time):
        if end_time is None:
            end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.start_time_ts = self.datetime_to_timestamp(start_time)
        self.end_time_ts = self.datetime_to_timestamp(end_time)
        self.start_time = self.format_datetime(start_time)
        self.end_time = self.format_datetime(end_time)

    @staticmethod
    def datetime_to_timestamp(date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S'))) * 1000

    @staticmethod
    def format_datetime(date):
        dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%Y-%m-%d')

    def get_data(self):
            df = pd.DataFrame()
            data_per_day = {
                '15m': 4*24,
                '1h': 24,
                '4h': 6,
                '1d': 1
            }
            counter = 0
            while self.start_time_ts < self.end_time_ts:
                delta = self.INTERVAL_TIME_DELTA.get(self.dist)
                if delta is None:
                    print("Wrong dist input")
                    break

                data = futures_client.klines(symbol=self.symbol, interval=self.dist, startTime=self.start_time_ts, limit=500)
                df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
                self.start_time_ts += len(data) * delta
                counter += len(data)  # count how many rows have been added
                print(f"Fetched {counter} rows so far.")
                time.sleep(3)

            if not df.empty:
                self.save_data(df)

    def save_data(self, df):
        header = ['Kline open time', 'Open price', 'High price', 'Low price', 'Close price',
                  'Volume', 'Kline close time', 'Quote asset volume', 'Number of trades',
                  'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
        df.columns = header
        file_name = os.path.join(self.path, f'Consolidated_{self.symbol}_{self.dist}.csv')
        df.to_csv(file_name, index=False)
        print(f"Data saved: {file_name}")


if __name__ == "__main__":
    download_path = os.path.expanduser("~\Downloads")
    test_data = GetDatafromServer(start_time="2019-09-10 00:00:00", dist="4h", symbol="BTCUSDT", path=download_path)
    test_data.get_data()
