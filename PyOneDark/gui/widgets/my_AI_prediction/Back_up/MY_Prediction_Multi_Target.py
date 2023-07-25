import os
import warnings
import pickle

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



class MY_Data_Ready():    
    # 1. 맨 마지막으로 저장된 데이터를 불러와야 함
    # 2. 맨 마지막으로 저장된 데이터에다가 Time_idx를 추가해야 함
    def __init__(self, dist=None):
        # load my_log.csv
        self.my_log = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\gui\widgets\my_AI_prediction\DataSample\my_log.csv')
        self.data = None
        self.dist = dist
        if dist == "15m":
            self.get_data_15m()
        elif dist == "1h":
            self.get_data_1h()
        elif dist == "4h":
            self.get_data_4h()
        elif dist == "1d":
            self.get_data_1d()
        else:
            print("dist is not correct")
        return self.data
    def get_data_15m(self):
        # csv data 불러오기
        df = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\gui\widgets\my_AI_prediction\DataSample\15m.csv')
        # time_idx 열 추가하기
        df['time_idx'] = df.index
        self.data = df
        return self.data
    def get_data_1h(self):
        # csv data 불러오기
        df = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\gui\widgets\my_AI_prediction\DataSample\1h.csv')
        # time_idx 열 추가하기
        df['time_idx'] = df.index
        self.data = df
        return self.data
    def get_data_4h(self):
        # csv data 불러오기
        df = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\gui\widgets\my_AI_prediction\DataSample\4h.csv')
        # time_idx 열 추가하기
        df['time_idx'] = df.index
        self.data = df
        return self.data
    def get_data_1d(self):
        # csv data 불러오기
        df = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\gui\widgets\my_AI_prediction\DataSample\1d.csv')
        # time_idx 열 추가하기
        df['time_idx'] = df.index
        self.data = df
        return self.data
    def set_path(self, path):
        self.path = path
    def set_data(self, data):
        self.data = data
    def load_data(self):
        # csv data 불러오기
        data = pd.read_csv(self.path)
        return data
    def add_time_idx(self):
        # time_idx 열 추가하기
        self.data['time_idx'] = self.data.index
        return self.data
    def update_data(self):
        # csv data 불러오기
        self.data = self.add_time_idx()
        return self.data
    # static method 생성
    @staticmethod
    def get_data_1h():
        return


class MY_Deeplearning():
    def __init__(self, data: pd.DataFrame):

        # 딥 러닝 시드를 42로 고정하는 이유 : 은하수를 위한 히치하이커 어쩌구 참조
        pl.seed_everything(42)

        self.max_prediction_length = 6 # 내가 예측하고자 하는 데이터의 길이
        self.max_encoder_length = 50 # 입력으로 사용하고자 하는 데이터의 길이 (24개로 6개 예측)
        self.batch_size = 128
        self.training_epoch = 5
        self.data = data        
        self.Dataset_ready(data = self.data)
        # self.Show_BL_peformance()
        self.Create_New_model()
        # self.Load_model()
        # self.Predict_selected(predict_start_time_idx=30)
        # self.Train_model()
        # self.Save_model()
        self.Find_hyper_parameters()
        # self.Show_Model_performance()
        # self.Show_Model_interpretation()
        # self.Predict_new()
        # 이거 해야 matplotlib 동작 함
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
        )
        self.validation = TimeSeriesDataSet.from_dataset(self.training, data, predict=True, stop_randomization=True)
        self.train_dataloader = self.training.to_dataloader(train=True, batch_size=self.batch_size, num_workers=0)
        self.val_dataloader = self.validation.to_dataloader(train=False, batch_size=self.batch_size * 10, num_workers=0)
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
        learning_rate=0.03,
        hidden_size=16,
        attention_head_size=1,
        dropout=0.1,
        hidden_continuous_size=8,
        output_size=[7, 7, 7, 7],  # 7 quantiles by default
        loss=QuantileLoss(),
        # Quantile loss는 분위수 회귀, 비선형적 예측을 할 때 사용된다고 한다.
        # log_interval=10,  # uncomment for learning rate finder and otherwise, e.g. to 10 for logging every 10 batches
        reduce_on_plateau_patience=4,
        )
        print(f"Number of parameters in network: {self.model.size()/1e3:.1f}k")
        return self.model

    def Load_model(self, state_dict_only: bool = False):
        if state_dict_only is True:
            self.model = TemporalFusionTransformer.from_dataset(
            self.training,
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
        else:
            self.model = torch.load(r"C:\Programming\python\TotheMoon\PyOneDark\Model_Storage\model.pt")
            print("전체 모델을 불러왔습니다. model.pt")

        return
    def Save_model(self, state_dict_only: bool = False):
        if state_dict_only is True:
            torch.save(self.model.state_dict(), "model_params.pt")
            print("모델의 파라미터를 저장 되었습니다. model_params.pt")
            return
        else:
            torch.save(self.model, r"C:\Programming\python\TotheMoon\PyOneDark\Model_Storage\model.pt")
            print("모델이 저장 되었습니다. model.pt")
            return
    
    # 모델 훈련 시작 (Trainer fit은 처음 부터 훈련, 미세조정은 Trainer.tune을 써야 함)
    def Train_model(self):
        # configure network and trainer
        early_stop_callback = EarlyStopping(monitor="val_loss", min_delta=1e-4, patience=10, verbose=False, mode="min")
        lr_logger = LearningRateMonitor()
        logger = TensorBoardLogger("lightning_logs")

        self.trainer = pl.Trainer(
            max_epochs=self.training_epoch,
            gpus= 0,
            enable_model_summary=True,
            gradient_clip_val=0.1,
            limit_train_batches=30,  # coment in for training, running valiation every 30 batches
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
    
    
    def Find_hyper_parameters(self):
        # 하이퍼 파라미터 최적화
        study = optimize_hyperparameters(
            self.train_dataloader,
            self.val_dataloader,
            model_path="optuna_test",
            n_trials=200,
            max_epochs=50,
            gradient_clip_val_range=(0.01, 1.0),
            hidden_size_range=(8, 128),
            hidden_continuous_size_range=(8, 128),
            attention_head_size_range=(1, 4),
            learning_rate_range=(0.001, 0.1),
            dropout_range=(0.1, 0.3),
            trainer_kwargs=dict(limit_train_batches=1.0),
            reduce_on_plateau_patience=4,
            use_learning_rate_finder=False,  # use Optuna to find ideal learning rate or use in-built learning rate finder
        )
        # save study results - also we can resume tuning at a later point in time
        with open("test_study.pkl", "wb") as fout:
            pickle.dump(study, fout)
        # show best hyperparameters
        print(study.best_trial.params)
        return

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
        
        # 새로운 데이터 예측하기
        new_raw_predictions, new_x = self.model.predict(new_prediction_data, mode="raw", return_x=True)
        self.model.plot_prediction(new_x, new_raw_predictions, idx=0, show_future_observed=False)
        return

if __name__ == "__main__":
    
    df = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\gui\widgets\my_AI_prediction\DataSample\1h.csv')
    # time_idx 열 추가하기
    df['time_idx'] = df.index
    data = df

    # data = MY_Data_Ready(dist = "1h")
    Model1 = MY_Deeplearning(data = data)


    # csv data 불러오기
