# import necessary libraries
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense

# load historical data
df = pd.read_csv('bitcoin_data.csv')

# normalize the data
scaler = MinMaxScaler()
df = scaler.fit_transform(df)

# split the data into training and testing sets
train_size = int(len(df) * 0.8)
test_size = len(df) - train_size
train, test = df[0:train_size,:], df[train_size:len(df),:]

# create the LSTM or RNN model
model = Sequential()
model.add(LSTM(50, input_shape=(1, df.shape[1]), return_sequences=True))
model.add(LSTM(100))
model.add(Dense(1))

# compile and fit the model
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(train_X, train_y, epochs=100, batch_size=1, verbose=2)

# evaluate the model on the test data
test_X = test[:, 0:-1]
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
test_y = test[:, -1]
test_y = test_y.reshape((len(test_y), 1))
model.evaluate(test_X, test_y, verbose=0)

# make predictions on new data
new_data = scaler.transform(new_data)
new_data = new_data.reshape((1, 1, new_data.shape[1]))
predictions = model.predict(new_data)
predictions = scaler.inverse_transform(predictions)
