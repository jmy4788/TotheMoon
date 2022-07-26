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

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.functions_main_window import *
import sys
import os
import time

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

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

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
        self.ticker = "BTCUSDT"
        self.dist = "5m"
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
        #기본 ticker / dist 셋팅
        self.ticker = "BTCUSDT"
        self.dist = "5m"
        # 차트 페이지 추가
        if btn.objectName() == "btn_chart":
            # Select Menu
            self.ui.left_menu.select_only_one(btn.objectName())
            # Load Page 3 
            MainFunctions.set_page(self, self.ui.load_pages.page_chart)
        
        if btn.objectName() == "BTC":
            self.ticker = "BTCUSDT"
            __chart_widget  = self.ui.load_pages.chart_v_layout.itemAt(1).widget()
            print("__chart_widget__은?", __chart_widget)
            if __chart_widget != None:
                self.ui.load_pages.chart_v_layout.removeWidget(__chart_widget)
                # 파이썬에서는 memory 누수에 대해서 크게 신경쓰지 않기로 하자
                #del __chart_widget
                __BTC_5m = BitcoinChart(self.ticker, self.dist)
                self.ui.load_pages.chart_v_layout.addWidget(__BTC_5m)
    
        if btn.objectName() == "ETH":
            self.ticker = "ETHUSDT"
            __chart_widget  = self.ui.load_pages.chart_v_layout.itemAt(1).widget()
            if __chart_widget != None:
                self.ui.load_pages.chart_v_layout.removeWidget(__chart_widget)
                # 파이썬에서는 memory 누수에 대해서 크게 신경쓰지 않기로 하자
                #del __chart_widget
                __ETH_5m = BitcoinChart(self.ticker, self.dist)
                self.ui.load_pages.chart_v_layout.addWidget(__ETH_5m)

        if btn.objectName() == "SOL":
            self.ticker = "SOLUSDT"
            __chart_widget  = self.ui.load_pages.chart_v_layout.itemAt(1).widget()
            if __chart_widget != None:
                self.ui.load_pages.chart_v_layout.removeWidget(__chart_widget)
                # 파이썬에서는 memory 누수에 대해서 크게 신경쓰지 않기로 하자
                #del __chart_widget
                __SOL__5m = BitcoinChart(self.ticker, self.dist)
                self.ui.load_pages.chart_v_layout.addWidget(__SOL__5m)
    
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
                print("여기 진입 하나?")
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
        self.dragPos = event.globalPos()

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

# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////


if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    #thread1 = Worker(window.init_candlesticks)
    #thread1.price.connect(window.chart.update_chart)
    #thread1.start()

    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec_())