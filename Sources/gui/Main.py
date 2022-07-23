import sys
import pandas as pd

from binance_f import RequestClient
from binance_f.constant.test import *

from new_candle import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # super().__init__()은 부모 class의 기능을 사용하겠다는 선언
        self.setWindowOpacity(0.9)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QMainWindow 입니다.')
        self.initMenu()
        chart1 = MyChart()
        thread1 = Worker(chart1.candledf)
        thread1.price.connect(chart1.update_chart)
        thread1.start()
        
        self.setCentralWidget(chart1)
        #wg = MyWidget()
        #self.setCentralWidget(wg)
        # self.center()
        self.resize(3440, 1440)
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
    app = QApplication(sys.argv)
    execution = MyWindow()
    app.exec()
    