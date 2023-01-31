from qt_core import *
from api_key import *
import pandas as pd
from datetime import datetime
import time


# 일단 api_key 모듈에서 home_key하고 home_secret 키를 가져오자.
spot_client = Spot(home_key, home_secret)

# 서버 타임은 현재 이 시간
server_time = spot_client.time()

# 내가 데이터를 모으고자 하는 기간
# 2021.01.19 오전 12시부터 2023.01.19 오전 12시까지의 데이터
# 아래는 timestamp 시간을 구하는 과정
"""
# Define the date and time
date_time = "2021-01-19 12:00:00"
# 1611025200000
date_time2 = "2023-01-19 12:00:00"
# 1674097200000

# Define the format of the input date and time
date_time_format = "%Y-%m-%d %H:%M:%S"

# Convert the date and time to a datetime object
date_time_obj = datetime.strptime(date_time, date_time_format)
date_time_obj2 = datetime.strptime(date_time2, date_time_format)
# Convert the datetime object to timestamp
timestamp = int(date_time_obj.timestamp())
timestamp2 = int(date_time_obj2.timestamp())
"""
# API에서 데이터를 갖고오기 위한 코드
df = pd.DataFrame()

# 1행 선언

start_time = 1611025200000
end_time = 1674097200000

while start_time < end_time:
    data = spot_client.klines(symbol='BTCUSDT', interval='1d', startTime = start_time, limit = 500)
    start_time += 24 * 3600 * 500 * 1000
    # Add a delay of 1 second
    time.sleep(2)
    print("start_time: ", start_time)
    # add data to df
    df = df.append(data, ignore_index=True)

# 헤더 추가 (1행)
header = ['Kline open time', 'Open price', 'High price', 'Low price', 'Close price', 'Volume', 'Kline close time', 
'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
df.set_axis(header, axis=1, inplace=True)
# 데이터 csv에 저장
with open('비트코인 일봉 2년치.csv', mode='w', newline='') as f:
    df.to_csv(f, index=False)