import re

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找所有阅读理解文章的标题和部分内容
reading_articles = re.findall(r"\{\s*'type': 'reading',\s*'title': '([^']*)',\s*'article': '([^']*)'", content)

print(f'找到 {len(reading_articles)} 篇阅读理解文章:')
print('=' * 60)

for i, (title, article) in enumerate(reading_articles, 1):
    print(f'{i}. 标题: {title}')
    print(f'   文章开头: {article[:100]}...')
    print()

# 检查是否还有中文标题
chinese_titles = [title for title, _ in reading_articles if re.search(r'[一-龯]', title)]
print(f'\n中文标题数量: {len(chinese_titles)}')

if chinese_titles:
    print('剩余的中文标题:')
    for title in chinese_titles:
        print(f'  - {title}')
else:
    print('✅ 所有标题都已经是英文了')