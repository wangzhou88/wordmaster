import codecs

with codecs.open('c:/Users/admin/Downloads/wordmaster/main.py', 'r', 'utf-8') as f:
    content = f.read()

# Fix multiple corrupted characters
replacements = [
    ('请说?.', '请说话..'),
    ('开始语音识?', '开始语音识别'),
    ('个字?', '个字母'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"Fixed: {repr(old)} -> {repr(new)}")

# Write back
with codecs.open('c:/Users/admin/Downloads/wordmaster/main.py', 'w', 'utf-8') as f:
    f.write(content)
print("Done fixing corrupted characters")
