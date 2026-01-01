# GitHub Actions工作流检查

## 🔍 如何找到"Build WordMaster APK"工作流

### 步骤1：访问GitHub仓库
```
https://github.com/wangzhou88/wordmaster
```

### 步骤2：点击Actions标签页
- 在仓库主页面顶部导航栏找到"Actions"（绿色图标）

### 步骤3：查找工作流
应该能看到：
- **工作流名称**: Build WordMaster APK
- **状态**: 最近运行时间
- **分支**: main分支

### 步骤4：手动触发构建
1. 点击"Build WordMaster APK"工作流
2. 点击"Run workflow"按钮
3. 选择参数：
   - Build type: `debug`
   - Python version: `3.11`
4. 点击"Run workflow"

## ✅ 工作流特征
- **文件名**: `.github/workflows/build-android.yml`
- **触发条件**: push到main/master分支，手动触发
- **支持参数**: build_type, python_version
- **构建环境**: Ubuntu Latest

## 🐛 如果找不到工作流

### 可能原因1：工作流未部署
检查工作流文件是否存在：
```
.github/workflows/build-android.yml
```

### 可能原因2：权限问题
确保您有GitHub仓库的管理权限

### 可能原因3：GitHub延迟
有时需要几分钟时间才能在Actions页面显示

## 📞 验证方法
推送一个小更改来触发自动构建：
```bash
git add .
git commit -m "触发APK构建"
git push origin main
```

然后在GitHub Actions页面查看构建状态。