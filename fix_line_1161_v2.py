with open('c:/Users/admin/Downloads/wordmaster/main.py', 'rb') as f:
    content = f.read()

old = b'\xe8\xaf\x8d?'
new = b'\xe8\xaf\x8d'

if old in content:
    content = content.replace(old, new)
    with open('c:/Users/admin/Downloads/wordmaster/main.py', 'wb') as f:
        f.write(content)
    print('Fixed!')
else:
    print('Pattern not found')
