from qt_core import *
from gui.widgets.my_combobox.my_combobox import MYCombobox
from gui.widgets.my_chart.my_chart import BitcoinChart

class ChartPage(QWidget):
    def __init__(self):
        super().__init__()

        self.ticker = "BTCUSDT"
        self.dist = "1h"

        # Create layout for the ChartPage
        self.main_layout = QVBoxLayout()

        # Top HLayout containing a combobox and radio buttons
        self.top_hlayout = QHBoxLayout()

        self.combobox = MYCombobox()
        self.combobox.addItem("BTCUSDT")
        self.combobox.addItem("ETHUSDT")
        self.combobox.addItem("SOLUSDT")
        self.combobox.addItem("ICPUSDT")

        
        self.combobox.currentIndexChanged.connect(self.update_ticker)
        self.top_hlayout.addWidget(self.combobox)
        self.top_hlayout.addStretch(1)
        # Radiobutton names
        time_frames = ["5m", "15m", "1h", "4h", "1d"]

        font = QFont()
        font.setPointSize(13)

        self.radio_buttons = {}  # Store radio buttons in a dictionary for easy access
        for frame in time_frames:
            btn = QRadioButton(frame, self)
            btn.setFont(font)
            if frame == self.dist:
                btn.setChecked(True)
            btn.toggled.connect(self.update_dist)
            self.radio_buttons[frame] = btn
            self.top_hlayout.addWidget(btn)

        self.main_layout.addLayout(self.top_hlayout)

        # DrawChart widget at the bottom
        self.chart = BitcoinChart(self.ticker, self.dist)
        self.main_layout.addWidget(self.chart)

        # Set the main layout
        self.setLayout(self.main_layout)

    def update_ticker(self, index):
        self.ticker = self.combobox.itemText(index)
        self.update_chart()

    def update_dist(self, checked):
        # Check which radio button is selected
        for frame, btn in self.radio_buttons.items():
            if btn.isChecked():
                self.dist = frame
                break
        self.update_chart()

    def update_chart(self):
        # Function that deletes and draws a new DrawChart QWidget
        self.chart.deleteLater()
        self.chart = BitcoinChart(self.ticker, self.dist)
        self.chart.setStyleSheet("background-color: lightgray;")  # Placeholder styling
        self.main_layout.addWidget(self.chart)
