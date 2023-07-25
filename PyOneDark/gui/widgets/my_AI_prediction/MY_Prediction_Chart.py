from qt_core import *
import pandas as pd


class Prediction_Chart(QChartView):
    
    default_font = QFont("SF Pro Medium", 10)
    default_color = QColor("#F5EAE7")
    __binance_red = QColor(195, 62, 80)
    __binance_green = QColor(95, 189, 123)
    __prediction_blue = QColor(199, 103, 132)
    __prediction_red = QColor(108, 140, 187)
    __white = QColor(255, 255, 255)

    def __init__(self, ticker: str = 'BTCUSDT', dist: str = '5m', limit: int = 50) -> None:
        super().__init__()
        self.ticker = ticker
        self.dist = dist
        self.limit = limit
        self.setBackgroundBrush(QColor("#2c313c"))
        self.init_chart()
        self.show()

    def init_chart(self, data : pd.DataFrame = None) -> None:
        if data is None:
            self.data = pd.read_csv(r'C:\Programming\python\TotheMoon\PyOneDark\Storage\Data\1h\test_for_chart_drawing.csv').tail(self.limit)
        else:
            self.data = data.tail(self.limit)

        series_old = QCandlestickSeries()
        series_old.setBodyOutlineVisible(False)
        series_old.setIncreasingColor(self.__binance_green)
        series_old.setDecreasingColor(self.__binance_red)
        series_old.setPen(self.__white)
        series_old.setBrush(self.__white)

        series_new = QCandlestickSeries()
        series_new.setBodyOutlineVisible(False)
        series_new.setIncreasingColor(QColor(self.__prediction_red))
        series_new.setDecreasingColor(QColor(self.__prediction_blue))
        series_new.setPen(self.__white)
        series_new.setBrush(self.__white)

        elems_old = (QCandlestickSet(float(ohlc['Open price']), float(ohlc['High price']), float(ohlc['Low price']), float(ohlc['Close price']), float(ohlc['Kline open time'])) for _, ohlc in self.data.iterrows() if not ohlc['decoder'])
        elems_new = (QCandlestickSet(float(ohlc['Open price']), float(ohlc['High price']), float(ohlc['Low price']), float(ohlc['Close price']), float(ohlc['Kline open time'])) for _, ohlc in self.data.iterrows() if ohlc['decoder'])

        for elem in elems_old:
            if elem.open() > elem.close():
                elem.setPen(self.__binance_red)
            else:
                elem.setPen(self.__binance_green)
            elem.setBrush(self.__white)
            series_old.append(elem)

        for elem in elems_new:
            if elem.open() > elem.close():
                elem.setPen(QColor(self.__prediction_blue))
            else:
                elem.setPen(QColor(self.__prediction_red))
            elem.setBrush(self.__white)
            series_new.append(elem)

        self.chart = QChart()
        self.chart.setBackgroundVisible(False)
        self.chart.addSeries(series_old)
        self.chart.addSeries(series_new)

        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("MM-dd HH:mm")
        self.axis_x.setLabelsColor(self.default_color)
        self.axis_x.setLabelsFont(self.default_font)
        self.axis_x.setTickCount(int(self.limit/5))

        start_time = self.data['Kline open time'].iloc[-self.limit] / 1000
        end_time = self.data['Kline open time'].iloc[-1] / 1000
        axis_x_margine = (end_time - start_time) / 50
        start_time = QDateTime.fromSecsSinceEpoch(int(start_time - axis_x_margine), Qt.OffsetFromUTC, 9*60*60)
        end_time = QDateTime.fromSecsSinceEpoch(int(end_time + axis_x_margine), Qt.OffsetFromUTC, 9*60*60)
        self.axis_x.setRange(start_time, end_time)

        self.axis_y = QValueAxis()
        self.axis_y.setLabelFormat("%i")
        self.axis_y.setLabelsColor(self.default_color)
        self.axis_y.setLabelsFont(self.default_font)
        self.axis_y.setRange(self.data['Low price'].min(), self.data['High price'].max())
        
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        series_old.attachAxis(self.axis_x)
        series_old.attachAxis(self.axis_y)
        series_new.attachAxis(self.axis_x)
        series_new.attachAxis(self.axis_y)

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
