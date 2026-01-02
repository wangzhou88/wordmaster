# 🐳 Docker本地构建环境设置指南

## 📋 系统要求

### Windows要求
- **操作系统**: Windows 10 64位版本 1903及更高版本，或 Windows 11
- **内存**: 最少4GB RAM
- **虚拟化**: 启用Hyper-V和容器功能
- **磁盘空间**: 至少20GB可用空间

### 检查Windows版本
```powershell
# 检查Windows版本
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, TotalPhysicalMemory

# 检查虚拟化支持
Get-WmiObject -Query "Select * from Win32_Processor" | Select-Object Name, VirtualizationFirmwareEnabled
```

## 🔧 Docker Desktop安装

### 步骤1: 下载Docker Desktop
1. 访问Docker官网: https://www.docker.com/products/docker-desktop
2. 下载适用于Windows的Docker Desktop
3. 文件名类似: `Docker Desktop Installer.exe`

### 步骤2: 安装Docker Desktop
1. **右键以管理员身份运行** `Docker Desktop Installer.exe`
2. 按照安装向导进行安装：
   - ✅ 启用Hyper-V（推荐）
   - ✅ 启用WSL 2（推荐）
   - ✅ 添加快捷方式
3. 重启计算机
4. 启动Docker Desktop并等待初始化完成

### 步骤3: 验证安装
```powershell
# 重启PowerShell（管理员权限）
docker --version
docker-compose --version

# 测试Docker运行
docker run hello-world
```

## ⚙️ Docker配置优化

### 启用WSL 2后端（推荐）
```powershell
# 在Docker Desktop设置中启用WSL 2
# Settings > General > Use the WSL 2 based engine
```

### 配置资源限制
```
Settings > Resources:
- CPU: 至少分配2个核心
- Memory: 至少分配4GB
- Swap: 至少1GB
- Disk image size: 至少20GB
```

### 启用Docker BuildKit
```powershell
# 设置环境变量
$env:DOCKER_BUILDKIT = "1"
```

## 📱 Android构建专用Docker镜像

### 方案1: 使用预构建镜像
```dockerfile
# Dockerfile.wordmaster
FROM python:3.11-slim

# 安装必要的系统依赖
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    git \
    build-essential \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 设置环境变量
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# 创建Android SDK目录
RUN mkdir -p $ANDROID_HOME

# 下载并安装Android命令行工具
RUN cd /tmp && \
    wget https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip && \
    unzip commandlinetools-win-11076708_latest.zip && \
    mkdir -p $ANDROID_HOME/cmdline-tools && \
    mv cmdline-tools $ANDROID_HOME/cmdline-tools/latest && \
    rm commandlinetools-win-11076708_latest.zip

# 接受许可证并安装SDK组件
RUN yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses
RUN $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager \
    "platform-tools" \
    "platforms;android-31" \
    "build-tools;31.0.0"

# 安装python-for-android
RUN pip install --upgrade setuptools wheel
RUN pip install python-for-android

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 默认命令
CMD ["bash"]
```

### 方案2: 直接运行构建命令
```bash
# 运行一次性构建容器
docker run --rm \
  -v "$(pwd):/app" \
  -w /app \
  python:3.11-slim \
  bash -c "
    apt-get update && apt-get install -y openjdk-11-jdk git &&
    export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 &&
    export ANDROID_HOME=/opt/android-sdk &&
    mkdir -p $ANDROID_HOME &&
    cd /tmp &&
    wget https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip &&
    unzip commandlinetools-win-11076708_latest.zip &&
    mkdir -p $ANDROID_HOME/cmdline-tools &&
    mv cmdline-tools $ANDROID_HOME/cmdline-tools/latest &&
    rm commandlinetools-win-11076708_latest.zip &&
    yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses &&
    $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager 'platform-tools' 'platforms;android-31' 'build-tools;31.0.0' &&
    pip install --upgrade setuptools wheel &&
    pip install python-for-android &&
    p4a apk --private /app --name wordmaster --package com.wordmaster.app
  "
```

## 🚀 快速构建脚本

### build-apk-docker.bat
```batch
@echo off
echo 🐳 Docker APK构建开始...

:: 检查Docker是否运行
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker未运行，请启动Docker Desktop
    pause
    exit /b 1
)

:: 运行构建
echo 📱 开始构建APK...
docker run --rm -v "%cd%:/app" -w /app python:3.11-slim bash -c "
apt-get update && apt-get install -y openjdk-11-jdk git &&
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 &&
export ANDROID_HOME=/opt/android-sdk &&
mkdir -p $ANDROID_HOME &&
cd /tmp &&
wget https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip &&
unzip commandlinetools-win-11076708_latest.zip &&
mkdir -p $ANDROID_HOME/cmdline-tools &&
mv cmdline-tools $ANDROID_HOME/cmdline-tools/latest &&
rm commandlinetools-win-11076708_latest.zip &&
yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses &&
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager 'platform-tools' 'platforms;android-31' 'build-tools;31.0.0' &&
pip install --upgrade setuptools wheel &&
pip install python-for-android &&
p4a apk --private /app --name wordmaster --package com.wordmaster.app
"

if %errorlevel% equ 0 (
    echo ✅ APK构建完成！
    echo 📁 APK文件位置: bin\wordmaster-1.0.0-debug.apk
) else (
    echo ❌ APK构建失败！
)

pause
```

## 🔍 故障排除

### 常见问题

#### 1. Docker Desktop启动失败
**解决方案**:
```powershell
# 以管理员身份运行PowerShell
Enable-WindowsOptionalFeature -Online -FeatureName containers -All
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
Restart-Computer
```

#### 2. 虚拟化未启用
**解决方案**:
- 重启计算机进入BIOS
- 启用Intel VT-x或AMD-V
- 启用Hyper-V

#### 3. 内存不足
**解决方案**:
- 关闭不必要的程序
- 在Docker Desktop中减少内存分配
- 考虑升级RAM

#### 4. 权限问题
**解决方案**:
```powershell
# 将用户添加到docker组（如果使用Linux）
sudo usermod -aG docker $USER

# Windows上确保以管理员身份运行
```

## 📊 性能优化

### 缓存优化
```dockerfile
# 在Dockerfile中优化缓存层
FROM python:3.11-slim

# 先复制依赖文件以利用缓存
COPY requirements.txt* ./
RUN pip install --no-cache-dir -r requirements.txt

# 然后复制源码
COPY . .
```

### 构建缓存
```bash
# 使用BuildKit缓存
DOCKER_BUILDKIT=1 docker build -t wordmaster-builder .

# 复用缓存
docker build --cache-from wordmaster-builder -t wordmaster-builder-new .
```

## 📋 验证清单

- [ ] Docker Desktop安装成功
- [ ] Docker服务运行正常
- [ ] 能够运行`docker run hello-world`
- [ ] Android构建镜像构建成功
- [ ] APK构建测试通过
- [ ] 构建脚本功能正常

## 🎯 下一步

Docker环境设置完成后，您就可以：
1. 运行`build-apk-docker.bat`构建APK
2. 使用自定义Docker镜像进行开发
3. 享受跨平台、一致的构建环境

---
**设置完成时间**: 准备就绪，等待Docker Desktop安装
**状态**: 🔧 等待用户安装Docker Desktop