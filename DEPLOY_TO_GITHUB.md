# 🚀 部署到 GitHub 仓库指南

## 📋 仓库信息
- **GitHub 仓库**: https://github.com/roccohia/xhshh
- **用户**: roccohia
- **项目**: 小红书数据分析自动化系统

## 🔧 部署步骤

### 1️⃣ 推送代码到 GitHub

#### 初始化本地仓库
```bash
# 在项目根目录执行
git init
git remote add origin https://github.com/roccohia/xhshh.git

# 添加所有文件
git add .
git commit -m "🎉 初始化小红书数据分析自动化系统"

# 推送到 GitHub
git push -u origin main
```

#### 确保关键文件已上传
检查以下文件是否已推送：
- ✅ `.github/workflows/daily_run.yml` - GitHub Actions 工作流
- ✅ `requirements.txt` - 依赖列表
- ✅ `scripts/telegram_push.py` - Telegram 推送脚本
- ✅ `analysis/run_analysis_simple.py` - 分析脚本（支持latest）
- ✅ 所有分析模块文件

### 2️⃣ 配置 GitHub Secrets

#### 进入仓库设置
1. 访问: https://github.com/roccohia/xhshh/settings/secrets/actions
2. 点击 "New repository secret"

#### 添加必需的 Secrets
| Secret 名称 | 值 | 说明 |
|-------------|----|----|
| `BOT_TOKEN` | 你的 Telegram Bot Token | 格式: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `CHAT_ID` | 你的 Telegram Chat ID | 格式: `123456789` 或 `-123456789` |

### 3️⃣ 创建 Telegram Bot

#### 步骤 1: 创建 Bot
1. 在 Telegram 搜索 `@BotFather`
2. 发送 `/newbot` 命令
3. 按提示设置 Bot 名称: `XHS Analysis Bot`
4. 设置用户名: `xhs_analysis_bot` (需要以_bot结尾)
5. 获取 Bot Token 并保存

#### 步骤 2: 获取 Chat ID
```bash
# 方法1: 给 Bot 发消息后访问
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates

# 方法2: 使用测试脚本
python scripts/test_telegram.py --token YOUR_TOKEN --chat-id YOUR_CHAT_ID
```

### 4️⃣ 配置 Cookie (重要)

#### 更新 Cookie 配置
编辑 `core/media_crawler/config/base_config.py`:

```python
# 更新为最新的有效 Cookie
COOKIES = "你的最新小红书Cookie"

# 建议配置
SAVE_DATA_OPTION = "csv"  # 改为 csv 格式便于分析
CRAWLER_MAX_NOTES_COUNT = 100  # 增加爬取数量
ENABLE_GET_COMMENTS = True  # 确保开启评论爬取
```

#### 获取最新 Cookie
1. 打开浏览器，登录小红书
2. 按 F12 打开开发者工具
3. 刷新页面，在 Network 标签找到请求
4. 复制 Cookie 值更新到配置文件

### 5️⃣ 测试部署

#### 本地测试
```bash
# 测试 Telegram 连接
python scripts/test_telegram.py --token YOUR_TOKEN --chat-id YOUR_CHAT_ID

# 测试完整流程
python scripts/test_automation.py --skip-crawler --bot-token YOUR_TOKEN --chat-id YOUR_CHAT_ID
```

#### GitHub Actions 测试
1. 访问: https://github.com/roccohia/xhshh/actions
2. 选择 "小红书数据分析自动化任务"
3. 点击 "Run workflow" 手动触发
4. 查看运行日志确认无错误

### 6️⃣ 监控和维护

#### 查看运行状态
- **Actions 页面**: https://github.com/roccohia/xhshh/actions
- **运行时间**: 每天北京时间 9:00
- **运行时长**: 预计 10-20 分钟

#### 常见问题处理

**1. Cookie 过期**
- 症状: 爬虫失败，返回登录页面
- 解决: 更新 `base_config.py` 中的 COOKIES

**2. Telegram 推送失败**
- 症状: 分析成功但未收到消息
- 解决: 检查 BOT_TOKEN 和 CHAT_ID 是否正确

**3. 依赖安装失败**
- 症状: GitHub Actions 在安装依赖时失败
- 解决: 检查 `requirements.txt` 格式

## 📱 预期结果

### 每日推送内容
你将在每天早上 9:00 收到包含以下内容的 Telegram 消息：

1. **📊 汇总消息**
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

2. **📁 附件文件**
- ☁️ 词云图 (PNG)
- 📅 Notion 内容日历 (CSV)
- 👥 KOC 用户列表 (CSV)
- 💡 选题建议 (CSV)
- 📋 详细分析报告 (TXT)

### 文件用途
- **词云图**: 直观查看热门关键词
- **Notion日历**: 导入 Notion 进行内容规划
- **KOC列表**: 寻找合作的优质用户
- **选题建议**: 获取数据驱动的内容创意
- **分析报告**: 了解详细的数据洞察

## 🔧 自定义配置

### 修改爬取关键词
编辑 `.github/workflows/daily_run.yml`:
```yaml
python scripts/run_crawler_enhanced.py --keyword "普拉提,健身,瑜伽,减肥" --limit 150
```

### 调整运行时间
修改 cron 表达式:
```yaml
schedule:
  # 每天北京时间 8:00 运行 (UTC 0:00)
  - cron: '0 0 * * *'
```

### 增加分析天数
修改 Notion 日历生成:
```yaml
python analysis/export_notionsheet.py --days 45
```

## 🚨 注意事项

### 1. 资源限制
- GitHub Actions 免费账户: 2000分钟/月
- 单次运行预计: 10-20分钟
- 每月可运行约 100-200 次

### 2. 数据合规
- 仅用于个人学习研究
- 遵守小红书使用条款
- 控制爬取频率和数量

### 3. 安全性
- 不要在代码中硬编码敏感信息
- 定期更换 Telegram Bot Token
- 及时更新过期的 Cookie

## 🎯 成功指标

部署成功后，你应该能够：
- ✅ 每天自动收到 Telegram 推送
- ✅ 获取最新的小红书数据分析
- ✅ 直接使用 Notion 内容日历
- ✅ 基于数据制定内容策略

## 🆘 故障排除

### 查看日志
1. 进入 Actions 页面
2. 点击最近的运行记录
3. 展开各个步骤查看详细日志

### 常用调试命令
```bash
# 本地测试爬虫
python scripts/run_crawler_enhanced.py --keyword "测试" --limit 10

# 测试分析流程
python analysis/run_analysis_simple.py --input latest

# 测试 Telegram 推送
python scripts/telegram_push.py --token TOKEN --chat-id CHAT_ID
```

## 🎉 部署完成

完成以上步骤后，你的自动化系统将：
- 🤖 每天自动运行数据分析
- 📱 实时推送结果到 Telegram
- 📊 提供数据驱动的内容洞察
- 🔄 持续监控小红书趋势

**祝贺！你现在拥有了一个完全自动化的小红书数据分析系统！** 🎊
