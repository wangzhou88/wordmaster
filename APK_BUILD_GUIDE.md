# 📱 WordMaster APK 构建指南

## 🚀 推荐方案：GitHub Actions 云端构建

这是最稳定可靠的方案，无需复杂的本地环境配置。

### 步骤 1：创建 GitHub 仓库

1. 访问 [GitHub](https://github.com/new) 创建新仓库
2. 仓库名称：`wordmaster`
3. 设置为 **Public**（公开仓库）
4. 不要初始化 README（我们已有）

### 步骤 2：推送代码到 GitHub

```bash
# 初始化 Git 仓库（如果还未初始化）
git init
git add .
git commit -m "WordMaster - 准备APK构建"

# 添加远程仓库（替换为你的GitHub仓库URL）
git remote add origin https://github.com/你的用户名/wordmaster.git

# 推送代码
git push -u origin main
```

### 步骤 3：启用 GitHub Actions

1. 进入 GitHub 仓库的 **Actions** 页面
2. 找到 "Build Android APK" 工作流
3. 点击 **Enable** 启用工作流

### 步骤 4：手动触发构建

1. 在 Actions 页面点击 **Run workflow**
2. 选择分支 `main`
3. 点击绿色 **Run workflow** 按钮

### 步骤 5：下载 APK

构建完成后（约 10-15 分钟）：
1. 进入 Actions 页面
2. 点击最新的构建任务
3. 在 Artifacts 部分下载 `wordmaster-debug.apk`

---

## 🛠️ 备选方案：本地 Buildozer 构建

⚠️ **注意**：本地构建需要配置 Android SDK/NDK，环境复杂且可能遇到各种问题。

### 环境准备

```bash
# 安装 Java 8+
# 下载并安装 Android Studio
# 配置 ANDROID_HOME 环境变量
```

### 本地构建命令

```bash
# 清理之前的构建
buildozer clean

# 构建 APK
buildozer android debug

# 如果需要发布版本
buildozer android release
```

构建后的 APK 位置：`bin/wordmaster-1.0-armeabi-v7a-debug.apk`

---

## 📋 构建配置确认

### Buildozer 配置
- ✅ 应用名称：WordMaster英语学习助手
- ✅ 包名：org.wordmaster.wordmaster
- ✅ 版本：1.0
- ✅ 权限：INTERNET, STORAGE, AUDIO
- ✅ 图标：已配置自适应图标

### 依赖库
- ✅ Kivy 2.2.1
- ✅ KivyMD 1.1.1
- ✅ gTTS (文本转语音)
- ✅ SpeechRecognition (语音识别)
- ✅ PyDub (音频处理)
- ✅ Matplotlib, NumPy, Pandas

### 资源文件
- ✅ 图标文件：data/icon_bg.png, data/icon_fg.png
- ✅ 数据库：wordmaster.db
- ✅ 音频文件：data/audio/

---

## 🔧 故障排除

### 常见问题

1. **构建失败**
   - 检查网络连接
   - 确保 GitHub Actions 已启用
   - 查看构建日志定位具体错误

2. **权限问题**
   - 确保仓库设置为 Public
   - 检查 GitHub Actions 权限设置

3. **依赖冲突**
   - 检查 requirements.txt 和 buildozer.spec 的一致性
   - 清理缓存后重新构建

### 构建日志位置
- **GitHub Actions**: 在 Actions 页面查看详细日志
- **本地构建**: 查看控制台输出和 `.buildozer` 目录

---

## 📱 安装 APK

1. 下载 APK 文件到手机
2. 在手机设置中允许"未知来源"安装
3. 安装 APK 文件
4. 首次启动可能需要授予权限

---

## 🎯 下一步

APK 构建成功后，您可以：
1. 在 Android 设备上测试应用功能
2. 分享 APK 给其他用户
3. 发布到应用商店（如需要）
4. 继续优化应用功能

---

**构建完成后，请告诉我结果，我将为您提供进一步的支持！**