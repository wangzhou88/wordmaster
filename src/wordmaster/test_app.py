"""
简化版WordMaster应用 - 仅用于测试BeeWare功能
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class TestApp(toga.App):
    def startup(self):
        """应用启动方法"""
        # 创建主容器
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        
        # 应用标题
        title_label = toga.Label(
            'WordMaster 测试版',
            style=Pack(font_size=24, font_weight='bold', padding=(0, 10))
        )
        self.main_box.add(title_label)
        
        # 测试文本
        test_label = toga.Label(
            '这是BeeWare框架测试应用',
            style=Pack(font_size=16, padding=(0, 10))
        )
        self.main_box.add(test_label)
        
        # 创建按钮
        test_button = toga.Button(
            '测试按钮',
            on_press=self.test_button_pressed,
            style=Pack(padding=10)
        )
        self.main_box.add(test_button)
        
        # 创建主窗口
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.size = (600, 400)
        
        # 显示主窗口
        self.main_window.show()

    def test_button_pressed(self, widget):
        """按钮点击事件"""
        dialog = toga.InfoDialog(
            title='测试成功',
            message='BeeWare框架工作正常！'
        )
        dialog.show(self.main_window)

def main():
    """主函数"""
    return TestApp()