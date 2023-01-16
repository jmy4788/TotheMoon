import os
import json

file_path = os.path.join(os.getcwd(),'gui','themes','default.json')

with open(file_path, 'r') as f:
    data = json.load(f)

dark_one = data["app_color"]["dark_one"]
dark_two = data["app_color"]["dark_two"]
dark_three = data["app_color"]["dark_three"]
dark_four = data["app_color"]["dark_four"]
bg_one = data["app_color"]["bg_one"]
bg_two = data["app_color"]["bg_two"]
bg_three = data["app_color"]["bg_three"]
icon_color = data["app_color"]["icon_color"]
icon_hover = data["app_color"]["icon_hover"]
icon_pressed = data["app_color"]["icon_pressed"]
icon_active = data["app_color"]["icon_active"]
context_color = data["app_color"]["context_color"]
context_hover = data["app_color"]["context_hover"]
context_pressed = data["app_color"]["context_pressed"]
text_title = data["app_color"]["text_title"]
text_foreground = data["app_color"]["text_foreground"]
text_description = data["app_color"]["text_description"]
text_active = data["app_color"]["text_active"]

PushBtn = f'''
QPushButton {{
    font-size: 13pt;
    font-family: SF Pro Heavy, malgun gothic, serif;
	border: none;
    padding-left: 10px;
    padding-right: 5px;
    color: {icon_color};
	border-radius: 8;	
	background-color: {dark_one};
}}
QPushButton:hover {{
	background-color: {context_hover};
}}
QPushButton:pressed {{	
	background-color: {context_pressed};
}}
'''


QLabel_title = '''
QLabel{
    color: #8a95aa;
    background-color: #2c313c;
    font-size: 14pt;
    font-family: SF Pro Heavy, malgun gothic, serif;
}'''
QLabel_title_kr = '''
QLabel{
    color: #8a95aa;
    background-color: #2c313c;
    font-size: 12pt;
    font-family: SF Pro Heavy, malgun gothic, serif;
}'''

QLabel_body = '''
QLabel{
    color: #8a95aa;
    background-color: #2c313c;
    font-size: 11pt;
    font-family: SF Pro regular, malgun gothic, serif;
}'''
QLabel_body_kr = '''
QLabel{
    color: #8a95aa;
    background-color: #2c313c;
    font-size: 10pt;
    font-family: SF Pro regular, malgun gothic, serif;
}'''
