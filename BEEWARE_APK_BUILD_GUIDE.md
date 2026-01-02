# WordMaster BeeWare APK构建指南

## 📋 项目概述

**项目**: WordMaster英语学习应用 (BeeWare版本)  
**构建工具**: BeeWare + Briefcase  
**目标平台**: Android  
**开发框架**: Toga (BeeWare原生UI框架)  

## 🏗️ BeeWare架构说明

### 与原Kivy版本的主要差异

1. **UI框架**: Kivy → Toga (原生UI)
2. **构建工具**: Buildozer → Briefcase
3. **平台支持**: 更好的原生体验
4. **代码结构**: 重新组织为标准的Python包结构

### 项目结构

```
wordmaster/
├── pyproject.toml          # Briefcase项目配置
├── src/wordmaster/         # 主要源码目录
│   ├── __init__.py         # 包初始化
│   ├── app.py             # 主应用文件 (Toga版本)
│   ├── utils/             # 工具模块
│   │   ├── audio_beeware.py    # BeeWare音频支持
│   │   ├── speech_recog_beeware.py  # BeeWare语音识别
│   │   └── ...            # 其他工具
│   └── data/              # 应用数据
│       ├── audio/         # 音频文件
│       └── ...            # 其他资源
└── ...                    # 其他文件
```

## 🚀 构建前准备

### 1. 系统要求

- **操作系统**: Linux (推荐) 或 macOS
- **Python**: 3.8+ (推荐 3.11)
- **Java**: OpenJDK 11+ (用于Android构建)
- **Android SDK**: API Level 21+
- **Git**: 用于版本控制

### 2. 安装BeeWare工具链

```bash
# 安装BeeWare核心工具
pip install briefcase

# 安装Toga UI框架
pip install toga

# 安装Android支持
pip install toga-android

# 安装构建依赖
pip install plyer pillow requests
```

### 3. 配置Android开发环境

```bash
# 设置环境变量
export ANDROID_HOME=/path/to/android-sdk
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# 接受Android SDK许可证
yes | sdkmanager --licenses
```

## 📦 本地构建APK

### 步骤1: 初始化BeeWare项目

```bash
# 进入项目目录
cd wordmaster

# 初始化Briefcase项目 (如果尚未完成)
briefcase create

# 生成Android平台文件
briefcase build android
```

### 步骤2: 构建APK

```bash
# 构建Android APK
briefcase build android

# 构建并运行在模拟器上
briefcase run android

# 构建并安装到连接的设备
briefcase run android --device <device_id>
```

### 步骤3: 打包发布

```bash
# 生成发布版APK
briefcase build android --release

# 生成AAB文件 (Google Play格式)
briefcase build android --release --format aab
```

## 🌐 GitHub Actions自动化构建

### 创建GitHub Actions工作流

创建 `.github/workflows/beeware-build-android.yml`:

```yaml
name: 🐝 WordMaster BeeWare APK构建

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:
    inputs:
      build_type:
        description: '构建类型'
        required: false
        default: 'debug'
        type: choice
        options:
        - debug
        - release

jobs:
  build-beeware-apk:
    name: 🐝 构建BeeWare APK
    runs-on: ubuntu-22.04
    timeout-minutes: 180
    
    env:
      PYTHON_VERSION: '3.11'
    
    steps:
    - name: 📥 检出代码
      uses: actions/checkout@v4
      
    - name: 🐍 设置Python环境
      uses: actions/setup-python@v5
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        cache: 'pip'
        
    - name: 📦 安装系统依赖
      run: |
        sudo apt-get update -y
        sudo apt-get install -y --no-install-recommends \
            openjdk-17-jdk \
            android-tools-adb \
            android-tools-fastboot \
            build-essential \
            git
        
    - name: 🐝 安装BeeWare工具链
      run: |
        python -m pip install --upgrade pip
        pip install briefcase toga toga-android
        
    - name: 📲 配置Android SDK
      run: |
        mkdir -p $HOME/android-sdk
        cd $HOME
        
        # 下载Android命令行工具
        curl -L -o commandlinetools.zip \
          "https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip"
        
        unzip -q commandlinetools.zip
        mkdir -p android-sdk/cmdline-tools
        mv cmdline-tools android-sdk/cmdline-tools/latest
        
        # 设置环境变量
        export ANDROID_HOME=$HOME/android-sdk
        export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
        export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$PATH
        
        # 安装必需的SDK组件
        yes | sdkmanager --sdk_root=$ANDROID_HOME --licenses
        sdkmanager --sdk_root=$ANDROID_HOME \
          "platform-tools" \
          "platforms;android-31" \
          "build-tools;33.0.2"
        
    - name: 🏗️ 构建BeeWare APK
      run: |
        export ANDROID_HOME=$HOME/android-sdk
        export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
        export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH
        
        echo "=== 构建类型: ${{ github.event.inputs.build_type || 'debug' }} ==="
        
        if [ "${{ github.event.inputs.build_type }}" = "release" ]; then
          briefcase build android --release
        else
          briefcase build android
        fi
        
    - name: 📊 检查构建结果
      run: |
        echo "=== 查找APK文件 ==="
        find . -name "*.apk" -type f
        
    - name: 📦 上传APK产物
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: wordmaster-beeware-apk-${{ github.sha }}
        path: |
          macOS/WordMaster/app/WordMaster.app/
          iOS/WordMaster/
          android/gradle/wrapper/
        retention-days: 30
```

## 🔧 常见问题与解决方案

### 1. 构建失败 - 依赖问题

**错误**: `ModuleNotFoundError: No module named 'toga'`

**解决方案**:
```bash
# 重新安装BeeWare工具链
pip uninstall briefcase toga toga-android
pip install --upgrade briefcase toga toga-android
```

### 2. Android SDK问题

**错误**: `Android SDK not found`

**解决方案**:
```bash
# 检查ANDROID_HOME环境变量
echo $ANDROID_HOME

# 重新下载和配置SDK
sdkmanager --sdk_root=$ANDROID_HOME --list_installed
```

### 3. Java版本冲突

**错误**: `JAVA_HOME is set to an invalid directory`

**解决方案**:
```bash
# 检查Java版本
java -version

# 设置正确的JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```

### 4. 权限问题

**错误**: `Permission denied`

**解决方案**:
```bash
# 添加执行权限
chmod +x $ANDROID_HOME/cmdline-tools/latest/bin/*
chmod +x $ANDROID_HOME/platform-tools/*
```

## 📱 测试与调试

### 本地测试

```bash
# 在桌面上运行应用 (开发模式)
briefcase dev

# 运行Android模拟器
emulator -avd <avd_name>

# 在模拟器上运行
briefcase run android
```

### 调试技巧

1. **日志查看**:
   ```bash
   # 查看Android设备日志
   adb logcat | grep -i wordmaster
   ```

2. **APK安装**:
   ```bash
   # 直接安装APK
   adb install android/gradle/wrapper/WordMaster-0.0.1-debug.apk
   ```

3. **性能分析**:
   ```bash
   # 监控应用性能
   adb shell top | grep wordmaster
   ```

## 🎯 构建优化建议

### 1. 减小APK大小

```toml
# 在pyproject.toml中配置
[tool.briefcase.app.wordmaster.android]
# 排除不必要的文件
exclude = [
    "*.pyc",
    "__pycache__",
    "*.pyo",
    "test*",
]
```

### 2. 优化启动时间

- 使用懒加载模式
- 减少初始化时的资源加载
- 优化Toga组件的创建

### 3. 平台特定优化

```python
# 检测平台并应用特定优化
if toga.platform.current_platform == "android":
    # Android特定优化
    pass
elif toga.platform.current_platform == "ios":
    # iOS特定优化
    pass
```

## 📋 部署检查清单

### 构建前检查
- [ ] Python环境正确配置
- [ ] BeeWare工具链安装完整
- [ ] Android SDK正确安装
- [ ] Java版本兼容 (11+)
- [ ] 项目文件结构完整

### 构建后检查
- [ ] APK文件成功生成
- [ ] APK大小合理 (< 100MB)
- [ ] 应用能正常启动
- [ ] 核心功能正常工作
- [ ] 音频播放功能正常

### 发布前检查
- [ ] 移除调试信息
- [ ] 优化APK大小
- [ ] 测试不同Android版本
- [ ] 验证权限配置
- [ ] 检查图标和启动画面

## 🚀 触发构建

### 方法1: 手动触发
1. 访问GitHub仓库
2. 点击"Actions"标签
3. 选择"BeeWare APK构建"工作流
4. 点击"Run workflow"
5. 选择构建类型并运行

### 方法2: 代码推送
- 推送代码到main分支自动触发

### 方法3: 本地构建
```bash
# 本地开发构建
briefcase dev

# 生产构建
briefcase build android --release
```

## 📈 预期结果

基于BeeWare的构建方案，预期能够：

1. ✅ **原生体验**: 使用Toga提供更好的原生UI体验
2. ✅ **更好的性能**: 原生组件比跨平台框架性能更优
3. ✅ **跨平台支持**: 同一套代码支持Android、iOS、桌面平台
4. ✅ **现代工具链**: 使用Briefcase提供现代化的构建流程
5. ✅ **更好的维护性**: BeeWare社区活跃，文档完善

---

**文档版本**: 1.0  
**最后更新**: 2026-01-02  
**状态**: 构建指南已完成，准备测试  