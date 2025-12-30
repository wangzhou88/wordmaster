with open('c:/Users/admin/Downloads/wordmaster/main.py', 'rb') as f:
    content = f.read()

pattern1 = b'# \xe8\xbf\x9b\xe5\xba\xa6\xe6\x9d\xa1\xe8\x83\x8c\xef\xbf\xbd?        with'
pattern2 = b'# \xe6\x9b\xb4\xe6\x96\xb0\xe8\xbf\x9b\xe5\xba\xa6\xe6\x9d\xa1\xe5\xa4\xa7\xe5\xb0\x8f\xef\xbf\xbd?        Clock'

replacement1 = b'# \xe8\xbf\x9b\xe5\xba\xa6\xe6\x9d\xa1\xe8\x83\x8c\xe8\x83\x8c\xe6\x99\xaf\n        with'
replacement2 = b'# \xe6\x9b\xb4\xe6\x96\xb0\xe8\xbf\x9b\xe5\xba\xa6\xe6\x9d\xa1\xe5\xa4\xa7\xe5\xb0\x8f\xe5\xa4\xa7\xe5\xb0\x8f\n        Clock'

print('Pattern1 found:', pattern1 in content)
print('Pattern2 found:', pattern2 in content)

content = content.replace(pattern1, replacement1)
content = content.replace(pattern2, replacement2)

with open('c:/Users/admin/Downloads/wordmaster/main.py', 'wb') as f:
    f.write(content)
print('Fixed')
