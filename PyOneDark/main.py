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

# Import api_key during development
from api_key import *

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.functions_main_window import *
import sys
import os
import time
import logging

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'

# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):



    def __init__(self):
        super().__init__()
        # common parameter set up
        self.ticker = "BTCUSDT"
        self.dist = "5m"
        self.login_flag = False
        self.order_flag = False
        
        self.login_key = None
        self.login_secret = None
        
        self.api_key = home_key
        self.api_secret = home_secret
        
        self.asset = None

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items
        self.login_flag = False
        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)
        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////

    # 테스트용 
    def combobox_event(self, sel_text):
        print(sel_text)
        btn = SetupMainWindow.setup_btns(self)
        # 차트 페이지 추가
        if sel_text == "BTC":
            self.ticker = "BTCUSDT"
            __chart_widget  = self.ui.load_pages.chart_v_layout.itemAt(1).widget()
            print("__chart_widget__은?", __chart_widget)
            if __chart_widget != None:
                self.ui.load_pages.chart_v_layout.removeWidget(__chart_widget)
                # 파이썬에서는 memory 누수에 대해서 크게 신경쓰지 않기로 하자
                #del __chart_widget
                __BTC_5m = BitcoinChart(self.ticker, self.dist)
                self.ui.load_pages.chart_v_layout.addWidget(__BTC_5m)
    
        if sel_text == "ETH":
            self.ticker = "ETHUSDT"
            __chart_widget  = self.ui.load_pages.chart_v_layout.itemAt(1).widget()
            if __chart_widget != None:
                self.ui.load_pages.chart_v_layout.removeWidget(__chart_widget)
                # 파이썬에서는 memory 누수에 대해서 크게 신경쓰지 않기로 하자
                #del __chart_widget
                __ETH_5m = BitcoinChart(self.ticker, self.dist)
                self.ui.load_pages.chart_v_layout.addWidget(__ETH_5m)

        if sel_text == "SOL":
            self.ticker = "SOLUSDT"
            __chart_widget  = self.ui.load_pages.chart_v_layout.itemAt(1).widget()
            if __chart_widget != None:
                self.ui.load_pages.chart_v_layout.removeWidget(__chart_widget)
                # 파이썬에서는 memory 누수에 대해서 크게 신경쓰지 않기로 하자
                #del __chart_widget
                __SOL__5m = BitcoinChart(self.ticker, self.dist)
                self.ui.load_pages.chart_v_layout.addWidget(__SOL__5m)
    
        
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)
        
        # Remove Selection If Clicked By "btn_close_left_column"
        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Get Title Bar Btn And Reset Active         
        top_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")
        top_settings.set_active(False)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////
        
        # HOME BTN
        if btn.objectName() == "btn_home":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.page_1)

        # WIDGETS BTN
        if btn.objectName() == "btn_widgets":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 2
            MainFunctions.set_page(self, self.ui.load_pages.page_2)

        # LOAD USER PAGE
        if btn.objectName() == "btn_add_user":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Load Page 3 
            MainFunctions.set_page(self, self.ui.load_pages.page_3)
        
        '''내가 추가한 Button Start from here'''
        # 차트 페이지 추가
        if btn.objectName() == "btn_chart":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())
            # Load Page 3 
            MainFunctions.set_page(self, self.ui.load_pages.page_chart)
        
        # 오더 페이지 아이콘 클릭시
        if btn.objectName() == "btn_wallet":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())
            # order_flag를 통해서 widget의 삭제 없이 문제 해결..!! (2022.11.23)
            if self.order_flag is False:
                if self.login_flag is True:
                    self.asset = MyWallet(key = self.api_key, secret = self.api_secret)
                    # add PyAsset in to page_order
                    self.ui.load_pages.page_order.layout().addWidget(self.asset)
                # 임시로 그냥 앱 추가
                self.asset = MyWallet(key = self.api_key, secret = self.api_secret)
                self.ui.load_pages.page_order.layout().addWidget(self.asset)
                self.order_flag = True
            # Load Page 3 
            MainFunctions.set_page(self, self.ui.load_pages.page_order)
            
        if btn.objectName() == "__btn_5m":
            self.dist = "5m"
            #self.ui.load_pages.chart_v_layout.__btn_5m.set_active()
            __chart_widget  = self.ui.load_pages.chart_v_layout.itemAt(1).widget()
            if __chart_widget != None:
                self.ui.load_pages.chart_v_layout.removeWidget(__chart_widget)
                # 파이썬에서는 memory 누수에 대해서 크게 신경쓰지 않기로 하자
                #del __chart_widget
                __5m = BitcoinChart(self.ticker, self.dist)
                self.ui.load_pages.chart_v_layout.addWidget(__5m)
        if btn.objectName() == "__btn_1h":
            self.dist = "1h"
            #self.ui.load_pages.chart_v_layout.__btn_1h.set_active()
            __chart_widget  = self.ui.load_pages.chart_v_layout.itemAt(1).widget()
            if __chart_widget != None:
                self.ui.load_pages.chart_v_layout.removeWidget(__chart_widget)
                # 파이썬에서는 memory 누수에 대해서 크게 신경쓰지 않기로 하자
                #del __chart_widget
                __1h = BitcoinChart(self.ticker, self.dist)
                self.ui.load_pages.chart_v_layout.addWidget(__1h)

            # 버튼이 누르면 일봉 Activate하는거 하나 필요
            # 한 dist activate되면 나머지 dist는 de-activate하는 코드 추가
            # Ticker명 Open하는 Box로 바꿀 필요 있음
            # 4h봉 / 일봉 추가 필요
            
        '''내가 추가한 Button Ends here'''

        # BOTTOM INFORMATION
        if btn.objectName() == "btn_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(btn.objectName())

                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_2,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                )

        # SETTINGS LEFT
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            # Change Left Column Menu
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self, 
                    menu = self.ui.left_column.menus.menu_1,
                    title = "Settings Left Column",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                )
        
        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////
        
        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn            
            top_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            top_settings.set_active_tab(False)            

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)
    
    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            event.accept()
    # MOVE WINDOW
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()
            
    def order_id_input_event(self):
        self.login_key = self.ui.load_pages.page_1.id_input.text()
        print(self.login_key)
    
    def order_pw_input_event(self):
        self.login_secret = self.ui.load_pages.page_1.pw_input.text()
        print(self.login_secret)
    # if order_login_btn_event is clicked, then order_id and order_pw is saved

    def order_login_btn_event(self):

        # 당신의 API Key & Secret Key 여기에 저장되었다. self.order_id, self.order_pw
        # print("self.order_id: ", self.order_id)
        # print("self.order_pw: ", self.order_pw)

        self.client = Spot(self.login_key, self.login_secret)

        # data Normal이면 login이 성공한 것임
        if self.client.account_status()['data'] == "Normal":
            self.ui.title_bar.binance_login_success()
            # clear the self.order_id and self.order_pw
            self.ui.load_pages.page_1.id_input.setText("")
            self.ui.load_pages.page_1.pw_input.setText("")
            self.login_flag = True
            
            # 로그인이 성공했으면 key를 새걸로 바꿈
            self.api_key = self.login_key
            self.api_secret = self.login_secret


# QThread 클래스
class Worker(QThread):
    price = Signal(object)
    def __init__(self, df):
        super().__init__()
        self.init_candle = df

    def run(self):
        __last_candle_opentime = self.init_candle[-1].openTime
        request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
        while True:
            new_price = request_client.get_candlestick_data(symbol='BTCUSDT', interval='5m', limit= 2)
            if __last_candle_opentime == new_price[-1].openTime:
                print("새로운 Candlestick이 없습니다.")
                __last_candle_opentime = new_price[-1].openTime
                time.sleep(3)
            else:
                print("새로운 Candlestick이 생성되었습니다.")
                self.price.emit(new_price[0])
                __last_candle_opentime = new_price[-1].openTime
                time.sleep(3)


class TimerThread(QThread):
    # 빈 시그널 만들기
    
    timeout = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout)

    def __del__(self):
        del self.timer

    def run(self):
        self.timer.start(2000)
        self.exec_()
# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////


if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    

    # 로그 메시지를 다른 로그 수집 시스템에 전송합니다.
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        level=logging.DEBUG,
                        filename="myapp.log")
    
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")
    logging.info("This is an info message.")
    logging.debug("This is a debug message.")

    # thread1 = Worker(window.init_candlesticks)
    # thread1.price.connect(window.chart.update_chart)
    # thread1.start()
    
    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec_())

    
