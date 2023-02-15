import os
import warnings
import pickle

from datetime import datetime
warnings.filterwarnings("ignore")  # avoid printing out absolute paths

os.chdir("../../..")

import matplotlib.pyplot as plt
import copy 
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping, LearningRateMonitor
from pytorch_lightning.loggers import TensorBoardLogger
import torch

from pytorch_forecasting import Baseline, TemporalFusionTransformer, TimeSeriesDataSet
from pytorch_forecasting.data import GroupNormalizer, TorchNormalizer, MultiNormalizer
from pytorch_forecasting.metrics import SMAPE, PoissonLoss, QuantileLoss, MultiLoss
from pytorch_forecasting.models.temporal_fusion_transformer.tuning import optimize_hyperparameters

from pytorch_forecasting.data.examples import get_stallion_data

import tensorflow as tf
import tensorboard as tb

tf.io.gfile = tb.compat.tensorflow_stub.io.gfile
torch.set_float32_matmul_precision('medium')
# 딥 러닝 시드를 42로 고정하는 이유 : 은하수를 위한 히치하이커 어쩌구 참조
pl.seed_everything(42)

class MY_Deeplearning():
    def __init__(self, data: pd.DataFrame, mode: str = 'Train'):
        # Hyperparameter (Default value)
        self.gradient_clip_val = 0.1
        self.hidden_size = 16
        self.lstm_layers = 2
        self.dropout = 0.1
        self.hidden_continuous_size = 8
        self.attention_head_size = 1
        self.learning_rate = 0.03

        
        # Model parameter (Default value)
        self.max_prediction_length = 4 # 내가 예측하고자 하는 데이터의 길이
        self.max_encoder_length = 48 # 입력으로 사용하고자 하는 데이터의 길이
        self.batch_size = 128
        self.training_epoch = 50

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # time_idx 추가
        data['time_idx'] = data.index
        self.data = data
        self.mode = mode

        self.time = datetime.now()
        self.time = self.time.strftime("%y%m%d_%H%M")
        self.model_path = self.time + "_IN_" + str(self.max_encoder_length) + "_OUT_" + str(self.max_prediction_length) + "pt"
        
        self.Dataset_ready(data = self.data)
        return

    def Run(self, mode: str = ''):
        mode = self.mode
        if mode == 'Hyperparams':
            # self.Find_hyper_params()
            self.resume_hyper_params()
        elif mode == 'Showhyperparams':
            self.Load_hyper_params(path = '230211_2330_Open price_IN_24_OUT_6pt.pkl')
        elif mode == 'Train':
            self.Show_BL_performance()
            self.Create_New_model()
            self.Train_model()
            self.Save_model()
            self.Show_Model_performance()
            self.Show_Model_interpretation()
            self.Predict_selected(predict_start_time_idx=1000)
            self.Predict_new()
        elif mode == 'Predict':
            self.Show_BL_performance()
            self.Load_model()
            self.Show_Model_performance()
            self.Show_Model_interpretation()
            self.Predict_selected(predict_start_time_idx=1000)
            self.Predict_new()
            return
        else:
            print('Wrong mode')
        plt.show()
    
        
    # 데이터로부터 TimeSeries 데이터 셋 만들기
    def Dataset_ready(self, data: pd.DataFrame):
        training_cutoff = data["time_idx"].max() - self.max_prediction_length
        self.training = TimeSeriesDataSet(
            data[lambda x: x.time_idx <= training_cutoff],
            time_idx="time_idx",
            target=["Open price", "High price", "Low price", "Close price"],
            group_ids=["Ignore"],
            min_encoder_length=self.max_encoder_length // 2,  # keep encoder length long (as it is in the validation set)
            max_encoder_length=self.max_encoder_length,
            min_prediction_length=1,
            max_prediction_length=self.max_prediction_length,
            static_reals=["Ignore"],
            time_varying_known_reals=["time_idx", "Kline open time", "Kline close time"],
            time_varying_unknown_reals=[
                "Open price",
                "High price",
                "Low price",
                "Close price",
                "Volume",
                "Quote asset volume",
                "Number of trades",
                "Taker buy base asset volume",
                "Taker buy quote asset volume",
            ],
                target_normalizer=MultiNormalizer(
                    [GroupNormalizer(groups=["Ignore"], transformation="softplus"), GroupNormalizer(groups=["Ignore"], transformation="softplus"),
                     GroupNormalizer(groups=["Ignore"], transformation="softplus"), GroupNormalizer(groups=["Ignore"], transformation="softplus")]
            ),
            add_relative_time_idx=True,
            add_target_scales=True,
        )
        self.validation = TimeSeriesDataSet.from_dataset(self.training, data, predict=True, stop_randomization=True)
        self.train_dataloader = self.training.to_dataloader(train=True, batch_size=self.batch_size, num_workers=0, pin_memory=torch.cuda.is_available())
        self.val_dataloader = self.validation.to_dataloader(train=False, batch_size=self.batch_size * 10, num_workers=0, pin_memory=torch.cuda.is_available())
        return
        
    def Show_BL_performance(self):
        for x, (y, weight) in iter(self.val_dataloader):
            actuals = y
            break
        baseline_predictions = Baseline().predict(self.val_dataloader)
        baseline_performance = [(actuals[i] - baseline_predictions[i]).abs().mean().item() for i in range(4)]
        
        print("베이스 라인 모델의 성능:", baseline_performance)
        return

    def Create_New_model(self):
        self.model = TemporalFusionTransformer.from_dataset(
        self.training,
        lstm_layers=self.lstm_layers,
        learning_rate=self.learning_rate,
        hidden_size=self.hidden_size,
        attention_head_size=self.attention_head_size,
        dropout=self.dropout,
        hidden_continuous_size=self.hidden_continuous_size,
        output_size=[7, 7, 7, 7], # 7 quantiles by default
        loss=QuantileLoss(),
        # Quantile loss는 분위수 회귀, 비선형적 예측을 할 때 사용된다고 한다.
        # log_interval=10, # uncomment for learning rate finder and otherwise, e.g. to 10 for logging every 10 batches
        reduce_on_plateau_patience=4,
        )
        if torch.cuda.is_available():
            self.model = self.model.cuda()
        print(f"Number of parameters in network: {self.model.size()/1e3:.1f}k")
        return self.model

    def Load_model(self, state_dict_only: bool = False):
        # 현재 미사용
        if state_dict_only is True:
            self.model = TemporalFusionTransformer.from_dataset(
            self.training,
            lstm_layers=2,
            learning_rate=0.03,
            hidden_size=16,
            attention_head_size=1,
            dropout=0.1,
            hidden_continuous_size=8,
            output_size=7,  # 7 quantiles by default
            loss=QuantileLoss(),
            # Quantile loss는 분위수 회귀, 비선형적 예측을 할 때 사용된다고 한다.
            # log_interval=10,  # uncomment for learning rate finder and otherwise, e.g. to 10 for logging every 10 batches
            reduce_on_plateau_patience=4,
            )
            self.model.load_state_dict(torch.load("model_params.pt"))
            print("모델의 파라미터를 불러 왔습니다.")
        # 현재 사용
        else:
            self.model = torch.load(r"C:\Programming\python\TotheMoon\PyOneDark\Model_Storage\230211_1817_Open price_IN_24_OUT_6pt",
                                    map_location=torch.device('cuda'))
            print("전체 모델을 불러왔습니다. 230211_1817_Open price_IN_24_OUT_6pt")
        self.model.to(self.device)
        return

    def Save_model(self, state_dict_only: bool = False):
        # 그리고 Text파일로 Model에 대한 Description 동봉
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)
        # 현재 미사용
        if state_dict_only is True:
            torch.save(self.model.state_dict(), self.model_path)
            print("모델의 파라미터를 저장 되었습니다.", self.model_path)
            return
        # 현재 사용
        else:
            print("현재 directory: ", os.getcwd())            
            torch.save(self.model, f"C:\Programming\python\TotheMoon\PyOneDark\Model_Storage\{self.model_path}")
            print("모델이 저장 되었습니다.", self.model_path)
            return

    
    # 모델 훈련 시작 (Trainer fit은 처음 부터 훈련, 미세조정은 Trainer.tune을 써야 함)
    def Train_model(self):
        # configure network and trainer
        early_stop_callback = EarlyStopping(monitor="val_loss", min_delta=1e-4, patience=10, verbose=False, mode="min")
        lr_logger = LearningRateMonitor()
        logger = TensorBoardLogger("lightning_logs")

        self.trainer = pl.Trainer(
            max_epochs=self.training_epoch,
            gpus= 1,  # change 0 to 1 to utilize CUDA
            enable_model_summary=True,
            gradient_clip_val=self.gradient_clip_val,
            limit_train_batches=1.0,  # comment in for training, running valiation every 30 batches
            # fast_dev_run=True,  # comment in to check that networkor dataset has no serious 
            auto_lr_find=True,
            callbacks=[lr_logger, early_stop_callback],
            logger=logger,
        )

        self.trainer.fit(
            self.model,
            train_dataloaders=self.train_dataloader,
            val_dataloaders=self.val_dataloader,
        )
        best_model_path = self.trainer.checkpoint_callback.best_model_path
        self.model = TemporalFusionTransformer.load_from_checkpoint(best_model_path)
        return self.model

    def Find_hyper_params(self):
        # 하이퍼 파라미터 최적화
        study = optimize_hyperparameters(
            self.train_dataloader,
            self.val_dataloader,
            model_path="optuna_test",
            n_trials=100,
            max_epochs=50,
            gradient_clip_val_range=(0.01, 1.0),
            hidden_size_range=(8, 128),
            hidden_continuous_size_range=(8, 128),
            attention_head_size_range=(1, 4),
            learning_rate_range=(0.001, 0.1),
            dropout_range=(0.1, 0.3),
            trainer_kwargs=dict(limit_train_batches=1.0, gpus=1),
            reduce_on_plateau_patience=4,
            use_learning_rate_finder=False,  # use Optuna to find ideal learning rate or use in-built learning rate finder
        )
        # save study results - also we can resume tuning at a later point in time
        # 저장
        with open(f"{self.model_path}.pkl", "wb") as fout:
            pickle.dump(study, fout)
        print(study.best_trial.params)
        return

    def resume_hyper_params(self):
        with open(f"C:\Programming\\230212_2215_IN_48_OUT_4pt.pkl", "rb") as fin:
            study = pickle.load(fin)
        study.optimize(objective, n_trials=100)
        with open(f"{self.model_path}.pkl", "wb") as fout:
            pickle.dump(study, fout)
        print(study.best_trial.params)
        return

    def Load_hyper_params(self, path: str = ""):
        # 불러오기
        with open(f"230212_2215_IN_48_OUT_4pt", "rb") as fin:
            study = pickle.load(fin)
        study.optimize(objective, n_trials=100)
        print("최적의 Hyper parameter는 : ", study.best_trial.params)
        return study

    def Show_Model_performance(self):
        # 모델의 성능
        best_performance = []
        raw_predictions, x = self.model.predict(self.val_dataloader, mode="raw", return_x=True)
        predictions = self.model.predict(self.val_dataloader)
        for x, (y, weight) in iter(self.val_dataloader):
            break
        actuals = y
        for i in range(4):
            performance = (actuals[i] - predictions[i]).abs().mean().item()
            best_performance.append(performance)
        print("Best Model의 훈련 후 성능은 ? :", best_performance)
        self.model.plot_prediction(x, raw_predictions, idx=0, add_loss_to_title=True)
        return
    
    def Show_Model_interpretation(self):
        # 모델의 해석
        raw_predictions, x = self.model.predict(self.val_dataloader, mode="raw", return_x=True)
        interpretation = self.model.interpret_output(raw_predictions, reduction="sum")
        self.model.plot_interpretation(interpretation)
        return

    def Predict_selected(self, predict_start_time_idx: int):
        raw_predictions, x = self.model.predict(
        self.training.filter(lambda x: x.time_idx_first_prediction == predict_start_time_idx),
        mode="raw",
        return_x=True,
        )
        self.model.plot_prediction(x, raw_predictions, idx=0, add_loss_to_title=True)
        return

    def Predict_new(self):
        encoder_data = self.data[lambda x: x.time_idx > x.time_idx.max() - self.max_encoder_length]
        last_data = self.data[lambda x: x.time_idx == x.time_idx.max()]
        time_delta = self.data["Kline open time"].diff().mode().values[0]

        # Decoder 데이터에 Kline open time 추가
        decoder_data = pd.concat(
        [last_data.assign(**{"Kline open time": lambda x: x["Kline open time"] + time_delta * i}) for i in range(1, self.max_prediction_length + 1)],
        ignore_index=True,
        )
        # Decoder 데이터에 time_idx 추가
        decoder_data["time_idx"] = last_data["time_idx"].values[0] + decoder_data.index + 1 
        # encoder_data와 decoder_data 합치기
        new_prediction_data = pd.concat([encoder_data, decoder_data], ignore_index=True)
        
        # Raw Data 출력 및 Plot
        new_raw_predictions, new_x = self.model.predict(new_prediction_data, mode="raw", return_x=True)
        self.model.plot_prediction(new_x, new_raw_predictions, idx=0, show_future_observed=False)

        # Prediction 데이터 출력
        prediction_y, prediction_x = self.model.predict(new_prediction_data, mode="prediction", return_x=True)
        self.prediction_x = prediction_x['decoder_time_idx'].tolist()
        self.prediction_y = prediction_y.tolist()

        print("예측 데이터는 ? : ", self.prediction_y)
        print("예측 데이터의 시간은 ? : ", self.prediction_x)
        return

    def Set_hyper_params(self, gradient_clip_val, hidden_size, lstm_layers, dropout, hidden_continuous_size, attention_head_size, learning_rate):
        self.gradient_clip_val = gradient_clip_val
        self.hidden_size = hidden_size
        self.lstm_layers = lstm_layers
        self.dropout = dropout
        self.hidden_continuous_size = hidden_continuous_size
        self.attention_head_size = attention_head_size
        self.learning_rate = learning_rate
        return
    
    def Set_model_params(self, max_prediction_length, max_encoder_length, batch_size, training_epoch):
        self.max_prediction_length = max_prediction_length
        self.max_encoder_length = max_encoder_length
        self.batch_size = batch_size
        self.training_epoch = training_epoch
        return

class MY_Blackbox():
    # 여기에 아마 Model 관리하는 module도 넣으면 될 것 같음?
    def __init__(self, data) -> None:
        # We have a 3 mode in MyDeeplearning Hyperparm, Train, Predict
        Model = MY_Deeplearning(data = data, mode='Hyperparams')
        Model.Run()
        return

if __name__ == "__main__":
    df = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\Data_Storage\1h\from200211_1200to220211_1200_1h.csv')
    data = df
    # data = MY_Data_Ready(dist = "1h")
    MY_Blackbox(data)

    