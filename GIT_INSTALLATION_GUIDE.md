# 🔧 Git 安装和配置完整指南

## 📥 第1步：下载Git

**官方下载链接：** https://git-scm.com/download/win

1. 访问上述链接
2. 下载会自动开始（如果没开始，手动点击下载）
3. 文件名类似：`Git-2.52.0.1-64-bit.exe`

## 📋 第2步：安装Git

### 安装选项（推荐设置）：

**组件选择：**
- ☑️ Git Bash Here
- ☑️ Git GUI Here
- ☑️ Git LFS (Large File Support)
- ☑️ Git Credential Manager
- ☑️ Git Bash and Git GUI
- ☑️ Git LFS (Large File Support)

**默认编辑器：**
- 选择 "Use Visual Studio Code as Git's default editor"（如果您安装了VS Code）
- 或者保持默认 "Use Vim"

**PATH environment：**
- 选择 "Git from the command line and also from 3rd-party software"

**HTTPS transport backend：**
- 选择 "Use the OpenSSL library"

**Line ending conversions：**
- 选择 "Checkout Windows-style, commit Unix-style line endings"

**Terminal emulator：**
- 选择 "Use Windows' default console window"

**Extra options：**
- ☑️ Enable file system caching
- ☑️ Enable Git Credential Manager

### 安装过程：
1. 运行下载的安装程序
2. 按照上述设置点击"Next"
3. 点击"Install"
4. 等待安装完成
5. 点击"Finish"

## 🔐 第3步：配置Git（重要！）

### 配置Git身份信息：

打开**命令提示符**（cmd）或**PowerShell**，运行：

```bash
git config --global user.name "wzixb0"
git config --global user.email "wzixb0@users.noreply.github.com"
```

### 验证安装：

```bash
git --version
```

应该显示类似：`git version 2.52.0.windows.1`

## 🔗 第4步：创建GitHub仓库

### 在GitHub网页创建：
1. 访问：https://github.com/new
2. 填写信息：
   ```
   Repository name: wordmaster
   Description: WordMaster英语学习助手 - AI智能英语学习应用
   Public ☑️
   ❌ 不要勾选 "Add a README file"
   ❌ 不要勾选 "Add .gitignore"
   ❌ 不要选择 License
   ```
3. 点击 "Create repository"

### 记录仓库URL：
创建成功后，页面会显示仓库URL：
`https://github.com/wzixb0/wordmaster.git`

## 📤 第5步：推送代码到GitHub

### 在项目文件夹中运行：

```bash
# 1. 进入项目目录
cd c:\Users\admin\Downloads\wordmaster

# 2. 初始化Git仓库
git init

# 3. 添加所有文件
git add .

# 4. 提交文件
git commit -m "WordMaster英语学习助手 - 准备APK构建"

# 5. 设置主分支
git branch -M main

# 6. 添加远程仓库
git remote add origin https://github.com/wzixb0/wordmaster.git

# 7. 推送到GitHub
git push -u origin main
```

### 输入GitHub凭据：
推送时可能会要求输入GitHub用户名和密码：
- **用户名：** wzixb0
- **密码：** 您的GitHub密码（如果启用了双重认证，需要使用个人访问令牌）

## ✅ 验证成功：

推送成功后，您应该能够：
1. 在 https://github.com/wzixb0/wordmaster 看到您的代码
2. 所有文件都已上传到GitHub

## 🚨 如果遇到错误：

### 常见错误和解决方案：

**错误1：Authentication failed**
```
解决方案：确保GitHub用户名和密码正确
如果启用了2FA，需要使用个人访问令牌作为密码
```

**错误2：Repository not found**
```
解决方案：检查仓库URL是否正确
确保仓库确实存在于GitHub上
```

**错误3：Permission denied**
```
解决方案：检查GitHub权限
确保您在wzixb0账户下有权限推送
```

---

## 📞 下一步：

完成Git安装和代码推送后，请告诉我：
- ✅ "Git安装完成" - 当Git安装完成时
- ✅ "代码推送成功" - 当代码成功推送到GitHub时
- ❓ "遇到错误" - 如果遇到任何问题

**然后我们就可以开始APK构建了！** 🚀