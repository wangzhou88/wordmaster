with open('c:/Users/admin/Downloads/wordmaster/main.py', 'rb') as f:
    content = f.read()

idx = content.find(b'\xe4\xbb\x8a\xe6\x97\xa5\xe5\xbe\x85\xe5\xa4\x8d')
print('Found at:', idx)
if idx > 0:
    print('Context:', repr(content[idx:idx+100]))
    
bad = content[idx:idx+145]

content = content.replace(bad, b'progress_layout.add_widget(create_label(text=f"今日待复习 {stats[\'need_review\']} 个单词"))')

with open('c:/Users/admin/Downloads/wordmaster/main.py', 'wb') as f:
    f.write(content)
print('Fixed')
