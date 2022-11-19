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

# QT CORE
# Change for PySide Or PyQt
# ///////////////////////// WARNING: ////////////////////////////
# Remember that changing to PyQt too many modules will have 
# problems because some classes have different names like: 
# Property (pyqtProperty), Slot (pyqtSlot), Signal (pyqtSignal)
# among others.
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtSvgWidgets import *
from PySide6.QtCharts import *
from binance.spot import Spot as Client
from binance.lib.utils import config_logging

style = '''
QPushButton {{
    font-size: 13pt;
    font-family: SF Pro Regular, malgun gothic, serif;
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