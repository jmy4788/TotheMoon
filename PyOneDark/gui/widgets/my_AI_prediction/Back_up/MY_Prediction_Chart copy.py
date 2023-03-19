from pickle import FALSE
from qt_core import *
import pandas as pd
import time

class Prediction_Chart(QChartView):
    
    default_font = QFont("SF Pro Medium", 10)
    default_color = QColor("#F5EAE7")

    def __init__(self, ticker: str = 'BTCUSDT', dist: str = '5m', limit: int = 50) -> None:
        super().__init__()
        self.ticker = ticker
        self.dist = dist
        self.limit = limit
        self.setBackgroundBrush(QColor("#2c313c"))
        self.init_chart()
        self.show()

    def init_chart(self) -> None:
        
        __binance_red = QColor(195, 62, 80)
        __binance_green = QColor(95, 189, 123)
        __white = QColor(255, 255, 255)

        df = pd.read_csv(r'C:\\Programming\\python\\TotheMoon\\PyOneDark\\Data_Storage\\1h\\test_for_chart_drawing.csv')
        df = df.tail(self.limit)
        
        request_client = Spot("g_api_key", "g_secret_key")
        self.init_candle = request_client.klines(symbol=self.ticker, interval=self.dist, limit=50)
        self.init_candle = df
       
        series_old = QCandlestickSeries()
        series_old.setBodyOutlineVisible(False)
        series_old.setIncreasingColor(__binance_green)
        series_old.setDecreasingColor(__binance_red)
        series_old.setPen(__white)
        series_old.setBrush(__white)

        series_new = QCandlestickSeries()
        series_new.setBodyOutlineVisible(False)
        series_new.setIncreasingColor(QColor("#33D4FF"))
        series_new.setDecreasingColor(QColor("#FF5733"))
        series_new.setPen(__white)
        series_new.setBrush(__white)

        elems_old = []
        elems_new = []
        for _, ohlc in self.init_candle.iterrows():
            elem = QCandlestickSet(float(ohlc['Open price']), float(ohlc['High price']), float(ohlc['Low price']), float(ohlc['Close price']), float(ohlc['Kline open time']))
            if ohlc['decoder']:
                if elem.open() > elem.close():
                    elem.setPen(QColor("#FF5733"))
                else:
                    elem.setPen(QColor("#33D4FF"))
                elem.setBrush(__white)
                elems_new.append(elem)
            else:
                if elem.open() > elem.close():
                    elem.setPen(__binance_red)
                else:
                    elem.setPen(__binance_green)
                elem.setBrush(__white)
                elems_old.append(elem)

        for elem in elems_old:
            series_old.append(elem)
        for elem in elems_new:
            series_new.append(elem)

        self.chart = QChart()
        self.chart.setBackgroundVisible(False)
        self.chart.addSeries(series_old)
        self.chart.addSeries(series_new)

        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("yy-MM-dd HH:mm")
        self.axis_x.setLabelsColor(self.default_color)
        self.axis_x.setLabelsFont(self.default_font)
        self.axis_x.setTickCount(int(self.limit/5))

        start_time = self.init_candle['Kline open time'].iloc[-self.limit] / 1000
        end_time = self.init_candle['Kline open time'].iloc[-1] / 1000
        axis_x_margine = (end_time - start_time) / 50
        start_time = QDateTime.fromSecsSinceEpoch(int(start_time - axis_x_margine), Qt.OffsetFromUTC, 9*60*60)
        end_time = QDateTime.fromSecsSinceEpoch(int(end_time + axis_x_margine), Qt.OffsetFromUTC, 9*60*60)
        self.axis_x.setRange(start_time, end_time)

        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%i")
        self.axis_y.setLabelsColor(self.default_color)
        self.axis_y.setLabelsFont(self.default_font)
        self.axis_y.setRange(self.init_candle['Low price'].min(), self.init_candle['High price'].max())
        
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        series_old.attachAxis(self.axis_x)
        series_new.attachAxis(self.axis_x)
        series_new.attachAxis(self.axis_y)
        series_old.attachAxis(self.axis_y)

        self.chart.setBackgroundBrush(QColor("#2c313c"))
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        self.chart.setBackgroundRoundness(0)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTheme(QChart.ChartThemeDark)
        self.chart.setTitleBrush(QColor("#FFFFFF"))
        self.chart.setTitleFont(QFont("SF Pro Medium", 12))
        self.chart.setTitle(f"{self.ticker} {self.dist} Chart")
        self.chart.legend().setVisible(False)
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)

"""

class Prediction_Chart(QChartView):
    default_font = QFont("SF Pro Medium", 10)
    default_color = QColor("#F5EAE7")
    def __init__(self, ticker: str = 'BTCUSDT', dist: str = '5m'):
        super().__init__()
        self.ticker = ticker
        self.dist = dist
        # self.init_candle = df
        self.setBackgroundBrush(QColor("#2c313c"))
        self.init_chart()
        self.show()


    def init_chart(self):
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
        self.series.setBrush(__white)

        # initial OHLC feeding
        self.elems = []
        highs = []
        lows = []
        request_client = Spot("g_api_key", "g_secret_key")
        self.init_candle = request_client.klines(symbol=self.ticker, interval=self.dist, limit= 50)

        # klines method에서 반환되는 값
        # [0]Kline open time [1]Open price [2]High price [3]Low price [4]Close price [5]Volume

        for ohlc in self.init_candle[:-1]:
            open = float(ohlc[1])
            high = float(ohlc[2])
            low = float(ohlc[3])
            close = float(ohlc[4])
            highs.append(high)
            lows.append(low)
            # 이미 내 코드에서는 opentime이 timestamp 형식으로 되어 있음
            # timestamp 형식이란?
            ts = float(ohlc[0])
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
        # data feeding
        self.chart.addSeries(self.series)
        self.chart.legend().hide()
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
        self.chart.setBackgroundBrush(QColor("#2c313c"))
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        # Github copilot이 추가한 내용
        self.chart.setBackgroundRoundness(0)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTheme(QChart.ChartThemeDark)
        self.chart.setTitleBrush(QColor("#FFFFFF"))
        self.chart.setTitleFont(QFont("SF Pro Medium", 12))
        self.chart.setTitle(f"{self.ticker} {self.dist} Chart")
        # setchart
        self.setChart(self.chart)
        self.setRenderHint(QPainter.Antialiasing)
        print("Axis를 업데이트 하겠습니다.")
        self.__update_Axis()



    def __update_Axis(self):
        __ts_start = self.init_candle[0][0]
        __ts_last = self.init_candle[-1][0]
        __margine = 60000*5
        __dt_start = QDateTime.fromMSecsSinceEpoch(__ts_start-__margine)
        __dt_last = QDateTime.fromMSecsSinceEpoch(__ts_last+__margine)
        self.axis_x.setRange(__dt_start, __dt_last)
        # Y range setting 하기 전 margine 설정
        __y_margine = 0.1 * (self.ay_max - self.ay_min)
        self.axis_y.setRange(self.ay_min-__y_margine, self.ay_max+__y_margine)
        # self.series.attachAxis(self.axis_x)
        # self.series.attachAxis(self.axis_y)

    def __del__(self):
        print("Bitcoinchart 객체가 죽었습니다.")
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

"""