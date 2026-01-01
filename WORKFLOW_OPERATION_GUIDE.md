# Build WordMaster APK 工作流操作指南

## 🎯 工作流已成功部署！

✅ **GitHub仓库**: https://github.com/wangzhou88/wordmaster  
✅ **工作流名称**: Build WordMaster APK  
✅ **文件位置**: `.github/workflows/build-android.yml`  
✅ **当前状态**: 已部署，等待触发  

## 🚀 如何手动触发构建

### 步骤1：访问GitHub Actions
1. 打开 https://github.com/wangzhou88/wordmaster
2. 点击顶部的 **"Actions"** 标签页
3. 您应该能看到 **"Build WordMaster APK"** 工作流

### 步骤2：手动触发构建
1. 点击 **"Build WordMaster APK"** 工作流名称
2. 在工作流详情页面，点击绿色的 **"Run workflow"** 按钮
3. 配置构建参数：
   ```
   Build type: debug (推荐用于测试)
   Python version: 3.11 (推荐版本)
   ```
4. 点击 **"Run workflow"** 开始构建

## 📊 监控构建进度

### 构建状态说明
- **🟡 黄色圆圈**: 排队等待中
- **🔵 蓝色圆圈**: 正在运行
- **🟢 绿色勾号**: 构建成功
- **🔴 红色叉号**: 构建失败

### 关键构建阶段
1. **Checkout code** - 检出代码 (1-2分钟)
2. **Set up Python** - 设置Python环境 (2-3分钟)
3. **Install system dependencies** - 安装系统依赖 (5-10分钟)
4. **Install build tools** - 安装构建工具 (10-15分钟)
5. **Install Android SDK** - 安装Android SDK (10-20分钟)
6. **Build APK** - 构建APK (30-60分钟) ⭐ 最重要阶段
7. **Upload artifacts** - 上传构建产物 (1-2分钟)

## 📱 获取APK文件

### 方法1：通过GitHub Actions页面
1. 构建完成后，在工作流详情页面底部
2. 找到 **"Artifacts"** 部分
3. 点击 **"wordmaster-apk-[提交哈希]"** 下载APK

### 方法2：直接下载链接
构建完成后，APK文件会上传到GitHub，您可以：
- 点击构建产物链接直接下载
- APK文件名格式：`wordmaster-debug.apk`

## 🔧 构建产物说明

### 成功构建后会生成：
- **APK文件**: `bin/wordmaster-debug.apk` (调试版本)
- **构建日志**: 详细的构建过程日志
- **系统信息**: 构建环境的详细信息

### APK文件特点：
- **大小**: 通常 20-50MB
- **类型**: debug版本（可安装到任何Android设备）
- **签名**: 开发签名（用于测试）

## 🛠️ 自动触发构建

### 推送到main/master分支时自动触发
```bash
# 修改代码后
git add .
git commit -m "更新应用功能"
git push origin main
```

### 触发条件
- ✅ 推送到 `main` 或 `master` 分支
- ✅ 创建Pull Request
- ✅ 手动触发 (workflow_dispatch)

## ⚠️ 故障排除

### 如果构建失败：

#### 1. 检查构建日志
- 点击失败的构建
- 查看每个步骤的详细日志
- 重点关注红色错误信息

#### 2. 常见问题
- **依赖安装失败**: 检查网络连接或尝试重新构建
- **Android SDK问题**: 等待几分钟让GitHub环境稳定
- **内存不足**: GitHub Actions有资源限制，可能需要优化

#### 3. 重新构建
- 点击失败的构建
- 点击右上角的 **"Re-run all jobs"** 按钮

### 如果工作流不显示：
1. 刷新GitHub页面
2. 清除浏览器缓存
3. 确认您有仓库的访问权限

## 📋 构建检查清单

### 构建前确认：
- [ ] 工作流文件已部署 (✅ 已确认)
- [ ] buildozer.spec配置正确
- [ ] requirements.txt包含所有依赖
- [ ] main.py是应用入口点

### 构建过程监控：
- [ ] 观察每个步骤的执行状态
- [ ] 特别关注"Build APK"阶段
- [ ] 检查是否有错误信息

### 构建完成后：
- [ ] 确认APK文件已生成
- [ ] 下载并测试APK文件
- [ ] 在Android设备上安装测试

## 🎯 下一步操作

1. **立即尝试**: 手动触发一次构建
2. **监控过程**: 观察整个构建流程
3. **获取APK**: 下载并测试生成的APK
4. **设置自动**: 推送到主分支测试自动触发

## 📞 技术支持

如果遇到问题：
1. 查看构建日志中的具体错误信息
2. 检查buildozer.spec配置
3. 确认所有依赖包都包含在requirements.txt中
4. 可以尝试重新运行构建

---

**当前Git提交**: 9d43824 (触发Build WordMaster APK工作流)  
**仓库地址**: https://github.com/wangzhou88/wordmaster  
**工作流文件**: `.github/workflows/build-android.yml`