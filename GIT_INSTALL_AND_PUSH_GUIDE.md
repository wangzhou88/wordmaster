# 🚀 Git安装与GitHub推送完整指南

## 🔧 情况分析

目前系统中**未安装Git**，需要先完成Git安装，然后才能将本地文件推送到GitHub仓库。

## 📋 执行计划

### 第1步：下载并安装Git

1. **访问Git官方下载页面**：
   - 链接：https://git-scm.com/download/win
   - 下载会自动开始，文件名类似：`Git-2.52.0.1-64-bit.exe`

2. **运行安装程序**，按照以下推荐设置选择：
   - ✅ 组件选择：全部勾选
   - ✅ 默认编辑器：选择VS Code（如果已安装）或Vim
   - ✅ PATH环境：选择"Git from the command line and also from 3rd-party software"
   - ✅ HTTPS传输：使用OpenSSL库
   - ✅ 换行符处理：Checkout Windows-style, commit Unix-style
   - ✅ 终端模拟器：使用Windows默认控制台
   - ✅ 额外选项：启用文件系统缓存和Git Credential Manager

3. **完成安装**，点击"Finish"

### 第2步：验证Git安装

1. **打开命令提示符**（按下Win+R，输入cmd，回车）
2. **运行验证命令**：
   ```bash
   git --version
   ```
3. **预期输出**：显示Git版本号，如：`git version 2.52.0.windows.1`

### 第3步：配置Git身份

1. **在命令提示符中运行**：
   ```bash
   git config --global user.name "wangzhou88"
git config --global user.email "wangzhou88@users.noreply.github.com"
   ```

2. **验证配置**：
   ```bash
   git config --list
   ```
   应该显示您刚才配置的用户名和邮箱

### 第4步：推送代码到GitHub

#### 方案A：使用批处理脚本（推荐）

1. **找到并运行脚本**：
   - 在文件资源管理器中打开项目文件夹：`c:\Users\admin\Downloads\wordmaster`
   - 双击运行：`GIT_PUSH_SCRIPT.bat`
   - 按照提示输入GitHub用户名：`wangzhou88`

2. **脚本会自动执行**：
   - 初始化Git仓库
   - 添加所有文件
   - 提交文件
   - 添加远程仓库
   - 推送代码到GitHub

#### 方案B：手动执行命令

1. **打开命令提示符**，进入项目目录：
   ```bash
   cd c:\Users\admin\Downloads\wordmaster
   ```

2. **初始化Git仓库**：
   ```bash
   git init
   ```

3. **添加所有文件**：
   ```bash
   git add .
   ```

4. **提交文件**：
   ```bash
   git commit -m "WordMaster - 准备APK构建"
   ```

5. **设置主分支**：
   ```bash
   git branch -M main
   ```

6. **添加远程仓库**：
   ```bash
   git remote add origin https://github.com/wangzhou88/wordmaster.git
   ```

7. **推送到GitHub**：
   ```bash
   git push -u origin main
   ```

### 第5步：验证推送结果

1. **访问GitHub仓库**：
   - 打开浏览器，访问：https://github.com/wangzhou88/wordmaster
   - 检查是否能看到您的代码文件

2. **启动GitHub Actions构建**：
   - 进入仓库的"Actions"页面
   - 找到"Build Android APK"工作流
   - 点击"Run workflow"开始构建

## 🚨 常见问题解决方案

### 问题1：Git命令未找到
- **原因**：Git未安装或PATH环境变量未配置
- **解决**：重新安装Git，确保选择正确的PATH选项

### 问题2：Authentication failed
- **原因**：GitHub用户名或密码错误
- **解决**：
  - 如果启用了双重认证，需要使用**个人访问令牌**作为密码
  - 生成令牌：https://github.com/settings/tokens
  - 权限：勾选"repo"权限

### 问题3：Repository not found
- **原因**：GitHub仓库不存在或URL错误
- **解决**：
  - 确保已在GitHub上创建仓库
  - 仓库名称：wordmaster
  - 检查远程URL是否正确

### 问题4：推送被拒绝
- **原因**：远程仓库有本地没有的提交
- **解决**：
  ```bash
  git pull origin main --rebase
  git push origin main
  ```

## 📱 成功后的下一步

1. **启动GitHub Actions构建**：
   - 访问：https://github.com/wangzhou88/wordmaster/actions
   - 点击"Run workflow"
   - 等待10-15分钟

2. **下载生成的APK**：
   - 构建完成后，在Artifacts部分下载`wordmaster-debug.apk`
   - 将APK安装到Android设备进行测试

3. **持续开发**：
   - 修改代码后，使用`git add . && git commit -m "描述" && git push`推送更新
   - GitHub Actions会自动触发新的构建

## 💡 提示

- **保持Git客户端更新**：定期更新Git版本，获得更好的性能和安全性
- **使用.gitignore文件**：忽略不必要的文件（如IDE配置、日志文件等）
- **定期提交**：频繁提交代码，避免丢失工作
- **使用分支**：为新功能创建独立分支，合并前进行代码评审

## 📞 遇到问题？

如果在执行过程中遇到任何问题，请提供以下信息，我将为您提供进一步帮助：
1. 遇到的具体错误信息
2. 执行到哪一步出现问题
3. 错误截图（如果有）

祝您Git安装和GitHub推送顺利！🚀