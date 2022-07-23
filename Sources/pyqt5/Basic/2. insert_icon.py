import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QIcon


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('insert icon')
        self.setWindowIcon(QIcon(iconpath+'Yeji.jpg'))
        self.setGeometry(1920/2, 1080/2, 500, 500)
        self.show()


if __name__ == '__main__':
    iconpath = r'C:\Users\jmy47\Downloads/'
    app = QApplication(sys.argv)
    ex = MyApp()
    print("before eventloop")
    app.exec()
    print("after eventloop")