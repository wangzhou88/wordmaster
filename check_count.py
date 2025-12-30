import re

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
reading_count = len(re.findall(r"'type': 'reading'", content))
title_count = len(re.findall(r"'title': '[^']*'", content))
chinese_title_count = len(re.findall(r"'title': '[一-龯][^']*'", content))

print(f'Reading comprehension articles: {reading_count}')
print(f'Titles found: {title_count}')
print(f'Chinese titles found: {chinese_title_count}')

# Also check how many reading articles we have total
print(f'\nTotal reading comprehension articles should be around 50 for elementary students')