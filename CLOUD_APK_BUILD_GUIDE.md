# WordMaster 云上构建APK使用指南

## 🚀 概述

您的WordMaster应用现在已经配置了完整的GitHub Actions云端构建流程，可以自动将Python/Kivy项目构建为Android APK文件。

## ✅ 当前状态

- ✅ GitHub Actions工作流已部署到云端
- ✅ 工作流文件：`.github/workflows/build-android.yml`
- ✅ 支持手动触发和自动触发
- ✅ 支持多种Python版本 (3.9-3.12)
- ✅ 支持调试和发布版本构建

## 🎯 如何使用云上构建

### 方法1: 自动触发构建（推荐）

当您向GitHub仓库推送代码时，GitHub Actions会自动开始构建APK：

1. 修改您的项目代码
2. 提交并推送更改：
   ```bash
   git add .
   git commit -m "更新应用功能"
   git push origin main
   ```
3. 访问您的GitHub仓库查看构建进度

### 方法2: 手动触发构建

1. 打开您的GitHub仓库：https://github.com/wangzhou88/wordmaster
2. 点击 **Actions** 标签页
3. 选择 **Build WordMaster APK** 工作流
4. 点击 **Run workflow** 按钮
5. 配置构建参数：
   - **Build type**: 选择 `debug`（调试版本）或 `release`（发布版本）
   - **Python version**: 选择Python版本（推荐3.11）
6. 点击 **Run workflow** 开始构建

## 📱 获取APK文件

构建完成后，您可以从以下位置下载APK：

1. 在GitHub仓库的 **Actions** 标签页中
2. 点击对应的构建运行
3. 在页面底部找到 **Artifacts** 部分
4. 下载 `wordmaster-apk-[commit-hash].zip` 文件
5. 解压后即可获得APK文件

## 🔧 工作流特性

### 触发条件
- **自动触发**: 推送到main/master分支
- **手动触发**: workflow_dispatch事件
- **PR触发**: 提交Pull Request时

### 构建环境
- **操作系统**: Ubuntu Latest
- **Python版本**: 3.11 (可配置)
- **超时时间**: 120分钟
- **Android SDK**: 自动安装和配置

### 构建步骤
1. 代码检出 (Checkout)
2. Python环境设置
3. 系统依赖安装
4. 构建工具安装 (buildozer, python-for-android)
5. Android SDK安装和配置
6. APK构建
7. 产物上传

## 📊 构建监控

### 查看构建状态
1. GitHub仓库 → Actions标签页
2. 查看所有工作流运行历史
3. 点击具体的运行查看详细日志

### 构建日志
- 完整的构建日志会在Actions页面显示
- 包括所有安装步骤和构建过程
- 错误信息会详细显示便于排查问题

### 构建摘要
构建完成后会生成摘要，包括：
- 提交哈希值
- 分支信息
- Python版本
- 构建时间
- APK文件大小（如果构建成功）

## 🛠️ 故障排除

### 常见问题

**1. 构建失败**
- 检查构建日志中的错误信息
- 确保所有依赖在requirements.txt中正确列出
- 检查buildozer.spec配置

**2. 网络连接问题**
- 工作流已配置国内镜像源
- 自动重试机制已启用
- 如仍有问题，可能是临时网络问题

**3. 依赖安装失败**
- 检查requirements.txt语法
- 确保所有依赖版本兼容
- 查看具体的依赖安装日志

### 联系支持
如果遇到问题，请：
1. 查看Actions页面的详细构建日志
2. 检查GitHub Issues
3. 在项目页面提交新的Issue

## 🎉 下一步

1. **测试APK**: 下载并测试生成的APK文件
2. **优化配置**: 根据需要调整buildozer.spec
3. **自动化发布**: 考虑配置自动发布到应用商店
4. **持续集成**: 设置代码质量检查和自动化测试

---

**注意**: 首次构建可能需要较长时间（10-30分钟），因为需要下载和配置所有依赖。后续构建会更快。

**更新日期**: 2026-01-01  
**版本**: 1.0