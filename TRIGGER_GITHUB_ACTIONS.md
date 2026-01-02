# 手动触发GitHub Actions工作流指南

## 步骤1：进入GitHub Actions页面

1. 在浏览器中打开GitHub仓库页面
2. 点击页面顶部的"Actions"标签

## 步骤2：查看工作流

1. 在左侧菜单中，找到名为"Build Android APK"的工作流
2. 点击该工作流进入详情页面

## 步骤3：手动触发工作流

1. 点击"Run workflow"按钮（位于工作流页面右上角）
2. 在弹出的下拉菜单中，选择构建类型：
   - 默认选择"debug"进行调试构建
   - 如需发布版本，选择"release"
3. 点击绿色的"Run workflow"按钮确认执行

## 步骤4：监控工作流执行

1. 工作流开始执行后，会显示一个实时更新的进度条
2. 点击进入任何步骤查看详细日志
3. 关注"Build APK"步骤，这是最关键的构建步骤

## 步骤5：下载构建产物

1. 构建完成后，页面底部会显示"Artifacts"部分
2. 点击"wordmaster-apk-{commit_hash}-{build_type}"下载APK文件
3. 点击"build-logs-{commit_hash}"下载构建日志

## 常见问题

### 工作流没有开始运行
- 检查是否已正确配置GitHub仓库权限
- 尝试刷新页面或等待几分钟

### 构建失败
- 下载并查看构建日志以找出具体错误
- 查看本项目中的`BUILD_ERROR_TROUBLESHOOTING.md`文档了解常见解决方案
- 检查代码是否与Android平台兼容

### APK文件未生成
- 检查工作流日志中的"查找构建产物"步骤
- 确保没有权限问题导致APK无法保存到Artifacts