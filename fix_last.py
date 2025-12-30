with open('c:/Users/admin/Downloads/wordmaster/main.py', 'rb') as f:
    content = f.read()

bad_pattern = b'"\xe4\xbb\x8a\xe6\x97\xa5\xe5\xbe\x85\xe5\xa4\x8d\xef\xbf\xbd? {stats[\'need_review\']} \xef\xbf\xbd?))"'
good_pattern = b'"\xe4\xbb\x8a\xe6\x97\xa5\xe5\xbe\x85\xe5\xa4\x8d\xe4\xb9\xa0 {stats[\'need_review\']} \xe4\xb8\xaa\xe5\x8d\x95\xe8\xaf\x8d"'

print('Found bad pattern:', bad_pattern in content)
content = content.replace(bad_pattern, good_pattern)

with open('c:/Users/admin/Downloads/wordmaster/main.py', 'wb') as f:
    f.write(content)
print('Fixed')
