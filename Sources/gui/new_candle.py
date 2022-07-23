from pyside6_modules import *
import pandas as pd
import time

from binance_f import RequestClient
from binance_f.constant.test import *



class Worker(QThread):
    price = Signal(object)
    def __init__(self, df):
        super().__init__()
        self.init_candle = df

    def run(self):
        __last_candle_opentime = self.init_candle[-1].openTime
        request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
        while True:
            new_price = request_client.get_candlestick_data(symbol='BTCUSDT', interval='1m', limit= 2)
            if __last_candle_opentime == new_price[-1].openTime:
                print("새로운 Candlestick이 없습니다.")
                __last_candle_opentime = new_price[-1].openTime
                time.sleep(5)
            else:
                print("새로운 Candlestick이 생성되었습니다.")
                self.price.emit(new_price[0])
                __last_candle_opentime = new_price[-1].openTime
                time.sleep(5)
                


class MyChart(QChartView):
    def __init__(self):
        super().__init__()
        self.initial_chart()
        self.show()


    def initial_chart(self):
        
        # get data from binance
        request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
        self.candledf = request_client.get_candlestick_data(symbol='BTCUSDT', interval='5m', limit= 200)

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
        for ohlc in self.candledf[:-1]:
            open = float(ohlc.open)
            high = float(ohlc.high)
            low = float(ohlc.low)
            close = float(ohlc.close)
            # 이미 내 코드에서는 opentime이 timestamp 형식으로 되어 있음
            ts = float(ohlc.openTime)
            elem = QCandlestickSet(open, high, low, close, ts)
            if open > close:
                elem.setPen(__binance_red)
            else:
                elem.setPen(__binance_green)
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
    def update_chart(self, new_price):

        # new_price를 database에 저장
        print("Candle df에 new_price를 append 하겠습니다.")
        self.candledf.append(new_price)
        print("Candle df에 new_price를 append 하였습니다.")
        
        #Axis 업데이트
        print("Axis를 업데이트 하겠습니다.")
        self.__update_Axis()

        # emit으로부터 받은 새로운 QCandlestickSet을 series에 추가
        print("emit으로 받은 데이터를 Series에 새로운 candlestick set으로 추가하겠습니다.")
        ohlc = new_price        
        open = float(ohlc.open)
        high = float(ohlc.high)
        low = float(ohlc.low)
        close = float(ohlc.close)
        ts = float(ohlc.openTime)
        elem = QCandlestickSet(open, high, low, close, ts)
        self.series.append(elem)
        print("emit으로 받은 데이터를 Series에 새로운 candlestick set으로 추가하였습니다.")


    def __update_Axis(self):
        __ts_start = self.candledf[0].openTime
        __ts_last = self.candledf[-1].openTime
        __margine = 60000*5
        __dt_start = QDateTime.fromMSecsSinceEpoch(__ts_start-__margine)
        __dt_last = QDateTime.fromMSecsSinceEpoch(__ts_last+__margine)
        self.axis_x.setRange(__dt_start, __dt_last)
        self.series.attachAxis(self.axis_x)
        self.series.attachAxis(self.axis_y)