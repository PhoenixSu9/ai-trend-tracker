# AI Trend Tracker - AI 趋势追踪器

🤖 自动化追踪AI领域最新动态，每日抓取RSS订阅源，每周生成Markdown格式的周报草稿。

## ✨ 功能特性

- 📡 **自动RSS抓取**: 每日自动从多个AI领域顶级博客和新闻源抓取最新文章
- 📊 **智能分类整理**: 按类别（AI研究、AI工具、AI新闻等）自动分类整理
- 📝 **周报自动生成**: 每周一自动生成Markdown格式的周报草稿
- 🔄 **GitHub Actions自动化**: 全流程自动化，无需手动干预
- 🚀 **即开即用**: Fork仓库后自动运行，无需额外配置

## 📋 目录结构

```
ai-trend-tracker/
├── .github/
│   └── workflows/
│       ├── daily-fetch.yml      # 每日RSS抓取工作流
│       └── weekly-report.yml    # 每周报告生成工作流
├── scripts/
│   ├── fetch_rss.py            # RSS抓取脚本
│   └── generate_report.py      # 周报生成脚本
├── data/
│   ├── daily/                  # 每日抓取的数据（JSON格式）
│   └── feeds/                  # RSS源数据
├── reports/                    # 生成的周报（Markdown格式）
├── config.json                 # 配置文件
├── requirements.txt            # Python依赖
└── README.md
```

## 🚀 快速开始

### 1. Fork此仓库

点击右上角的 "Fork" 按钮，将此仓库复制到你的GitHub账号下。

### 2. 启用GitHub Actions

1. 进入你Fork的仓库
2. 点击 "Actions" 标签
3. 如果提示启用工作流，点击 "I understand my workflows, go ahead and enable them"

### 3. 手动触发首次运行（可选）

1. 进入 "Actions" 标签
2. 选择 "AI Trend Tracker - Daily RSS Fetch"
3. 点击 "Run workflow" 按钮手动触发第一次抓取

### 4. 查看结果

- **每日数据**: 查看 `data/daily/` 目录下的JSON文件
- **周报**: 查看 `reports/` 目录下的Markdown文件

## ⚙️ 配置说明

编辑 `config.json` 文件来自定义RSS源和设置：

```json
{
  "rss_feeds": [
    {
      "name": "OpenAI Blog",
      "url": "https://openai.com/blog/rss.xml",
      "category": "AI Research"
    }
    // 添加更多RSS源...
  ],
  "output": {
    "daily_data_dir": "data/daily",
    "reports_dir": "reports",
    "max_items_per_feed": 10
  },
  "report": {
    "weekly_day": "monday",
    "max_items_per_category": 15
  }
}
```

### 添加自定义RSS源

在 `config.json` 的 `rss_feeds` 数组中添加新的RSS源：

```json
{
  "name": "你的RSS源名称",
  "url": "https://example.com/feed.xml",
  "category": "分类名称"
}
```

## 📅 自动化时间表

- **每日抓取**: 每天UTC时间00:00（北京时间08:00）
- **周报生成**: 每周一UTC时间01:00（北京时间09:00）

可以在 `.github/workflows/` 目录下的YAML文件中修改 `cron` 表达式来调整时间。

## 🛠️ 本地运行

### 安装依赖

```bash
pip install -r requirements.txt
```

### 抓取RSS数据

```bash
python scripts/fetch_rss.py
```

### 生成周报

```bash
python scripts/generate_report.py
```

## 📊 数据源

当前追踪的AI资讯源包括：

- **OpenAI Blog** - OpenAI官方博客
- **DeepMind Blog** - Google DeepMind官方博客
- **Hugging Face Blog** - Hugging Face技术博客
- **MIT AI News** - MIT人工智能新闻
- **The Batch by DeepLearning.AI** - Andrew Ng的AI周报

## 🤝 贡献

欢迎贡献！你可以：

1. 添加更多优质的AI RSS源
2. 改进报告生成模板
3. 优化分类和过滤逻辑
4. 提交Bug报告和功能建议

## 📄 许可证

MIT License

## 🔗 相关链接

- [RSS规范](https://www.rssboard.org/rss-specification)
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [feedparser库文档](https://feedparser.readthedocs.io/)

---

**注意**: 首次运行后，数据需要累积几天才能生成有意义的周报。建议先手动触发几次每日抓取，或等待自动运行几天后再查看周报效果。
