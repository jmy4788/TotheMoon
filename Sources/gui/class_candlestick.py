from pyside6_modules import *
import pandas as pd


# 여기는 QGraphicView > 
class MyGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setWindowOpacity(0.9)
        self.initUI()
        

    def initUI(self):
        __file_path = r"C:\\Programming\\python\\TotheMoon\\Storage\\"
        df = pd.read_csv(__file_path + 'candle.csv')
        self.scene.addItem(Candle(df))
        self.setScene(self.scene)
        self.setGeometry(0, 0, 1000, 564)
        self.show()


class Candle(QGraphicsObject):
    """
    QGraphicsItem 중 하나로 QGraphicsObject가 있고
    GraphicsObject는 기본 적으로 paint와 boundingRect 메소드를
    탑재해야 합니다.
    """
    def __init__(self, df):
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
        self.font.setFamily('D2coding')
        self.font.setPixelSize(10)

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
            self.painter.drawLine(QPointF(__x_offset + 5*i, h_max - h), QPointF(__x_offset + 5*i, h_max - l))
            self.painter.drawRect(QRectF(__x_offset + (5*i-__rect_width/2), h_max - o, __rect_width, o - c))
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
        y_range = y_max-y_min
        y_interval = y_range / y_index
        __x_offset = 1000
        for i, index in enumerate(df.index):
            if i % 10 == 0:
                y_label = (i+1) * y_interval
                # drawText에 QRectF를 섞으면 __bound_rect를 return하기도 함
                __bound_rect = self.painter.drawText(QRectF(self.__label_x_offset, y_label, 100, 50), 1,
                                                     f'{(y_max-y_label)*10:0.2f}')
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
        bound_rect = QRectF(min(bound_x), min(bound_y), max(bound_width)+50, max(bound_height))
        print(bound_rect)
        return bound_rect
