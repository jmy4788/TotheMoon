import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, LSTM, Dropout
import matplotlib.pyplot as plt
import time
import os
from datetime import datetime


class Era:
    def __init__(self, **kwargs):
        """
        Era is made of csv file.
        which will be used as input
        i am going to preprocess to train and validate deep learning model.
        :param kwargs:
        """
        self.modelname = None
        self.datapath = None
        self.epochs = 10
        self.lookback = 10
        self._model = None
        self.predictions = None
        self.pure_prediction = None

        if "modelname" in kwargs:
            self.modelname = kwargs["modelname"]
        if "datapath" in kwargs:
            self.datapath = kwargs["datapath"]
        if "epochs" in kwargs:
            self.epochs = kwargs["epochs"]
        if "lookback" in kwargs:
            self.lookback = kwargs["lookback"]

        _model_path = r"C:\Users\jmy47\OneDrive\바탕 화면\TotheMoon\Models"
        _model_list = os.listdir(_model_path)
        if self.modelname in _model_list:
            self.load_model()
        else:
            self.new_model()
        # features[0] = training, feature[1] = validation, feature[2] = test
        if self.datapath is not None:
            self.features, self.labels = self.preprocessing()

    def set_modelname(self, modelname):
        self.modelname = modelname
        self.load_model()

    def set_datapath(self, datapath):
        self.datapath = datapath
        self.features, self.labels = self.preprocessing()

    def set_epochs(self, epochs):
        self.epochs = epochs

    def set_lookback(self, lookback):
        self.lookback = lookback

    def preprocessing(self):
        df = pd.read_csv(self.datapath)
        # cols contain column data
        cols = list(df)
        # at this point, data transformed to numpy
        df = df.to_numpy()
        # load columns
        price, price_time = df[:, 0], df[:, 1]
        depth, depth_time = df[:, 2], df[:, 3]
        # min_max scaling the Data
        price = self.min_max_scale(price)
        depth = self.min_max_scale(depth)
        # create time - window data set
        features_price, labels_price = self.create_time_series_xy(price, self.lookback)
        features_depth, labels_depth = self.create_time_series_xy(depth, self.lookback)
        # concatenate price and depth to one dataset
        features = np.dstack((features_price, features_depth))
        labels = np.hstack((labels_price, labels_depth))
        # features[0] = training set, features[1] = validation set, features[2] = test set
        features = self.slicer(features)
        labels = self.slicer(labels)
        return features, labels

    @staticmethod
    def create_time_series_xy(data, look_back):
        """
        :param data: times series feature
        :param look_back: number of previous data as input
        :return: input data X(feature) and output data Y(labels)
        np.array(안에 리스트 형태로 들어가야 2d array로 출력됨)
        """
        features, labels = [], []
        size = np.shape(data)[0]
        for i in range(size - look_back):
            features.append(data[i:(i + look_back)])
            labels.append([data[i + look_back]])
        return np.array(features), np.array(labels)

    @staticmethod
    def min_max_scale(array):
        """
        :param array: Numpy Array
        :return: Numpy Array after min-max scaling
        소수점 3자리 수 까지 계산(Calculates to the third decimal place)
        """
        array_min = np.full(np.shape(array), min(array))
        array_max = np.full(np.shape(array), max(array))
        result = (array - array_min) / (array_max - array_min)
        result = np.round(result, 3)
        return result

    @staticmethod
    def slicer(array):
        """
        :param array: numpy array
        :return: training array, test array
        """
        size = np.shape(array)[0]
        train_boundary = int(size * 0.6)
        validate_boundary = int(size * 0.8)
        train = array[:train_boundary]
        validate = array[train_boundary:validate_boundary]
        test = array[validate_boundary:]
        return [train, validate, test]

    def new_model(self):
        """
        keras Input에 대해서, Batch Size에 의해 결정될 shape는 생략 가능
        loss 함수는 MSE, optimizer는 Adam이 좋은 결과를 보여준다고 해서 사용 중
        """
        inputs = keras.Input(batch_input_shape=(1, self.lookback, 2))
        x = LSTM(64, stateful=True, return_sequences=True)(inputs)
        x = Dropout(0.25)(x)
        x = LSTM(64, stateful=True, return_sequences=True)(x)
        x = Dropout(0.25)(x)
        x = LSTM(64, stateful=True)(x)
        x = Dropout(0.25)(x)
        outputs = Dense(2, activation='linear')(x)
        self._model = keras.Model(inputs=inputs, outputs=outputs, name='BTCUSDT_AI_TRADING')
        self._model.compile(loss=keras.losses.MeanSquaredError(), optimizer=keras.optimizers.Adam())
        print(self._model.summary())

    def load_model(self):
        """
        :return:
        """
        self._model = keras.models.load_model(fr"C:\Users\jmy47\OneDrive\바탕 화면\TotheMoon\Models\{self.modelname}")
        print(self._model.summary())

    def train_model(self):
        """
        모델 training > Save의 과정을 캡슐화한 함수
        여기서는 training data만을 사용해 훈련 함
        features[0], labels[0] = training data set
        validation data를 이용해서 모델의 훈련을 검증함
        feature[1], labels[1] = validation set
        """
        for i in range(self.epochs):
            print("epochs count : ", i+1)
            history = self._model.fit(self.features[0], self.labels[0], batch_size=1, shuffle=False,
                                      validation_data=(self.features[1], self.labels[1]), validation_batch_size=1)
            # error calculation to find optimal epochs
            loss = history.history['loss'][0]
            val_loss = history.history['val_loss'][0]
            error = val_loss-loss
            print(f"validation loss - real loss = {error}")
            self._model.reset_states()
        _time = datetime.now().strftime("%y%m%d_%H%M")
        name = 'LSTM64'+'_TS'+str(self.lookback)+'_EPOCH'+str(self.epochs)+'_'+_time
        self._model.save(fr"C:\Users\jmy47\OneDrive\바탕 화면\TotheMoon\Models\{name}")

    def test_model(self):
        self.predictions = self._model.predict(self.features[2], batch_size=1)

    def predict_model(self, look_ahead):
        """
        input 중 look_back 길이 만큼의 데이터를 통해 look_ahead까지의
        미래를 예측하는 함수 return은 sample과 features
        """
        # validation set의 뒤 일부분이 입력으로 들어감
        feature = self.features[1]
        print("time before prediction starting : ", time.perf_counter())
        prediction_input = feature[-self.lookback:]
        predictions = np.zeros((look_ahead, self.lookback, np.shape(feature)[2]))
        for i in range(look_ahead):
            prediction = self._model.predict(prediction_input, batch_size=1)
            predictions[i] = prediction
            prediction_input = np.vstack((prediction_input[1:], [prediction]))
        self.pure_prediction = predictions[:, 0, :]
        print("time after prediction starting : ", time.perf_counter())
        return self.pure_prediction

    def show_model(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax3 = fig.add_subplot(3, 1, 3)
        ax1.set_xlabel('Time(interval=10s)')
        ax1.set_ylabel('test set labels raw data')
        ax1.set_ylim(0, 1)
        ax2.set_xlabel('Time(interval=10s)')
        ax2.set_ylabel('test set labels predicted from model')
        ax2.set_ylim(0, 1)
        ax3.set_xlabel('Time(interval=10s)')
        ax3.set_ylabel('test setp prediction by using some validation set')
        ax3.set_ylim(0, 1)
        ax1.plot(self.labels[2])
        ax2.plot(self.predictions)
        ax3.plot(self.pure_prediction)
        plt.show()


if __name__ == '__main__':
    _data_path = r"C:\Users\jmy47\OneDrive\바탕 화면\TotheMoon\Data/"
    file_list = os.listdir(_data_path)
    csv_generator = (csv for csv in file_list if csv.endswith('.csv'))
    era = Era(epochs=100, lookback=64)
    era.set_modelname('LSTM64_TS64_EPOCH100_201109_1053')
    era.set_datapath(_data_path+'1022 1213.csv')
    """
    for path in csv_generator:
        era.set_datapath(_data_path + path)
        era.train_model()
    """
    era.test_model()
    era.predict_model(400)
    era.show_model()
