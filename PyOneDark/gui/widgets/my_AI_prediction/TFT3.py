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
from pytorch_forecasting.data import GroupNormalizer, TorchNormalizer
from pytorch_forecasting.metrics import SMAPE, PoissonLoss, QuantileLoss, MultiLoss
from pytorch_forecasting.models.temporal_fusion_transformer.tuning import optimize_hyperparameters
from pytorch_forecasting.data.examples import get_stallion_data

import tensorflow as tf
import tensorboard as tb
tf.io.gfile = tb.compat.tensorflow_stub.io.gfile


# csv data 불러오기
df = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\gui\widgets\my_AI_prediction\DataSample\1h.csv')
# time_idx 열 추가하기
df['time_idx'] = df.index
data = df
data.sample(10, random_state=521)
# print(data.describe())

"""
다음 단계는 데이터 프레임을 PyTorch Forecasting TimeSeriesDataSet로 변환하는 것입니다.
어떤 기능이 범주형인지 연속형인지, 어떤 기능이 정적인지 시간에 따라 변하는지 데이터셋에 알리는 것 외에도 데이터를 정규화하는 방법도 결정해야 합니다.
여기에서 각 시계열을 개별적으로 표준 척도화하고 값이 항상 양수임을 나타냅니다.
일반적으로 훈련할 때 각 인코더 시퀀스에서 동적으로 크기를 조정하는 EncoderNormalizer는 정규화로 인한 미리 보기 편향을 피하기 위해 선호됩니다.
그러나 예를 들어 데이터에 0이 많기 때문에 합리적으로 안정적인 정규화를 찾는 데 문제가 있는 경우 미리 보기 편향을 허용할 수 있습니다.
또는 추론에서 보다 안정적인 정규화를 기대합니다.
후자의 경우 추론을 실행할 때 존재하지 않는 "이상한" 점프를 배우지 않도록 하여 보다pip 현실적인 데이터 세트에서 훈련합니다.
"""

# 6은 내가 예측하고자 하는 최대의 넘버, 예를 들어 1시간봉이라고 하면 6개?
max_prediction_length = 6
# max_encoder_length is the length of the encoder sequence, i.e. the number of time steps the RNN sees before making a prediction
# 는 결국에, 내가 입력으로 사용하고자 하는 데이터의 길이를 의미한다.
max_encoder_length = 24
training_cutoff = data["time_idx"].max() - max_prediction_length
# *** Time series 데이터 생성 ***
training = TimeSeriesDataSet(
    data[lambda x: x.time_idx <= training_cutoff],
    time_idx="time_idx",
    target="Close price",
    group_ids=["Ignore"],
    min_encoder_length=max_encoder_length // 2,  # keep encoder length long (as it is in the validation set)
    max_encoder_length=max_encoder_length,
    min_prediction_length=1,
    max_prediction_length=max_prediction_length,
    # static_categoricals=["agency", "sku"],
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
        target_normalizer=GroupNormalizer(
        groups=["Ignore"], transformation="softplus"
    ),
    # 멀티 노멀라이즈 가능한 것인지?!
    # target_normalizer=MultiNormalizer([TorchNormalizer(), TorchNormalizer(), TorchNormalizer(), TorchNormalizer(), TorchNormalizer()])
)
# *** Time series 데이터 생성 ***


# create validation set (predict=True) which means to predict the last max_prediction_length points in time
# for each series

validation = TimeSeriesDataSet.from_dataset(training, data, predict=True, stop_randomization=True)
print("validation은 어떤 데이터 형태를 지니는 것이지? : ", validation)

# create dataloaders for model
batch_size = 128  # set this between 32 to 128
# 배치사이즈가 128이라는건, 즉 128개씩 끊어서 학습하겠다는 것

train_dataloader = training.to_dataloader(train=True, batch_size=batch_size, num_workers=0)
# train_dataloader = <torch.utils.data.dataloader.DataLoader object at 0x000001B47DC8F730>
val_dataloader = validation.to_dataloader(train=False, batch_size=batch_size * 10, num_workers=0)


"""
마지막으로 관찰된 볼륨을 반복하여 다음 6개월을 예측하는 기본 모델을 평가하면
우리가 능가하려는 간단한 벤치마크를 얻을 수 있습니다.
"""
# calculate baseline mean absolute error, i.e. predict next value as the last available value from the history
"""
targets = []
for x, (y, weight) in iter(val_dataloader):
    for i in range(5):
        targets.append(y[i])
actuals = torch.cat(targets)
"""
# Base line model의 성능 검증을 위한 코드
actuals = torch.cat([y for x, (y, weight) in iter(val_dataloader)])
baseline_predictions = Baseline().predict(val_dataloader)
print("BaseLine model의 성능은? : ", (actuals - baseline_predictions).abs().mean().item())

# 참조
# Actual 값은 아래와 같은 형태로 나옴
# tensor([[20763.6602, 20748.0391, 20810.1797, 20814.8203, 20828.5898, 20834.9805]])


# configure network and trainer
# 딥 러닝 시드를 42로 고정하는 이유 : 은하수를 위한 히치하이커 어쩌구 참조
pl.seed_everything(42)




"""
TemporalFusionTransformer의 경우 최적 학습률이 제안된 것보다 약간 낮은 것으로 보입니다.
또한 PyTorch Lightning은 때때로
낮은 학습 속도의 노이즈로 인해 혼동을 일으키고 너무 낮은 속도를 제안할 수 있기 때문에 제안된 학습 속도를 직접 사용하고 싶지 않습니다.
수동 제어가 필수적입니다. 학습률로 0.03을 선택하기로 결정합니다.
"""


# configure network and trainer
early_stop_callback = EarlyStopping(monitor="val_loss", min_delta=1e-4, patience=10, verbose=False, mode="min")
lr_logger = LearningRateMonitor()  # log the learning rate
logger = TensorBoardLogger("lightning_logs")  # logging results to a tensorboard

trainer = pl.Trainer(
    max_epochs=50,
    gpus= 0,
    enable_model_summary=True,
    # gradient_clip_val 0.1 -> 1로 바꿨음
    auto_lr_find=True,
    gradient_clip_val=0.1,
    limit_train_batches=30,  # coment in for training, running valiation every 30 batches
    # fast_dev_run=True,  # comment in to check that networkor dataset has no serious bugs
    callbacks=[lr_logger, early_stop_callback],
    logger=logger,
)

# Quantile loss는 분위수 회귀, 비선형적 예측을 할 때 사용된다고 한다.

# Local 저장된 모델 불러오기
# tft = TemporalFusionTransformer()
# tft.load_state_dict(torch.load('best_model.pt'))

# 새로운 모델 생성

tft = TemporalFusionTransformer.from_dataset(
    training,
    learning_rate=0.03,
    hidden_size=16,
    attention_head_size=1,
    dropout=0.1,
    hidden_continuous_size=8,
    output_size=7,  # 7 quantiles by default
    loss=QuantileLoss(),
    # log_interval=10,  # uncomment for learning rate finder and otherwise, e.g. to 10 for logging every 10 batches
    reduce_on_plateau_patience=4,
)

print(f"Number of parameters in network: {tft.size()/1e3:.1f}k")


# 모델 훈련하기

trainer.fit(
    tft,
    train_dataloaders=train_dataloader,
    val_dataloaders=val_dataloader,
)

# load the best model according to the validation loss
# (given that we use early stopping, this is not necessarily the last epoch)
best_model_path = trainer.checkpoint_callback.best_model_path
best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)


# 하이퍼 파라미터 최적화
# create study
study = optimize_hyperparameters(
    train_dataloader,
    val_dataloader,
    model_path="optuna_test",
    n_trials=200,
    max_epochs=50,
    gradient_clip_val_range=(0.01, 1.0),
    hidden_size_range=(8, 128),
    hidden_continuous_size_range=(8, 128),
    attention_head_size_range=(1, 4),
    learning_rate_range=(0.001, 0.1),
    dropout_range=(0.1, 0.3),
    trainer_kwargs=dict(limit_train_batches=30),
    reduce_on_plateau_patience=4,
    use_learning_rate_finder=False,  # use Optuna to find ideal learning rate or use in-built learning rate finder
)

# save study results - also we can resume tuning at a later point in time
with open("test_study.pkl", "wb") as fout:
    pickle.dump(study, fout)

# show best hyperparameters
print(study.best_trial.params)


# 트레이닝 끝난 이후 모델 저장
# torch.save(best_tft.state_dict(), 'best_model.pt')


# best model을 local에 저장하는 함수
# best_tft.save_checkpoint("best_tft_model.pt")
# 내가 궁금한 것 : 계속 추가되는 데이터가 있을 때 작은 Data set을 계속해서 Model에 훈련시켜도 Model의 성능에 영향은 없을까?
# 검증 할 수 있는 방법 : Referece model을 local 에 저장해놓고, 새로운 Dataset을 학습 했을 때와 학습 안 했을 때의 성능을 비교하는 것
# 그리고 추가 학습을 했을 때, 기존 데이터에 대한 성능과 새로운 데이터에 대한 성능 2가지를 모두 비교해보아야 할 필요가 있음

# 2023.01.29 일요일
# 아래 부분이 결국에 훈련된 모델을 이용해서 예측 값을 뽑아내는 부분이기 때문에 가장 중요한 부분이 될 거네
# 모델 훈련은 끝난 상태

# 모델의 성능 검증
actuals = torch.cat([y[0] for x, y in iter(val_dataloader)])
print("val_dataloader로 부터 뽑아낸 실제 값은? : ", actuals)
predictions = best_tft.predict(val_dataloader)
print("val_dataloader로 부터 뽑아낸 best_tft 모델의 예측 값은?: ", predictions)
print("best tft model의 훈련 후 성능 : ", (actuals - predictions).abs().mean())

# 모델의 예측 값
raw_predictions, x = best_tft.predict(val_dataloader, mode="raw", return_x=True)


# print("x = model의 입력 :", x)
# decoder_time_idx = x['decoder_time_idx'].reshape(-1, 1)

# print("raw_predictions = model의 출력 :", raw_predictions)

# print("x 인코더 타겟의 dimension = :", x['encoder_target'].shape)
# print("디코더의 time idx :", decoder_time_idx)

#for idx in range(10):  # plot 10 examples
# fig, ax = plt.subplots()

# 이 plot_prediction 좆같은 코드가 안돌아가는게 현재 문제임
best_tft.plot_prediction(x, raw_predictions, idx=0, add_loss_to_title=True)

# 변수별로 뭐가 중요한지 확인하는 것 같은데 잘 모르겠다.
# predictions_vs_actuals = best_tft.calculate_prediction_actual_by_variable(x, predictions)
# best_tft.plot_prediction_actual_by_variable(predictions_vs_actuals)

"""
변수 중요도
이 모델은 아키텍처 구축 방식으로 인해 해석 기능이 내장되어 있습니다.
어떻게 보이는지 봅시다.
먼저 interpret_output()으로 해석을 계산하고 이후에 plot_interpretation()으로 플롯합니다.
"""
interpretation = best_tft.interpret_output(raw_predictions, reduction="sum")
best_tft.plot_interpretation(interpretation)

# 이거 plt.show()해야지 그림 그려짐
plt.show()


# 1. 2023.01.29 내가 잠정적으로 내린 결론은, Pytorch의 포장된 data들을 내가 분석 / 가공 해서 사용하기는 상당히 어려울 것 같다
# 2. 다만 predict가 제공하는 것은 비교할 수 있기 때문에 해당 기능을 사용하면 될 수도 ? 
# 3. 입력 데이터 확인하는 방법하고, 이제 plt.show()추가해서 plot까지는 되는데 왜 plot_prediction idx = 1이되면 에러가 나는지 확인해야함
# 4. 3번에 대한 에러 이유는 애초에 3번은 단위 시간당 데이터가 적어도 340개는 있는 놈 이었음 내거에서는 에러 났던 것이 당연
# 
# 회색은 attention인 것 같음

# 아래는 Wrost performer를 그리는 코드
# mean_losses = SMAPE(reduction="none")(predictions, actuals).mean(1)
# indices = mean_losses.argsort(descending=True)  # sort losses
# best_tft.plot_prediction(x, raw_predictions, idx=indices, add_loss_to_title=SMAPE(quantiles=best_tft.loss.quantiles))