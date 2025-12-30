with open('c:/Users/admin/Downloads/wordmaster/main.py', 'rb') as f:
    content = f.read()

old1 = b"\xe8\xaf\x8d\xef\xbf\xbd'"
new1 = b"\xe8\xaf\x8d\xe5\xba\x93'"

old2 = b"\xe5\x8d\x95\xe8\xaf\x8d\xef\xbf\xbd)"
new2 = b"\xe5\x8d\x95\xe8\xaf\x8d)"

if old1 in content:
    content = content.replace(old1, new1)
    print('Fixed old1')

if old2 in content:
    content = content.replace(old2, new2)
    print('Fixed old2')

with open('c:/Users/admin/Downloads/wordmaster/main.py', 'wb') as f:
    f.write(content)
print('Done')
