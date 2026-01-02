# 使用GitHub Actions构建WordMaster APK指南

## 概述

由于python-for-android依赖的`sh`包不支持Windows系统，我们无法直接在Windows环境中构建APK。解决方案是使用GitHub Actions在Linux环境中构建APK，然后下载到本地。

## 步骤指南

### 1. 推送代码到GitHub

首先，确保您的代码已提交并推送到GitHub仓库：

```bash
git add .
git commit -m "准备构建APK"
git push origin main
```

### 2. 访问GitHub Actions

1. 在浏览器中访问您的GitHub仓库
2. 点击顶部的"Actions"标签页
3. 您会看到可用的工作流，包括"📱 WordMaster APK构建"

### 3. 手动触发工作流

有几种方式可以触发工作流：

#### 方法1：使用workflow_dispatch事件

GitHub Actions工作流已配置为支持手动触发：

1. 进入"📱 WordMaster APK构建"工作流页面
2. 点击右侧的"Run workflow"按钮
3. 在下拉菜单中选择构建类型（debug或release）
4. 点击绿色的"Run workflow"按钮

#### 方法2：通过推送代码自动触发

工作流配置为在推送到main或master分支时自动运行，只需推送代码即可触发。

### 4. 监控工作流运行

1. 点击正在运行的工作流
2. 您可以看到每个步骤的进度
3. 点击每个步骤可以查看详细日志

工作流将执行以下步骤：
- 📥 检出代码
- 🐍 设置Python环境
- 📦 安装系统依赖
- 🔧 安装构建工具
- 🌐 配置网络和Git
- 📱 安装Android SDK
- 🔍 检查构建环境
- 🚀 构建APK
- 📊 检查构建结果
- 📦 上传APK产物
- 📋 上传构建日志
- 📝 构建摘要

### 5. 下载生成的APK

工作流成功完成后：

1. 进入已完成的工作流运行页面
2. 滚动到页面底部，找到"Artifacts"区域
3. 点击"wordmaster-apk-{commit-hash}-{build-type}"下载APK文件
4. 解压下载的压缩文件，您将获得APK文件

## 工作流配置分析

项目中的工作流配置文件为`.github/workflows/build-android.yml`，主要包含：

1. **环境设置**：Ubuntu-22.04运行器，Python 3.11
2. **Android配置**：Android API 31，ARM64架构
3. **构建工具**：python-for-android和buildozer
4. **构建流程**：清理、构建、检查、上传产物

## 常见问题解决

### 1. 构建失败怎么办？

如果构建失败，您可以：

1. 查看工作流的日志输出，定位错误原因
2. 检查buildozer.spec配置文件是否正确
3. 确保项目依赖完整
4. 查看.buildozer目录中的详细日志

### 2. 下载的APK无法安装？

如果下载的APK无法安装，可能是因为：

1. APK是为调试模式构建的，需要在Android设备上启用"未知来源"选项
2. 需要在Android设备上安装兼容的架构版本（ARM64或ARMv7）

### 3. 想自动触发构建？

您可以通过以下方式自动触发构建：

1. 每次推送代码到main分支时自动触发
2. 设置定期构建（例如每周一次）
3. 在特定标签推送时触发

## 总结

通过使用GitHub Actions，我们可以在Linux环境中成功构建WordMaster APK，而不受Windows系统兼容性的限制。虽然无法在本地Windows环境中直接构建APK，但通过GitHub Actions，我们可以轻松地构建APK并下载到本地进行测试。