# WordMaster APK 构建流程详解

## 📋 构建概述

WordMaster APK构建是一个完全自动化的CI/CD流程，通过GitHub Actions在云端执行，支持一键构建和自动部署。

## 🔄 完整构建流程

### 第一阶段：构建触发

#### 1.1 自动触发（推荐）
```bash
# 推送代码到main分支自动触发
git add .
git commit -m "更新代码"
git push origin main
```

**触发条件**：
- Push到main/master分支
- 文件更改不在`.gitignore`的`paths-ignore`中
- PR合并到main分支

#### 1.2 手动触发
1. 访问 GitHub仓库：https://github.com/wangzhou88/wordmaster
2. 点击"Actions"标签
3. 选择"Build WordMaster APK"工作流
4. 点击"Run workflow"按钮
5. 选择构建参数：
   - **Build type**: debug/release
   - **Python version**: 3.9/3.10/3.11/3.12

### 第二阶段：云端构建执行

#### 2.1 环境准备（1-2分钟）
```yaml
# GitHub Actions自动执行以下步骤：
- name: Checkout code
  uses: actions/checkout@v4

- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: 3.11
    cache: 'pip'
```

**执行内容**：
- 检出最新代码
- 安装Python 3.11
- 配置pip缓存
- 设置构建环境

#### 2.2 依赖安装（3-5分钟）
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install buildozer
    pip install -r requirements.txt
```

**执行内容**：
- 更新pip到最新版本
- 安装Buildozer构建工具
- 安装项目依赖包
- 验证依赖完整性

#### 2.3 准备构建环境（5-8分钟）
```yaml
- name: Setup Android SDK
  run: |
    buildozer android clean
    buildozer android debug
```

**执行内容**：
- 清理之前的构建缓存
- 下载Android SDK
- 配置Java环境
- 初始化Android构建环境

#### 2.4 APK构建（30-60分钟）
```yaml
- name: Build APK
  run: buildozer android debug
```

**构建过程**：
1. **编译Python代码**
   - 解析main.py主文件
   - 编译Python源码到字节码
   - 处理Kivy界面布局

2. **资源打包**
   - 处理data/目录下的音频文件
   - 打包图标和图片资源
   - 生成应用图标

3. **Android APK生成**
   - 调用Android SDK编译
   - 生成debug APK文件
   - 签名APK（debug模式自动签名）

4. **最终打包**
   - 优化APK大小
   - 验证APK完整性
   - 生成构建产物

### 第三阶段：构建产物处理

#### 3.1 产物上传
```yaml
- name: Upload APK
  uses: actions/upload-artifact@v4
  with:
    name: wordmaster-apk
    path: bin/*.apk
```

**上传内容**：
- `wordmaster-0.1-debug.apk` - 主APK文件
- 构建日志文件
- 调试信息文件

#### 3.2 构建状态通知
```yaml
- name: Show build result
  run: |
    echo "✅ APK构建完成！"
    echo "📱 APK大小: $(ls -lh bin/*.apk | awk '{print $5}')"
    echo "📍 下载链接: https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}"
```

## 📱 APK获取流程

### 方法1：GitHub Actions页面下载
1. 访问：https://github.com/wangzhou88/wordmaster/actions
2. 找到最新的成功构建
3. 点击进入构建详情
4. 在"Artifacts"部分点击"wordmaster-apk"
5. 下载解压得到APK文件

### 方法2：API下载
```bash
# 通过GitHub CLI下载（如果已安装）
gh run download <run-id> --name wordmaster-apk

# 直接链接下载
curl -L -o wordmaster.apk \
  "https://github.com/wangzhou88/wordmaster/suites/<suite-id>/artifacts/<artifact-id>"
```

## 🔧 构建参数配置

### debug构建（推荐用于测试）
```yaml
build_type: "debug"
特点：
- ✅ 构建速度快（30-60分钟）
- ✅ 支持调试功能
- ✅ 自动签名，无需额外配置
- ❌ APK体积较大
- ❌ 性能稍差

适用于：功能测试、内部验证、开发调试
```

### release构建（用于发布）
```yaml
build_type: "release"
特点：
- ✅ APK体积优化
- ✅ 性能最佳
- ✅ 完整功能
- ❌ 构建时间较长（60-120分钟）
- ❌ 需要应用签名配置

适用于：正式发布、分发用户
```

## 🚨 常见问题与解决方案

### 问题1：构建失败
**错误信息**：`buildozer android debug failed`

**解决方案**：
1. 检查requirements.txt依赖是否兼容
2. 确认main.py语法正确
3. 查看构建日志定位具体错误
4. 修复后重新触发构建

### 问题2：构建超时
**错误信息**：`Error: The operation was canceled.`

**解决方案**：
1. 简化应用功能，减少构建复杂度
2. 检查网络连接，确保依赖下载正常
3. 重新触发构建

### 问题3：APK无法安装
**可能原因**：
- 未开启"未知来源"安装权限
- Android版本不兼容
- APK文件损坏

**解决方案**：
1. 在Android设置中允许"未知来源"安装
2. 检查Android版本要求（通常需要Android 4.1+）
3. 重新下载APK文件

## 📊 构建性能指标

### 时间统计
- **环境准备**: 1-2分钟
- **依赖安装**: 3-5分钟  
- **SDK配置**: 5-8分钟
- **APK构建**: 30-60分钟
- **总计**: 39-75分钟

### 文件大小
- **debug APK**: 通常50-100MB
- **release APK**: 通常30-80MB

### 资源占用
- **GitHub Actions**: Ubuntu容器
- **CPU**: 2核并行处理
- **内存**: 7GB RAM
- **存储**: 临时空间10GB

## 🎯 构建最佳实践

### 1. 代码准备
```python
# 确保main.py结构正确
if __name__ == '__main__':
    WordMasterApp().run()

# 资源文件路径使用相对路径
audio_path = os.path.join(os.path.dirname(__file__), 'data', 'audio')
```

### 2. 依赖管理
```txt
# requirements.txt保持简洁
kivy>=2.1.0
pydub>=0.25.1
sqlite3  # 通常已内置，无需添加
```

### 3. 权限配置
```ini
# buildozer.spec关键配置
[app]
title = WordMaster
package.name = wordmaster
package.domain = com.wordmaster.app

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.versioncode = 1
android.versionname = 1.0

android.add_libs_zip = False
```

### 4. 图标和启动画面
```ini
# 配置应用图标
android.icon.filename = icon_bg.png

# 配置启动画面（可选）
android.splashscreen = icon_fg.png
```

## 🔄 自动化优化

### 构建缓存
GitHub Actions自动缓存：
- pip依赖包
- Android SDK组件
- Python虚拟环境

### 并行构建
支持多Python版本并行测试：
- Python 3.9
- Python 3.10  
- Python 3.11
- Python 3.12

### 失败重试
自动重试机制：
- 网络超时重试3次
- 依赖安装失败自动重试
- 构建过程错误提供详细日志

## 📈 监控和通知

### 构建状态监控
- GitHub页面实时显示构建进度
- 邮件通知构建结果
- Webhook支持第三方集成

### 性能监控
- 构建时间统计
- APK大小变化趋势
- 成功率分析

---

**总结**：WordMaster APK构建流程完全自动化，从代码提交到APK生成全程云端处理，确保构建质量和效率。只需简单的git push即可获得可安装的Android APK文件！