import pyqtgraph as pg
from PyQt5 import QtGui, QtCore


class CandlesticksItem(pg.GraphicsObject):
    def __init__(self, df):
        pg.GraphicsObject.__init__(self)
        self.picture = QtGui.QPicture()
        self.CandleSticks(df)

    def CandleSticks(self, df):
        p = QtGui.QPainter(self.picture)
        p.setBrush(pg.mkBrush('#232328'))
        p.setPen(pg.mkPen('#232328'))
        prev_chuse = False
        start = ""
        ll = df['저가'].min()
        hh = df['고가'].max() - df['저가'].min()
        for i, index in enumerate(df.index):
            chuse = df['추세05'][index] and df['추세10'][index] and df['추세20'][index]
            if prev_chuse != chuse:
                if chuse:
                    start = i
                else:
                    w = i - start
                    p.drawRect(QtCore.QRectF(start, ll, w, hh))
            if prev_chuse and index == df.index[-1]:
                w = i - start
                p.drawRect(QtCore.QRectF(start, ll, w, hh))
            prev_chuse = chuse
        for i, index in enumerate(df.index):
            if i == len(df) - 1:
                break
            c = df['현재가'][index]
            o = df['시가'][index]
            h = df['고가'][index]
            ll = df['저가'][index]
            if c >= o:
                p.setPen(pg.mkPen('#e6e6eb'))
                p.setBrush(pg.mkBrush('#e6e6eb'))
            else:
                p.setPen(pg.mkPen('#646469'))
                p.setBrush(pg.mkBrush('#646469'))
            p.drawLine(QtCore.QPointF(i, h), QtCore.QPointF(i, ll))
            p.drawRect(QtCore.QRectF(i - 0.25, o, 0.25 * 2, c - o))
            if index != df.index[-1]:
                ema050 = df['지수이평05'][index]
                ema051 = df['지수이평05'][i+1]
                ema100 = df['지수이평10'][index]
                ema101 = df['지수이평10'][i+1]
                ema200 = df['지수이평20'][index]
                ema201 = df['지수이평20'][i+1]
                p.setPen(pg.mkPen('#e6e6eb'))
                p.drawLine(QtCore.QPointF(i, ema050), QtCore.QPointF(i + 1, ema051))
                p.setPen(pg.mkPen('#87878c'))
                p.drawLine(QtCore.QPointF(i, ema100), QtCore.QPointF(i + 1, ema101))
                p.setPen(pg.mkPen('#404040'))
                p.drawLine(QtCore.QPointF(i, ema200), QtCore.QPointF(i + 1, ema201))
        p.end()

    def paint(self, p, *args):
        if args is None:
            return
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


class LastCandlestickItem(pg.GraphicsObject):
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


class VolumeBarsItem(pg.GraphicsObject):
    def __init__(self, df):
        pg.GraphicsObject.__init__(self)
        self.picture = QtGui.QPicture()
        self.VolumeBars(df)

    def VolumeBars(self, df):
        p = QtGui.QPainter(self.picture)
        for i, index in enumerate(df.index):
            c = df['현재가'][index]
            o = df['시가'][index]
            v = df['거래량'][index]
            if c >= o:
                p.setPen(pg.mkPen('#e6e6eb'))
                p.setBrush(pg.mkBrush('#e6e6eb'))
            else:
                p.setPen(pg.mkPen('#646469'))
                p.setBrush(pg.mkBrush('#646469'))
            p.drawRect(QtCore.QRectF(i - 0.25, 0, 0.25 * 2, v))
        p.end()

    def paint(self, p, *args):
        if args is None:
            return
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


class LastVolumeBarItem(pg.GraphicsObject):
    def __init__(self, x, c, o, v):
        pg.GraphicsObject.__init__(self)
        self.picture = QtGui.QPicture()
        self.LastVolumebar(x, c, o, v)

    def LastVolumebar(self, x, c, o, v):
        p = QtGui.QPainter(self.picture)
        p.setBrush(pg.mkBrush('#1e1e23'))
        p.setPen(pg.mkPen('#1e1e23'))
        p.drawRect(QtCore.QRectF(x - 0.25, 0, 0.25 * 2, v))
        if c >= o:
            p.setPen(pg.mkPen('#e6e6eb'))
            p.setBrush(pg.mkBrush('#e6e6eb'))
        else:
            p.setPen(pg.mkPen('#646469'))
            p.setBrush(pg.mkBrush('#646469'))
        p.drawRect(QtCore.QRectF(x - 0.25, 0, 0.25 * 2, v))
        p.end()

    def paint(self, p, *args):
        if args is None:
            return
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())
