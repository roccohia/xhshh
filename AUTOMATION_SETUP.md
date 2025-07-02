# 🤖 GitHub Actions 自动化部署指南

## 📋 系统概览

这个自动化系统将每天北京时间 9:00 自动执行以下流程：
1. 🕷️ 爬取小红书数据
2. 📊 运行数据分析
3. 📅 生成 Notion 内容日历
4. 📱 推送结果到 Telegram

## 🔧 部署步骤

### 1️⃣ 创建 Telegram Bot

#### 创建 Bot
1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot` 命令
3. 按提示设置 Bot 名称和用户名
4. 获取 Bot Token（格式：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）

#### 获取 Chat ID
1. 将 Bot 添加到你的聊天中
2. 发送任意消息给 Bot
3. 访问：`https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. 在返回的 JSON 中找到 `chat.id` 字段

### 2️⃣ 配置 GitHub Secrets

在你的 GitHub 仓库中设置以下 Secrets：

1. 进入仓库 → Settings → Secrets and variables → Actions
2. 点击 "New repository secret" 添加：

| Secret 名称 | 值 | 说明 |
|-------------|----|----|
| `BOT_TOKEN` | 你的 Telegram Bot Token | 用于发送消息 |
| `CHAT_ID` | 你的 Telegram Chat ID | 接收消息的聊天 |

### 3️⃣ 启用 GitHub Actions

1. 确保 `.github/workflows/daily_run.yml` 文件已提交
2. 进入仓库 → Actions 页面
3. 如果看到工作流，点击启用
4. 工作流将在每天北京时间 9:00 自动运行

### 4️⃣ 手动测试

#### 测试 Telegram 连接
```bash
# 安装依赖
pip install python-telegram-bot

# 测试连接
python scripts/test_telegram.py --token YOUR_BOT_TOKEN --chat-id YOUR_CHAT_ID
```

#### 测试完整流程
```bash
# 本地测试（不包含 Telegram）
python scripts/test_automation.py --skip-crawler

# 完整测试（包含 Telegram）
python scripts/test_automation.py --bot-token YOUR_TOKEN --chat-id YOUR_CHAT_ID
```

#### 手动触发 GitHub Actions
1. 进入仓库 → Actions
2. 选择 "小红书数据分析自动化任务"
3. 点击 "Run workflow"

## 📊 工作流详情

### 触发条件
- **定时触发**: 每天北京时间 9:00 (UTC 1:00)
- **手动触发**: 在 Actions 页面手动运行

### 执行步骤
1. **环境准备**: 设置 Python 3.10 环境
2. **依赖安装**: 安装 requirements.txt 中的依赖
3. **数据爬取**: 爬取关键词相关的小红书内容
4. **数据分析**: 运行 4 个分析模块
5. **日历生成**: 生成 Notion 内容日历
6. **结果推送**: 发送分析结果到 Telegram
7. **文件清理**: 清理旧文件，保持存储空间

### 错误处理
- 每个步骤都有错误处理，单步失败不会中断整个流程
- 失败的步骤会记录日志，便于排查问题
- 分析结果会上传为 Artifacts，保留 7 天

## 📱 Telegram 推送内容

### 推送文件类型
1. **☁️ 词云图** (PNG) - 关键词可视化
2. **📅 Notion 内容日历** (CSV) - 可直接导入 Notion
3. **👥 KOC 用户列表** (CSV) - 筛选出的优质用户
4. **💡 选题建议** (CSV) - 内容创作建议
5. **📋 分析报告** (TXT) - 详细分析结果

### 消息格式示例
```
🤖 小红书数据分析报告
📅 生成时间: 2025-07-02 09:00:00

📊 本次分析生成了 5 个文件:

🔤 关键词分析: keywords_analysis_20250702_090000.csv
☁️ 词云图: wordcloud_20250702_090000.png
🏆 竞品分析: competitor_analysis_20250702_090000.csv
👥 KOC用户筛选: koc_users_20250702_090000.csv
💡 选题建议: topic_suggestions_20250702_090000.csv

🎯 分析完成，请查看附件获取详细结果！
```

## 🔍 监控和维护

### 查看运行状态
1. 进入 GitHub 仓库 → Actions
2. 查看最近的工作流运行记录
3. 点击具体运行查看详细日志

### 常见问题排查

#### 1. 爬虫失败
- **原因**: Cookie 过期、网络问题、反爬机制
- **解决**: 更新 Cookie 配置，调整爬取频率

#### 2. 分析失败
- **原因**: 数据格式问题、依赖缺失
- **解决**: 检查数据文件，更新依赖版本

#### 3. Telegram 推送失败
- **原因**: Token 错误、网络问题、文件过大
- **解决**: 验证 Token 和 Chat ID，检查文件大小

### 日志查看
- **GitHub Actions 日志**: 在 Actions 页面查看
- **本地日志**: `logs/` 目录下的日志文件
- **Telegram 推送日志**: `logs/telegram_push.log`

## ⚙️ 自定义配置

### 修改运行时间
编辑 `.github/workflows/daily_run.yml` 中的 cron 表达式：
```yaml
schedule:
  # 每天北京时间 8:00 运行 (UTC 0:00)
  - cron: '0 0 * * *'
```

### 修改爬取关键词
编辑工作流文件中的关键词参数：
```yaml
python scripts/run_crawler_enhanced.py --keyword "瑜伽,健身,减肥" --limit 200
```

### 调整分析参数
修改分析脚本的参数：
```yaml
python analysis/export_notionsheet.py --days 45
```

## 🚨 注意事项

### 1. 资源限制
- GitHub Actions 免费账户每月有 2000 分钟限制
- 单次运行预计消耗 10-20 分钟
- 建议监控使用量，避免超限

### 2. 数据安全
- 不要在代码中硬编码敏感信息
- 使用 GitHub Secrets 存储 Token
- 定期更换 Bot Token

### 3. 合规使用
- 遵守小红书的使用条款
- 控制爬取频率，避免对服务器造成压力
- 仅用于个人学习和研究目的

### 4. 存储管理
- 定期清理旧的分析文件
- Artifacts 自动保留 7 天
- 可以下载重要的分析结果进行备份

## 🎯 扩展功能

### 1. 多关键词轮换
可以配置每天爬取不同的关键词：
```python
keywords_by_day = {
    0: "普拉提,瑜伽",      # 周一
    1: "健身,减肥",        # 周二
    2: "运动,塑形",        # 周三
    # ...
}
```

### 2. 结果对比
保存历史数据，进行趋势对比分析

### 3. 多平台推送
除了 Telegram，还可以推送到微信、邮箱等

### 4. 智能调度
根据数据质量动态调整爬取策略

## 🎉 总结

这个自动化系统将帮助你：
- 📊 **持续监控**: 每天自动获取最新数据
- 🎯 **精准分析**: 多维度数据分析和洞察
- 📱 **即时通知**: 第一时间获取分析结果
- 🔄 **无人值守**: 完全自动化运行

设置完成后，你将每天早上收到前一天的小红书数据分析报告，为内容创作提供数据支持！
