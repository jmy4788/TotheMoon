import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


"""
Q MainWindow에서는 Qt.AlignVcenter가 안 먹는 것 같음
Q Widget 에서만 아래 명령어가 먹네, 내일 다시 생각해봐야 할 듯
> QMainWindow에서는 layout 동작 안함, 자체 layout이  따로 존재하기 때문
"""


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.font = QFont("마루부리", 11)
        self.setFont(self.font)
        #init UI를 구성한다.
        self.initUI()

    def initUI(self):
        wg = Double_Widget()
        self.setCentralWidget(wg)
        self.setWindowTitle('QMainWindow창 입니다.')

        #메뉴바 구성
        menubar = self.menuBar()
        filemenu = menubar.addMenu('&File')
        #filemenu.addAction(exitAction)

        self.resize(1920, 1080)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        #cp = QDesktopWidget().availableGeometry().center()
        #qr.moveCenter(cp)
        self.move(qr.topLeft())


class Widget(QWidget):

    def __init__(self):
        super().__init__()
        #init UI를 구성한다.
        self.initUI()

    def initUI(self):
        # 폰트 설정
        font1 = QFont("마루부리", 11)
        font2 = QFont("나눔스퀘어", 11)

        grid = QGridLayout()
        self.setLayout(grid)

        label1 = QLabel('폰트 테스트1', self)
        label2 = QLabel('폰트 테스트2', self)
        label1.setAlignment(Qt.AlignCenter)
        label2.setAlignment(Qt.AlignCenter)
        label1.setFont(font1)
        label2.setFont(font2)

        grid.addWidget(label1, 0, 0)
        grid.addWidget(label2, 1, 0)
        # addWidget(배치시킬 위젯, 행 위치, 열 위치, 행 폭, 열 폭)

        self.setWindowTitle('ct widget')
        self.setGeometry(300, 300, 300, 200)
        self.show()


class Double_Widget(QWidget):

    def __init__(self):
        super().__init__()
        #init UI를 구성한다.
        self.initUI()

    def initUI(self):
        # 폰트 설정
        wg1 = Widget()
        wg2 = Widget()

        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(wg1, 0, 0)
        grid.addWidget(wg2, 0, 1)

        self.setWindowTitle('ct widget')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyle(QStyleFactory().create('Windows'))
    ex = MyWindow()
    app.exec()
