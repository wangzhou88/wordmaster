# 🚀 Git 代码推送完整命令

## 在项目文件夹中依次运行以下命令：

### 1. 进入项目目录
```bash
cd c:\Users\admin\Downloads\wordmaster
```

### 2. 初始化Git仓库（如果还没有初始化）
```bash
git init
```

### 3. 添加所有文件到Git
```bash
git add .
```

### 4. 提交文件到本地仓库
```bash
git commit -m "WordMaster英语学习助手 - 准备APK构建"
```

### 5. 设置主分支为main
```bash
git branch -M main
```

### 6. 添加远程GitHub仓库
```bash
git remote add origin https://github.com/wzixb0/wordmaster.git
```

### 7. 推送到GitHub（首次推送）
```bash
git push -u origin main
```

---

## 🎯 完整复制粘贴版本：

如果您想一次性复制所有命令：

```bash
cd c:\Users\admin\Downloads\wordmaster && git init && git add . && git commit -m "WordMaster英语学习助手 - 准备APK构建" && git branch -M main && git remote add origin https://github.com/wzixb0/wordmaster.git && git push -u origin main
```

---

## 🔐 GitHub凭据输入：

推送过程中可能会要求输入GitHub凭据：

### 用户名：
```
wzixb0
```

### 密码：
- 如果您没有启用双重认证：使用您的GitHub密码
- 如果启用了双重认证：使用个人访问令牌（Personal Access Token）

## 📝 如果遇到提示：

### 首次使用Git可能会提示：
- **用户配置确认**：输入 "yes"
- **编辑提交信息**：按 `ESC` 然后输入 `:wq` 保存

---

## ✅ 成功标志：

推送成功后，您应该能看到：
- 类似这样的消息：
  ```
  Enumerating objects: X, done.
  Counting objects: 100% (X/X), done.
  Delta compression using up to X threads
  Compressing objects: 100% (X/X), done.
  Writing objects: 100% (X/X), X.XX MiB | X.XX MiB/s, done.
  Total X (delta X), reused 0 (delta 0), pack-reused 0
  To https://github.com/wzixb0/wordmaster.git
   * [new branch]      main -> main
  Branch 'main' set up to track remote branch 'main' from 'origin'.
  ```

## 🚨 常见错误和解决方案：

### 错误1：fatal: could not read Username
**解决方案：** 确保GitHub用户名和密码正确输入

### 错误2：fatal: repository not found
**解决方案：** 检查仓库URL是否正确，确保仓库确实存在于GitHub上

### 错误3：Permission denied
**解决方案：** 检查GitHub账户权限，确保您有推送权限

---

## 📞 下一步：

推送成功后，请告诉我：
- ✅ **"代码推送成功"** - 当代码成功推送到GitHub时

然后我们就可以开始APK构建了！🎯