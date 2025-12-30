with open('c:/Users/admin/Downloads/wordmaster/main.py', 'rb') as f:
    content = f.read()

# Fix all remaining corrupted patterns
# The corrupted character U+FFFD is EF BF BD in UTF-8

# Pattern 1: 词? -> 词库
content = content.replace(b'\xe8\xaf\x8d\xef\xbf\xbd?', b'\xe8\xaf\x8d\xe5\xba\x93')

# Pattern 2: 单词? -> 单词
content = content.replace(b'\xe5\x8d\x95\xe8\xaf\x8d\xef\xbf\xbd', b'\xe5\x8d\x95\xe8\xaf\x8d')

with open('c:/Users/admin/Downloads/wordmaster/main.py', 'wb') as f:
    f.write(content)

print('Fixed all remaining corrupted patterns')
