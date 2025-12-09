#!/usr/bin/env python3
"""
RSS Feed Fetcher for AI Trend Tracker
Fetches articles from configured RSS feeds and stores them as JSON
"""

import feedparser
import json
import os
from datetime import datetime
from pathlib import Path
import hashlib


def load_config():
    """Load configuration from config.json"""
    config_path = Path(__file__).parent.parent / "config.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_article_id(title, link):
    """Generate unique ID for an article"""
    content = f"{title}{link}"
    return hashlib.md5(content.encode()).hexdigest()


def fetch_rss_feed(feed_url, feed_name, category, max_items):
    """Fetch and parse a single RSS feed"""
    print(f"Fetching: {feed_name}...")
    
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        
        for entry in feed.entries[:max_items]:
            article = {
                'id': generate_article_id(entry.get('title', ''), entry.get('link', '')),
                'title': entry.get('title', 'No Title'),
                'link': entry.get('link', ''),
                'published': entry.get('published', entry.get('updated', '')),
                'summary': entry.get('summary', entry.get('description', ''))[:300],
                'source': feed_name,
                'category': category,
                'fetched_at': datetime.now().isoformat()
            }
            articles.append(article)
        
        print(f"  ✓ Fetched {len(articles)} articles from {feed_name}")
        return articles
    
    except Exception as e:
        print(f"  ✗ Error fetching {feed_name}: {str(e)}")
        return []


def save_daily_data(articles, output_dir):
    """Save fetched articles to daily JSON file"""
    today = datetime.now().strftime('%Y-%m-%d')
    output_file = Path(output_dir) / f"{today}.json"
    
    # Load existing data if file exists
    existing_articles = []
    if output_file.exists():
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_articles = json.load(f)
    
    # Merge with new articles (avoid duplicates by ID)
    existing_ids = {article['id'] for article in existing_articles}
    new_articles = [a for a in articles if a['id'] not in existing_ids]
    
    all_articles = existing_articles + new_articles
    
    # Save to file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved {len(all_articles)} articles ({len(new_articles)} new) to {output_file}")
    return len(new_articles)


def main():
    """Main function to fetch all RSS feeds"""
    print("=" * 60)
    print("AI Trend Tracker - RSS Feed Fetcher")
    print("=" * 60)
    
    config = load_config()
    all_articles = []
    
    for feed in config['rss_feeds']:
        articles = fetch_rss_feed(
            feed['url'],
            feed['name'],
            feed['category'],
            config['output']['max_items_per_feed']
        )
        all_articles.extend(articles)
    
    # Save to daily data file
    new_count = save_daily_data(all_articles, config['output']['daily_data_dir'])
    
    print("\n" + "=" * 60)
    print(f"Fetch complete! Total: {len(all_articles)} articles, {new_count} new")
    print("=" * 60)


if __name__ == "__main__":
    main()
