#!/usr/bin/env python3
import re
from pathlib import Path

html = Path('index.html').read_text()
img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
sources = re.findall(img_pattern, html)

print('📋 All image references in HTML:')
valid_count = 0
for i, src in enumerate(sources, 1):
    if src.startswith('http'):
        status = '✓'
        exists_text = 'remote URL'
    else:
        exists = Path(src).exists()
        status = '✓' if exists else '❌'
        exists_text = 'found' if exists else 'MISSING'
        if exists:
            valid_count += 1
    print(f'  {status} {i}. {src} ({exists_text})')

print(f'\n✅ All {len(sources)} image references are valid!' if valid_count >= len([s for s in sources if not s.startswith('http')]) else f'\n⚠️ {len([s for s in sources if not s.startswith('http')]) - valid_count} images missing!')
