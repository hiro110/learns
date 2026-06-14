# 📚 hiro110's learns

気になったブログや記事のURLを投げると、日本語で要約してこのリポジトリにストックし、GitHub Pages で公開する個人ナレッジベースです。

🔗 公開サイト: https://hiro110.github.io/learns/

## 仕組み

| ファイル | 役割 |
| --- | --- |
| `index.html` | 記事一覧（カード表示） |
| `articles/<slug>.html` | 各記事の要約ページ |
| `css/style.css` | スタイル |
| `_add_article.py` | 記事ページ生成＋一覧更新の補助スクリプト |

## 運用フロー

1. 気になるURLをチャットに貼る
2. Claude が本文を取得し、日本語で要約
3. `_add_article.py` で記事ページを生成・一覧を更新
4. commit & push → GitHub Pages に自動反映
