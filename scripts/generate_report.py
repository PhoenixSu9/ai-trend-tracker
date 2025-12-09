#!/usr/bin/env python3
"""
Weekly Report Generator for AI Trend Tracker
Aggregates daily data and generates a weekly Markdown report
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


def load_config():
    """Load configuration from config.json"""
    config_path = Path(__file__).parent.parent / "config.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_week_files(data_dir, days=7):
    """Get list of daily data files for the past week"""
    data_path = Path(data_dir)
    files = []
    
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        file_path = data_path / f"{date_str}.json"
        
        if file_path.exists():
            files.append(file_path)
    
    return files


def load_week_data(data_dir, days=7):
    """Load all articles from the past week"""
    files = get_week_files(data_dir, days)
    all_articles = []
    seen_ids = set()
    
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            articles = json.load(f)
            for article in articles:
                if article['id'] not in seen_ids:
                    all_articles.append(article)
                    seen_ids.add(article['id'])
    
    return all_articles


def categorize_articles(articles):
    """Group articles by category"""
    categorized = defaultdict(list)
    
    for article in articles:
        category = article.get('category', 'Other')
        categorized[category].append(article)
    
    return categorized


def format_article(article, index):
    """Format a single article as Markdown"""
    title = article['title']
    link = article['link']
    source = article['source']
    summary = article.get('summary', '').strip()
    
    md = f"{index}. **[{title}]({link})**\n"
    md += f"   - 来源: {source}\n"
    
    if summary:
        # Clean summary
        summary_clean = summary.replace('\n', ' ').strip()
        if len(summary_clean) > 200:
            summary_clean = summary_clean[:200] + "..."
        md += f"   - 摘要: {summary_clean}\n"
    
    return md


def generate_weekly_report(articles, config):
    """Generate weekly report in Markdown format"""
    # Get date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    # Generate header
    report = f"# AI 趋势追踪周报\n\n"
    report += f"**报告周期**: {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}\n\n"
    report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += f"---\n\n"
    
    # Add summary
    report += f"## 📊 本周概览\n\n"
    report += f"本周共追踪到 **{len(articles)}** 篇文章，来自多个AI领域的前沿资讯源。\n\n"
    
    # Categorize articles
    categorized = categorize_articles(articles)
    
    # Sort categories
    category_order = config['report'].get('include_categories', [])
    sorted_categories = sorted(
        categorized.keys(),
        key=lambda x: category_order.index(x) if x in category_order else 999
    )
    
    # Generate content by category
    for category in sorted_categories:
        articles_in_category = categorized[category]
        
        # Sort by date (newest first)
        articles_in_category.sort(
            key=lambda x: x.get('published', ''),
            reverse=True
        )
        
        # Limit items per category
        max_items = config['report'].get('max_items_per_category', 15)
        articles_to_show = articles_in_category[:max_items]
        
        report += f"## 🔥 {category}\n\n"
        report += f"本分类共 {len(articles_in_category)} 篇文章，展示前 {len(articles_to_show)} 篇：\n\n"
        
        for idx, article in enumerate(articles_to_show, 1):
            report += format_article(article, idx) + "\n"
        
        report += "\n"
    
    # Add footer
    report += f"---\n\n"
    report += f"## 📝 说明\n\n"
    report += f"本报告由 AI Trend Tracker 自动生成，通过追踪多个AI领域RSS源，汇总整理最新动态。\n\n"
    report += f"数据来源包括：\n"
    
    sources = set(article['source'] for article in articles)
    for source in sorted(sources):
        report += f"- {source}\n"
    
    return report


def save_report(report, output_dir):
    """Save weekly report to file"""
    today = datetime.now().strftime('%Y-%m-%d')
    week_num = datetime.now().isocalendar()[1]
    year = datetime.now().year
    
    output_file = Path(output_dir) / f"weekly-report-{year}-W{week_num:02d}-{today}.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✓ Weekly report saved to: {output_file}")
    return output_file


def main():
    """Main function to generate weekly report"""
    print("=" * 60)
    print("AI Trend Tracker - Weekly Report Generator")
    print("=" * 60)
    
    config = load_config()
    
    # Load data from past week
    print("\nLoading data from the past 7 days...")
    articles = load_week_data(config['output']['daily_data_dir'], days=7)
    print(f"✓ Loaded {len(articles)} unique articles")
    
    if len(articles) == 0:
        print("\n⚠ No articles found. Please run fetch_rss.py first.")
        return
    
    # Generate report
    print("\nGenerating weekly report...")
    report = generate_weekly_report(articles, config)
    
    # Save report
    output_file = save_report(report, config['output']['reports_dir'])
    
    print("\n" + "=" * 60)
    print("Weekly report generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
