import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('C:\Programming\python\TotheMoon\PyOneDark\BTC데이터\네시간_copy.csv')

# i want to use only columns 1, 2, 3, 4, 5
df = df.iloc[:, 1:6]

# Convert the dataframe to a NumPy array
data = df.to_numpy()

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