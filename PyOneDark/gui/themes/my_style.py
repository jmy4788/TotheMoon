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

label_st = '''
QLabel {
    color: #FFFFFF;
    background-color: #2c313c;
    font-size: 15pt;
    font-family: SF Pro Heavy, malgun gothic, serif;
}
'''