from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

import time
import csv
import pandas as pd

request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)

#timestamp의 타임은 1970년을 기준으로 한 누적초
#윈도우에서는 timestamp 형태의 시간을 1000으로 Divide해야 함


def init():

    return liens


def callback(frame):
    mark_price = request_client.get_mark_price(symbol="BTCUSDT")
    mark_depth = request_client.get_order_book(symbol="BTCUSDT", limit=10)
    t1 = (mark_price.time / 1000)
    t2 = t1 - curtime
    with open('data.csv', 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([mark_price.markPrice, t1])
    xdata.append(t2)
    ydata.append(mark_price.markPrice)
    ln.set_data(xdata, ydata)
    time.sleep(1)
    return ln,


if __name__ == '__main__':
    fig, ax = plt.subplots()

    xdata, ydata = [], []
    ln, = plt.plot([], [])

    curtime = time.time()
    while True:
        """ matplotlib에서 Animation으로 Plot하는 함수 내부에
        market price request 하는 기능과 Data를 CSV로 Save하는 기능이
        포함되어 있음, interval = 1초 """
        ani = FuncAnimation(fig, callback, init_func=init, blit=True)
        plt.show()





