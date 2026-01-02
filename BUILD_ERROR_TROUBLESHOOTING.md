# WordMaster APK构建错误详细排查指南

## 1. 错误概述

```
Buildozer failed to execute the last command
The error might be hidden in the log above this error
Please read the full log, and search for it before
raising an issue with buildozer itself.
Error: Process completed with exit code 1.
```

## 2. 排查步骤

### 2.1 查看GitHub Actions工作流详细日志

1. 进入GitHub仓库的"Actions"页面
2. 点击失败的构建工作流
3. 展开每个步骤查看详细日志
4. 特别关注：
   - 安装依赖的步骤
   - 构建APK的步骤
   - 错误信息前后的内容

### 2.2 常见问题排查

#### 2.2.1 依赖问题

**现象**: 构建过程中出现模块导入错误或依赖安装失败

**解决方案**:
1. 进一步简化buildozer.spec中的requirements
2. 移除可能与Android不兼容的Python包
3. 使用Android兼容的替代方案

#### 2.2.2 内存限制

**现象**: 构建过程因内存不足而中断

**解决方案**:
1. 在GitHub Actions工作流中添加--no-cache标志
2. 增加虚拟内存或交换空间

#### 2.2.3 Android SDK/NDK版本不兼容

**现象**: 构建工具无法找到正确的SDK或NDK版本

**解决方案**:
1. 检查并更新GitHub Actions工作流中的Android SDK版本
2. 确保buildozer.spec中的android.api与SDK版本兼容

#### 2.2.4 Kivy版本不兼容

**现象**: 构建过程中出现Kivy相关错误

**解决方案**:
1. 在buildozer.spec中指定特定的Kivy版本
2. 确认kivy_compat.py中的兼容性修复正确

### 2.3 简化构建方案

如果上述排查方法无法解决问题，可以尝试以下简化方案：

#### 方案1: 最小依赖构建

在buildozer.spec中仅保留最基础的依赖：

```
requirements = python3,kivy
```

#### 方案2: 使用更简单的主文件

创建一个简化版的main.py文件：

```python
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class WordMaster(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Button(text='Hello World'))
        return layout

WordMaster().run()
```

#### 方案3: 启用详细日志

在buildozer.spec中添加：

```
[buildozer]
log_level = 2
```

## 3. 高级调试技巧

### 3.1 本地构建测试

如果可能，在本地Linux环境（使用Docker）测试构建过程：

```bash
# 使用Docker构建
docker run -it -v $(pwd):/app python:3.11 bash
# 进入容器后
apt-get update && apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
cd /app
pip install buildozer
buildozer android debug
```

### 3.2 添加调试代码

在main.py中添加更多调试信息：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 3.3 检查构建环境

在GitHub Actions工作流中添加环境检查步骤：

```yaml
- name: 🔍 检查构建环境
  run: |
    echo "=== Python版本 ==="
    python --version
    pip --version
    
    echo "=== Android环境 ==="
    echo $ANDROID_HOME
    ls -la $ANDROID_HOME
    
    echo "=== Java环境 ==="
    echo $JAVA_HOME
    java -version
    
    echo "=== buildozer版本 ==="
    buildozer --version
```

## 4. 进一步修改建议

基于目前的情况，我建议进行以下修改：

1. **创建一个极简的buildozer.spec文件**，仅包含必要的配置
2. **创建一个简化版main.py**，去除所有可能导致问题的复杂功能
3. **修改GitHub Actions工作流**，添加更多环境检查和日志记录
4. **实施分步构建**，先确保基本功能可以构建，再逐步添加功能

## 5. 总结

APK构建问题通常是由以下原因造成的：

1. **不兼容的依赖**: 某些Python包与Android平台不兼容
2. **版本冲突**: 不同组件之间的版本不匹配
3. **资源限制**: 构建环境的内存或存储空间不足
4. **配置错误**: buildozer.spec或工作流配置不正确

通过系统地排查这些问题，我们可以确定构建失败的根本原因，并实施有效的解决方案。