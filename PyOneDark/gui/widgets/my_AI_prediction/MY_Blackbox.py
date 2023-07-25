from MY_Prediction_Multi_Target_GPU import MY_Deeplearning
import pandas as pd



class MY_Blackbox():
    """ MY_Blackbox 클래스는
    결국 TFT 모델 매니지먼트 모듈이 되어야 함
    """
    def __init__(self, data) -> None:
        self.data = self.data_preprocess(data)
        print(self.data)
        Model = MY_Deeplearning(data = self.data, mode='Predict')
        self.prediction = Model.Run()
        self.cur_encoder_length = Model.max_encoder_length
        self.cur_decoder_length = Model.max_decoder_length

        print("현재 Encoder의 길이는 ? : ", self.cur_encoder_length)
        print("현재 Decoder의 길이는 ? : ", self.cur_decoder_length)
        print("예측 데이터는 ? : ", self.prediction)
        # self.post_process()
        # Output 값으로 Encoder의 길이와 Decoder의 길이가 나가야 함 혹은 Dataframe 안에 그거를 포함 시키는 것도 나쁘지 않을지도?!
        return

    def data_preprocess(self, data):
        """ 데이터 전처리 Method
        1. 데이터프레임에 'time_idx' 열 추가하기
        2. 데이터프레임에 상승 / 하강을 표현해주는 Bullish 열 추가하기
        """
        data['time_idx'] = data.index
        data['Bullish'] = data['Open price'] < data['Close price']

        return data

    def data_slicing(self, data: pd.DataFrame):
        data = self.data
        encoder_length = 10
        decoder_length = 5

        slices = []
        start = 0
        while start + encoder_length <= len(data):
            end = start + encoder_length
            slice = data[start:end]
            slices.append(slice)
            start += decoder_length
        print(slices)
        # 입력 Data를 Cutting 해야 함
        # Cutting 한 입력 데이터를 Model.prediction에 넣어서 결과를 예측 한다.
        # 예측 결과를 출력한다.
        return

    def post_process(self):
        data_len = len(self.data)
        interval = self.data['Kline open time'][1] - self.data['Kline open time'][0]
        
        
        print("self.prediction은 ? : ", self.prediction)
        # add OHLC from prediction
        new_data = {'Open price': self.prediction[1][0], 'High price': self.prediction[1][1], 'Low price': self.prediction[1][2], 'Close price': self.prediction[1][3]}
        new_data = pd.DataFrame(new_data)
        self.data = self.data.append(new_data, ignore_index=True)

        print(self.data)
        
        
        # Decoder & Encoder에 Marking
        encoder_indices = slice(data_len - self.cur_encoder_length, data_len - 1)
        decoder_indices = slice(data_len, None)
        self.data['encoder'] = False
        self.data.loc[encoder_indices, 'encoder'] = True
        self.data['decoder'] = False
        self.data.loc[decoder_indices, 'decoder'] = True

        # Set the 'Kline open time' column for the specified range of rows
        for i in range(data_len, data_len + self.cur_decoder_length):
            self.data.loc[i, 'Kline open time'] = self.data['Kline open time'][i-1] + interval
        print(self.data)
        self.data.to_csv(r'C:\Programming\python\TotheMoon\PyOneDark\Data_Storage\1h\test.csv', index=False)

        return self.data


# 모델 관리 모듈에는 뭐가 들어가 있어야 할까?
# > 현재 저장 된 모듈의 모든 정보가 들어가 있어야 할 것 
# > 저장된 모듈과, 현재 들어간 데이터의 Matching 작업
# 그래도 하루 반 만에 몰입하는 그림을 만들어 냈네 정민영 장하다.



if __name__ == "__main__":
    df = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\Data_Storage\1h\from200211_1200to220211_1200_1h.csv')
    data = df
    # data = MY_Data_Ready(dist = "1h")
    print("전처리 하기 전 data는 : 입니다", df)
    MY_Blackbox(data)
    