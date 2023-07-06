
# qt코어 및 API 키 임포트
from qt_core import *
from api_key import *

# 시간 관련 모듈 임포트
import datetime
import time

# 판다스
import pandas as pd

# 선물 client 생성
futures_client = UMFutures(home_key, home_secret)

class GetDatafromServer():
    def __init__(self, 
    start_time: str = "2020-01-19 12:00:00", 
    end_time: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
    dist: str= "", 
    path: str = r"C:\Programming\Python\TotheMoon\PyOneDark\Storage\Data"
    ) -> None:

        server_time = futures_client.time()
        print("현재 Binance API의 서버 시간은 : ", server_time)
        # 시간 포맷 갖고 장난
        self.start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        self.end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        self.start_time = self.start_time.strftime('%y%m%d_%H%M')
        self.end_time = self.end_time.strftime('%y%m%d_%H%M')

        # self.start_time은 start_time의 timestamp 시간
        self.start_time_ts = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))) * 1000
        # self.end_time은 end_time의 timestamp 시간
        self.end_time_ts = int(time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S'))) * 1000
        self.dist = dist
        self.path = path
        return
    
    def get_data(self):
        df = pd.DataFrame()
        while self.start_time_ts < self.end_time_ts:

            data = futures_client.klines(symbol='ETHUSDT', interval=self.dist, startTime = self.start_time_ts, limit = 500)
            data = pd.DataFrame(data)

            if self.dist == "15m":
                self.path = r'C:\Programming\python\TotheMoon\PyOneDark\Storage\Data\15m'
                self.start_time_ts += 15 * 60 * 500 * 1000
            elif self.dist == "1h":
                self.path = r'C:\Programming\python\TotheMoon\PyOneDark\Storage\Data\1h'
                self.start_time_ts += 3600 * 500 * 1000
            elif self.dist == "4h":
                self.path = r'C:\Programming\python\TotheMoon\PyOneDark\Storage\Data\4h'
                self.start_time_ts += 4 * 3600 * 500 * 1000
            elif self.dist == "1d":
                self.path = r'C:\Programming\python\TotheMoon\PyOneDark\Storage\Data\1d'
                self.start_time_ts += 24 * 3600 * 500 * 1000
            else:
                print("Wrong dist input")
                break
            # Add a delay of 0.2 seconds to avoid hitting the rate limit
            time.sleep(0.2)
            # Convert the data to a pandas DataFrame
            # df = df.append(data, ignore_index=True)
            df = pd.concat([df, data], ignore_index=True)

        # 데이터프레임 헤더 지정
        header = ['Kline open time', 'Open price', 'High price', 
        'Low price', 'Close price', 'Volume', 'Kline close time', 'Quote asset volume', 
        'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
        df = df.set_axis(header, axis=1)
        # format to datetime
        # 데이터 저장
        file_name = self.path + "\\" + 'from' + self.start_time + 'to' + self.end_time + '_' + self.dist + ".csv"
        with open(file_name, mode='w', newline='') as f:
            df.to_csv(f, index=False)
        print("데이터 저장 완료 : ", file_name)
        return df

    def set_start_time(self, start_time: str) -> None:
        self.start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        self.start_time = self.start_time.strftime('%y%m%d_%H%M')
        self.start_time_ts = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))) * 1000
        return

    def set_end_time(self, end_time: str) -> None:
        self.end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        self.end_time = self.end_time.strftime('%y%m%d_%H%M')
        self.end_time_ts = int(time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S'))) * 1000
        return

    def set_dist(self, dist: str) -> None:
        self.dist = dist
        return

    def set_path(self, path: str) -> None:
        self.path = path
        return
    
    def prepare_data_for_LTSF_input(self, df) -> pd.DataFrame:
        df['date'] = pd.to_datetime(df['Kline open time'], unit='ms')
        df['date'] = df['date'].dt.strftime('%Y-%m-%d %I:%M:%S %p')
        df['Kline open time'] = df['date']
        df = df.drop(['Kline close time', 'Quote asset volume', 'Taker buy quote asset volume', 'Ignore', 'date'], axis=1)
        file_name = self.path + "\\" + 'from' + self.start_time + 'to' + self.end_time + '_' + self.dist + 'LTSF' + ".csv"
        with open(file_name, mode='w', newline='') as f:
            df.to_csv(f, index=False)
        return df

if __name__ == "__main__":
    test_data = GetDatafromServer(dist="1d")
    test_data.set_start_time("2017-01-01 12:00:00")
    data = test_data.get_data()
    LTSF = test_data.prepare_data_for_LTSF_input(data)
