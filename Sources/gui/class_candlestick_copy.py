from pyside6_modules import *
import pandas as pd
import time

from binance_f import RequestClient
from binance_f.constant.test import *



class Worker(QThread):
    price = Signal(object)
    def __init__(self, df):
        super().__init__()
        self.initial_candle = df

    def run(self):
        __last_candle_opentime = self.initial_candle[-1].openTime
        request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
        while True:
            cur_price = request_client.get_candlestick_data(symbol='BTCUSDT', interval='1m', limit= 1)
            if __last_candle_opentime == cur_price[0].openTime:
                print("새로운 Candlestick이 없습니다")
                time.sleep(10)
            else:
                print("새로운 Candlestick이 나타났습니다.")
                # __last_candle_opentime을 여기서 update 해버림
                __last_candle_opentime = cur_price[0].openTime
                self.price.emit(cur_price)
                time.sleep(10)


class MyChart(QChartView):
    def __init__(self):
        super().__init__()
        self.initial_chart()
        self.show()


    def initial_chart(self):
        
        # get data from binance
        request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
        self.candledf = request_client.get_candlestick_data(symbol='BTCUSDT', interval='1m')

        # Candlestick series > Candlestick set의 모음
        self.series = QCandlestickSeries()
        
        # Color
        __binance_red = QColor(195, 62, 80)
        __binance_green = QColor(95, 189, 123)
        __white = QColor(255, 255, 255)
        self.series.setIncreasingColor(__binance_green)
        self.series.setDecreasingColor(__binance_red)
        self.series.setBodyOutlineVisible(False)
        self.series.setPen(__white)

        # Binance candlestick obejct의 method 'close', 'closeTime', 'high', 'ignore', 'json_parse', 'low', 'numTrades', 'open', 'openTime', 'quoteAssetVolume', 'takerBuyBaseAssetVolume', 'takerBuyQuoteAssetVolume', 'volume'
        # initial OHLC feeding
        for ohlc in self.candledf:
            open = float(ohlc.open)
            high = float(ohlc.high)
            low = float(ohlc.low)
            close = float(ohlc.close)
            # 이미 내 코드에서는 opentime이 timestamp 형식으로 되어 있음
            ts = float(ohlc.openTime)
            elem = QCandlestickSet(open, high, low, close, ts)
            self.series.append(elem)

        # chart object legend : 범례
        self.chart = QChart()
        self.chart.legend().hide()
        # data feeding
        self.chart.addSeries(self.series)
        # axis
        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("hh:mm:ss")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)
        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%i")
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)
        # margin
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        # setchart
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        
    @Slot(object)
    def update_chart(self, cur_price):

        # 1. Series에서 Axis를 제거
        print("Series에서 Axis를 제거하겠습니다.")
        self.series.detachAxis(self.axis_x)
        self.series.detachAxis(self.axis_y)
        print("Series에서 Axis를 제거하였습니다.")

        # 2. 차트에서 모든 Series하고 Axis를 제거
        print("차트에서 모든 Series를 및 Axis를 제거하겠습니다.")
        self.chart.removeSeries(self.series)
        self.chart.removeAxis(self.axis_x)
        self.chart.removeAxis(self.axis_y)
        print("차트에서 모든 Series 및 Axis를 제거하였습니다.")
        
        # emit으로부터 받은 새로운 QCandlestickSet을 series에 추가
        print("emit으로 받은 데이터를 Series에 새로운 candlestick set으로 추가하겠습니다.")
        ohlc = cur_price[0]        
        open = float(ohlc.open)
        high = float(ohlc.high)
        low = float(ohlc.low)
        close = float(ohlc.close)
        ts = float(ohlc.openTime)
        elem = QCandlestickSet(open, high, low, close, ts)
        self.series.append(elem)
        print("emit으로 받은 데이터를 Series에 새로운 candlestick set으로 추가하였습니다.")
        
        # chart에 series 추가
        print("차트에 Series를 추가하겠습니다.")
        self.chart.addSeries(self.series)
        print("차트에 Series를 추가하였습니다.")
        # axis_x에 max range를 emit에서 받은 새로운 time을 추가
        self.axis_x.setMax(QDateTime.fromMSecsSinceEpoch(ohlc.openTime+60000))
        # self.axis_y.setMax(float(ohlc.high)+float(1000))
        
        # chart에 axis x set
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        # series에 axis 추가
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)
        
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.show()
        
        print("새로운 Candle stick이 추가되었습니다.")
        # 새로 추가해야 하는 function > series의 맨 앞 candle 지우기
        
        
        