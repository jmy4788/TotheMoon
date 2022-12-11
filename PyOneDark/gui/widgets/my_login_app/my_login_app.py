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
# my common style을 import 하는 행
from gui.themes.my_style import style



# Login App 자체를 QWidget으로 보고 해당 Login App의 Class를 만들어야 함
# 예를 들어, page_1의 객체 주소를 전달받았다고 했을 때, 해당 객체 주소에 LoginApp을 마지막에 추가해야 함

# PY PUSH BUTTON
# ///////////////////////////////////////////////////////////////
class LoginApp(QWidget):
    def __init__(self, target):
        super().__init__()
        self.display(target)

    def display(self, target):
        # style sheet 예시
        # self.setStyleSheet(u"font-size: 13pt;font-family: SF Pro Regular, malgun gothic, serif")
        # import thems
        self = target
        themes = Themes()
        self.themes = themes.items

        # 기본 layout 설정
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setObjectName(u"login_layout")

        # setContentsMargins order left top right bottom
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Center the layout
        self.layout.setAlignment(Qt.AlignCenter)

        # add layout2 QHBoxlayout
        self.layout2 = QHBoxLayout()
        self.layout2.setSpacing(0)
        self.layout2.setObjectName(u"login_layout2")
        self.layout2.setContentsMargins(0, 0, 0, 0)

        # add "Ubpit" button to self.layout2
        self.upbit_button = QPushButton(self)
        self.upbit_button.setObjectName(u"upbit_button")
        self.upbit_button.setText("Upbit")
        self.upbit_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.upbit_button.setStyleSheet(style.format(
            _radius=8,
            _color='#FFFFFF', 
            _bg_color='#093687',
            _bg_color_hover=self.themes["app_color"]['dark_three'],
            _bg_color_pressed=self.themes["app_color"]['dark_four'],
        ))
        self.layout2.addWidget(self.upbit_button)
        
        # add "Binance" button to self.layout2
        self.binance_button = QPushButton(self)
        self.binance_button.setObjectName(u"binance_button")
        self.binance_button.setText("Binance")
        self.binance_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.binance_button.setStyleSheet(style.format(
            _color='#000000',
            _radius=8,
            _bg_color='#FCD535',
            _bg_color_hover=self.themes["app_color"]['dark_three'],
            _bg_color_pressed='#FBC740'
        ))
        self.layout2.addWidget(self.binance_button)
        self.layout.addLayout(self.layout2)


        # id_input to self.layout
        self.id_input = PyLineEdit(
            text = "",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"])
        font = QFont()
        font.setFamily(u"SF Pro Regular")
        font.setPointSize(11)
        self.id_input.setFont(font)
        self.id_input.setObjectName(u"id_input")
        self.id_input.setPlaceholderText("ID를 입력하세요.")
        
    

        self.layout.addWidget(self.id_input)
        # set id_input size policy
        self.id_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.id_input.setMinimumHeight(40)
        self.id_input.setMaximumHeight(40)
        self.id_input.setMinimumWidth(400)
        self.id_input.setMaximumWidth(400)
        self.id_input.setEchoMode(QLineEdit.Password)

        # pw_input to self.layout
        self.pw_input = PyLineEdit(
            text = "",
            radius = 8,
            border_size = 2,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["white"],
            bg_color = self.themes["app_color"]["dark_one"],
            bg_color_active = self.themes["app_color"]["dark_three"],
            context_color = self.themes["app_color"]["context_color"])
        self.pw_input.setObjectName(u"pw_input")
        self.pw_input.setPlaceholderText("PW를 입력하세요.")
        self.layout.addWidget(self.pw_input)
        # set pw_input size policy
        self.pw_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pw_input.setMinimumHeight(40)
        self.pw_input.setMaximumHeight(40)
        self.pw_input.setMinimumWidth(400)
        self.pw_input.setMaximumWidth(400)
        self.pw_input.setEchoMode(QLineEdit.Password)

        # set font SF Pro Regular
        font = QFont()
        font.setFamily(u"SF Pro Regular")
        # make font bold
        font.setBold(True)
        font.setPointSize(11)
        self.pw_input.setFont(font)

        # login button to self.layout
        self.login_btn = PyPushButton(
            text = "Login",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        # set button size to 600
        self.login_btn.setMinimumHeight(50)
        self.login_btn.setMaximumHeight(50)
        self.login_btn.setMinimumWidth(400)
        self.login_btn.setMaximumWidth(400)

        self.login_btn.setObjectName(u"login_btn")
        font = QFont()
        font.setFamily(u"SF Pro")
        font.setPointSize(11)
        self.login_btn.setFont(font)

        self.layout.addWidget(self.login_btn)
        self.setLayout(self.layout)