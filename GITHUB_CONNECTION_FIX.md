# 🛠️ GitHub连接重置问题解决方案

## 🚨 错误信息
```
fatal: unable to access 'https://github.com/wangzhou88/wordmaster.git/': Recv failure: Connection was reset
```

这是一个网络连接问题，表明您的计算机无法建立到GitHub服务器的连接。

## 📋 解决方案

### 方案1：检查网络连接

1. **测试基本网络连接**
   ```cmd
   ping github.com
   ```
   - 如果没有响应，说明网络连接有问题
   - 如果有响应，继续下一步

2. **测试GitHub HTTPS访问**
   ```cmd
   curl -v https://github.com
   ```
   - 如果连接失败，说明网络或防火墙阻止了HTTPS连接

### 方案2：使用SSH协议替代HTTPS

1. **检查是否已有SSH密钥**
   ```cmd
   dir %userprofile%\.ssh
   ```
   - 如果有id_rsa和id_rsa.pub文件，跳过步骤2

2. **生成SSH密钥**
   ```cmd
   ssh-keygen -t rsa -b 4096 -C "wangzhou88@users.noreply.github.com"
   ```
   - 按Enter键接受默认位置
   - 可以选择设置密码（推荐）

3. **查看SSH公钥**
   ```cmd
   type %userprofile%\.ssh\id_rsa.pub
   ```
   - 复制输出的全部内容

4. **添加SSH密钥到GitHub**
   - 访问：https://github.com/settings/keys
   - 点击"New SSH key"
   - 粘贴SSH公钥
   - 点击"Add SSH key"

5. **使用SSH URL进行推送**
   ```cmd
   cd c:\Users\admin\Downloads\wordmaster
   git remote set-url origin git@github.com:wangzhou88/wordmaster.git
   git push -u origin main
   ```

### 方案3：检查防火墙和代理设置

1. **临时关闭防火墙测试**
   - 打开"Windows安全中心" → "防火墙和网络保护" → "关闭防火墙"
   - 测试Git推送
   - 测试完成后重新开启防火墙

2. **检查代理设置**
   ```cmd
   git config --global --get http.proxy
   git config --global --get https.proxy
   ```
   - 如果有代理设置，可以尝试移除
   ```cmd
   git config --global --unset http.proxy
   git config --global --unset https.proxy
   ```

3. **设置HTTP代理（如果需要）**
   ```cmd
   git config --global http.proxy http://代理服务器:端口
   git config --global https.proxy https://代理服务器:端口
   ```

### 方案4：使用GitHub Desktop

1. **下载GitHub Desktop**
   - 访问：https://desktop.github.com/download/
   - 安装并启动

2. **克隆或创建仓库**
   - 点击"Clone a repository"
   - 选择wordmaster仓库
   - 设置本地路径：`C:\Users\admin\Downloads\wordmaster`
   - 点击"Clone"

3. **提交和推送**
   - 将项目文件复制到克隆的文件夹
   - 在GitHub Desktop中提交更改
   - 点击"Push origin"

### 方案5：使用国内GitHub镜像

1. **使用GitHub镜像**
   ```cmd
   git clone https://github.com.cnpmjs.org/wangzhou88/wordmaster.git
   ```

### 方案6：手动上传文件

1. **创建GitHub仓库**
   - 访问：https://github.com/new
   - 仓库名：wordmaster
   - 点击"Create repository"

2. **手动上传文件**
   - 进入仓库页面
   - 点击"Add file" → "Upload files"
   - 选择项目文件进行上传
   - 点击"Commit changes"

## 💡 常见问题

### 1. 为什么会出现连接重置？
   - 网络不稳定
   - 防火墙或安全软件阻止
   - GitHub服务器暂时不可用
   - 代理设置问题

### 2. SSH连接提示"Permission denied"？
   - 确保SSH密钥已正确添加到GitHub
   - 确保使用了正确的GitHub用户名
   - 检查SSH代理设置

### 3. 如何测试GitHub是否可访问？
   ```cmd
   ping github.com
   telnet github.com 443
   ```

## 📝 成功标志

当您能够成功执行以下命令时，说明连接问题已解决：
```cmd
git clone https://github.com/wangzhou88/wordmaster.git
git push -u origin main
```

## 🎯 下一步

1. **尝试上述解决方案**
2. **成功连接后**：运行 `SIMPLE_GIT_PUSH.bat` 推送代码
3. **启动构建**：访问 https://github.com/wangzhou88/wordmaster/actions 开始构建

如果所有方案都失败，建议：
- 更换网络环境（如使用手机热点）
- 等待一段时间后重试
- 联系网络管理员检查网络设置

祝您成功解决GitHub连接问题！