# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# STYLE
# ///////////////////////////////////////////////////////////////
class MYCombobox(QComboBox):
    def __init__(self, parent=None):
        super(MYCombobox, self).__init__(parent)

        # Sample items
        for i in range(5):
            self.addItem(f"Item {i}")

        # Set the fixed width and height
        self.setFixedWidth(80)
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QComboBox {
                background-color: #1b1e23;
                color: white;
                border: 2px solid #2a2d33;
                border-radius: 8px;
                padding: 5px;
                font : Arial;
                font-size : 13px;
                font-weight: bold;
                text-align: center;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #1b1e23;
                color: white;
                border: 2px solid #2a2d33;
                selection-background-color: #568af2;
                font : Arial;
                font-weight: bold;
                text-align: center;
            }
        """)

    def showPopup(self):
        self.view().setStyleSheet("""
            QListView {
                background-color: #1b1e23;
                border: none;
                font: Arial;
                font-weight: bold;
            }
            QListView::item {
                color: white;
                padding: 5px;
            }
            QListView::item:hover {
                background-color: #568af2;
            }
        """)
        super(MYCombobox, self).showPopup()