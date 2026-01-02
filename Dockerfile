# WordMaster Android构建镜像
# 基于Python 3.11，包含完整的Android开发环境

FROM python:3.11-slim

# 设置标签
LABEL maintainer="WordMaster Development Team"
LABEL description="WordMaster Android APK构建环境"
LABEL version="1.0"

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# 创建非root用户
RUN groupadd -r builder && useradd -r -g builder -m -s /bin/bash builder

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    # Java和Android开发工具
    openjdk-11-jdk \
    wget \
    unzip \
    curl \
    git \
    # 构建工具
    build-essential \
    autoconf \
    automake \
    # 压缩工具
    gzip \
    tar \
    # 权限工具
    sudo \
    # 清理缓存
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# 配置Java环境
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# 创建Android SDK目录
ENV ANDROID_HOME=/opt/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# 创建Android SDK目录
RUN mkdir -p $ANDROID_HOME

# 下载并安装Android命令行工具
WORKDIR /tmp
RUN wget -q https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip && \
    unzip -q commandlinetools-win-11076708_latest.zip && \
    mkdir -p $ANDROID_HOME/cmdline-tools && \
    mv cmdline-tools $ANDROID_HOME/cmdline-tools/latest && \
    rm commandlinetools-win-11076708_latest.zip

# 接受许可证并安装Android SDK组件
RUN yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --licenses

# 安装Android SDK组件
RUN $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager \
    "platform-tools" \
    "platforms;android-31" \
    "build-tools;31.0.0" \
    "system-images;android-31;google_apis;x86_64" \
    "platforms;android-30" \
    "build-tools;30.0.3"

# 升级Python工具并安装python-for-android
RUN pip install --upgrade setuptools wheel pip

# 安装python-for-android
RUN pip install python-for-android

# 切换到工作目录
WORKDIR /app

# 设置工作目录权限
RUN chown -R builder:builder /app

# 切换到builder用户
USER builder

# 暴露端口（如果需要调试）
EXPOSE 8000

# 设置默认命令
CMD ["/bin/bash"]