# WordMaster APK 构建工作流指南

## 📱 工作流概述

WordMaster项目现在配置了完整的GitHub Actions工作流，可以自动构建Android APK文件。

## 🏗️ 工作流特性

### 主要功能
- **自动构建**: 推送到main/master分支时自动触发
- **手动触发**: 支持通过GitHub界面手动启动构建
- **多Python版本支持**: 支持Python 3.9, 3.10, 3.11, 3.12
- **调试和发布版本**: 支持debug和release构建
- **自动上传**: 构建成功后自动上传APK文件

### 触发条件
1. **自动触发**: 
   - 推送到 `main` 或 `master` 分支
   - 拉取请求合并到 `main` 或 `master` 分支

2. **手动触发**:
   - 在GitHub Actions页面点击 "Run workflow"
   - 选择构建类型和Python版本

## 🔧 工作流配置

### 环境要求
- **操作系统**: Ubuntu Latest
- **Python版本**: 3.11 (默认)
- **超时时间**: 120分钟
- **构建工具**: Buildozer + python-for-android

### 关键组件
1. **Android SDK**: 自动安装和配置
2. **Python环境**: 自动安装指定版本
3. **构建工具**: Buildozer, Cython, python-for-android
4. **镜像源**: 配置国内镜像源提升下载速度

## 📁 项目文件结构

```
wordmaster/
├── main.py                 # 应用主文件
├── requirements.txt        # Python依赖
├── buildozer.spec         # Buildozer配置文件
├── .github/
│   └── workflows/
│       └── build-android.yml  # GitHub Actions工作流
└── data/                  # 应用资源文件
    ├── audio/            # 音频文件
    ├── icon_bg.png       # 图标背景
    └── icon_fg.png       # 图标前景
```

## 🚀 使用方法

### 方法1: 自动构建 (推荐)
1. **推送代码到GitHub**
   ```bash
   git add .
   git commit -m "更新应用代码"
   git push origin main
   ```

2. **监控构建进度**
   - 访问: https://github.com/wangzhou88/wordmaster/actions
   - 查看最新的工作流运行状态

### 方法2: 手动触发构建
1. **打开GitHub Actions页面**
   - 访问: https://github.com/wangzhou88/wordmaster/actions

2. **手动运行工作流**
   - 点击 "Build WordMaster APK" 工作流
   - 点击 "Run workflow" 按钮
   - 选择构建参数:
     - **Build type**: debug 或 release
     - **Python version**: 3.9, 3.10, 3.11, 3.12
   - 点击 "Run workflow" 开始构建

## 📱 下载APK文件

### 构建完成后
1. **进入构建详情页**
   - 在Actions页面点击具体的工作流运行

2. **查看构建摘要**
   - 页面底部显示构建结果摘要
   - 包含文件大小和下载链接

3. **下载APK**
   - 滚动到 "Artifacts" 部分
   - 点击 "wordmaster-apk-{提交哈希}" 下载链接
   - 解压下载的zip文件获取APK

### 构建产物
- **APK文件**: `bin/wordmaster-debug.apk`
- **构建日志**: 包含详细的构建过程日志
- **保留时间**: 
  - APK文件: 30天
  - 构建日志: 7天

## 🔍 故障排除

### 常见构建错误

#### 1. 依赖安装失败
**错误**: `ERROR: Could not install packages due to an OSError`
**解决方案**: 
- 检查requirements.txt中的包名和版本
- 确认网络连接和镜像源配置

#### 2. Android SDK问题
**错误**: `ANDROID_HOME not found` 或SDK工具缺失
**解决方案**:
- 工作流会自动安装SDK，通常不需要手动干预
- 检查构建日志中的SDK安装步骤

#### 3. 内存不足
**错误**: `MemoryError` 或构建进程被杀死
**解决方案**:
- 构建过程需要较多内存，建议等待
- 如果频繁出现，考虑优化requirements

#### 4. 编译超时
**错误**: 构建超过120分钟超时
**解决方案**:
- 检查代码是否有语法错误
- 优化Python依赖，减少不必要的包

### 构建日志分析
1. **查看详细日志**
   - 点击构建步骤查看具体错误
   - 重点关注红色❌标记的步骤

2. **关键检查点**
   - Python环境设置
   - Android SDK安装
   - Buildozer构建过程
   - APK文件生成

## 📊 性能优化

### 构建速度优化
1. **缓存机制**: 
   - pip包缓存
   - Python环境缓存
   
2. **镜像源配置**:
   - 使用清华大学镜像源
   - GitHub镜像源加速

3. **并行构建**:
   - 支持矩阵构建
   - 多个Python版本同时测试

### APK大小优化
1. **移除不必要的依赖**
2. **优化资源文件**
3. **使用ProGuard压缩** (release版本)

## 🔒 安全注意事项

### 敏感信息
- 工作流不包含任何密钥或密码
- 所有敏感操作通过GitHub Secrets处理

### 代码安全
- 只在main/master分支自动构建
- 支持拉取请求检查
- 详细的构建日志记录

## 📞 获取帮助

### 遇到问题？
1. **查看构建日志**了解具体错误
2. **检查项目配置文件**确认设置正确
3. **参考故障排除部分**找到解决方案
4. **联系开发者**获取进一步支持

### 持续改进
- 根据构建结果优化配置
- 定期更新构建工具版本
- 收集用户反馈改进工作流

---
**最后更新**: 2025-12-31  
**工作流版本**: v2.0  
**维护者**: WordMaster开发团队