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

# Please replace these with your Binance API credentials

class TradingWidget(QWidget):
    def __init__(self):
        super().__init__()

        
        self.layout = QGridLayout()

        # The ComboBox for asset selection.
        self.asset_selection = QComboBox()
        self.asset_selection.addItems(["Bitcoin", "Ethereum", "Solana"])  # Add your assets here
        self.layout.addWidget(QLabel("Select asset:"), 0, 0)
        self.layout.addWidget(self.asset_selection, 0, 1)

        # Label to display current position
        self.position_label = QLabel("Current position: Not fetched yet")
        self.layout.addWidget(self.position_label, 1, 0, 1, 2)

        # The Slider for position adjustment within a range.
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 100)  # Set the range according to your needs
        self.layout.addWidget(QLabel("Set new position (0-100):"), 2, 0)
        self.layout.addWidget(self.position_slider, 2, 1)

        # The LineEdit for precise position adjustment.
        self.position_input = QLineEdit()
        self.layout.addWidget(self.position_input, 3, 0, 1, 2)

        # Button to execute trade
        self.trade_button = QPushButton("Execute trade")
        self.layout.addWidget(self.trade_button, 4, 0, 1, 2)

        self.setLayout(self.layout)
