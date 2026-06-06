#!/usr/bin/env python3
"""
Usage: python _add_article.py <url> <title> <date> <excerpt> <summary_html>
Called by Claude when a new article summary is ready.
Updates index.html and creates articles/<slug>.html
"""

import sys, os, re, json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent

def slugify(title: str) -> str:
    s = re.sub(r'[^\w\s-]', '', title.lower())
    s = re.sub(r'[\s_-]+', '-', s).strip('-')
    return s[:60] or 'article'

def unique_slug(base_slug: str) -> str:
    slug = base_slug
    i = 2
    while (BASE / 'articles' / f'{slug}.html').exists():
        slug = f'{base_slug}-{i}'
        i += 1
    return slug

def build_article_html(url: str, title: str, date: str, summary_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — hiro110's learns</title>
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <header>
    <h1>📚 hiro110's learns</h1>
    <span>気になる記事の要約集</span>
  </header>
  <main>
    <p class="breadcrumb"><a href="../index.html">← 一覧に戻る</a></p>
    <div class="article-header">
      <h1>{title}</h1>
      <div class="meta">
        <span>📅 {date}</span>
        <span class="source">🔗 <a href="{url}" target="_blank" rel="noopener">{url}</a></span>
      </div>
    </div>
    <div class="summary">
{summary_html}
    </div>
  </main>
</body>
</html>"""

def update_index(slug: str, title: str, date: str, excerpt: str):
    index_path = BASE / 'index.html'
    content = index_path.read_text(encoding='utf-8')

    card = f'''      <a class="article-card" href="articles/{slug}.html">
        <h2>{title}</h2>
        <div class="meta"><span>📅 {date}</span></div>
        <p class="excerpt">{excerpt}</p>
      </a>'''

    if '<div class="empty">' in content:
        content = content.replace(
            '      <div class="empty">まだ記事がありません。URLを貼り付けて最初の記事を追加しましょう！</div>',
            card
        )
    else:
        content = content.replace(
            '    <div id="articles-list" class="articles-grid">\n',
            f'    <div id="articles-list" class="articles-grid">\n{card}\n'
        )

    index_path.write_text(content, encoding='utf-8')

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print("Usage: _add_article.py <url> <title> <date> <excerpt> <summary_html_file>")
        sys.exit(1)

    url = sys.argv[1]
    title = sys.argv[2]
    date = sys.argv[3]
    excerpt = sys.argv[4]
    summary_html = Path(sys.argv[5]).read_text(encoding='utf-8')

    slug = unique_slug(slugify(title))

    article_path = BASE / 'articles' / f'{slug}.html'
    article_path.write_text(
        build_article_html(url, title, date, summary_html),
        encoding='utf-8'
    )

    update_index(slug, title, date, excerpt)

    print(f"Created: articles/{slug}.html")
