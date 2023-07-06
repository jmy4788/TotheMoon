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


class MyWallet(QWidget):
    # MyWallet get the param client
    # ///////////////////////////////////////////////////////////////
    def __init__(self, key=None, secret=None, parent=None):
        # super(PyAsset, self).__init__(parent)는 super().__init__(parent)와 같음 Python 2,3 버젼차이
        super(MyWallet, self).__init__(parent)
        self.key = key
        self.secret = secret
        
        self.spot_client = Spot(key=self.key, secret=self.secret)
        self.future_client = UMFutures(key=self.key, secret=self.secret)
        
        # Hiding value 선언
        self.staking_is_hiding =  None
        self.spot_is_hiding = None
        self.futures_is_hiding = None

    # ----------My Wallet Layout 셋팅----------------
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # add strech는 위와 아래의 빈 공간의 비율을 의미함
        self.layout.addStretch(1)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
    # ----------Spot 버튼 / 위젯 추가----------------
        self.add_spot_btn()
        self.spot = Spot_widget(self.spot_client)
        self.layout.addWidget(self.spot)
    # ----------Staking 버튼 / 위젯 추가----------------
        self.add_staking_btn()
        self.staking = Staking_widget(self.spot_client)
        self.layout.addWidget(self.staking)
    # ----------Futures 버튼 / 위젯 추가----------------
        self.add_futures_btn()
        self.futures = Futures_widget(self.future_client)
        self.layout.addWidget(self.futures)

    # ----------Staking 펼치기 / 숨기기 기능----------------
    def add_staking_btn(self):
        self.staking_folding_btn = QPushButton()        
        self.staking_folding_btn.setStyleSheet(my_style.PushBtn)
        # set the style for button
        self.staking_folding_btn.setText('Staking ▲')
        self.staking_folding_btn.clicked.connect(self.staking_folding_func)
        self.layout.addWidget(self.staking_folding_btn)

    def staking_folding_func(self):
        if self.staking_is_hiding is True:
            self.staking_folding_btn.setText('Staking ▲')
            self.staking.show()
            self.staking_is_hiding = False
        else:
            self.staking.hide()
            self.staking_folding_btn.setText('Staking ▶')
            self.staking_is_hiding = True
    # ----------Spot 펼치기 / 숨기기 기능----------------
    def add_spot_btn(self):
        self.spot_folding_btn = QPushButton()
        self.spot_folding_btn.setStyleSheet(my_style.PushBtn)
        self.spot_folding_btn.setText('SPOT ▲')
        self.spot_folding_btn.clicked.connect(self.spot_folding_func)
        self.layout.addWidget(self.spot_folding_btn)

    def spot_folding_func(self):
        if self.spot_is_hiding is True:
            self.spot_folding_btn.setText('Spot ▲')
            self.spot.show()
            self.spot_is_hiding = False
        else:
            self.spot.hide()
            self.spot_folding_btn.setText('Spot ▶')
            self.spot_is_hiding = True
    # ----------Futures 펼치기 / 숨기기 기능----------------
    def add_futures_btn(self):
        self.futures_folding_btn = QPushButton()
        self.futures_folding_btn.setStyleSheet(my_style.PushBtn)
        self.futures_folding_btn.setText('Futures ▲')
        self.futures_folding_btn.clicked.connect(self.futures_folding_func)
        self.layout.addWidget(self.futures_folding_btn)

    def futures_folding_func(self):
        if self.futures_is_hiding is True:
            self.futures_folding_btn.setText('Futures ▲')
            self.futures.show()
            self.futures_is_hiding = False
        else:
            self.futures.hide()
            self.futures_folding_btn.setText('Futures ▶')
            self.futures_is_hiding = True
    # USD Valuation 하는 Static method
    @staticmethod
    def get_usd_valuation(client, symbol, amount):
        if symbol == 'BTC' or symbol == 'SOL' or symbol == 'ETH' or symbol == 'ICP':
            market_price = client.ticker_price(symbol + 'USDT')['price']
            usd_valuation = float(market_price) * float(amount)
            usd_valuation = "{:.2f}".format(usd_valuation)
            return usd_valuation
        else:
            usd_valuation = '0'
            """
            market_price = client.ticker_price(symbol + 'BTC')['price']
            btc_valuation = float(market_price) * float(amount)
            btc_valuation = "{:.8f}".format(btc_valuation)
            btc_valuation = float(btc_valuation)
            usd_valuation = client.ticker_price('BTCUSDT')['price']
            usd_valuation = float(usd_valuation) * btc_valuation
            usd_valuation = "{:.2f}".format(usd_valuation)
            """
            return usd_valuation

class Spot_widget(QWidget):
    def __init__(self, client, parent=None):
        # super(PyAsset, self).__init__(parent)는 super().__init__(parent)와 같음 Python 2,3 버젼차이
        super(Spot_widget, self).__init__(parent)
        self.client = client
        self.user_asset = self.client.user_asset()
        
        #layout 추가
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.headline()
        self.initial_table()
        
        # QTimer를 이용해 10초마다 데이터 업데이트
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(10000)
        
    # ----------Header 라인 작성----------------
    def headline(self):
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(0)        
        # tags안에 있는 내용들을 모두 label로 추가시키고 labe_st를 적용 했음
        tags = ['Asset', 'free', 'locked', 'withdrawing', 'ipoable', 'btcValuation', 'USDValuation']
        for tag in tags:
            label = QLabel(tag)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(my_style.QLabel_title)
            self.header_layout.addWidget(label)
        # Add the QHboxLayout to the QVboxLayout
        self.layout.addLayout(self.header_layout)
    
    def initial_table(self):
        usd_sum = 0
        free_sum = 0
        locked_sum = 0
        withdrawing_sum = 0
        ipoable_sum = 0
        btcValuation_sum = 0

        for asset in self.user_asset:
            # Set the asset name
            asset_name = asset['asset']
            # Set the asset value
            asset_value = asset['free']
            # Set the asset locked
            asset_locked = asset['locked']
            # Set the asset withdrawing
            asset_withdrawing = asset['withdrawing']
            # Set the asset ipoable
            asset_ipoable = asset['ipoable']
            # Set the asset btcValuation
            asset_btcValuation = asset['btcValuation']
            # Set the asset usdValuation
            asset_usdValuation = MyWallet.get_usd_valuation(self.client, asset_name, asset_value)
            
            # calculate the sum
            free_sum += float(asset_value)
            locked_sum += float(asset_locked)
            withdrawing_sum += float(asset_withdrawing)
            ipoable_sum += float(asset_ipoable)
            btcValuation_sum += float(asset_btcValuation)
            usd_sum += float(asset_usdValuation)
            
            # Set the asset name
            asset_name_widget = QLabel(asset_name, parent=self)
            asset_name_widget.setAlignment(Qt.AlignCenter)
            asset_name_widget.setObjectName('asset_name_widget')
            asset_name_widget.setStyleSheet(my_style.QLabel_body)
            
            # Set the asset value
            asset_value_widget = QLabel(asset_value, parent=self)
            asset_value_widget.setAlignment(Qt.AlignCenter)
            asset_value_widget.setObjectName('asset_value_widget')
            asset_value_widget.setStyleSheet(my_style.QLabel_body)

            # Set the asset locked
            asset_locked_widget = QLabel(asset_locked, parent=self)
            asset_locked_widget.setAlignment(Qt.AlignCenter)
            asset_locked_widget.setObjectName('asset_locked_widget')
            asset_locked_widget.setStyleSheet(my_style.QLabel_body)

            # Set the asset withdrawing
            asset_withdrawing_widget = QLabel(asset_withdrawing, parent=self)
            asset_withdrawing_widget.setAlignment(Qt.AlignCenter)
            asset_withdrawing_widget.setObjectName('asset_withdrawing_widget')
            asset_withdrawing_widget.setStyleSheet(my_style.QLabel_body)


            # Set the asset ipoable
            asset_ipoable_widget = QLabel(asset_ipoable, parent=self)
            asset_ipoable_widget.setAlignment(Qt.AlignCenter)
            asset_ipoable_widget.setObjectName('asset_ipoable_widget')
            asset_ipoable_widget.setStyleSheet(my_style.QLabel_body)

            # Set the asset btcValuation
            asset_btcValuation_widget = QLabel(asset_btcValuation, parent=self)
            asset_btcValuation_widget.setAlignment(Qt.AlignCenter)
            asset_btcValuation_widget.setObjectName('asset_btcValuation_widget')
            asset_btcValuation_widget.setStyleSheet(my_style.QLabel_body)
            
            # Set the asset usdValuation
            asset_usdValuation_widget = QLabel(asset_usdValuation, parent=self)
            asset_usdValuation_widget.setAlignment(Qt.AlignCenter)
            asset_usdValuation_widget.setObjectName('asset_usdValuation_widget')
            asset_usdValuation_widget.setStyleSheet(my_style.QLabel_body)

            # QLabel adding to layout
            asset_layout = QHBoxLayout()
            asset_layout.setContentsMargins(0, 0, 0, 0)
            asset_layout.setSpacing(0)
            asset_layout.addWidget(asset_name_widget)
            asset_layout.addWidget(asset_value_widget)
            asset_layout.addWidget(asset_locked_widget)
            asset_layout.addWidget(asset_withdrawing_widget)
            asset_layout.addWidget(asset_ipoable_widget)
            asset_layout.addWidget(asset_btcValuation_widget)
            asset_layout.addWidget(asset_usdValuation_widget)
            self.layout.addLayout(asset_layout)

        asset_name = QLabel('Total')
        asset_name.setAlignment(Qt.AlignCenter)
        asset_name.setStyleSheet(my_style.QLabel_body)
        asset_value = QLabel("{:.2f}".format(free_sum))
        asset_value.setAlignment(Qt.AlignCenter)
        asset_value.setStyleSheet(my_style.QLabel_body)
        asset_locked = QLabel("{:.2f}".format(locked_sum))
        asset_locked.setAlignment(Qt.AlignCenter)
        asset_locked.setStyleSheet(my_style.QLabel_body)
        asset_withdrawing = QLabel("{:.2f}".format(withdrawing_sum))
        asset_withdrawing.setAlignment(Qt.AlignCenter)
        asset_withdrawing.setStyleSheet(my_style.QLabel_body)
        asset_ipoable = QLabel("{:.2f}".format(ipoable_sum))
        asset_ipoable.setAlignment(Qt.AlignCenter)
        asset_ipoable.setStyleSheet(my_style.QLabel_body)
        asset_btcValuation = QLabel("{:.6f}".format(btcValuation_sum))
        asset_btcValuation.setAlignment(Qt.AlignCenter)
        asset_btcValuation.setStyleSheet(my_style.QLabel_body)
        asset_usdValuation = QLabel("{:.2f}".format(usd_sum))
        asset_usdValuation.setAlignment(Qt.AlignCenter)
        asset_usdValuation.setStyleSheet(my_style.QLabel_body)
        asset_layout = QHBoxLayout()
        asset_layout.setContentsMargins(0, 0, 0, 0)
        asset_layout.setSpacing(0)
        asset_layout.addWidget(asset_name)
        asset_layout.addWidget(asset_value)
        asset_layout.addWidget(asset_locked)
        asset_layout.addWidget(asset_withdrawing)   
        asset_layout.addWidget(asset_ipoable)
        asset_layout.addWidget(asset_btcValuation)
        asset_layout.addWidget(asset_usdValuation)
        self.layout.addLayout(asset_layout)


    def update_table(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                # item is a layout
                while item.count():
                    item.takeAt(0).widget().setParent(None)
        self.headline()
        self.initial_table()


class Staking_widget(QWidget):
    def __init__(self, client, parent=None):
        # super(PyAsset, self).__init__(parent)는 super().__init__(parent)와 같음 Python 2,3 버젼차이
        super(Staking_widget, self).__init__(parent)
        self.client = client
        self.user_staking = self.client.staking_product_position("STAKING")

        #layout 추가
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.headline()
        self.initial_table()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(10000)
        

    def headline(self):
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(0)        
        # tags안에 있는 내용들을 모두 label로 추가시키고 labe_st를 적용 했음
        tags = ['asset(period)', 'Amount', 'APY(%)', 'PurchaseTime', 'DeliverDate', 'USD Conversion']
        for tag in tags:
            label = QLabel(tag)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(my_style.QLabel_title)
            self.header_layout.addWidget(label)
        # Add the QHboxLayout to the QVboxLayout
        self.layout.addLayout(self.header_layout)
    
    def initial_table(self):
        amount_sum = 0
        usd_sum = 0
        
        for staking in self.user_staking:
            # Unpack the data
            asset_name = staking['asset']
            amount = staking['amount']
            apy = str(float(staking['apy']) * 100)
            purchaseTime = staking['purchaseTime']
            deliverDate = staking['deliverDate']
            

            # Convert the time format
            purchasTime = datetime.datetime.fromtimestamp(purchaseTime/1000)
            deliverDate = datetime.datetime.fromtimestamp(deliverDate/1000)
            # Covnert time format to str type
            purchaseTime = purchasTime.strftime('%y-%m-%d %H:%M')
            deliverDate = deliverDate.strftime('%y-%m-%d %H:%M')
            # 만약 asset_name이 BTC 또는 SOL 또는 ETH라면
            staking_pos_usdValuation = MyWallet.get_usd_valuation(self.client, asset_name, amount)

            # Calculate the total amount and usd value
            amount_sum += float(amount)
            usd_sum += float(staking_pos_usdValuation)

            staking_pos_asset = QLabel(asset_name)
            staking_pos_asset.setAlignment(Qt.AlignCenter)
            staking_pos_asset.setObjectName('asset')
            staking_pos_asset.setStyleSheet(my_style.QLabel_body)

            staking_pos_amount = QLabel("{:.4f}".format(float(amount)))
            staking_pos_amount.setAlignment(Qt.AlignCenter)
            staking_pos_amount.setObjectName('amount')
            staking_pos_amount.setStyleSheet(my_style.QLabel_body)

            staking_pos_apy = QLabel("{:.2f}".format(float(apy)))
            staking_pos_apy.setAlignment(Qt.AlignCenter)
            staking_pos_apy.setObjectName('apy')
            staking_pos_apy.setStyleSheet(my_style.QLabel_body)

            staking_pos_purchaseTime = QLabel(purchaseTime)
            staking_pos_purchaseTime.setAlignment(Qt.AlignCenter)
            staking_pos_purchaseTime.setObjectName('purchaseTime')
            staking_pos_purchaseTime.setStyleSheet(my_style.QLabel_body)

            staking_pos_deliverDate = QLabel(deliverDate)
            staking_pos_deliverDate.setAlignment(Qt.AlignCenter)
            staking_pos_deliverDate.setObjectName('deliverDate')
            staking_pos_deliverDate.setStyleSheet(my_style.QLabel_body)

            staking_pos_usd_valuation_widget = QLabel(staking_pos_usdValuation)
            staking_pos_usd_valuation_widget.setAlignment(Qt.AlignCenter)
            staking_pos_usd_valuation_widget.setObjectName('usd_valuation')
            staking_pos_usd_valuation_widget.setStyleSheet(my_style.QLabel_body)

            staking_pos_layout = QHBoxLayout()
            staking_pos_layout.setContentsMargins(0, 0, 0, 0)
            staking_pos_layout.setSpacing(0)
            staking_pos_layout.addWidget(staking_pos_asset)
            staking_pos_layout.addWidget(staking_pos_amount)
            staking_pos_layout.addWidget(staking_pos_apy)
            staking_pos_layout.addWidget(staking_pos_purchaseTime)
            staking_pos_layout.addWidget(staking_pos_deliverDate)
            staking_pos_layout.addWidget(staking_pos_usd_valuation_widget)
            self.layout.addLayout(staking_pos_layout)
        # Total 표현
        staking_pos_name = QLabel('Total')
        staking_pos_name.setAlignment(Qt.AlignCenter)
        staking_pos_name.setStyleSheet(my_style.QLabel_body)
        staking_pos_name.setObjectName('asset')
        staking_pos_amount = QLabel("{:.4f}".format(amount_sum))
        staking_pos_amount.setAlignment(Qt.AlignCenter)
        staking_pos_amount.setObjectName('amount')
        staking_pos_amount.setStyleSheet(my_style.QLabel_body)
        staking_pos_usd_valuation_widget = QLabel("{:.4f}".format(usd_sum))
        staking_pos_usd_valuation_widget.setAlignment(Qt.AlignCenter)
        staking_pos_usd_valuation_widget.setObjectName('usd_valuation')
        staking_pos_usd_valuation_widget.setStyleSheet(my_style.QLabel_body)
        staking_pos_layout = QHBoxLayout()
        staking_pos_layout.setContentsMargins(0, 0, 0, 0)
        staking_pos_layout.setSpacing(0)
        staking_pos_layout.addWidget(staking_pos_name)
        staking_pos_layout.addWidget(staking_pos_amount)
        staking_pos_layout.addWidget(QLabel(''))
        staking_pos_layout.addWidget(QLabel(''))
        staking_pos_layout.addWidget(QLabel(''))
        staking_pos_layout.addWidget(staking_pos_usd_valuation_widget)
        self.layout.addLayout(staking_pos_layout)


    def update_table(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                # item is a layout
                while item.count():
                    item.takeAt(0).widget().setParent(None)
        self.headline()
        self.initial_table()

class Futures_widget(QWidget):
    def __init__(self, client, parent=None): 
        # super(PyAsset, self).__init__(parent)는 super().__init__(parent)와 같음 Python 2,3 버젼차이
        super(Futures_widget, self).__init__(parent)
        self.client = client

        #layout 추가
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.headline()
        self.initial_table()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(5000)
        

    def headline(self):
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(0)        
        # tags안에 있는 내용들을 모두 label로 추가시키고 labe_st를 적용 했음
        tags = ['티커', '지갑잔고(A)', '미실현손익(B)', '마진잔고(A+B)', '유지증거금', '초기증거금', 
        '포지션개설증거금', '주문개설증거금', '사용가능', '출금가능']
        for tag in tags:
            label = QLabel(tag)
            # QLabel 가운데 정렬
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(my_style.QLabel_title_kr)
            self.header_layout.addWidget(label)
        # Add the QHboxLayout to the QVboxLayout
        self.layout.addLayout(self.header_layout)
    
    def initial_table(self):
        wallet_balance_sum = 0
        unrealized_profit_sum = 0
        margin_balance_sum = 0
        maint_margin_sum = 0
        initial_margin_sum = 0
        position_initial_margin_sum = 0
        open_order_initial_margin_sum = 0
        available_balance_sum = 0
        max_withdraw_amount_sum = 0

        account = self.client.account()
        assets = account['assets']
        positions = account['positions']
        
        for asset in assets:
            if asset['asset'] in ['BTC', 'USDT', 'SOL', 'ETH', 'ICP']:
                # Unpack the data
                asset_name = asset['asset']
                wallet_balance = asset['walletBalance']
                unrealized_profit = asset['unrealizedProfit']
                margin_balance = asset['marginBalance']
                maint_margin = asset['maintMargin']
                initial_margin = asset['initialMargin']
                position_initial_margin = asset['positionInitialMargin']
                open_order_initial_margin = asset['openOrderInitialMargin']
                available_balance = asset['availableBalance']
                max_withdraw_amount = asset['maxWithdrawAmount']

                # Add the data to the table
                self.table_layout = QHBoxLayout()
                self.table_layout.setContentsMargins(0, 0, 0, 0)
                self.table_layout.setSpacing(0)
                # tags안에 있는 내용들을 모두 label로 추가시키고 labe_st를 적용 했음
                tags = [asset_name, wallet_balance, unrealized_profit, margin_balance, maint_margin, initial_margin,
                position_initial_margin, open_order_initial_margin, available_balance, max_withdraw_amount]
                for tag in tags:
                    if tag is asset_name:
                        label = QLabel(tag)
                        label.setAlignment(Qt.AlignCenter)
                        label.setStyleSheet(my_style.QLabel_body)
                        self.table_layout.addWidget(label)
                    else:
                        tag = float(tag)
                        label = QLabel("{:.4f}".format(tag))
                        label.setAlignment(Qt.AlignCenter)
                        label.setStyleSheet(my_style.QLabel_body)
                        self.table_layout.addWidget(label)
                # Add the QHboxLayout to the QVboxLayout
                self.layout.addLayout(self.table_layout)

                wallet_balance_sum += float(wallet_balance)
                unrealized_profit_sum += float(unrealized_profit)
                margin_balance_sum += float(margin_balance)
                maint_margin_sum += float(maint_margin)
                initial_margin_sum += float(initial_margin)
                position_initial_margin_sum += float(position_initial_margin)
                open_order_initial_margin_sum += float(open_order_initial_margin)
                available_balance_sum += float(available_balance)
                max_withdraw_amount_sum += float(max_withdraw_amount)
            else:
                continue
        # Add the data to the table
        self.table_layout = QHBoxLayout()
        self.table_layout.setContentsMargins(0, 0, 0, 0)
        self.table_layout.setSpacing(0)
        # tags안에 있는 내용들을 모두 label로 추가시키고 labe_st를 적용 했음
        tags = ['TOTAL', wallet_balance_sum, unrealized_profit_sum, margin_balance_sum, maint_margin_sum, initial_margin_sum,
        position_initial_margin_sum, open_order_initial_margin_sum, available_balance_sum, max_withdraw_amount_sum]
        for tag in tags:
            if tag == 'TOTAL':
                label = QLabel(tag)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(my_style.QLabel_body)
                self.table_layout.addWidget(label)
            else:
                label = QLabel("{:.4f}".format(tag))
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(my_style.QLabel_body)
                self.table_layout.addWidget(label)
        # Add the QHboxLayout to the QVboxLayout
        self.layout.addLayout(self.table_layout)
        # add QPush button as the spacer
        self.spacer = QPushButton("Position")
        self.spacer.setStyleSheet(my_style.PushBtn)
        self.layout.addWidget(self.spacer)

        # 중간 Head line 추가
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(0)
        # tags안에 있는 내용들을 모두 label로 추가시키고 labe_st를 적용 했음
        tags = ['티커', '포지션크기', '진입가', '미실현손익', '포지션개설증거금',
                '주문개설증거금', '유지증거금', '초기마진', '레버리지', '격리', 'Long/Short']
        for tag in tags:
            label = QLabel(tag)
            # QLabel 가운데 정렬
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(my_style.QLabel_title_kr)
            self.header_layout.addWidget(label)
        self.layout.addLayout(self.header_layout)
        # Add the QHboxLayout to the QVboxLayout

        for position in positions:
            if position['symbol'] in ['BTCUSDT', 'SOLUSDT', 'ETHUSDT', 'ICPUSDT']:
            # Unpack the data
                symbol = position['symbol']
                position_amount = position['positionAmt']
                entry_price = position['entryPrice']
                unrealized_pnl = position['unrealizedProfit']
                position_initial_margin = position['positionInitialMargin']
                open_order_initial_margin = position['openOrderInitialMargin']
                maint_margin = position['maintMargin']
                initial_margin = position['initialMargin']
                leverage = position['leverage']
                isolated = position['isolated']
                position_side = position['positionSide']
                # Add the data to the table
                self.table_layout = QHBoxLayout()
                self.table_layout.setContentsMargins(0, 0, 0, 0)
                self.table_layout.setSpacing(0)
                # tags안에 있는 내용들을 모두 label로 추가시키고 labe_st를 적용 했음
                tags = [symbol, position_amount, entry_price, unrealized_pnl, position_initial_margin,
                open_order_initial_margin, maint_margin, initial_margin, leverage, isolated, position_side]
                for tag in tags:
                    if tag is symbol or tag is position_side:
                        label = QLabel(tag)
                        label.setAlignment(Qt.AlignCenter)
                        label.setStyleSheet(my_style.QLabel_body)
                        self.table_layout.addWidget(label)
                    else:
                        tag = float(tag)
                        label = QLabel("{:.4f}".format(tag))
                        label.setAlignment(Qt.AlignCenter)
                        label.setStyleSheet(my_style.QLabel_body)
                        self.table_layout.addWidget(label)
        # Add the QHboxLayout to the QVboxLayout
                self.layout.addLayout(self.table_layout)
    def update_table(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                # item is a layout
                while item.count():
                    item.takeAt(0).widget().setParent(None)
        self.headline()
        self.initial_table()