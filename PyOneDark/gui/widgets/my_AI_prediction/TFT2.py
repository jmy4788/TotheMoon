import os
import warnings

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
from pytorch_forecasting.data import GroupNormalizer
from pytorch_forecasting.metrics import SMAPE, PoissonLoss, QuantileLoss
from pytorch_forecasting.models.temporal_fusion_transformer.tuning import optimize_hyperparameters

from pytorch_forecasting.data.examples import get_stallion_data

import tensorflow as tf
import tensorboard as tb
tf.io.gfile = tb.compat.tensorflow_stub.io.gfile

# 여기서 데이터를 불러왔고
data = get_stallion_data()

# 오리지널 데이터 저장해보자
# data.to_csv(r"C:\Programming\python\TotheMoon\PyOneDark\gui\widgets\my_AI_prediction\DataSample\original_data.csv", index=False)

# Time index 설정
# Time index는 데이터를 월별로 보여줌
data["time_idx"] = data["date"].dt.year * 12 + data["date"].dt.month
data["time_idx"] -= data["time_idx"].min()

# add additional features
data["month"] = data.date.dt.month.astype(str).astype("category")  # categories have be strings
data["log_volume"] = np.log(data.volume + 1e-8)
data["avg_volume_by_sku"] = data.groupby(["time_idx", "sku"], observed=True).volume.transform("mean")
data["avg_volume_by_agency"] = data.groupby(["time_idx", "agency"], observed=True).volume.transform("mean")

# we want to encode special days as one variable and thus need to first reverse one-hot encoding
special_days = [
    "easter_day",
    "good_friday",
    "new_year",
    "christmas",
    "labor_day",
    "independence_day",
    "revolution_day_memorial",
    "regional_games",
    "fifa_u_17_world_cup",
    "football_gold_cup",
    "beer_capital",
    "music_fest",
]
data[special_days] = data[special_days].apply(lambda x: x.map({0: "-", 1: x.name})).astype("category")

data.sample(10, random_state=521)
# 일단 여기까지만 하고 다시 저장
# data.to_csv(r"C:\Programming\python\TotheMoon\PyOneDark\gui\widgets\my_AI_prediction\DataSample\preprocess_data.csv", index=False)


"""
다음 단계는 데이터 프레임을 PyTorch Forecasting TimeSeriesDataSet로 변환하는 것입니다.
어떤 기능이 범주형인지 연속형인지, 어떤 기능이 정적인지 시간에 따라 변하는지 데이터셋에 알리는 것 외에도 데이터를 정규화하는 방법도 결정해야 합니다.
여기에서 각 시계열을 개별적으로 표준 척도화하고 값이 항상 양수임을 나타냅니다.
일반적으로 훈련할 때 각 인코더 시퀀스에서 동적으로 크기를 조정하는 EncoderNormalizer는 정규화로 인한 미리 보기 편향을 피하기 위해 선호됩니다.
그러나 예를 들어 데이터에 0이 많기 때문에 합리적으로 안정적인 정규화를 찾는 데 문제가 있는 경우 미리 보기 편향을 허용할 수 있습니다.
또는 추론에서 보다 안정적인 정규화를 기대합니다.
후자의 경우 추론을 실행할 때 존재하지 않는 "이상한" 점프를 배우지 않도록 하여 보다pip 현실적인 데이터 세트에서 훈련합니다.
"""
max_prediction_length = 6
max_encoder_length = 24
training_cutoff = data["time_idx"].max() - max_prediction_length

training = TimeSeriesDataSet(
    data[lambda x: x.time_idx <= training_cutoff],
    time_idx="time_idx",
    target="volume",
    group_ids=["agency", "sku"],
    min_encoder_length=max_encoder_length // 2,  # keep encoder length long (as it is in the validation set)
    max_encoder_length=max_encoder_length,
    min_prediction_length=1,
    max_prediction_length=max_prediction_length,
    static_categoricals=["agency", "sku"],
    static_reals=["avg_population_2017", "avg_yearly_household_income_2017"],
    time_varying_known_categoricals=["special_days", "month"],
    variable_groups={"special_days": special_days},  # group of categorical variables can be treated as one variable
    time_varying_known_reals=["time_idx", "price_regular", "discount_in_percent"],
    time_varying_unknown_categoricals=[],
    time_varying_unknown_reals=[
        "volume",
        "log_volume",
        "industry_volume",
        "soda_volume",
        "avg_max_temp",
        "avg_volume_by_agency",
        "avg_volume_by_sku",
    ],
    target_normalizer=GroupNormalizer(
        groups=["agency", "sku"], transformation="softplus"
    ),  # use softplus and normalize by group
    add_relative_time_idx=True,
    add_target_scales=True,
    add_encoder_length=True,
)

# create validation set (predict=True) which means to predict the last max_prediction_length points in time
# for each series
validation = TimeSeriesDataSet.from_dataset(training, data, predict=True, stop_randomization=True)

# create dataloaders for model
batch_size = 128  # set this between 32 to 128
train_dataloader = training.to_dataloader(train=True, batch_size=batch_size, num_workers=0)
val_dataloader = validation.to_dataloader(train=False, batch_size=batch_size * 10, num_workers=0)

"""
마지막으로 관찰된 볼륨을 반복하여 다음 6개월을 예측하는 기본 모델을 평가하면
우리가 능가하려는 간단한 벤치마크를 얻을 수 있습니다.
"""

# calculate baseline mean absolute error, i.e. predict next value as the last available value from the history
actuals = torch.cat([y for x, (y, weight) in iter(val_dataloader)])
baseline_predictions = Baseline().predict(val_dataloader)
# BaseLine prediction의 성능 검증
print((actuals - baseline_predictions).abs().mean().item())


# configure network and trainer
# 딥 러닝 시드를 42로 고정하는 이유 : 은하수를 위한 히치하이커 어쩌구 참조
pl.seed_everything(42)

trainer = pl.Trainer(
    gpus=0,
    # clipping gradients is a hyperparameter and important to prevent divergance
    # of the gradient for recurrent neural networks
    gradient_clip_val=0.1,
)

tft = TemporalFusionTransformer.from_dataset(
    training,
    # not meaningful for finding the learning rate but otherwise very important
    learning_rate=0.03,
    hidden_size=16,  # most important hyperparameter apart from learning rate
    # number of attention heads. Set to up to 4 for large datasets
    attention_head_size=1,
    dropout=0.1,  # between 0.1 and 0.3 are good values
    hidden_continuous_size=8,  # set to <= hidden_size
    output_size=7,  # 7 quantiles by default
    loss=QuantileLoss(),
    # reduce learning rate if no improvement in validation loss after x epochs
    reduce_on_plateau_patience=4,
)
print(f"Number of parameters in network: {tft.size()/1e3:.1f}k")

# 최적의 Leraning rate 파라미터 찾는 기능
res = trainer.tuner.lr_find(
    tft,
    train_dataloaders=train_dataloader,
    val_dataloaders=val_dataloader,
    max_lr=1,
    min_lr=1e-6,
)

print(f"suggested learning rate: {res.suggestion()}")
fig = res.plot(show=True, suggest=True)
fig.show()

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
    max_epochs=5,
    gpus= 0,
    enable_model_summary=True,
    gradient_clip_val=0.1,
    limit_train_batches=30,  # coment in for training, running valiation every 30 batches
    # fast_dev_run=True,  # comment in to check that networkor dataset has no serious bugs
    callbacks=[lr_logger, early_stop_callback],
    logger=logger,
)


tft = TemporalFusionTransformer.from_dataset(
    training,
    learning_rate=0.03,
    hidden_size=16,
    attention_head_size=1,
    dropout=0.1,
    hidden_continuous_size=8,
    output_size=7,  # 7 quantiles by default
    loss=QuantileLoss(),
    log_interval=10,  # uncomment for learning rate finder and otherwise, e.g. to 10 for logging every 10 batches
    reduce_on_plateau_patience=4,
)
print(f"Number of parameters in network: {tft.size()/1e3:.1f}k")

# fit network
trainer.fit(
    tft,
    train_dataloaders=train_dataloader,
    val_dataloaders=val_dataloader,
)

print("여기는 진입 했으려나?!")
# load the best model according to the validation loss
# (given that we use early stopping, this is not necessarily the last epoch)
best_model_path = trainer.checkpoint_callback.best_model_path
best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)

actuals = torch.cat([y[0] for x, y in iter(val_dataloader)])
predictions = best_tft.predict(val_dataloader)
print("TFT model prediction result : ", (actuals - predictions).abs().mean())

raw_predictions, x = best_tft.predict(val_dataloader, mode="raw", return_x=True)
# print("입력값 x = :", x)
# x 인코더 타겟 = : torch.Size([350, 24])

for idx in range(10):  # plot 10 examples
    print(idx)
    fig = best_tft.plot_prediction(x, raw_predictions, idx=idx, add_loss_to_title=True)
plt.show()