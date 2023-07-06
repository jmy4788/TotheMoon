# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////


# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *
from gui.widgets import *
from gui.core.json_themes import Themes
from gui.themes import my_style
# my common style을 import 하는 행

import datetime

# QLabel style
theme = Themes().items

import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QSlider, QLabel
from PySide6.QtCore import Qt
from binance.client import Client

# Please replace these with your Binance API credentials
API_KEY = "YOUR_BINANCE_API_KEY"
API_SECRET = "YOUR_BINANCE_API_SECRET"

class TradingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.binance_client = Client(API_KEY, API_SECRET)

        self.layout = QVBoxLayout(self)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(-1)
        self.slider.setMaximum(1)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.slider_value_changed)

        self.status_label = QLabel("Neutral")

        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.status_label)

    def slider_value_changed(self, value):
        if value == 1:
            # Place spot order with 100% of current asset
            self.status_label.setText("Placed spot order")
            # self.binance_client.order_market_buy(...)
        elif value == -1:
            # Place short futures position with 100% of current asset
            self.status_label.setText("Placed short futures position")
            # self.binance_client.futures_create_order(...)
        else:
            # Neutral state: 50% spot order and 50% short futures position
            self.status_label.setText("Placed 50% spot order and 50% short futures position")
            # self.binance_client.order_market_buy(...)
            # self.binance_client.futures_create_order(...)

app = QApplication(sys.argv)

window = TradingWidget()
window.show()

sys.exit(app.exec())
