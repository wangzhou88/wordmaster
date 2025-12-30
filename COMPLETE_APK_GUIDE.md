# 🎯 WordMaster APK 构建完整指南

## 📋 任务清单
- [ ] 1. 创建GitHub仓库
- [ ] 2. 推送代码到GitHub
- [ ] 3. 修改应用配置（如需要）

---

## 🟢 方案A：自动化脚本（推荐）

### 步骤1：创建GitHub仓库
1. 访问 https://github.com/new
2. 填写仓库信息：
   ```
   Repository name: wordmaster
   Description: WordMaster英语学习助手
   Public ☑️ (必须)
   ```
3. 点击 "Create repository"

### 步骤2：运行推送脚本
1. 双击运行 `GIT_PUSH_SCRIPT.bat`
2. 输入您的GitHub用户名
3. 等待推送完成

### 步骤3：启用Actions并构建
1. 访问您的GitHub仓库
2. 进入 Actions 页面
3. 启用 "Build Android APK" 工作流
4. 点击 "Run workflow"

---

## 🔧 方案B：手动操作

### 1. 创建GitHub仓库
访问 https://github.com/new
```
仓库名：wordmaster
描述：WordMaster英语学习助手 - AI智能英语学习应用
Public ☑️
```

### 2. 推送代码命令
```bash
# 初始化并推送
git init
git add .
git commit -m "WordMaster - 准备APK构建"
git remote add origin https://github.com/您的用户名/wordmaster.git
git branch -M main
git push -u origin main
```

### 3. 配置修改选项

#### 应用名称修改
编辑 `buildozer.spec` 第5行：
```ini
title = WordMaster英语学习助手  # 修改为您喜欢的名称
```

#### 版本号修改
编辑 `buildozer.spec` 第32行：
```ini
version = 1.0  # 修改版本号
```

#### 包名修改
编辑 `buildozer.spec` 第9-11行：
```ini
package.name = wordmaster  # 应用名称
package.domain = org.wordmaster  # 包域名
```

#### 权限修改
编辑 `buildozer.spec` 权限部分：
```ini
android.permissions = android.permission.INTERNET, android.permission.WRITE_EXTERNAL_STORAGE
```

---

## 🚀 快速启动指南

### 立即开始：
1. 📝 创建GitHub仓库 (5分钟)
2. 🔧 运行推送脚本 (2分钟)
3. ⚡ 启动APK构建 (15分钟)
4. 📱 下载并安装APK

### 遇到问题？
- 查看构建日志
- 检查网络连接
- 确认仓库设置为Public

---

## 📱 构建完成后

1. **下载APK**: Actions页面 → 最新构建 → Artifacts
2. **安装到手机**: 允许未知来源 → 安装APK
3. **测试功能**: 打开应用检查各项功能

---

**需要立即开始吗？请告诉我您的GitHub用户名！**