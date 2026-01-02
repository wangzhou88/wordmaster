#!/usr/bin/env python
# 简单UI测试脚本 - 验证Toga UI组件

import sys

try:
    import toga
    from toga.style import Pack
    from toga.style.pack import COLUMN, ROW
    
    # 尝试创建一个简单的应用
    class SimpleUITest(toga.App):
        def startup(self):
            # 创建主容器
            self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
            
            # 添加标题
            title_label = toga.Label(
                'Toga UI 测试',
                style=Pack(font_size=24, font_weight='bold', padding=(0, 10))
            )
            self.main_box.add(title_label)
            
            # 添加标签
            label = toga.Label(
                'Toga UI组件正常工作',
                style=Pack(font_size=16, padding=(0, 10))
            )
            self.main_box.add(label)
            
            # 添加按钮
            test_button = toga.Button(
                '点击测试',
                on_press=self.button_pressed,
                style=Pack(padding=10)
            )
            self.main_box.add(test_button)
            
            # 创建主窗口
            self.main_window = toga.MainWindow(title="Toga UI测试")
            self.main_window.content = self.main_box
            self.main_window.size = (600, 400)
            
            # 显示主窗口
            self.main_window.show()
        
        def button_pressed(self, widget):
            dialog = toga.InfoDialog(
                title='测试成功',
                message='Toga UI交互正常工作!'
            )
            dialog.show(self.main_window)
    
    # 创建应用实例
    app = SimpleUITest("Toga UI测试", "com.example.ui_test")
    print("成功创建Toga UI应用实例")
    
    # 运行应用 - 注意：这会阻塞直到窗口关闭
    # app.main_loop()
    
    print("UI组件创建成功！可以运行app.main_loop()来显示窗口")
    
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)