from qt_core import *
from api_key import *

# 시간 관련 모듈 임포트
import datetime
import time

# 판다스
import pandas as pd

# 선물 client 생성
futures_client = UMFutures(home_key, home_secret)
exchange_info = futures_client.exchange_info()
print(exchange_info.rateLimits)
# 서버 타임은 현재 이 시간