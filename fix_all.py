import codecs

with codecs.open('c:/Users/admin/Downloads/wordmaster/main.py', 'r', 'utf-8') as f:
    content = f.read()

# Fix all corrupted characters
replacements = [
    ('请说?..', '请说话..'),
    ('开始语音识?', '开始语音识别'),
    ('个字?', '个字母'),
    ('今日待复?', '今日待复习'),
    ('最近测试成?', '最近测试成绩'),
    ('选择题 85?', '选择题 85分'),
    ('填空题 75?', '填空题 75分'),
    ('听写题 70?', '听写题 70分'),
    ('进度条大?', '进度条大小'),
    ('父容器大?', '父容器大小'),
    ('进度条宽?', '进度条宽度'),
    ('屏幕管理?', '屏幕管理器'),
]

for old, new in replacements:
    if old in content:
        count = content.count(old)
        content = content.replace(old, new)
        print(f"Fixed: {repr(old)} -> {repr(new)} ({count} occurrences)")

# Write back
with codecs.open('c:/Users/admin/Downloads/wordmaster/main.py', 'w', 'utf-8') as f:
    f.write(content)
print("Done fixing all corrupted characters")
