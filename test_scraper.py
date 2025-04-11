from newspaper import Article
from newspaper import build

# This builds a collection of articles from NDTV homepage
paper = build('https://www.ndtv.com', memoize_articles=False)

print(f"Total articles found: {len(paper.articles)}")

for i, article in enumerate(paper.articles[:5]):
    article.download()
    article.parse()
    print(f"\n{i+1}. {article.title}")
    print(article.text[:200])  # Print first 200 chars of article