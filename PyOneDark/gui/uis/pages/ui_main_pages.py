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


class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(800, 600)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        
        # Page_1은 Welcome page
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.pages.addWidget(self.page_1)
        
        """
        기존 내용
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1_layout = QVBoxLayout(self.page_1)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)
        
        self.welcome_base = QFrame(self.page_1)
        self.welcome_base.setObjectName(u"welcome_base")
        self.welcome_base.setMinimumSize(QSize(300, 150))
        self.welcome_base.setMaximumSize(QSize(300, 150))
        self.welcome_base.setFrameShape(QFrame.NoFrame)
        self.welcome_base.setFrameShadow(QFrame.Raised)
        self.center_page_layout = QVBoxLayout(self.welcome_base)
        self.center_page_layout.setSpacing(10)
        self.center_page_layout.setObjectName(u"center_page_layout")
        self.center_page_layout.setContentsMargins(0, 0, 0, 0)
        self.logo = QFrame(self.welcome_base)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(300, 120))
        self.logo.setMaximumSize(QSize(300, 120))
        self.logo.setFrameShape(QFrame.NoFrame)
        self.logo.setFrameShadow(QFrame.Raised)
        self.logo_layout = QVBoxLayout(self.logo)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.center_page_layout.addWidget(self.logo)
        self.label = QLabel(self.welcome_base)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)
        self.center_page_layout.addWidget(self.label)
        self.page_1_layout.addWidget(self.welcome_base, 0, Qt.AlignHCenter)
        """

        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2_layout = QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area = QScrollArea(self.page_2)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setStyleSheet(u"background: transparent;")
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.contents = QWidget()
        self.contents.setObjectName(u"contents")
        self.contents.setGeometry(QRect(0, 0, 840, 580))
        self.contents.setStyleSheet(u"background: transparent;")
        self.verticalLayout = QVBoxLayout(self.contents)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.title_label = QLabel(self.contents)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet(u"font-size: 16pt")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.title_label)

        self.description_label = QLabel(self.contents)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.description_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.description_label)

        self.row_1_layout = QHBoxLayout()
        self.row_1_layout.setObjectName(u"row_1_layout")

        self.verticalLayout.addLayout(self.row_1_layout)

        self.row_2_layout = QHBoxLayout()
        self.row_2_layout.setObjectName(u"row_2_layout")

        self.verticalLayout.addLayout(self.row_2_layout)

        self.row_3_layout = QHBoxLayout()
        self.row_3_layout.setObjectName(u"row_3_layout")

        self.verticalLayout.addLayout(self.row_3_layout)

        self.row_4_layout = QVBoxLayout()
        self.row_4_layout.setObjectName(u"row_4_layout")

        self.verticalLayout.addLayout(self.row_4_layout)

        self.row_5_layout = QVBoxLayout()
        self.row_5_layout.setObjectName(u"row_5_layout")

        self.verticalLayout.addLayout(self.row_5_layout)

        self.scroll_area.setWidget(self.contents)

        self.page_2_layout.addWidget(self.scroll_area)

        self.pages.addWidget(self.page_2)
        
<<<<<<< HEAD

        #### Order page ####
        self.page_order = QWidget()
        self.page_order.setObjectName(u"page_order")
        self.vlayout_order= QVBoxLayout(self.page_order)
        self.vlayout_order.setObjectName(u"vlayout_order")
        
        self.pages.addWidget(self.page_order)


        #### Chart Page ####
        self.page_chart = QWidget()
        self.vlayout_chart_l1 = QVBoxLayout(self.page_chart)
        self.vlayout_chart_l1.setObjectName(u"vlayout_chart_l1")
        self.vlayout_chart_l2 = QVBoxLayout()
        self.vlayout_chart_l2.setObjectName(u"vlayout_chart_l2")
        self.hlayout_chart_l2 = QHBoxLayout()
        self.hlayout_chart_l2.setObjectName(u"hlayout_chart_l2")
        
        #self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        #self.chart_h_layout.addItem(self.horizontalSpacer)

        # layer2에 있는 hlayout을 layer2에 있는 vlayout에 추가
        self.vlayout_chart_l2.addLayout(self.hlayout_chart_l2)
        # layer2에 있는 hlayout을 layer1에 있는 vlayout에 추가
        self.vlayout_chart_l1.addLayout(self.vlayout_chart_l2)
        

        # page_order 생성 및 pages에 추가
        self.page_order = QWidget()
        self.page_order.setObjectName(u"page_order")
        self.vlayout_order = QVBoxLayout(self.page_order)
        self.vlayout_order.setObjectName(u"vlayout_order")
        self.pages.addWidget(self.page_order)

        # page_chart 생성 및 pages에 추가
        self.page_chart = QWidget()
        self.page_chart.setObjectName(u"page_chart")

        # 일단 vertical layout 생성
        self.vlayout_chart = QVBoxLayout(self.page_chart)
        self.vlayout_chart.setObjectName(u"vlayout_chart")
        
        # 하위 Layer에 vertical layout 및 horitzontal layout 생성
        self.vlayout_chart_l2 = QVBoxLayout()
        self.vlayout_chart_l2.setObjectName(u"vlayout_chart_l2")
        self.hlayout_chart_l2 = QHBoxLayout()
        self.hlayout_chart_l2.setObjectName(u"hlayout_chart_l2")

        self.chart_v_layout.addLayout(self.chart_h_layout)
        self.verticalLayout_7.addLayout(self.chart_v_layout)
>>>>>>> 5e6d830ffda79f4b0366631b6930fc8998f181b2
        self.pages.addWidget(self.page_chart)


        #### Predict page ####
        self.page_predict = QWidget()
        self.page_predict.setObjectName(u"page_predict")
        self.verticalLayout_8 = QVBoxLayout(self.page_predict)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.predict_v_layout = QVBoxLayout()
        self.predict_v_layout.setObjectName(u"predict_v_layout")
        self.predict_h_layout = QHBoxLayout()
        self.predict_h_layout.setObjectName(u"predict_h_layout")
        self.predict_v_layout.addLayout(self.predict_h_layout)
        self.verticalLayout_8.addLayout(self.predict_v_layout)
        self.pages.addWidget(self.page_predict)

        # 트레이딩 Page here
        self.page_trading = QWidget()
        self.page_trading.setObjectName(u"page_trading")
        self.trading_v_layout = QVBoxLayout(self.page_trading)
        self.trading_v_layout.setObjectName(u"trading_v_layout")
        
        self.pages.addWidget(self.page_trading)

        #이 아래에는 Qt Desginer에서 기본적으로 갖고 있던 Code
        self.main_pages_layout.addWidget(self.pages)
        self.retranslateUi(MainPages)
        self.pages.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainPages)
    
    # setupUi
    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        # self.label.setText(QCoreApplication.translate("MainPages", u"Welcome To PyOneDark GUI", None))
        self.title_label.setText(QCoreApplication.translate("MainPages", u"Custom Widgets Page", None))
        self.description_label.setText(QCoreApplication.translate("MainPages", u"Here will be all the custom widgets, they will be added over time on this page.\n"
"I will try to always record a new tutorial when adding a new Widget and updating the project on Patreon before launching on GitHub and GitHub after the public release.", None))
        #self.empty_page_label.setText(QCoreApplication.translate("MainPages", u"Empty Page", None))
    # retranslateUi