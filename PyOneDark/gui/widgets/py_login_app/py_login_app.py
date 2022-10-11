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
# STYLE
# ///////////////////////////////////////////////////////////////
style = '''
QPushButton {{
	border: none;
    padding-left: 10px;
    padding-right: 5px;
    color: {_color};
	border-radius: {_radius};	
	background-color: {_bg_color};
}}
QPushButton:hover {{
	background-color: {_bg_color_hover};
}}
QPushButton:pressed {{	
	background-color: {_bg_color_pressed};
}}
'''


"""
일단 Login 하려면
LoginApp의 목적
self.ui.loadpage.page1에 LoginApp을 띄워야 함
page1이 QWidget이기 때문에, QWidget에 추가하는 Function이 있으면 됨

"""

# PY PUSH BUTTON
# ///////////////////////////////////////////////////////////////
class LoginApp(QWidget):
    def __init__(self):
        super().__init__()

    def display(self):
        # import thems
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
        self.pw_input.setPlaceholderText("PW")
        self.layout.addWidget(self.pw_input)
        # set pw_input size policy
        self.pw_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pw_input.setMinimumHeight(40)
        self.pw_input.setMaximumHeight(40)
        self.pw_input.setMinimumWidth(400)
        self.pw_input.setMaximumWidth(400)
        # set font SF Pro Regular
        font = QFont()
        font.setFamily(u"SF Pro Regular")
        # make font bold
        font.setBold(True)
        font.setPointSize(11)
        self.pw_input.setFont(font)

        # login button to self.layout
        self.login_button = PyPushButton(
            text = "Login",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        # set button size to 600
        self.login_button.setMinimumHeight(50)
        self.login_button.setMaximumHeight(50)
        self.login_button.setMinimumWidth(400)
        self.login_button.setMaximumWidth(400)

        self.login_button.setObjectName(u"login_button")
        font = QFont()
        font.setFamily(u"SF Pro")
        font.setPointSize(11)
        self.login_button.setFont(font)

        self.layout.addWidget(self.login_button)
        # set layout
        self.setLayout(self.layout)