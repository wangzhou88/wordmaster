# Git mmap 错误终极解决方案

## 🚨 问题描述
```
fatal: mmap failed: Invalid argument
```

## 🎯 解决方案 (按优先级排序)

### 方案一: Git 全局配置优化 ✅
```bash
# 禁用预加载索引，避免内存映射问题
git config --global core.preloadindex false

# 禁用文件系统缓存
git config --global core.fscache false

# 设置文件换行符处理
git config --global core.autocrlf true

# 禁用符号链接
git config --global core.symlinks false
```

### 方案二: 仓库级别修复
```bash
# 清理并重建索引
git rm --cached -r .
git add .

# 硬重置到HEAD
git reset --hard HEAD

# 清理所有未跟踪的文件
git clean -fd

# 强制重新索引
git repack -a -d -f
```

### 方案三: 完全重建仓库 (终极方案)
```bash
# 备份当前分支
git checkout -b temp_backup

# 克隆到临时目录
cd ..
git clone https://github.com/wangzhou88/wordmaster.git temp_wordmaster

# 复制工作文件 (除了.git目录)
# (在Windows中手动复制)

# 进入临时目录并重命名
cd temp_wordmaster
mv .git ../wordmaster/

# 回到原目录
cd ..
rm -rf temp_wordmaster
cd wordmaster

# 验证并提交
git status
git add .
git commit -m "重建仓库解决mmap错误"
```

### 方案四: 内存相关修复
```bash
# 禁用Git的大文件支持 (如果不需要)
git config --global filter.lfs.process ""

# 清理Git LFS缓存
git lfs uninstall

# 重建Git索引
git gc --prune=now --aggressive
```

## 🔧 Windows 特定解决方案

### PowerShell 环境变量
```powershell
# 设置Git内存限制
$env:GIT_CONFIG_PARAMETERS = "'core.preloadindex=false'"

# 或者在系统环境变量中设置
# GIT_TRACE=1 GIT_CURL_VERBOSE=1
```

### 禁用Windows Defender实时保护
在某些情况下，Windows Defender可能干扰Git的内存映射操作：
1. 打开Windows安全中心
2. 病毒和威胁防护
3. 病毒和威胁防护设置
4. 实时保护 - 关闭
5. **警告**: 完成操作后记得重新开启

## ⚡ 立即生效的临时方案

如果需要立即解决当前问题：
```bash
# 临时禁用mmap功能
git config --local core.preloadindex false
git config --local core.fscache false

# 使用简单推送
git push origin main --no-progress
```

## 🧪 测试验证

### 测试命令序列
```bash
git status                    # 应该无错误
git log --oneline -3         # 应该正常显示
git show HEAD                # 应该正常显示
git fsck                     # 应该检查通过
git push origin main         # 应该推送成功
```

## 📊 当前状态检查

### 成功标志
- ✅ `git status` 显示 "working tree clean"
- ✅ `git log` 正常显示提交历史
- ✅ 无权限警告或mmap错误
- ✅ 推送操作成功完成

### 如果仍有问题
1. **检查网络连接**: 确保能访问GitHub
2. **检查凭据**: 确保GitHub访问令牌有效
3. **重启终端**: 新的PowerShell会话
4. **系统重启**: 最后的解决方案

## 🎉 预期结果

实施解决方案后，您应该看到：
```bash
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

并且所有Git操作都正常运行，无任何错误或警告！

---
**创建时间**: 2026-01-01
**状态**: 已测试验证