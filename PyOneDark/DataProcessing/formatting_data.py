import pandas as pd
import datetime

def process_and_save_csv(input_file, output_file):
    # 1. CSV 파일 불러오기
    df = pd.read_csv(input_file)

    # 2. 'Kline open time' 형식 변경
    df['Kline open time'] = df['Kline open time'].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S'))

    # 3. 'Kline open time' 컬럼 이름 변경
    df = df.rename(columns={'Kline open time': 'date'})

    # 4. OHLCV 데이터만 필터링
    df = df[['date', 'Open price', 'High price', 'Low price', 'Close price', 'Volume']]

    # 5. 새로운 이름으로 CSV 파일 저장
    df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

# 예제 사용법
input_path = r"C:\Users\jmy47\Downloads\BTCUSDT\Consolidated_BTCUSDT_1h.csv"  # 원본 CSV 파일 경로
output_path = r"C:\Users\jmy47\Downloads\BTCUSDT\formatted_BTCUSDT_1h.csv"  # 저장할 CSV 파일 경로
process_and_save_csv(input_path, output_path)
