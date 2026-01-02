# WordMaster APK构建指南

## 问题与解决方案

在尝试在Windows环境中构建WordMaster APK时，我们遇到了一个关键问题：**python-for-android依赖的`sh`包不支持Windows系统**。这导致buildozer无法识别Android目标，从而无法构建APK。

我们找到了两个解决方案：

1. **使用GitHub Actions在Linux环境中构建APK**：这是我们采用的方案，因为项目中已经配置了相关工作流。
2. **使用WSL或Docker创建Linux环境**：虽然可行，但相比直接使用GitHub Actions更为复杂。

## 使用GitHub Actions构建APK

由于项目已经配置了GitHub Actions工作流文件，我们可以直接使用它来构建APK。

### 步骤1：推送代码到GitHub仓库

确保你的代码已经提交并推送到GitHub仓库。

### 步骤2：使用GitHub Actions工作流

有几种方式可以触发工作流：

1. **自动触发**：当你推送到main或master分支时，工作流会自动运行。
2. **手动触发**：在GitHub仓库的"Actions"标签页中，选择"📱 WordMaster APK构建"工作流，然后点击"Run workflow"按钮。

### 步骤3：监控工作流运行

在工作流运行期间，你可以实时查看日志输出：

1. 进入GitHub仓库的"Actions"标签页
2. 点击正在运行的工作流
3. 点击每个步骤查看详细日志

### 步骤4：下载生成的APK

工作流成功完成后，APK文件将作为GitHub Actions的产物（Artifacts）上传：

1. 进入已完成的工作流运行
2. 滚动到页面底部，找到"Artifacts"区域
3. 点击"wordmaster-apk-{commit-hash}-{build-type}"下载APK文件

## 工作流配置分析

项目中的GitHub Actions工作流文件（`.github/workflows/build-android.yml`）包含以下关键配置：

```yaml
jobs:
  build-apk:
    name: 构建APK文件
    runs-on: ubuntu-22.04
    timeout-minutes: 180
    
    env:
      PYTHON_VERSION: '3.11'
      ANDROID_API: '31'
      ANDROID_ARCH: 'arm64-v8a'
    
    steps:
    # ... 各种步骤
```

工作流主要执行以下步骤：

1. **环境设置**：
   - 检出代码
   - 设置Python环境
   - 安装系统依赖和构建工具

2. **Android SDK配置**：
   - 下载并配置Android命令行工具
   - 安装Android SDK组件
   - 设置环境变量

3. **构建APK**：
   - 清理之前的构建
   - 运行buildozer构建命令

4. **上传产物**：
   - 上传APK文件
   - 上传构建日志

## 在本地构建APK的替代方案

如果你仍然希望尝试在本地构建APK，可以考虑以下选项：

1. **使用WSL**：在Windows子系统Linux中设置构建环境
2. **使用Docker**：创建一个Linux容器环境
3. **使用虚拟化**：在虚拟机中安装Linux并设置构建环境

这些方案都需要额外的设置和配置，但可以实现本地构建。

## 总结

虽然我们无法在Windows环境中直接构建APK，但GitHub Actions提供了一个可靠的替代方案。通过使用项目中的工作流配置，我们可以轻松地在Linux环境中构建APK并下载到本地进行测试。