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
from gui.themes.my_style import *

# QLabel style
theme = Themes().items
label_st = '''
QLabel {
    color: #FFFFFF;
    background-color: #2c313c;
    font-size: 15pt;
    font-family: SF Pro Heavy, malgun gothic, serif;
}
'''

class MyAsset(QWidget):
    # PyAsset get the param client
    # ///////////////////////////////////////////////////////////////
    def __init__(self, client, parent=None):
        # super(PyAsset, self).__init__(parent)는 super().__init__(parent)와 같음 Python 2,3 버젼차이
        super(MyAsset, self).__init__(parent)
        self.client = client

        # set TOP QVBoxlayout
        self.top_layout = QVBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(0)
        self.setLayout(self.top_layout)
        print('self.layout은?', self.layout())
        self.set_asset_title()
        self.dp_user_asset(self.get_user_asset())


        
    # API 파트
    # Get user asset data from server
    def get_user_asset(self):
        # Get the user asset
        user_asset = self.client.user_asset()
        # Return the user asset
        return user_asset
    
    # dp_user_asset에 있는 내용을 모두 label로 추가시키고 labe_st를 적용 했음
    def dp_user_asset(self, user_asset):
        header = ['asset', 'free', 'locked', 'withdrawing', 'ipoable', 'btcValuation']
        for asset in user_asset:
            # Set the asset name
            asset_name = asset[header[0]]
            # Set the asset value
            asset_value = asset[header[1]]
            # Set the asset locked
            asset_locked = asset[header[2]]
            # Set the asset withdrawing
            asset_withdrawing = asset[header[3]]
            # Set the asset ipoable
            asset_ipoable = asset[header[4]]
            # Set the asset btcValuation
            asset_btcValuation = asset[header[5]]    
            # Set the asset name
            asset_name_widget = QLabel(asset_name)
            asset_name_widget.setObjectName('asset_name_widget')
            asset_name_widget.setStyleSheet(label_st)
            
            # Set the asset value
            asset_value_widget = QLabel(asset_value)
            asset_value_widget.setObjectName('asset_value_widget')
            asset_value_widget.setStyleSheet(label_st)

            # Set the asset locked
            asset_locked_widget = QLabel(asset_locked)
            asset_locked_widget.setObjectName('asset_locked_widget')
            asset_locked_widget.setStyleSheet(label_st)

            # Set the asset withdrawing
            asset_withdrawing_widget = QLabel(asset_withdrawing)
            asset_withdrawing_widget.setObjectName('asset_withdrawing_widget')
            asset_withdrawing_widget.setStyleSheet(label_st)

            # Set the asset ipoable
            asset_ipoable_widget = QLabel(asset_ipoable)
            asset_ipoable_widget.setObjectName('asset_ipoable_widget')
            asset_ipoable_widget.setStyleSheet(label_st)

            # Set the asset btcValuation
            asset_btcValuation_widget = QLabel(asset_btcValuation)
            asset_btcValuation_widget.setObjectName('asset_btcValuation_widget')
            asset_btcValuation_widget.setStyleSheet(label_st)

            #QHboxLayout
            asset_layout = QHBoxLayout()
            asset_layout.setContentsMargins(0, 0, 0, 0)
            asset_layout.setSpacing(0)
            asset_layout.addWidget(asset_name_widget)
            asset_layout.addWidget(asset_value_widget)
            asset_layout.addWidget(asset_locked_widget)
            asset_layout.addWidget(asset_withdrawing_widget)
            asset_layout.addWidget(asset_ipoable_widget)
            asset_layout.addWidget(asset_btcValuation_widget)
            self.layout().addLayout(asset_layout)


    def set_asset_title(self):
        # add 5 Qlabel to the QHboxLayout
        self.asset_title = QHBoxLayout()
        self.asset_title.setContentsMargins(0, 0, 0, 0)
        self.asset_title.setSpacing(0)        
        # tags안에 있는 내용들을 모두 label로 추가시키고 labe_st를 적용 했음
        tags = ['Asset', 'free', 'locked', 'withdrawing', 'ipoable', 'btcValuation']
        for tag in tags:
            label = QLabel(tag)
            label.setStyleSheet(label_st)
            self.asset_title.addWidget(label)
        # Add the QHboxLayout to the QVboxLayout
        self.layout().addLayout(self.asset_title)