# 📱 WordMaster 本地APK构建指南

## ⚠️ 重要说明

**当前Buildozer 1.5.0版本只支持iOS，不支持Android！**

本指南提供了几种本地Android构建的方案，但建议优先使用GitHub Actions云端构建。

## 🎯 可选方案对比

| 方案 | 复杂度 | 成功率 | 耗时 | 推荐度 |
|------|--------|--------|------|--------|
| **GitHub Actions** | ⭐ | 95% | 15分钟 | ⭐⭐⭐⭐⭐ |
| **Python-for-Android** | ⭐⭐⭐⭐ | 60% | 2-4小时 | ⭐⭐⭐ |
| **Android Studio** | ⭐⭐⭐⭐⭐ | 40% | 4-8小时 | ⭐⭐ |
| **Docker容器** | ⭐⭐⭐⭐ | 70% | 1-2小时 | ⭐⭐⭐ |

## 🚀 方案一：使用Python-for-Android (推荐)

### 1. 环境准备
```bash
# 升级基础工具
pip install --upgrade setuptools wheel

# 安装python-for-android
pip install python-for-android

# 检查安装
p4a --version
```

### 2. 检查Java环境
```bash
java -version
# 需要Java 8或11
```

### 3. 安装Android SDK (通过命令行)
```bash
# 下载Android命令行工具
# https://developer.android.com/studio#command-tools

# 设置环境变量 (在Windows上)
set ANDROID_HOME=C:\Android
set PATH=%PATH%;C:\Android\cmdline-tools\latest\bin;C:\Android\platform-tools
```

### 4. 构建APK
```bash
# 初始化项目
p4a apk --name "WordMaster" --package com.wordmaster.app --version 1.0.0

# 或者使用现有buildozer.spec
p4a apk --requirements=kivy,sqlite3,requests,plyer,pydub,SpeechRecognition,Pillow,pygame
```

## 🐳 方案二：使用Docker容器

### 1. 安装Docker Desktop for Windows
- 下载: https://www.docker.com/products/docker-desktop/

### 2. 使用Android构建容器
```bash
# 拉取Kivy Android构建容器
docker pull kivy/python-for-android

# 进入容器进行构建
docker run -it -v $(pwd):/app kivy/python-for-android bash
cd /app
p4a apk --name WordMaster
```

## 🏗️ 方案三：Android Studio (最复杂)

### 1. 下载安装Android Studio
- https://developer.android.com/studio

### 2. 通过SDK Manager安装
- Android SDK Platform 33
- Android SDK Build-Tools 33.0.0
- Android NDK (用于编译原生代码)
- Android SDK Tools

### 3. 配置环境变量
```bash
set ANDROID_HOME=C:\Users\%USERNAME%\AppData\Local\Android\Sdk
set ANDROID_NDK_HOME=%ANDROID_HOME%\ndk\25.1.8937393
set PATH=%PATH%;%ANDROID_HOME%\cmdline-tools\latest\bin
```

### 4. 使用buildozer
```bash
# 在Android Studio终端中执行
buildozer android debug --verbose
```

## 🔧 常见问题解决方案

### 问题1: "Java not found"
**解决方案**:
```bash
# 下载并安装Java 11
# https://adoptium.net/
# 设置JAVA_HOME环境变量
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-11.0.19.7-hotspot
```

### 问题2: "Android SDK权限错误"
**解决方案**:
```bash
# 以管理员权限运行
# 右键命令提示符 -> "以管理员身份运行"
```

### 问题3: "NDK版本不兼容"
**解决方案**:
```bash
# 在Android Studio SDK Manager中安装NDK r23c
# 或者设置兼容的NDK版本
```

### 问题4: "内存不足"
**解决方案**:
```bash
# 增加Java堆内存
set JAVA_OPTS=-Xmx4g
```

### 问题5: "网络超时"
**解决方案**:
```bash
# 使用国内镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple python-for-android
```

## 📋 构建检查清单

在开始构建前，请确认：

- [ ] Python 3.8+ 已安装
- [ ] Java 8或11已安装
- [ ] Android SDK已安装并配置环境变量
- [ ] 有至少4GB可用内存
- [ ] 网络连接稳定
- [ ] buildozer.spec文件存在且配置正确

## 🎯 推荐策略

### 立即可用方案 (推荐)
1. **使用GitHub Actions**
   - 访问: https://github.com/wangzhou88/wordmaster/actions
   - 点击 "Run workflow"
   - 15分钟后下载APK

### 学习目的方案
2. **如果确实需要本地构建**
   - 优先尝试 python-for-android 方案
   - 准备充足时间 (2-4小时)
   - 确保网络稳定

### 备选方案
3. **使用在线构建服务**
   - Appetize.io
   - CircleCI
   - AppVeyor

## 💡 总结

**对于大多数用户，强烈推荐使用GitHub Actions云端构建**，原因：

1. **零配置** - 无需安装复杂的Android开发环境
2. **稳定性高** - GitHub提供经过测试的构建环境
3. **节省时间** - 无需处理环境配置问题
4. **免费使用** - GitHub Actions对公开仓库免费
5. **便于分享** - 构建结果自动存储在GitHub

本地Android构建虽然技术可行，但对于非专业开发者来说，投入产出比太低。建议将精力集中在应用功能开发和测试上，而不是环境配置上。

---

**最后更新**: 2026-01-02
**推荐方案**: GitHub Actions云端构建