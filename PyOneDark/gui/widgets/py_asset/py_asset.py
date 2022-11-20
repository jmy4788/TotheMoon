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

# PyAsset is QWidgets that can be used to display assets in the main page
# ///////////////////////////////////////////////////////////////
class PyAsset(QWidget):
    # PyAsset get the param client
    # ///////////////////////////////////////////////////////////////
    def __init__(self, client, parent=None):
        super(PyAsset, self).__init__(parent)
        self.client = client
        self.show_asset()

    # Show the asset as the list into PyAsset
    # ///////////////////////////////////////////////////////////////
    def show_asset(self):
        # Get the theme
        theme = Themes().items
        # Set the layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        # Set the style
        self.setStyleSheet(style.format(
            # QPushbutton color
            _color=theme['app_color']['text_title'],
            _radius=theme['radius'],
            _bg_color=theme['app_color']['bg_one'],
            _bg_color_hover=theme['app_color']['icon_hover'],
            _bg_color_pressed=theme['app_color']['icon_pressed']
        ))
        # Set the asset
        self.set_asset()

    # Set the asset
    # ///////////////////////////////////////////////////////////////
    def set_asset(self):
        # Get the theme
        theme = Themes().items
        # Set the asset
        self.asset = self.client.user_asset
        # self.asset is the list of dictionary that key is "asset", "free", "locked", "withdrawing", "ipoable", "btcValuation"
        for asset in self.asset:
            # Set the asset name
            self.asset_name = asset['asset']
            # Set the asset value
            self.asset_value = asset['free']
            # Set the asset locked
            self.asset_locked = asset['locked']
            # Set the asset withdrawing
            self.asset_withdrawing = asset['withdrawing']
            # Set the asset ipoable
            self.asset_ipoable = asset['ipoable']
            # Set the asset btcValuation
            self.asset_btcValuation = asset['btcValuation']
            # Set the asset layout
            self.asset_layout = QHBoxLayout()
            self.asset_layout.setContentsMargins(0, 0, 0, 0)
            self.asset_layout.setSpacing(0)
            self.setLayout(self.asset_layout)
            # Set the asset name
            self.asset_name_widget = QLabel(self.asset_name)
            self.asset_name_widget.setObjectName('asset_name_widget')
            self.asset_name_widget.setStyleSheet('''

                #asset_name_widget {{
                    font-size: 13pt;
                    font-family: SF Pro Regular, malgun gothic, serif;
                    color: {_color};
                }}
            '''.format(
                _color=theme['text']
            ))
            # Set the asset value
            self.asset_value_widget = QLabel(self.asset_value)
            self.asset_value_widget.setObjectName('asset_value_widget')
            self.asset_value_widget.setStyleSheet('''

                #asset_value_widget {{
                    font-size: 13pt;
                    font-family: SF Pro Regular, malgun gothic, serif;
                    color: {_color};
                }}
            '''.format(
                _color=theme['text']
            ))
            # Set the asset locked
            self.asset_locked_widget = QLabel(self.asset_locked)
            self.asset_locked_widget.setObjectName('asset_locked_widget')
            self.asset_locked_widget.setStyleSheet('''

                #asset_locked_widget {{
                    font-size: 13pt;
                    font-family: SF Pro Regular, malgun gothic, serif;
                    color: {_color};
                }}
            '''.format(
                _color=theme['text']
            ))
            # Set the asset withdrawing
            self.asset_withdrawing_widget = QLabel(self.asset_withdrawing)
            self.asset_withdrawing_widget.setObjectName('asset_withdrawing_widget')
            self.asset_withdrawing_widget.setStyleSheet('''

                #asset_withdrawing_widget {{
                    font-size: 13pt;
                    font-family: SF Pro Regular, malgun gothic, serif;
                    color: {_color};
                }}
            '''.format(
                _color=theme['text']
            ))
            # Set the asset ipoable
            self.asset_ipoable_widget = QLabel(self.asset_ipoable)
            self.asset_ipoable_widget.setObjectName('asset_ipoable_widget')
            self.asset_ipoable_widget.setStyleSheet('''

                #asset_ipoable_widget {{
                    font-size: 13pt;
                    font-family: SF Pro Regular, malgun gothic, serif;
                    color: {_color};
                }}
            '''.format(
                _color=theme['text']
            ))
            # Set the asset btcValuation
            self.asset_btcValuation_widget = QLabel(self.asset_btcValuation)
            self.asset_btcValuation_widget.setObjectName('asset_btcValuation_widget')
            self.asset_btcValuation_widget.setStyleSheet('''

                #asset_btcValuation_widget {{
                    font-size: 13pt;
                    font-family: SF Pro Regular, malgun gothic, serif;
                    color: {_color};

                }}
            '''.format(
                _color=theme['text']
            ))
            # Add the asset name widget into asset layout
            self.asset_layout.addWidget(self.asset_name_widget)
            # Add the asset value widget into asset layout
            self.asset_layout.addWidget(self.asset_value_widget)
            # Add the asset locked widget into asset layout
            self.asset_layout.addWidget(self.asset_locked_widget)
            # Add the asset withdrawing widget into asset layout
            self.asset_layout.addWidget(self.asset_withdrawing_widget)
            # Add the asset ipoable widget into asset layout
            self.asset_layout.addWidget(self.asset_ipoable_widget)
            # Add the asset btcValuation widget into asset layout
            self.asset_layout.addWidget(self.asset_btcValuation_widget)