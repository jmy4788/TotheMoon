import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('C:\Programming\python\TotheMoon\PyOneDark\BTC데이터\네시간_copy.csv')

# 소수점 없애야 함
# 소수점 없애고 모두 하나의 데이터로 묶어야 함

# OHLCV의 열만 불러옴
df = df.iloc[:, 1:6]
# 인트로 바꾸어 줌
df = df.astype(int)
# 모두 하나의 데이터로 묶어줌
df = df.iloc[:, 0:5].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# Create new dataframe
New_df = pd.DataFrame()
for i in range(len(df)):
    if i+4 < len(df):
        data = df[i]+' '+df[i+1]+' '+df[i+2]+' '+df[i+3]+' '+df[i+4]
        New_df.loc[i, "New data"] = data

print(New_df)
# Save New df to csv
New_df.to_csv(r'C:\Programming\python\TotheMoon\PyOneDark\BTC데이터\New_df.csv', index=False)




"""

# 2. 우선 5개의 열을 1개의 행 데이터로 묶어야 함
# 3. 그리고 50개의 행 데이터를 1개의 행 데이터로 통합해야 함

# Number of timesteps
timesteps = 50

# Create a sliding window of size 50
input_3d = np.array([data[i:i+timesteps] for i in range(len(data)-timesteps)])
input_3d = input_3d.astype(np.int64)

# output_3d is the except the 1st 50 rows from df
output_3d = data[timesteps:]
output_3d = output_3d.astype(np.int64)


# Print the shape of the 3D array
print(input_3d.shape)
print(output_3d.shape)
print("데이터의 type은? : ", type(input_3d[0][1][0]))

print(output_3d.shape)
print(output_3d[0])
"""