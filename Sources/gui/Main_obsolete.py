import sys
import pandas as pd

from binance_f import RequestClient
from binance_f.constant.test import *

from class_candlestick import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # super().__init__()은 부모 class의 기능을 사용하겠다는 선언
        self.setWindowOpacity(0.9)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QMainWindow 입니다.')
        self.initMenu()
        gv = MyGraphicsView()
        self.setCentralWidget(gv)
        #wg = MyWidget()
        #self.setCentralWidget(wg)
        # self.center()
        self.resize(1920, 1080)
        self.show()
        
    def initMenu(self):
        exitAction = QAction(QIcon('exit2.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QCoreApplication.quit)
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

    def center(self):
        # QT6 부터는 QDesktopWidget이 QScreen으로 바뀜
        qr = self.frameGeometry()
        cp = QScreen.availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    initial_candlestick = request_client.get_candlestick_data(symbol='BTCUSDT', interval='5m')
    __file_path = r"C:\\Programming\\python\\TotheMoon\\Storage\\"
    df = pd.read_csv(__file_path + 'candle.csv')
    opens = df['Open']
    highs = df['High']
    lows = df['Low']
    closes = df['Close']


     # data
        self.series = QCandlestickSeries()
        self.series.setIncreasingColor(Qt.red)
        self.series.setDecreasingColor(Qt.blue)



    app = QApplication(sys.argv)
    execution = MyWindow()
    app.exec()
    