from pickle import FALSE
from qt_core import *
import pandas as pd
import time


class BitcoinChart(QChartView):
    default_font = QFont("SF Pro Medium", 10)
    default_color = QColor("#F5EAE7")
    def __init__(self, ticker, dist):
        super().__init__()
        self.ticker = ticker
        self.dist = dist
        # self.init_candle = df
        self.setBackgroundBrush(QColor("#2c313c"))
        self.initial_chart()
        self.show()


    def initial_chart(self):
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

        self.elems = []
        highs = []
        lows = []
        request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
        self.init_candle = request_client.get_candlestick_data(symbol=self.ticker, interval=self.dist, limit= 50)
        for ohlc in self.init_candle[:-1]:
            open = float(ohlc.open)
            high = float(ohlc.high)
            low = float(ohlc.low)
            close = float(ohlc.close)
            highs.append(high)
            lows.append(low)
            # 이미 내 코드에서는 opentime이 timestamp 형식으로 되어 있음
            # timestamp 형식이란?
            ts = float(ohlc.openTime)
            elem = QCandlestickSet(open, high, low, close, ts)
            print("추가되는 QCandle stick은: ", elem)
            # elems에 추가
            self.elems.append(elem)
            if open > close:
                elem.setPen(__binance_red)
            else:
                elem.setPen(__binance_green)
            self.series.append(elem)
        # initial chart에서의 Y min / max
        self.ay_min = min(lows)
        self.ay_max = max(highs)
        # chart object legend : 범례
        self.chart = QChart()
        self.chart.setBackgroundVisible(False)
        self.chart.legend().hide()
        # data feeding
        self.chart.addSeries(self.series)
        # axis X setting
        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("hh:mm:ss")
        self.axis_x.setLabelsColor(self.default_color)
        self.axis_x.setLabelsFont(self.default_font)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)
        # axis Y setting
        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%i")
        self.axis_y.setLabelsColor(self.default_color)
        self.axis_y.setLabelsFont(self.default_font)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)
        
        
        # margin
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        # setchart
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        print("Axis를 업데이트 하겠습니다.")
        self.__update_Axis()
        
    @Slot(object)
    def update_chart(self, new_price):

        # 색상 Setting
        __binance_red = QColor(195, 62, 80)
        __binance_green = QColor(95, 189, 123)
        
        # new_price를 database에 저장
        self.init_candle.append(new_price)
        del self.init_candle[0]
        
        print("new Price를 추가하고 기존 price 를 지우겠습니다.")
        # Thread의 Emit에서 받은 새로운 QCandlestick set을 series에 추가
        ohlc = new_price        
        open = float(ohlc.open)
        high = float(ohlc.high)
        low = float(ohlc.low)
        close = float(ohlc.close)
        ts = float(ohlc.openTime)
        elem = QCandlestickSet(open, high, low, close, ts)
        self.elems.append(elem)
        if open > close:
                elem.setPen(__binance_red)
        else:
                elem.setPen(__binance_green)
        self.series.append(elem)
        # 여기서 axis 업데이트 전 기존 min / max값과의 비교
        if low < self.ay_min:
            self.ay_min = low
        if high > self.ay_max:
            self.ay_max = high
        
        # 맨 뒤에 new_price를 추가 할 때 맨 앞에서는 legacy data를 지워야 함
        r_elem = self.elems.pop(0)
        print("Series에서 지워질 elem은 :", r_elem)
        print(self.series.remove(r_elem))
        
        # Axis 업데이트
        print("Axis를 업데이트 하겠습니다.")
        self.__update_Axis()



    def __update_Axis(self):
        __ts_start = self.init_candle[0].openTime
        __ts_last = self.init_candle[-1].openTime
        __margine = 60000*5
        __dt_start = QDateTime.fromMSecsSinceEpoch(__ts_start-__margine)
        __dt_last = QDateTime.fromMSecsSinceEpoch(__ts_last+__margine)
        self.axis_x.setRange(__dt_start, __dt_last)
        # Y range setting 하기 전 margine 설정
        __y_margine = 0.1 * (self.ay_max - self.ay_min)
        self.axis_y.setRange(self.ay_min-__y_margine, self.ay_max+__y_margine)
        # self.series.attachAxis(self.axis_x)
        # self.series.attachAxis(self.axis_y)