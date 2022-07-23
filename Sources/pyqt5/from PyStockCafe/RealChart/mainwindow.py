import sys
import time
import pandas as pd
from PyQt5 import QtWidgets
from multiprocessing import Process, Queue
from chartitem import *
from worker import Worker


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.font = QtGui.QFont()
        self.font.setFamily('나눔고딕')
        self.font.setPixelSize(12)

        self.setWindowTitle("실시간 5분봉 차트 예제 - 오른쪽 빈칸에 종목코드를 입력 후 엔터 또는 차트검색")
        self.setFont(self.font)
        self.setGeometry(1600, 350, 610, 630)

        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(5, 5, 400, 65)
        self.textEdit.setReadOnly(True)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setStyleSheet("font: 9pt '나눔고딕'; color: rgb(230, 230, 235); background: rgb(30, 30, 35);")

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(410, 5, 195, 30)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setStyleSheet("font: 9pt '나눔고딕'; color: rgb(230, 230, 235); background: rgb(30, 30, 35);")
        self.lineEdit.returnPressed.connect(self.ButtonClicked_01)

        self.pushButton = QtWidgets.QPushButton("차트검색", self)
        self.pushButton.setGeometry(410, 40, 195, 30)
        self.pushButton.clicked.connect(self.ButtonClicked_01)

        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(5, 72, 600, 550)

        pg.setConfigOptions(background='#1e1e23', foreground='#96969b')

        mc_pg = pg.GraphicsLayoutWidget()
        self.mc_pg_01 = mc_pg.addPlot(row=0, col=0, axisItems={'bottom': pg.DateAxisItem()})
        self.SetPgPyqtgraph(self.mc_pg_01)
        self.mc_pg_02 = mc_pg.addPlot(row=1, col=0, axisItems={'bottom': pg.DateAxisItem()})
        self.SetPgPyqtgraph(self.mc_pg_02)
        self.mc_pg_02.setXLink(self.mc_pg_01)
        qGraphicsGridLayout = mc_pg.ci.layout
        qGraphicsGridLayout.setRowStretchFactor(0, 2)
        qGraphicsGridLayout.setRowStretchFactor(1, 1)
        self.mc_pg_vboxLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.mc_pg_vboxLayout.setContentsMargins(5, 5, 5, 5)
        self.mc_pg_vboxLayout.addWidget(mc_pg)

        self.mc_pg_lastindex = None
        self.mc_pg_lastcandlestick = None
        self.mc_pg_lastvolumebar = None
        self.mc_pg_legend1 = None
        self.mc_pg_legend2 = None
        self.mc_pg_name = None

        self.writer = Writer()
        self.writer.data0.connect(self.UpdateTexedit)
        self.writer.data1.connect(self.UpdateChart)
        self.writer.start()

    def SetPgPyqtgraph(self, pgplot):
        pgplot.showAxis('left', False)
        pgplot.showAxis('right', True)
        pgplot.getAxis("right").setStyle(tickTextWidth=42, autoExpandTextSpace=False, autoReduceTextSpace=False)
        pgplot.getAxis("right").setTickFont(self.font)
        pgplot.getAxis("bottom").setTickFont(self.font)

    def ButtonClicked_01(self):
        code = self.lineEdit.text()
        if code == "":
            dataQ.put("종목코드를 입력하십시오.")
            return
        else:
            tranQ.put(code)

    def UpdateTexedit(self, msg):
        self.textEdit.append(msg)

    def UpdateChart(self, df):
        x = len(df) - 1
        c = df['현재가'][-1]
        o = df['시가'][-1]
        h = df['고가'][-1]
        low = df['저가'][-1]
        v = df['거래량'][-1]
        y = df['고가'].max()
        if self.mc_pg_lastindex != df.index[-1] or self.mc_pg_name != df['종목명'][0]:
            self.mc_pg_01.clear()
            self.mc_pg_02.clear()
            self.mc_pg_lastindex = df.index[-1]
            self.mc_pg_01.addItem(CandlesticksItem(df))
            self.mc_pg_lastcandlestick = LastCandlestickItem(x, c, o, h, low)
            self.mc_pg_01.addItem(self.mc_pg_lastcandlestick)
            self.UpdateMcpgMarker(df)
            self.mc_pg_legend1 = pg.TextItem(color='#e6e6eb', border='#323237', fill=(50, 50, 55, 200))
            self.mc_pg_legend1.setFont(self.font)
            self.mc_pg_legend1.setPos(0, df['고가'].max())
            self.mc_pg_legend1.setText(self.GetMainLegendText(df))
            self.mc_pg_01.addItem(self.mc_pg_legend1)
            self.mc_pg_01.getAxis('bottom').setTicks([list(zip(range(len(df.index))[::12], df.index[::12]))])
            self.mc_pg_02.addItem(VolumeBarsItem(df))
            self.mc_pg_lastvolumebar = LastVolumeBarItem(x, c, o, v)
            self.mc_pg_02.addItem(self.mc_pg_lastvolumebar)
            self.mc_pg_legend2 = pg.TextItem(color='#e6e6eb', border='#323237', fill=(50, 50, 55, 200))
            self.mc_pg_legend2.setFont(self.font)
            self.mc_pg_legend2.setPos(0, df['거래량'].max())
            self.mc_pg_legend2.setText(self.GetSubLegendText(df))
            self.mc_pg_02.addItem(self.mc_pg_legend2)
            self.mc_pg_02.getAxis("bottom").setLabel(text=df['종목명'][0])
            self.mc_pg_02.getAxis('bottom').setTicks([list(zip(range(len(df.index))[::12], df.index[::12]))])
            self.cross_hair(y, df['전일종가'][0], main_pg=self.mc_pg_01, sub_pg=self.mc_pg_02)
            if self.mc_pg_name != df['종목명'][0]:
                self.mc_pg_01.enableAutoRange(x=True, y=True)
                self.mc_pg_02.enableAutoRange(x=True, y=True)
                self.mc_pg_name = df['종목명'][0]
        else:
            self.mc_pg_01.removeItem(self.mc_pg_lastcandlestick)
            self.mc_pg_lastcandlestick = LastCandlestickItem(x, c, o, h, low)
            self.mc_pg_01.addItem(self.mc_pg_lastcandlestick)
            self.mc_pg_legend1.setText(self.GetMainLegendText(df))
            self.mc_pg_02.removeItem(self.mc_pg_lastvolumebar)
            self.mc_pg_lastvolumebar = LastVolumeBarItem(x, c, o, v)
            self.mc_pg_02.addItem(self.mc_pg_lastvolumebar)
            self.mc_pg_legend2.setText(self.GetSubLegendText(df))

    def UpdateMcpgMarker(self, df):
        pc = df['전일종가'][-1]
        df2 = df[df['저가'] <= df['지수이평05']]
        df2 = df2[df2['현재가'] > df2['직전현재가']]
        df2 = df2[df2['현재가'] > df2['시가']]
        df2 = df2[df2['거래량'] > df2['직전거래량']]
        df2 = df2[df2['현재가'] <= pc * 1.10]
        df2 = df2[df2['지수이평05'] > df2['직전지수이평05']]
        df2 = df2[df2['지수이평10'] > df2['직전지수이평10']]
        df2 = df2[df2['지수이평20'] > df2['직전지수이평20']]
        df3 = df2[df2['저가'] <= df2['지수이평10']]
        for index in df2.index:
            if index in df3.index:
                df2.drop(index=index, inplace=True)
        df4 = df[df['현재가'] <= df['지수이평10'] * 0.99]
        gap = (df['고가'].max() - df['저가'].min()) / 20
        for i, index1 in enumerate(df.index):
            for index2 in df2.index:
                if index1 == index2:
                    y = df['저가'][index1] - gap
                    marker = pg.ArrowItem(angle=90, baseAngle=20, headLen=10, headWidth=5, tailLen=None,
                                          pen='#e6e6eb', brush='#e6e6eb')
                    marker.setPos(i, y)
                    self.mc_pg_01.addItem(marker)
            for index2 in df3.index:
                if index1 == index2:
                    y = df['저가'][index1] - gap
                    marker = pg.ArrowItem(angle=90, baseAngle=20, headLen=10, headWidth=5, tailLen=None,
                                          pen='#96969b', brush='#96969b')
                    marker.setPos(i, y)
                    self.mc_pg_01.addItem(marker)
            for index2 in df4.index:
                if index1 == index2:
                    y = df['고가'][index1] + gap
                    marker = pg.ArrowItem(angle=-90, baseAngle=20, headLen=10, headWidth=5, tailLen=None,
                                          pen='#000000', brush='#000000')
                    marker.setPos(i, y)
                    self.mc_pg_01.addItem(marker)

    def cross_hair(self, y, pc, main_pg=None, sub_pg=None):
        if main_pg is not None:
            vLine1 = pg.InfiniteLine(angle=90, movable=False)
            vLine1.setPen(pg.mkPen('#ffffff', width=0.5))
            hLine = pg.InfiniteLine(angle=0, movable=False)
            hLine.setPen(pg.mkPen('#ffffff', width=0.5))
            main_pg.addItem(vLine1, ignoreBounds=True)
            main_pg.addItem(hLine, ignoreBounds=True)
            main_vb = main_pg.getViewBox()
            label = pg.TextItem(color='#e6e6eb', border='#323237', fill=(50, 50, 55, 200))
            label.setFont(self.font)
            label.setPos(15, y)
            label.setText(f"전일종가 {pc}\n라인종가 000000\n등락율     0.00%")
            main_pg.addItem(label)
        if sub_pg is not None:
            vLine2 = pg.InfiniteLine(angle=90, movable=False)
            vLine2.setPen(pg.mkPen('#ffffff', width=0.5))
            sub_pg.addItem(vLine2, ignoreBounds=True)
            sub_vb = sub_pg.getViewBox()

        def mouseMoved(evt):
            pos = evt[0]
            if main_pg is not None and main_pg.sceneBoundingRect().contains(pos):
                mousePoint = main_vb.mapSceneToView(pos)
                per = round((mousePoint.y() / pc - 1) * 100, 2)
                label.setText(f"전일종가 {pc}\n라인종가 {int(mousePoint.y())}\n등락율     {per}%")
                vLine1.setPos(mousePoint.x())
                hLine.setPos(mousePoint.y())
                if sub_pg is not None:
                    vLine2.setPos(mousePoint.x())
            if sub_pg is not None and sub_pg.sceneBoundingRect().contains(pos):
                mousePoint = sub_vb.mapSceneToView(pos)
                vLine1.setPos(mousePoint.x())
                vLine2.setPos(mousePoint.x())
        if main_pg is not None:
            main_pg.proxy = pg.SignalProxy(main_pg.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)
        if sub_pg is not None:
            sub_pg.proxy = pg.SignalProxy(main_pg.scene().sigMouseMoved, rateLimit=20, slot=mouseMoved)

    # noinspection PyMethodMayBeStatic
    def GetMainLegendText(self, df):
        ema05 = df['지수이평05'][-1]
        ema10 = df['지수이평10'][-1]
        ema20 = df['지수이평20'][-1]
        c = df['현재가'][-1]
        per = round((c / df['전일종가'][-1] - 1) * 100, 2)
        text = f"05이평 {ema05}\n10이평 {ema10}\n20이평 {ema20}\n등락율 {per}%\n현재가 {c}"
        return text

    # noinspection PyMethodMayBeStatic
    def GetSubLegendText(self, df):
        per = round(df['거래량'][-1] / df['거래량'][-2] * 100, 2)
        text = f"거래량 {df['거래량'][-1]}\n증감 {per}%"
        return text


class Writer(QtCore.QThread):
    data0 = QtCore.pyqtSignal(str)
    data1 = QtCore.pyqtSignal(pd.DataFrame)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            if not dataQ.empty():
                data = dataQ.get()
                if type(data) == str:
                    self.data0.emit(data)
                elif type(data) == pd.DataFrame:
                    self.data1.emit(data)
            time.sleep(0.0001)


if __name__ == "__main__":
    dataQ, tranQ = Queue(), Queue()
    Process(target=Worker, args=(dataQ, tranQ,), daemon=True).start()
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    dark_palette = QtGui.QPalette()
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(40, 40, 45))
    dark_palette.setColor(QtGui.QPalette.Background, QtGui.QColor(40, 40, 45))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(190, 190, 195))
    dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(40, 40, 45))
    dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(30, 30, 35))
    dark_palette.setColor(QtGui.QPalette.Text, QtGui.QColor(190, 190, 195))
    dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(40, 40, 45))
    dark_palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(190, 190, 195))
    app.setPalette(dark_palette)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
