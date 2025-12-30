with open('c:/Users/admin/Downloads/wordmaster/main.py', 'rb') as f:
    content = f.read()

old = b'\xe4\xb8\xaa\xe5\x8d\x95\xef\xbf\xbd'
new = b'\xe4\xb8\xaa\xe5\x8d\x95\xe8\xaf\x8d'

if old in content:
    content = content.replace(old, new)
    with open('c:/Users/admin/Downloads/wordmaster/main.py', 'wb') as f:
        f.write(content)
    print('Fixed!')
else:
    print('Pattern not found, trying different approach...')
    # Search for all U+FFFD
    if b'\xef\xbf\xbd' in content:
        count = content.count(b'\xef\xbf\xbd')
        print(f'Found {count} U+FFFD characters')
        # Try replacing them all
        content = content.replace(b'\xef\xbf\xbd', b'\x8d')
        with open('c:/Users/admin/Downloads/wordmaster/main.py', 'wb') as f:
            f.write(content)
        print('Replaced all U+FFFD with �')
