# 使用示例 (Usage Examples)

本文档提供 AI Trend Tracker 的详细使用示例。

## 基本使用

### 1. 本地运行 RSS 抓取

```bash
# 安装依赖
pip install -r requirements.txt

# 运行 RSS 抓取
python scripts/fetch_rss.py
```

输出示例：
```
============================================================
AI Trend Tracker - RSS Feed Fetcher
============================================================
Fetching: OpenAI Blog...
  ✓ Fetched 5 articles from OpenAI Blog
Fetching: Google AI Blog...
  ✓ Fetched 8 articles from Google AI Blog
...

✓ Saved 30 articles (30 new) to data/daily/2025-12-09.json

============================================================
Fetch complete! Total: 30 articles, 30 new
============================================================
```

### 2. 本地生成周报

```bash
python scripts/generate_report.py
```

输出示例：
```
============================================================
AI Trend Tracker - Weekly Report Generator
============================================================

Loading data from the past 7 days...
✓ Loaded 180 unique articles

Generating weekly report...
✓ Weekly report saved to: reports/weekly-report-2025-W50-2025-12-09.md

============================================================
Weekly report generation complete!
============================================================
```

## 自定义配置

### 添加新的 RSS 源

编辑 `config.json`，在 `rss_feeds` 数组中添加：

```json
{
  "name": "Your Custom Blog",
  "url": "https://yourblog.com/feed.xml",
  "category": "AI Research"
}
```

### 调整抓取数量

在 `config.json` 中修改：

```json
{
  "output": {
    "max_items_per_feed": 20  // 每个源最多抓取 20 篇
  }
}
```

### 修改周报限制

```json
{
  "report": {
    "max_items_per_category": 20,  // 每个分类最多显示 20 篇
    "summary_max_length": 300      // 摘要最大长度 300 字符
  }
}
```

## GitHub Actions 使用

### 手动触发工作流

1. 进入 GitHub 仓库的 "Actions" 标签
2. 选择要运行的工作流：
   - "AI Trend Tracker - Daily RSS Fetch" (每日抓取)
   - "AI Trend Tracker - Weekly Report" (周报生成)
3. 点击 "Run workflow" 按钮
4. 选择分支（通常是 `main`）
5. 点击绿色的 "Run workflow" 按钮确认

### 修改运行时间

编辑 `.github/workflows/daily-fetch.yml`：

```yaml
on:
  schedule:
    # 修改为你想要的时间 (cron 格式)
    - cron: '0 8 * * *'  # 每天 08:00 UTC
```

常用 cron 表达式：
- `0 0 * * *` - 每天 00:00 UTC
- `0 */6 * * *` - 每 6 小时一次
- `0 0 * * 1` - 每周一 00:00 UTC
- `0 1 1 * *` - 每月 1 号 01:00 UTC

## 集成到博客

### 方法 1: 直接链接

在你的博客中添加指向 GitHub 仓库的链接：

```markdown
查看 [本周 AI 趋势报告](https://github.com/your-username/ai-trend-tracker/tree/main/reports)
```

### 方法 2: 自动同步

创建一个新的 GitHub Actions 工作流 `.github/workflows/sync-to-blog.yml`：

```yaml
name: Sync Reports to Blog

on:
  push:
    paths:
      - 'reports/*.md'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout ai-trend-tracker
        uses: actions/checkout@v4
        with:
          path: tracker
      
      - name: Checkout blog repo
        uses: actions/checkout@v4
        with:
          repository: your-username/your-blog-repo
          token: ${{ secrets.BLOG_PAT }}
          path: blog
      
      - name: Copy reports
        run: |
          cp -r tracker/reports/* blog/content/ai-reports/
      
      - name: Commit and push
        run: |
          cd blog
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          git commit -m "Update AI trend reports" || echo "No changes"
          git push
```

### 方法 3: 使用 GitHub Pages

1. 在仓库设置中启用 GitHub Pages
2. 选择 `main` 分支的 `/reports` 文件夹作为源
3. 你的报告将可通过 `https://your-username.github.io/ai-trend-tracker/` 访问

## 高级用法

### 过滤特定主题

修改 `scripts/fetch_rss.py`，添加关键词过滤：

```python
def fetch_rss_feed(feed_url, feed_name, category, max_items, keywords=None):
    # ... existing code ...
    
    for entry in feed.entries:
        title = entry.get('title', '')
        
        # 如果设置了关键词过滤
        if keywords:
            if not any(kw.lower() in title.lower() for kw in keywords):
                continue
        
        # ... rest of code ...
```

### 添加邮件通知

创建 `.github/workflows/email-report.yml`：

```yaml
name: Email Weekly Report

on:
  schedule:
    - cron: '0 2 * * 1'  # 每周一 02:00 UTC

jobs:
  send-email:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Get latest report
        id: report
        run: |
          REPORT=$(ls -t reports/*.md | head -1)
          echo "file=$REPORT" >> $GITHUB_OUTPUT
      
      - name: Send email
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.EMAIL_USERNAME }}
          password: ${{ secrets.EMAIL_PASSWORD }}
          subject: AI Trend Tracker - Weekly Report
          body: file://${{ steps.report.outputs.file }}
          to: your-email@example.com
          from: AI Trend Tracker
```

## 故障排除

### 问题：RSS 源无法访问

**解决方案**：
1. 检查 RSS URL 是否正确
2. 尝试在浏览器中直接访问 RSS URL
3. 某些网站可能有访问限制，考虑更换源

### 问题：GitHub Actions 没有自动运行

**解决方案**：
1. 确保在仓库设置中启用了 Actions
2. 检查工作流文件的 cron 语法是否正确
3. 首次设置后可能需要手动触发一次

### 问题：生成的报告为空

**解决方案**：
1. 确保已运行过 RSS 抓取脚本
2. 检查 `data/daily/` 目录是否有数据文件
3. 确认数据文件中有内容

## 贡献指南

欢迎贡献！请参考以下步骤：

1. Fork 此仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

### 添加新的 RSS 源建议

在提交新的 RSS 源时，请确保：

1. 源的内容与 AI 领域相关
2. RSS feed 稳定可访问
3. 内容质量高且更新频繁
4. 在 config.json 中按字母顺序添加
5. 在 PR 描述中说明添加原因

## 资源链接

- [RSS 2.0 规范](https://www.rssboard.org/rss-specification)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Cron 表达式生成器](https://crontab.guru/)
- [feedparser 库文档](https://feedparser.readthedocs.io/)
