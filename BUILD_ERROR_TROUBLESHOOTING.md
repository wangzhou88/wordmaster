# WordMaster APK构建错误排查指南

## 错误信息

```
# Buildozer failed to execute the last command 
# The error might be hidden in the log above this error 
# Please read the full log, and search for it before 
# raising an issue with buildozer itself. 
# In case of a bug report, please add a full log with log_level = 2 
Error: Process completed with exit code 1.
```

## 错误排查步骤

### 1. 检查工作流日志

1. 在GitHub仓库的"Actions"页面中，找到失败的工作流运行
2. 点击失败的工作流运行，查看详细日志
3. 重点关注错误出现的步骤和具体错误信息

### 2. 查看buildozer.spec配置

检查buildozer.spec文件中的配置是否正确：

```ini
[app]
title = WordMaster
package.name = wordmaster
package.domain = com.wordmaster.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,json,txt,md,pkl,db,pyc,pyo
version = 1.0.0
requirements = python3,kivy>=2.0.0,sqlite3,requests,plyer,pydub,SpeechRecognition,Pillow,pygame
orientation = portrait
fullscreen = 0

[android]
api = 31
android.permissions = android.permission.RECORD_AUDIO,android.permission.INTERNET,android.permission.ACCESS_NETWORK_STATE,android.permission.WRITE_EXTERNAL_STORAGE,android.permission.READ_EXTERNAL_STORAGE
android.archs = arm64-v8a,armeabi-v7a
```

确保配置中没有语法错误或无效的值。

### 3. 检查依赖项

在requirements部分列出的Python包可能存在问题：

1. 某些包可能不支持Android平台
2. 某些包的版本可能与Android构建环境不兼容
3. 某些包可能需要特定的配置

### 4. 常见解决方案

1. **简化依赖项**：
   - 尝试减少requirements中的包数量
   - 逐个添加包，确定哪个包导致问题

2. **检查代码问题**：
   - 确保main.py中没有语法错误
   - 检查代码中是否使用了不兼容的模块

3. **更新buildozer.spec**：
   - 尝试使用更简单的配置
   - 确保android.api值与工作流中设置的值一致

### 5. 修复后的配置示例

尝试使用以下简化的buildozer.spec配置：

```ini
[app]
title = WordMaster
package.name = wordmaster
package.domain = com.wordmaster.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,json,txt,md,pkl,db,pyc,pyo
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[android]
api = 31
android.permissions = android.permission.RECORD_AUDIO,android.permission.INTERNET,android.permission.ACCESS_NETWORK_STATE,android.permission.WRITE_EXTERNAL_STORAGE,android.permission.READ_EXTERNAL_STORAGE
android.archs = arm64-v8a
```

### 6. 检查具体错误日志

如果上述解决方案不起作用，我们需要查看工作流的完整错误日志，特别是：

1. 错误发生的具体步骤
2. 错误消息的详细内容
3. 错误前后的相关日志

## 进一步操作

如果需要进一步的帮助，请提供以下信息：

1. GitHub Actions工作流中失败步骤的完整日志
2. 当前使用的buildozer.spec文件内容
3. main.py文件的内容（特别是开头的import语句）