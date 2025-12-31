# 🛠️ WordMaster 本地APK构建指南

## 📋 环境要求

### 系统要求
- **操作系统**: Windows 10/11, macOS 10.14+, 或 Linux
- **Python**: 3.8 或更高版本
- **内存**: 最少 4GB RAM (推荐 8GB+)
- **存储**: 至少 10GB 可用空间
- **网络**: 稳定的互联网连接

### 必需软件清单

1. **Python 3.8+**
   - 下载: https://python.org/downloads/
   - 安装时勾选 "Add Python to PATH"

2. **Java Development Kit (JDK) 8+**
   - 下载: https://adoptium.net/ (推荐 OpenJDK)
   - 或从 Oracle 官网下载

3. **Android SDK**
   - 方式1: 安装 Android Studio
   - 方式2: 仅安装命令行工具

4. **Buildozer**
   - 通过 pip 安装: `pip install buildozer`

---

## 🔧 环境配置步骤

### 步骤 1: 安装 Python 依赖

```bash
# 进入项目目录
cd c:\Users\admin\Downloads\wordmaster

# 安装项目依赖
pip install -r requirements.txt

# 安装 Buildozer
pip install buildozer
```

### 步骤 2: 配置 Android SDK

#### 选项 A: 使用 Android Studio
1. 下载并安装 [Android Studio](https://developer.android.com/studio)
2. 启动 Android Studio
3. 通过 SDK Manager 安装:
   - Android SDK Platform
   - Android SDK Build-Tools
   - Android SDK Tools
   - Android Emulator (可选)

#### 选项 B: 仅使用命令行工具
```bash
# 下载 Android 命令行工具
# https://developer.android.com/studio#command-tools

# 解压到任意目录，如:
# C:\Android\cmdline-tools

# 设置环境变量
ANDROID_HOME=C:\Android
PATH=%PATH%;C:\Android\cmdline-tools\latest\bin;C:\Android\platform-tools
```

### 步骤 3: 验证环境配置

```bash
# 检查 Python 版本
python --version

# 检查 Java 版本
java -version

# 检查 Android SDK
adb version

# 检查 Buildozer
buildozer --version
```

---

## 🚀 本地构建过程

### 构建前准备

```bash
# 1. 进入项目目录
cd c:\Users\admin\Downloads\wordmaster

# 2. 清理之前的构建缓存 (可选)
buildozer clean

# 3. 检查 buildozer.spec 配置
# 文件已配置好，包含:
# - 应用名称: WordMaster英语学习助手
# - 包名: org.wordmaster.wordmaster
# - 版本: 1.0
# - 权限: INTERNET, STORAGE, AUDIO
```

### 执行构建

```bash
# 开始构建 APK (debug 版本)
buildozer android debug

# 如果遇到网络问题，可以指定镜像源
buildozer android debug --android_api 33

# 构建发布版本 (需要签名)
buildozer android release
```

### 构建过程说明

构建过程分为以下阶段:
1. **初始化** (1-2分钟)
   - 检查环境
   - 下载依赖

2. **编译** (5-10分钟)
   - 编译 Python 代码
   - 生成 APK

3. **打包** (2-3分钟)
   - 整合资源
   - 生成最终 APK

**总耗时**: 约 8-15 分钟 (取决于网络和硬件)

---

## 📱 构建产物

### APK 文件位置

构建成功后，APK 文件位于:
```
bin/wordmaster-1.0-armeabi-v7a-debug.apk
```

### 文件命名规则
- `wordmaster`: 应用包名
- `1.0`: 版本号
- `armeabi-v7a`: ARM 架构
- `debug`: 构建类型

### APK 大小
预期大小: 50-80MB
- 包含完整的 Python 运行时
- 包含所有依赖库
- 包含音频和图标资源

---

## 🔍 故障排除

### 常见错误及解决方案

#### 1. Buildozer 安装失败
```bash
# 错误: Microsoft Visual C++ 14.0 is required
# 解决: 安装 Visual Studio Build Tools
# 下载: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

#### 2. Android SDK 找不到
```bash
# 错误: ANDROID_HOME not set
# 解决: 设置环境变量
set ANDROID_HOME=C:\Android
set PATH=%PATH%;%ANDROID_HOME%\platform-tools
```

#### 3. Python 依赖冲突
```bash
# 错误: Could not find compatible version
# 解决: 升级 pip 和 setuptools
python -m pip install --upgrade pip setuptools wheel
```

#### 4. 内存不足
```bash
# 错误: Java heap space
# 解决: 增加 Java 堆内存
set JAVA_OPTS=-Xmx4g
```

#### 5. 网络超时
```bash
# 错误: Connection timeout
# 解决: 增加超时时间
buildozer android debug --android_api 33 --android_ndk_api 21
```

---

## 📋 构建检查清单

### 环境检查
- [ ] Python 3.8+ 已安装
- [ ] JDK 8+ 已安装
- [ ] Android SDK 已安装并配置
- [ ] Buildozer 已安装
- [ ] 项目依赖已安装

### 配置检查
- [ ] buildozer.spec 文件存在
- [ ] requirements.txt 文件存在
- [ ] 图标文件已配置 (data/icon_bg.png, data/icon_fg.png)
- [ ] 数据库文件已存在 (wordmaster.db)
- [ ] 音频资源已准备好 (data/audio/)

### 构建检查
- [ ] 执行 `buildozer android debug`
- [ ] 等待构建完成 (8-15分钟)
- [ ] 检查 APK 文件是否生成
- [ ] 验证 APK 文件大小 (50-80MB)

---

## 🎯 下一步操作

### 1. 测试 APK
- 将 APK 文件传输到 Android 设备
- 在设备设置中允许"未知来源"安装
- 安装并启动应用

### 2. 优化构建
```bash
# 如果需要减小 APK 大小
buildozer android debug --android_api 33 --android_ndk_api 21

# 如果需要发布版本
buildozer android release
# 注意: 发布版本需要签名配置
```

### 3. 调试问题
```bash
# 查看详细日志
buildozer android debug logcat

# 查看构建日志
buildozer android debug clean build
```

---

**提示**: 首次构建可能需要下载大量依赖，请确保网络连接稳定。如果遇到问题，请提供具体错误信息以便进一步诊断。