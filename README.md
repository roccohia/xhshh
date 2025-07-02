# 🤖 小红书数据分析自动化系统

[![GitHub Actions](https://github.com/roccohia/xhshh/workflows/小红书数据分析自动化任务/badge.svg)](https://github.com/roccohia/xhshh/actions)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> 🎯 **每天自动爬取小红书数据，智能分析并推送到 Telegram**

基于 MediaCrawler 的全自动小红书数据分析系统，每天北京时间 9:00 自动运行，提供关键词分析、竞品研究、KOC筛选、选题建议等功能，并将结果自动推送到 Telegram。

## ✨ 核心功能

### 🕷️ 自动数据采集
- 每日定时爬取小红书笔记内容
- 支持多关键词搜索
- 自动获取笔记详情和评论数据

### 📊 智能数据分析
- **🔤 关键词分析**: jieba分词 + 词云图生成
- **🏆 竞品分析**: 互动率计算 + 内容类型分类
- **👥 KOC筛选**: 智能评分 + 多维度筛选
- **💡 选题建议**: 标题模式识别 + AI增强分析

### 📅 内容规划工具
- 生成 30 天 Notion 内容日历
- 智能匹配目标人群和关键词
- 提供具体的创作建议

### 📱 自动推送通知
- Telegram Bot 自动推送分析结果
- 包含图表、数据文件和详细报告
- 支持移动端随时查看

## 🚀 快速开始

### 1️⃣ 克隆仓库
```bash
git clone https://github.com/roccohia/xhshh.git
cd xhshh
```

### 2️⃣ 安装依赖
```bash
pip install -r requirements.txt
```

### 3️⃣ 配置 Telegram Bot
1. 找 `@BotFather` 创建 Telegram Bot
2. 获取 Bot Token 和 Chat ID
3. 在 GitHub 仓库设置中添加 Secrets:
   - `BOT_TOKEN`: 你的 Bot Token
   - `CHAT_ID`: 你的 Chat ID

### 4️⃣ 更新小红书 Cookie

编辑 `core/media_crawler/config/base_config.py`，更新小红书 Cookie

### 5️⃣ 启用自动化
GitHub Actions 将每天北京时间 9:00 自动运行

## 📊 分析结果示例

### 每日推送内容
```
🤖 小红书数据分析报告
📅 生成时间: 2025-07-02 09:00:00

📊 本次分析生成了 5 个文件:
🔤 关键词分析: keywords_analysis_*.csv
☁️ 词云图: wordcloud_*.png
🏆 竞品分析: competitor_analysis_*.csv
👥 KOC用户筛选: koc_users_*.csv
💡 选题建议: topic_suggestions_*.csv
📅 Notion内容日历: notion_content_calendar.csv

🎯 分析完成，请查看附件获取详细结果！
```

### 输出文件类型
- **☁️ 词云图** (PNG) - 关键词可视化
- **📅 Notion日历** (CSV) - 直接导入使用
- **👥 KOC列表** (CSV) - 优质用户筛选
- **💡 选题建议** (CSV) - 内容创作指导
- **📋 分析报告** (TXT) - 详细数据洞察

## 🔧 本地测试

### 测试 Telegram 连接
```bash
python scripts/test_telegram.py --token YOUR_TOKEN --chat-id YOUR_CHAT_ID
```

### 测试完整流程
```bash
python scripts/test_automation.py --skip-crawler --bot-token YOUR_TOKEN --chat-id YOUR_CHAT_ID
```

### 手动运行分析
```bash
# 爬取数据
python scripts/run_crawler_enhanced.py --keyword "普拉提" --limit 50

# 运行分析
python analysis/run_analysis_simple.py --input latest

# 生成 Notion 日历
python analysis/export_notionsheet.py --days 30

# 推送到 Telegram
python scripts/telegram_push.py --token YOUR_TOKEN --chat-id YOUR_CHAT_ID
```

## 📁 项目结构

```
xhshh/
├── .github/workflows/
│   └── daily_run.yml              # GitHub Actions 工作流
├── core/media_crawler/            # 爬虫核心
├── scripts/
│   ├── run_crawler_enhanced.py    # 增强爬虫脚本
│   ├── telegram_push.py           # Telegram 推送
│   └── test_*.py                  # 测试脚本
├── analysis/
│   ├── keyword_analysis.py        # 关键词分析
│   ├── competitor_analysis.py     # 竞品分析
│   ├── koc_filter.py             # KOC 筛选
│   ├── topic_generator.py        # 选题建议
│   ├── export_notionsheet.py     # Notion 导出
│   └── run_analysis_simple.py    # 一键分析
├── output/                        # 分析结果输出
├── requirements.txt               # 依赖列表
└── README.md                      # 项目说明
```

## ⚙️ 自定义配置

### 修改爬取关键词
编辑 `.github/workflows/daily_run.yml`:
```yaml
python scripts/run_crawler_enhanced.py --keyword "瑜伽,健身,减肥" --limit 100
```

### 调整运行时间
```yaml
schedule:
  # 每天北京时间 8:00 运行 (UTC 0:00)
  - cron: '0 0 * * *'
```

### 增加分析天数
```yaml
python analysis/export_notionsheet.py --days 45
```

## 📈 应用场景

### 🎯 内容创作者
- 每日获取数据驱动的选题建议
- 了解热门关键词和趋势变化
- 分析竞品内容策略
- 使用 Notion 日历规划内容

### 📊 营销团队
- 筛选优质 KOC 进行合作
- 监控品牌相关话题热度
- 制定数据驱动的营销策略
- 跟踪竞品动态和表现

### 🔍 数据分析师
- 自动化日常数据收集工作
- 获取多维度的数据洞察
- 生成可视化分析报告
- 进行长期趋势分析

## 🚨 注意事项

- 仅用于个人学习和研究目的
- 遵守小红书平台使用条款
- 合理控制爬取频率和数量
- 及时更新过期的 Cookie 配置

## 📖 详细文档

- [📋 部署指南](DEPLOY_TO_GITHUB.md) - 完整的部署步骤
- [📊 分析模块指南](ANALYSIS_GUIDE.md) - 各分析模块详细说明
- [📅 Notion 导出指南](NOTION_EXPORT_GUIDE.md) - Notion 集成使用
- [🤖 自动化完成总结](AUTOMATION_COMPLETE.md) - 系统功能总览

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 📄 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🎉 致谢

- 基于 [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 项目
- 感谢所有开源贡献者

---

⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！