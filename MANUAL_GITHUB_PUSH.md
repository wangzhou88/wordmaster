# 📦 手动GitHub推送指南

## 🔧 步骤1：创建GitHub仓库

1. 访问 https://github.com/new
2. 填写信息：
   ```
   Repository name: wordmaster
   Description: WordMaster英语学习助手
   Public ☑️
   ```
3. 点击 "Create repository"

## 📁 步骤2：下载项目文件

我会为您准备一个压缩包，包含所有必要的文件：
<minimax:tool_call>
<invoke name="RunCommand">
<parameter name="command">cd .. && zip -r wordmaster-project.zip wordmaster/ -x "wordmaster/.git/*" "wordmaster/__pycache__/*" "wordmaster/build/*" "wordmaster/dist/*" "wordmaster/.venv/*"