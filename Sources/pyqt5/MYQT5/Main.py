import sys
import pandas as pd
from datetime import datetime

# QPicture는 도화지 QPainter는 펜이라고 생각할 수 있음
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowOpacity(0.9)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QMainWindow 입니다.')
        self.initMenu()
        wg = MyWidget()
        self.setCentralWidget(wg)
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


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        # 폰트 설정
        self.font = QFont()
        self.font.setFamily('나눔손글씨 펜')
        self.font.setPixelSize(11)
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        # addWidget(QLayoutItem *item, int row, int column, int rowSpan = 1, int columnSpan = 1,
        # Qt::Alignment alignment = Qt::Alignment())
        gw = MyGraphicsView()
        cp = CurPos()
        grid.addWidget(gw, 0, 0)
        grid.addWidget(cp, 1, 0)
        self.setWindowTitle('QWidget')
        # self.setGeometry(0, 0, 1920, 1080)
        self.show()


class MyGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setWindowOpacity(0.9)
        self.initUI()

    def initUI(self):
        self.scene.addItem(Candle())
        self.setScene(self.scene)
        self.setGeometry(0, 0, 1000, 564)
        self.show()


class Candle(QGraphicsObject):
    """
    QGraphicsItem 중 하나로 QGraphicsObject가 있고
    GraphicsObject는 기본 적으로 paint와 boundingRect 메소드를
    탑재해야 합니다.
    """

    def __init__(self):
        csv = save_candle_csv()
        df = pd.read_csv(csv)
        super().__init__()
        # QPicture = 도화지
        self.picture = QPicture()
        self.picture2 = QPicture()
        # 하나의 GraphicsObject에서 하나의 Painter(?)
        self.painter = QPainter()
        # self.picture.setBoundingRect(QRect(0, 0, 500, 500))
        # self.setOpacity(0.8)
        self.__binance_red = QColor(195, 62, 80)
        self.__binance_green = QColor(95, 189, 123)
        # 폰트 설정
        self.font = QFont()
        self.font.setFamily('나눔손글씨 펜')
        self.font.setPixelSize(11)

        self.initUI(df)
        self.ylabel(df)

    def initUI(self, df):
        print("init UI 메서드가 실행되었습니다.")
        self.painter.begin(self.picture)
        self.painter.setBackground(QBrush(QColor(000, 100, 255)))

        h_max = max(df['High']) / 10
        l_min = min(df['Low'])

        for i, index in enumerate(df.index):
            if i == len(df) - 1:
                break
            # 20으로 나눈거는 스케일링
            o = df['Open'][index] / 10
            h = df['High'][index] / 10
            l = df['Low'][index] / 10
            c = df['Close'][index] / 10
            v = df['Volume'][i]
            # 종가가 시가보다 높으면 Bullish(Red)
            # 낮으면 Bearish(Green)
            __line_width = 1
            if c >= o:
                self.painter.setPen(QPen(self.__binance_green, __line_width))
                self.painter.setBrush(QBrush(self.__binance_green, Qt.BrushStyle.SolidPattern))

            else:
                self.painter.setPen(QPen(self.__binance_red, __line_width))
                self.painter.setBrush(QBrush(self.__binance_red, Qt.BrushStyle.SolidPattern))
            __rect_width = 3
            __x_offset = 0
            # QPointF(x pos, y pos)
            # QRectF(x pos, y pos, width, height)

            # height 는 양수일 때 아래로 그려지고 음수 일 때 위로 그려짐
            # width 는 양수일 때 오른쪽으로 그려지고 음수일 때 왼쪽으로 그려짐
            self.painter.drawLine(QPointF(__x_offset + 5 * i, h_max - h), QPointF(__x_offset + 5 * i, h_max - l))
            self.painter.drawRect(QRectF(__x_offset + (5 * i - __rect_width / 2), h_max - o, __rect_width, o - c))
            # 볼륨 바 그리기
            self.painter.drawRect(__x_offset + (5 * i - __rect_width / 2), 500, __rect_width, - v / 100)
        self.__label_x_offset = __x_offset + (5 * i - __rect_width / 2)
        self.painter.end()

    def ylabel(self, df):
        self.painter.begin(self.picture2)
        self.painter.setFont(self.font)
        print("ylabel 메서드가 실행되었습니다")
        # 파이썬에서는 이미 유니코드를 사용하기 때문에 QString 클래스를 쓸 필요가 없다.

        y_max = max(df['High']) / 10
        y_min = min(df['Low']) / 10
        print("ymax : ", y_max)
        print("ymin : ", y_min)

        y_index = len(df)
        y_range = y_max - y_min
        y_interval = y_range / y_index
        __x_offset = 1000
        for i, index in enumerate(df.index):
            if i % 10 == 0:
                y_label = (i + 1) * y_interval
                # drawText에 QRectF를 섞으면 __bound_rect를 return하기도 함
                __bound_rect = self.painter.drawText(QRectF(self.__label_x_offset, y_label, 100, 50), 1,
                                                     f'{(y_max - y_label) * 10:0.2f}')
                print(i, y_label)
                print('__bound_rect : ', __bound_rect)
        """
        for i, index in enumerate(df.index):
            if i == len(df) - 1:
                break
        """
        self.painter.end()

    def paint(self, painter, *args):
        print("paint method가 실행되었습니다.")
        if args is None:
            print("paint method가 실행되었습니다.")
            return
        painter.drawPicture(0, 0, self.picture)
        painter.drawPicture(0, 0, self.picture2)

    # 현재 문제는 boundingRect에서 나오는 것 같음

    def boundingRect(self):
        # bounding rect (x, y, width, height)

        bound_x = [self.picture.boundingRect().x(), self.picture2.boundingRect().x()]
        bound_y = [self.picture.boundingRect().y(), self.picture2.boundingRect().y()]
        bound_width = [self.picture.boundingRect().width(), self.picture2.boundingRect().width()]
        bound_height = [self.picture.boundingRect().height(), self.picture2.boundingRect().height()]

        print('self.picture.boundingRect().x() : ', self.picture.boundingRect().x())
        print('self.picture.boundingRect().y() : ', self.picture.boundingRect().y())
        print('self.picture.boundingRect().width() : ', self.picture.boundingRect().width())
        print('self.picture.boundingRect().height() : ', self.picture.boundingRect().height())

        print('self.picture2.boundingRect().x() : ', self.picture2.boundingRect().x())
        print('self.picture2.boundingRect().y() : ', self.picture2.boundingRect().y())
        print('self.picture2.boundingRect().width() : ', self.picture2.boundingRect().width())
        print('self.picture2.boundingRect().height() : ', self.picture2.boundingRect().height())
        bound_rect = QRectF(min(bound_x), min(bound_y), max(bound_width) + 50, max(bound_height))
        print(bound_rect)
        return bound_rect


"""
class LastCandle(pg.GraphicsObject):
    def __init__(self, x, c, o, h, low):
        pg.GraphicsObject.__init__(self)
        self.picture = QtGui.QPicture()
        self.LastCandleStick(x, c, o, h, low)

    def LastCandleStick(self, x, c, o, h, low):
        p = QtGui.QPainter(self.picture)
        if c >= o:
            p.setPen(pg.mkPen('#e6e6eb'))
            p.setBrush(pg.mkBrush('#e6e6eb'))
        else:
            p.setPen(pg.mkPen('#646469'))
            p.setBrush(pg.mkBrush('#646469'))
        p.drawLine(QtCore.QPointF(x, h), QtCore.QPointF(x, low))
        p.drawRect(QtCore.QRectF(x - 0.25, o, 0.25 * 2, c - o))
        p.end()

    def paint(self, p, *args):
        if args is None:
            return
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())
"""

class CurPos(QWidget):
    def __init__(self):
        super().__init__()
        self.label = []
        self.__is_first = True
        # 리스트 컴프리헨션으로 QLabel 10개 만들어 봤음
        self.label = [QLabel() for x in range(10)]
        self.timer = QTimer(self)
        self.layout = QGridLayout()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CentralWidget 입니다.')
        self.first_row()
        self.timer.start(5000)
        self.timer.timeout.connect(self.second_row)
        self.setLayout(self.layout)

    def first_row(self):
        first_row_list = ['심볼', '사이즈', '진입 가격', '시장 평균가', '청산 가격', '마진 비율', '마진', 'PNL(ROE %)',
                          'ADL', '전체 포지션 종료', '전체 포지션 이익실현(TP) / 스탑 로스(SL)']
        for index, content in enumerate(first_row_list):
            self.layout.addWidget(QLabel(f'{content}'), 0, index)
        return

    def second_row(self):
        for i in range(10):
            self.layout.addWidget(self.label[i], 1, i)
        __pos_sets = request_client.get_position()
        for index, pos in enumerate(__pos_sets):
            if pos.symbol == 'BTCUSDT' and pos.positionSide == 'BOTH':
                # data1, data2의 type이 float이었음
                data0 = pos.symbol
                data1 = pos.positionAmt
                data2 = pos.entryPrice
                data3 = pos.markPrice
                self.label[0].setText(f'{pos.symbol}')
                self.label[1].setText(f'{pos.positionAmt}')
                self.label[2].setText(f'{pos.entryPrice}')
                self.label[3].setText(f'{pos.markPrice}')
                self.label[4].setText(f'{pos.liquidationPrice}')
                self.label[5].setText(f'{pos.leverage}')
                self.label[6].setText(f'{pos.unrealizedProfit}')
                self.label[7].setText('아직 모름')
                self.label[8].setText('아직 모름')
                self.label[9].setText('아직 모름')
                for i in range(10):
                    self.label[i].repaint()
                return


def show_pos(pos_sets):
    for pos in pos_sets:
        if pos.symbol == 'BTCUSDT':
            print("pos.symbol:", pos.symbol)
            print("pos.entryPrice:", pos.entryPrice)
            print("pos.isAutoAddMargin:", pos.isAutoAddMargin)
            print("pos.leverage:", pos.leverage)
            print("pos.maxNotionalValue:", pos.maxNotionalValue)
            print("pos.liquidationPrice:", pos.liquidationPrice)
            print("pos.markPrice:", pos.markPrice)
            print("pos.positionAmt:", pos.positionAmt)
            print("pos.unrealizedProfit:", pos.unrealizedProfit)
            print("pos.isolatedMargin:", pos.isolatedMargin)
            print("pos.positionSide:", pos.positionSide)


def save_candle_csv():
    __file_path = r'D:\재테크/'
    __time = datetime.now().strftime('%m%d %H%M')
    __file_name = __file_path+__time+'.csv'
    result = request_client.get_candlestick_data(symbol='BTCUSDT', interval='5m')
    candle_col = ['OpenTime', 'Open', 'High', 'Low', 'Close', 'CloseTime']
    df = pd.DataFrame(columns=candle_col)
    for i in result:
        i.openTime = datetime.fromtimestamp(i.openTime/1000)
        print('OpenTime : ', i.openTime)
        print('Open : ', i.open)
        print('High : ', i.high)
        print('Low : ', i.low)
        print('Close : ', i.close)
        print('CloseTime : ', i.closeTime)
        print('Volume : ', i.volume)
        one_candle = {'OpenTime': i.openTime, 'Open': i.open, 'High': i.high, 'Low': i.low, 'Close': i.close,
                      'CloseTime': i.closeTime, 'Volume': i.volume}
        df = df.append(one_candle, ignore_index=True)
    df.to_csv(__file_name, index=False)
    return __file_name


if __name__ == '__main__':
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    app = QApplication(sys.argv)
    ex = MyWindow()
    # gv = MyGraphicsView()
    app.exec()

