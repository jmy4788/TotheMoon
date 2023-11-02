import logging
from qt_core import *
from ..my_combobox import MYCombobox
from ..py_slider import PySlider
from ..py_push_button import PyPushButton

from gui.core.json_themes import Themes

themes = Themes()
themes = themes.items

style_sheet_trading = """
QRadioButton {
    font: bold 15px;
    color: #ffffff;
    padding: 10px;
}
QRadioButton::indicator {
    width: 20px;
    height: 20px;
    border-radius: 7px;
    background: #c3ccdf;
}
QRadioButton::indicator:checked {
    background-color: #0075FF;
}
QLabel {
    color: #ffffff;  /* Text color */
    font-size: 15px;  /* Font size */
    font-weight: bold;  /* Font weight */
}
QLineEdit {
        font-size: 13px;
        font-weight: bold;
        color: #dce1ec;
        background-color: #2c313c;
        border: 1px solid #6c99f4;
        border-radius: 5px;
        padding: 3px;
    }
QLineEdit:focus {
        border: 2px solid #00ff7f;
    }
QLineEdit:disabled {
        background-color: #cccccc;
    }
"""

class OrderCreationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        # Layout
        layout = QVBoxLayout()

        # 폰트 설정
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)

        # 1.1.1 Stacked widget 생성
        self.stacked_widget = QStackedWidget(self)
        # 1.1.2 Spot 위젯 및 레이아웃 생성
        self.spot_widget = QWidget(self)
        self.spot_layout = QVBoxLayout(self.spot_widget)
        # 1.1.3 Futures 위젯 및 레이아웃 생성
        self.futures_widget = QWidget(self)
        self.futures_layout = QVBoxLayout(self.futures_widget)
        # 1.1.4 Stacked 위젯 안에 Spot 및 Futures 위젯 추가
        self.stacked_widget.addWidget(self.spot_widget)
        self.stacked_widget.addWidget(self.futures_widget)
        # 1.1.5 Tab widget 추가 to switch between Spot and Futures
        self.tab_widget = QTabWidget(self)
        self.tab_widget.addTab(self.spot_widget, "Spot")
        self.tab_widget.addTab(self.futures_widget, "Futures")
        self.tab_widget.setStyleSheet("""
            QWidget {
            background-color: #343b48;
            color: #8a95aa;
            }
            QTabWidget::pane {
                background-color: #343b48;
            }
            QTabBar::tab {
                background-color: #4a5360;
                color: #8a95aa;
                width: 80px; /* Tab width */
                height: 30px; /* Tab height */
                font-size: 13px; /* Font size */
            }
            QTabBar::tab:selected {
                background-color: #343b48;
                color: #8a95aa;
            }
        """)
        # 1.1.6 layout에 tab widget 추가
        layout.addWidget(self.tab_widget)



        # 2.1.1 Comobo box 추가
        self.spot_combo = MYCombobox()
        self.futures_combo = MYCombobox()
        self.spot_combo.addItem("BTCUSDT")
        self.spot_combo.addItem("ETHUSDT")
        self.futures_combo.addItem("BTCUSDT")
        self.futures_combo.addItem("ETHUSDT")
        # 2.1.2 Comobo box를 layout에 추가
        self.spot_layout.addWidget(self.spot_combo)
        self.futures_layout.addWidget(self.futures_combo)
        
        # road text from self.futures_combo

        # 2.2.1 Buy 및 Sell 버튼 Here
        self.btn_grp_buy_sell = QButtonGroup(self)
        self.radio_buy = QRadioButton("Buy")
        self.radio_buy.setStyleSheet(style_sheet_trading)
        self.radio_sell = QRadioButton("Sell")
        self.radio_sell.setStyleSheet(style_sheet_trading)
        self.btn_grp_buy_sell.addButton(self.radio_buy)
        self.btn_grp_buy_sell.addButton(self.radio_sell)
        self.radio_buy.setChecked(True)
        # 2.2.2 Buy 및 Sell 버튼 Layout 추가
        self.hlayout_buy_sell = QHBoxLayout()
        self.hlayout_buy_sell.addWidget(self.radio_buy)
        self.hlayout_buy_sell.addWidget(self.radio_sell)
        self.futures_layout.addLayout(self.hlayout_buy_sell)

        # 2.3.1 Limit, Market, Stop 버튼 Here
        self.btn_grp_order = QButtonGroup(self)
        self.radio_limit = QRadioButton("Limit")
        self.radio_limit.setStyleSheet(style_sheet_trading)
        self.radio_market = QRadioButton("Market")
        self.radio_market.setStyleSheet(style_sheet_trading)
        self.radio_stop = QRadioButton("Stop")
        self.radio_stop.setStyleSheet(style_sheet_trading)
        self.btn_grp_order.addButton(self.radio_limit)
        self.btn_grp_order.addButton(self.radio_market)
        self.btn_grp_order.addButton(self.radio_stop)
        self.radio_limit.setChecked(True)
        # 2.3.2 Limit, Market, Stop 버튼 Layout 추가
        self.hlayout_limit_market_stop = QHBoxLayout()
        self.hlayout_limit_market_stop.addWidget(self.radio_limit)
        self.hlayout_limit_market_stop.addWidget(self.radio_market)
        self.hlayout_limit_market_stop.addWidget(self.radio_stop)
        self.futures_layout.addLayout(self.hlayout_limit_market_stop)

        # 2.4.1 입력용 - QLabel 및 QLineEdit
        self.lbl_price = QLabel("Price :")
        self.lbl_qty = QLabel("Quantity :")
        self.lbl_stop_price = QLabel("Stop Price:")
        self.lbl_price.setStyleSheet(style_sheet_trading)
        self.lbl_qty.setStyleSheet(style_sheet_trading)
        self.lbl_stop_price.setStyleSheet(style_sheet_trading)

        self.input_price = QLineEdit(self)
        self.input_price.setStyleSheet(style_sheet_trading)
        self.input_qty = QLineEdit(self)
        self.input_qty.setStyleSheet(style_sheet_trading)
        self.input_stop_price = QLineEdit(self)
        self.input_stop_price.setStyleSheet(style_sheet_trading)
        
        # 2.4.2 Grid layout 생성 (QLabel, QLineEdit 입력을 위한)
        grid = QGridLayout()
        grid.addWidget(self.lbl_price, 0, 0)
        grid.addWidget(self.input_price, 0, 1)
        grid.addWidget(self.lbl_qty, 1, 0)
        grid.addWidget(self.input_qty, 1, 1)
        grid.addWidget(self.lbl_stop_price, 2, 0)
        grid.addWidget(self.input_stop_price, 2, 1)
        self.futures_layout.addLayout(grid)

        # 2.5.1 슬라이더 입력 Here
        self.price_slider = PySlider(
            margin=8,
            bg_size=10,
            bg_radius=5,
            handle_margin=-3,
            handle_size=16,
            handle_radius=8,
            bg_color = themes["app_color"]["dark_three"],
            bg_color_hover = themes["app_color"]["dark_four"],
            handle_color = themes["app_color"]["context_color"],
            handle_color_hover = themes["app_color"]["context_hover"],
            handle_color_pressed = themes["app_color"]["context_pressed"]
        )
        self.price_slider.setOrientation(Qt.Horizontal)
        # 2.5.2 슬라이더 기능 추가
        self.lbl_slider_value = QLabel("0%")
        self.lbl_slider_value.setStyleSheet(style_sheet_trading)
        self.price_slider.valueChanged.connect(lambda: self.lbl_slider_value.setText(f"{self.price_slider.value()} %"))
        # self.price_slider.setMaximumWidth(400)
        
        # 2.5.3 슬라이더와 슬라이더 값 표시를 위한 레이아웃 추가
        self.hlayout_slider = QHBoxLayout()
        # 23.10.03 여기에 Available value 추가 해야 함
        self.hlayout_slider.addWidget(self.lbl_slider_value)
        self.hlayout_slider.addWidget(self.price_slider)
        self.futures_layout.addLayout(self.hlayout_slider)

        # 2.6.1 Binance 주문 생성에 입력하는 파라미터 Display label
        self.lbl_intro = QLabel("Your order will be created with below params")
        self.lbl_intro.setStyleSheet("color: #dce1ec; font-size: 17px; font-weight: bold;")
        self.lbl_binance_input = QLabel("Binance Input Parameters:\n")
        self.lbl_binance_input.setStyleSheet("color: #dce1ec; font-size: 15px; font-weight: bold;")
        self.futures_layout.addWidget(self.lbl_intro)
        self.futures_layout.addWidget(self.lbl_binance_input)
        
        # 2.7.1 주문 생성 버튼 (Excute Order) 추가
        self.btn_execute_order = QPushButton("Execute order", self)
        self.btn_execute_order.setStyleSheet("""
            QPushButton {
                font-weight: bold;  
                background-color: #2c313c;
                border: 1px solid #6c99f4;
                color: #dce1ec;
                padding: 3px 3px;
                text-align: center;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #6c99f4;
            }
            QPushButton:pressed {
                background-color: #568af2;
            }
        """)

        self.btn_execute_order.clicked.connect(self.place_order)
        self.futures_layout.addWidget(self.btn_execute_order)
        self.futures_layout.addStretch(1)
        
        # 3.1.1 프레임 및 Main layout 설정
        frame = QFrame()
        frame.setLayout(layout)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(frame)
        

        # Events
        self.radio_limit.toggled.connect(self.update_input_fields_visibility)
        self.radio_market.toggled.connect(self.update_input_fields_visibility)
        self.radio_stop.toggled.connect(self.update_input_fields_visibility)
        self.update_input_fields_visibility()

        # Connect signals to update lbl_binance_input
        
        self.futures_combo.currentTextChanged.connect(self.update_binance_input)
        self.radio_buy.toggled.connect(self.update_binance_input)
        self.radio_sell.toggled.connect(self.update_binance_input)
        self.radio_limit.toggled.connect(self.update_binance_input)
        self.radio_market.toggled.connect(self.update_binance_input)
        self.radio_stop.toggled.connect(self.update_binance_input)
        self.input_price.textChanged.connect(self.update_binance_input)
        self.input_qty.textChanged.connect(self.update_binance_input)
        self.input_stop_price.textChanged.connect(self.update_binance_input)
        
        # If you had some initial default values, you might want to call update_binance_input once at the end of your init to populate lbl_binance_input
        self.update_binance_input()


    def update_binance_input(self):
        symbol = self.futures_combo.currentText()  # Replace this with your actual symbol
        side = "BUY" if self.radio_buy.isChecked() else "SELL"
        order_type = "LIMIT" if self.radio_limit.isChecked() else ("MARKET" if self.radio_market.isChecked() else "STOP")
        price = self.input_price.text()
        quantity = self.input_qty.text()
        stop_price = self.input_stop_price.text()
        binance_input = f"Symbol: {symbol}\nSide: {side}\nType: {order_type}\nPrice: {price}\nQuantity: {quantity}\nStop Price: {stop_price}"
        self.lbl_binance_input.setText(binance_input)

    def update_input_fields_visibility(self):
        """Hide/show input fields based on order type"""
        self.input_price.setVisible(self.radio_limit.isChecked() or self.radio_stop.isChecked())
        self.lbl_price.setVisible(self.radio_limit.isChecked() or self.radio_stop.isChecked())
        self.input_stop_price.setVisible(self.radio_stop.isChecked())
        self.lbl_stop_price.setVisible(self.radio_stop.isChecked())

    def place_order(self):
        pass

