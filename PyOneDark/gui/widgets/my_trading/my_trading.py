import logging
from qt_core import *
from ..my_combobox import MYCombobox
config_logging(logging, logging.DEBUG)

class OrderCreationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Layout
        layout = QVBoxLayout()

        # Configure font for radio buttons
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)

        self.radio_spot = QRadioButton("Spot")
        self.radio_spot.setFont(font)
        self.radio_futures = QRadioButton("Futures")
        self.radio_futures.setFont(font)
        self.radio_spot.setChecked(True)
        self.btn_grp_type = QButtonGroup(self)
        self.btn_grp_type.addButton(self.radio_spot)
        self.btn_grp_type.addButton(self.radio_futures)

        # Combobox for choosing Ticker
        self.combo_ticker = MYCombobox()
        self.combo_ticker.addItem("BTCUSDT")
        self.combo_ticker.addItem("ETHUSDT")

        # Horizontal layout for Spot radio button and combobox
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.radio_spot)
        hlayout.addWidget(self.combo_ticker)

        # Buy/Sell buttons with color toggle on press
        self.btn_buy = QPushButton("Buy", self)
        self.btn_buy.setCheckable(True)
        self.btn_buy.pressed.connect(lambda: self.btn_buy.setStyleSheet("background-color: rgb(85, 170, 105); color: white;"))
        self.btn_buy.released.connect(lambda: self.btn_buy.setStyleSheet("background-color: rgb(95, 189, 123); color: white;"))
        
        self.btn_sell = QPushButton("Sell", self)
        self.btn_sell.setCheckable(True)
        self.btn_sell.pressed.connect(lambda: self.btn_sell.setStyleSheet("background-color: rgb(185, 52, 70); color: white;"))
        self.btn_sell.released.connect(lambda: self.btn_sell.setStyleSheet("background-color: rgb(195, 62, 80); color: white;"))
        
        self.btn_buy.toggled.connect(self.on_buy_sell_toggle)
        self.btn_sell.toggled.connect(self.on_buy_sell_toggle)

        # Radio buttons for order type: Limit, Market, Stop
        self.radio_limit = QRadioButton("Limit")
        self.radio_market = QRadioButton("Market")
        self.radio_stop = QRadioButton("Stop")
        self.radio_limit.setChecked(True)
        self.btn_grp_order = QButtonGroup(self)
        self.btn_grp_order.addButton(self.radio_limit)
        self.btn_grp_order.addButton(self.radio_market)
        self.btn_grp_order.addButton(self.radio_stop)

        # Input fields
        self.lbl_price = QLabel("Price:")
        self.input_price = QLineEdit(self)
        self.lbl_qty = QLabel("Quantity:")
        self.input_qty = QLineEdit(self)
        self.lbl_stop_price = QLabel("Stop Price:")
        self.input_stop_price = QLineEdit(self)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.lbl_slider_value = QLabel("0%")
        self.slider.valueChanged.connect(lambda: self.lbl_slider_value.setText(f"{self.slider.value()}%"))

        self.btn_execute_order = QPushButton("Execute Order", self)
        self.btn_execute_order.clicked.connect(self.place_order)

        # Setup layout
        layout.addLayout(hlayout)
        layout.addWidget(self.radio_futures)
        layout.addWidget(self.btn_buy)
        layout.addWidget(self.btn_sell)
        layout.addWidget(self.radio_limit)
        layout.addWidget(self.radio_market)
        layout.addWidget(self.radio_stop)
        
        grid = QGridLayout()
        grid.addWidget(self.lbl_price, 0, 0)
        grid.addWidget(self.input_price, 0, 1)
        grid.addWidget(self.lbl_qty, 1, 0)
        grid.addWidget(self.input_qty, 1, 1)
        grid.addWidget(self.lbl_stop_price, 2, 0)
        grid.addWidget(self.input_stop_price, 2, 1)
        
        layout.addLayout(grid)
        layout.addWidget(self.slider)
        layout.addWidget(self.lbl_slider_value)
        layout.addWidget(self.btn_execute_order)
        
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


    def update_input_fields_visibility(self):
        """Hide/show input fields based on order type"""
        self.input_price.setVisible(self.radio_limit.isChecked() or self.radio_stop.isChecked())
        self.lbl_price.setVisible(self.radio_limit.isChecked() or self.radio_stop.isChecked())
        self.input_stop_price.setVisible(self.radio_stop.isChecked())
        self.lbl_stop_price.setVisible(self.radio_stop.isChecked())

    def on_buy_sell_toggle(self, checked):
        """Deselect the opposite button when one of the buy/sell buttons is selected."""
        if self.sender() == self.btn_buy and checked:
            self.btn_sell.setChecked(False)
        elif self.sender() == self.btn_sell and checked:
            self.btn_buy.setChecked(False)

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
            if self.radio_futures.isChecked():
                # Place a futures order
                response = UMFutures.new_order(**order_params)
            elif self.radio_spot.isChecked():
                # Place a spot order
                response = Spot.new_order(**order_params)
            
            logging.info(response)

        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )