#!/usr/bin/env python
# 简单Toga测试脚本

import sys

# 尝试导入Toga
try:
    import toga
    print(f"成功导入Toga版本: {toga.__version__}")
    
    # 尝试创建一个简单的应用
    class SimpleApp(toga.App):
        def startup(self):
            self.main_window = toga.MainWindow(title="简单测试")
            self.main_window.show()
    
    app = SimpleApp("简单测试", "com.example.simple")
    print("成功创建Toga应用实例")
    
    # 检查是否可以导入各个模块
    import toga.widgets
    print("成功导入Toga widgets")
    
    import toga.style
    print("成功导入Toga style")
    
    print("所有测试通过！Toga正常工作")
    
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)