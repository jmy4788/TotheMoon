import logging
from qt_core import *
from ..my_combobox import MYCombobox
config_logging(logging, logging.DEBUG)
from PyQt5.QtWidgets import QWidget, QPushButton, QRadioButton, QSlider, QComboBox


class BaseTradingWidget(QWidget):
    def __init__(self, parent=None):
        super(BaseTradingWidget, self).__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: #2c313c;
            }
            QPushButton {
                background-color: #343b48;
                color: #dce1ec;
            }
            /* Add more styles */
        """)

        # Initialize your MyComboBox here
        self.tickerComboBox = MyComboBox(self)

        # Initialize Buy and Sell buttons
        self.buyButton = QPushButton("Buy", self)
        self.sellButton = QPushButton("Sell", self)

        # Initialize Radio buttons for order type
        self.limitRadio = QRadioButton("Limit", self)
        self.marketRadio = QRadioButton("Market", self)
        self.stopRadio = QRadioButton("Stop", self)

        # Initialize Slider for asset-based quantity
        self.assetSlider = QSlider(self)

        # Initialize Order Execution button
        self.executeButton = QPushButton("Execute Order", self)

        # Add these widgets to layout (not shown here)

class SpotWidget(BaseTradingWidget):
    def __init__(self, parent=None):
        super(SpotWidget, self).__init__(parent)
        # Spot-specific functionalities

class FuturesWidget(BaseTradingWidget):
    def __init__(self, parent=None):
        super(FuturesWidget, self).__init__(parent)
        # Futures-specific functionalities