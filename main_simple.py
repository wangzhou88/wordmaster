"""
WordMaster - 简化版主文件
用于测试基本APK构建功能
"""
import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# 设置应用基本颜色
PRIMARY_COLOR = get_color_from_hex('#2196F3')
BACKGROUND_COLOR = get_color_from_hex('#FFFFFF')
TEXT_COLOR = get_color_from_hex('#333333')

# 设置窗口尺寸（安卓兼容）
Window.size = (360, 640)
Window.clearcolor = BACKGROUND_COLOR

class WordMasterApp(App):
    def build(self):
        # 主布局
        main_layout = BoxLayout(
            orientation='vertical',
            padding=[20, 40, 20, 40],
            spacing=20
        )
        
        # 应用标题
        title_label = Label(
            text='[b]WordMaster[/b]',
            font_size='32sp',
            markup=True,
            color=PRIMARY_COLOR,
            size_hint_y=0.2
        )
        
        # 副标题
        subtitle_label = Label(
            text='英语学习助手',
            font_size='18sp',
            color=TEXT_COLOR,
            size_hint_y=0.15
        )
        
        # 欢迎消息
        welcome_label = Label(
            text='欢迎使用WordMaster！\n\n这是简化版，用于测试APK构建。',
            font_size='16sp',
            color=TEXT_COLOR,
            text_size=(None, None),
            halign='center',
            valign='middle',
            size_hint_y=0.5
        )
        
        # 按钮布局
        button_layout = BoxLayout(
            orientation='horizontal',
            spacing=20,
            size_hint_y=0.15
        )
        
        # 添加按钮
        button1 = Button(
            text='测试按钮 1',
            background_color=PRIMARY_COLOR,
            size_hint_x=0.5
        )
        
        button2 = Button(
            text='测试按钮 2',
            background_color=PRIMARY_COLOR,
            size_hint_x=0.5
        )
        
        # 将组件添加到布局
        main_layout.add_widget(title_label)
        main_layout.add_widget(subtitle_label)
        main_layout.add_widget(welcome_label)
        button_layout.add_widget(button1)
        button_layout.add_widget(button2)
        main_layout.add_widget(button_layout)
        
        return main_layout

if __name__ == '__main__':
    # 启用调试日志
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    # 运行应用
    WordMasterApp().run()