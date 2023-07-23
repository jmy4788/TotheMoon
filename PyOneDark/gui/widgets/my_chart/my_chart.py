from qt_core import *
import pandas as pd
import time


class BitcoinChart(QChartView):
    default_font = QFont("SF Pro Medium", 10)
    default_color = QColor("#F5EAE7")
    binance_red = QColor(195, 62, 80)
    binance_green = QColor(95, 189, 123)
    
    def __init__(self, ticker, dist):
        super().__init__()
        self.ticker = ticker
        self.dist = dist
        self.setBackgroundBrush(QColor("#2c313c"))
        self.initial_chart()
        self.show()

    def initial_chart(self):
        self.series = QCandlestickSeries()
        self.series.setIncreasingColor(self.binance_green)
        self.series.setDecreasingColor(self.binance_red)
        self.series.setBodyOutlineVisible(False)
        self.series.setPen(self.default_color)
        self.series.setBrush(self.default_color)

        request_client = Spot("g_api_key", "g_secret_key")
        self.init_candle = request_client.klines(symbol=self.ticker, interval=self.dist, limit=50)

        self.elems = [self._create_candlestick_set(ohlc) for ohlc in self.init_candle[:-1]]
        for elem in self.elems:
            self.series.append(elem)

        self.ay_min = min(elem.low() for elem in self.elems)
        self.ay_max = max(elem.high() for elem in self.elems)
        
        self.chart = QChart()
        self.chart.setBackgroundVisible(False)
        self.chart.addSeries(self.series)
        self.chart.legend().hide()
        
        self._setup_chart_axes()
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.__update_Axis()

    def _create_candlestick_set(self, ohlc):
        open, high, low, close, ts = map(float, (ohlc[1], ohlc[2], ohlc[3], ohlc[4], ohlc[0]))
        elem = QCandlestickSet(open, high, low, close, ts)
        elem.setPen(self.binance_green if open <= close else self.binance_red)
        return elem

    def _setup_chart_axes(self):
        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("hh:mm:ss")
        self.axis_x.setLabelsColor(self.default_color)
        self.axis_x.setLabelsFont(self.default_font)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)

        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%i")
        self.axis_y.setLabelsColor(self.default_color)
        self.axis_y.setLabelsFont(self.default_font)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)
        self.series.attachAxis(self.axis_y)
        self.chart.setBackgroundBrush(QColor("#2c313c"))
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        self.chart.setBackgroundRoundness(0)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTheme(QChart.ChartThemeDark)
        self.chart.setTitleBrush(QColor("#FFFFFF"))
        self.chart.setTitleFont(QFont("SF Pro Medium", 12))
        self.chart.setTitle(f"{self.ticker} {self.dist} Chart")

    @Slot(object)
    def update_chart(self, new_price):
        self.init_candle.append(new_price)
        del self.init_candle[0]
        
        elem = self._create_candlestick_set(new_price)
        self.elems.append(elem)
        self.series.append(elem)

        if elem.low() < self.ay_min:
            self.ay_min = elem.low()
        if elem.high() > self.ay_max:
            self.ay_max = elem.high()
        
        r_elem = self.elems.pop(0)
        self.series.remove(r_elem)
        
        self.__update_Axis()

    def __update_Axis(self):
        __ts_start, __ts_last = self.init_candle[0][0], self.init_candle[-1][0]
        __margine = 60000*5
        __dt_start = QDateTime.fromMSecsSinceEpoch(__ts_start - __margine)
        __dt_last = QDateTime.fromMSecsSinceEpoch(__ts_last + __margine)
        self.axis_x.setRange(__dt_start, __dt_last)
        __y_margine = 0.1 * (self.ay_max - self.ay_min)
        self.axis_y.setRange(self.ay_min - __y_margine, self.ay_max + __y_margine)

    def __del__(self):
        print("Bitcoinchart 객체가 죽었습니다.")
