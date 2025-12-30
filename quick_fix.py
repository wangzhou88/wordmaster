import codecs

with codecs.open('c:/Users/admin/Downloads/wordmaster/main.py', 'r', 'utf-8') as f:
    lines = f.readlines()

fixes = [
    ('# 进度条背？        with', '# 进度条背景\n        with'),
    ('# 更新进度条大？        Clock', '# 更新进度条大小\n        Clock'),
]

for i, line in enumerate(lines):
    for old, new in fixes:
        if old in line:
            lines[i] = line.replace(old, new)
            print(f"Line {i+1} fixed")

with codecs.open('c:/Users/admin/Downloads/wordmaster/main.py', 'w', 'utf-8') as f:
    f.writelines(lines)
print("Done")
