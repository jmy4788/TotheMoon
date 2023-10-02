import logging
from qt_core import *
from ..my_combobox import MYCombobox
config_logging(logging, logging.DEBUG)


class OrderCreationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def create_order_type_widget(self):
        widget = QWidget(self)
        layout = QVBoxLayout(widget)
        
        btn_grp_buy_sell = QButtonGroup(self)

        radio_buy = QRadioButton("Buy")
        radio_buy.setStyleSheet("QRadioButton { color: #55AA69; }")
        radio_sell = QRadioButton("Sell")
        radio_sell.setStyleSheet("QRadioButton { color: #B93446; }")

        # Add buttons to button group
        btn_grp_buy_sell.addButton(radio_buy)
        btn_grp_buy_sell.addButton(radio_sell)

        radio_buy.setChecked(True)

        # Radio buttons for order type: Limit, Market, Stop
        radio_limit = QRadioButton("Limit")
        radio_market = QRadioButton("Market")
        radio_stop = QRadioButton("Stop")
        # setup radio buttons... (omitted for brevity)
        
        layout.addWidget(btn_buy)
        layout.addWidget(btn_sell)
        layout.addWidget(radio_limit)
        layout.addWidget(radio_market)
        layout.addWidget(radio_stop)
        
        combo = MYCombobox()
        combo.addItem("BTCUSDT")
        combo.addItem("ETHUSDT")
        layout.addWidget(combo)

        return widget, layout
        
    def init_ui(self):
        # Layout
        layout = QVBoxLayout()

        # 폰트 설정
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)

        self.stacked_widget = QStackedWidget(self)
        # Create a Spot widget
        self.spot_widget = QWidget(self)
        self.spot_layout = QVBoxLayout(self.spot_widget)
        # Add additional Spot-specific UI elements to self.spot_layout if needed

        # Create a Futures widget
        self.futures_widget = QWidget(self)
        self.futures_layout = QVBoxLayout(self.futures_widget)
        # Add additional Futures-specific UI elements to self.futures_layout if needed

        # Add widgets to the stacked widget
        self.stacked_widget.addWidget(self.spot_widget)
        self.stacked_widget.addWidget(self.futures_widget)

        # Tab widget to switch between Spot and Futures
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




        # Combobox for choosing Ticker
        self.spot_combo = MYCombobox()
        self.futures_combo = MYCombobox()
        self.spot_combo.addItem("BTCUSDT")
        self.spot_combo.addItem("ETHUSDT")
        self.futures_combo.addItem("BTCUSDT")
        self.futures_combo.addItem("ETHUSDT")

        # Add comboboxes to the respective layouts
        self.spot_layout.addWidget(self.spot_combo)
        self.futures_layout.addWidget(self.futures_combo)
        
        # Horizontal layout for Spot radio button and combobox
        layout.addWidget(self.tab_widget)

        # Buy/Sell buttons with color toggle on press
        
        style_sheet_radio = """
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
        """
        # 4.1.1 Buy 및 Sell 버튼 Here
        self.btn_grp_buy_sell = QButtonGroup(self)
        self.radio_buy = QRadioButton("Buy")
        self.radio_buy.setStyleSheet(style_sheet_radio)
        self.radio_sell = QRadioButton("Sell")
        self.radio_sell.setStyleSheet(style_sheet_radio)
        self.btn_grp_buy_sell.addButton(self.radio_buy)
        self.btn_grp_buy_sell.addButton(self.radio_sell)
        self.radio_buy.setChecked(True)
        # 4.1.2 Buy 및 Sell 버튼 Layout 추가
        self.hlayout_buy_sell = QHBoxLayout()
        self.hlayout_buy_sell.addWidget(self.radio_buy)
        self.hlayout_buy_sell.addWidget(self.radio_sell)
        self.futures_layout.addLayout(self.hlayout_buy_sell)

        # 4.2.1 Limit, Market, Stop 버튼 Here
        self.btn_grp_order = QButtonGroup(self)
        self.radio_limit = QRadioButton("Limit")
        self.radio_limit.setStyleSheet(style_sheet_radio)
        self.radio_market = QRadioButton("Market")
        self.radio_market.setStyleSheet(style_sheet_radio)
        self.radio_stop = QRadioButton("Stop")
        self.radio_stop.setStyleSheet(style_sheet_radio)
        self.btn_grp_order.addButton(self.radio_limit)
        self.btn_grp_order.addButton(self.radio_market)
        self.btn_grp_order.addButton(self.radio_stop)
        self.radio_limit.setChecked(True)
        # 4.2.2 Limit, Market, Stop 버튼 Layout 추가
        self.hlayout_limit_market_stop = QHBoxLayout()
        self.hlayout_limit_market_stop.addWidget(self.radio_limit)
        self.hlayout_limit_market_stop.addWidget(self.radio_market)
        self.hlayout_limit_market_stop.addWidget(self.radio_stop)
        self.futures_layout.addLayout(self.hlayout_limit_market_stop)

        # 4.3.1 입력필드 Here
        self.lbl_price = QLabel("Price:")
        self.input_price = QLineEdit(self)
        self.lbl_qty = QLabel("Quantity:")
        self.input_qty = QLineEdit(self)
        self.lbl_stop_price = QLabel("Stop Price:")
        self.input_stop_price = QLineEdit(self)
        # 4.3.2 슬라이더 입력 Here
        self.slider = QSlider(Qt.Horizontal)
        self.lbl_slider_value = QLabel("0%")
        self.slider.valueChanged.connect(lambda: self.lbl_slider_value.setText(f"{self.slider.value()}%"))
        # 4.3.3 Excute Order 버튼 Here
        self.btn_execute_order = QPushButton("Execute Order", self)
        self.btn_execute_order.clicked.connect(self.place_order)
        
        grid = QGridLayout()
        grid.addWidget(self.lbl_price, 0, 0)
        grid.addWidget(self.input_price, 0, 1)
        grid.addWidget(self.lbl_qty, 1, 0)
        grid.addWidget(self.input_qty, 1, 1)
        grid.addWidget(self.lbl_stop_price, 2, 0)
        grid.addWidget(self.input_stop_price, 2, 1)
        
        self.futures_layout.addLayout(grid)
        self.futures_layout.addWidget(self.slider)
        self.futures_layout.addWidget(self.lbl_slider_value)
        self.futures_layout.addWidget(self.btn_execute_order)
        
        # Frame for grouping
        frame = QFrame()
        frame.setLayout(layout)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(frame)

        # Events
        self.radio_limit.toggled.connect(self.update_input_fields_visibility)
        self.radio_market.toggled.connect(self.update_input_fields_visibility)
        self.radio_stop.toggled.connect(self.update_input_fields_visibility)
        self.update_input_fields_visibility()

        self.lbl_binance_input = QLabel("Binance Input Parameters:\n")
        
        self.futures_layout.addWidget(self.lbl_binance_input)
        
        # Connect signals to update lbl_binance_input
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
        symbol = "YOUR_SYMBOL_HERE"  # Replace this with your actual symbol
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
        if self.btn_buy.isChecked():
            order_type = "BUY"
        elif self.btn_sell.isChecked():
            order_type = "SELL"
        else:
            # Neither button selected, show an error or return without doing anything
            QMessageBox.warning(self, "Warning", "Please select either Buy or Sell!")
            return
        if self.sender() == self.btn_buy:
            order_type = "BUY"
        else:
            order_type = "SELL"

        if self.radio_limit.isChecked():
            order_method = "LIMIT"
        elif self.radio_market.isChecked():
            order_method = "MARKET"
        else:
            order_method = "STOP"

        # Collect common order parameters
        order_params = {
            "symbol": self.combo_ticker.currentText(),
            "side": order_type,
            "type": order_method,
            "quantity": float(self.input_qty.text()),
            "timeInForce": "GTC",
        }

        # Add price if relevant based on order method
        if self.input_price.isVisible():
            order_params["price"] = float(self.input_price.text())

        try:
            if self.tab_widget.currentIndex() == 1:  # If Futures tab is active
                # Place a futures order
                response = UMFutures.new_order(**order_params)
            else:  # Default to Spot if no tab or the first tab is active
                # Place a spot order
                response = Spot.new_order(**order_params)

            logging.info(response)

        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
