import pandas as pd
import numpy as np

input = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\BTC데이터\Input_df.csv')
output = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\BTC데이터\output_df.csv')

input = input.values.tolist()
output = output.values.tolist()



print(input[0])
print(output[0])