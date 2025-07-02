# ✅ GitHub 部署检查清单

## 📋 部署前检查

### 🔧 本地环境检查
- [ ] Python 3.10+ 已安装
- [ ] Git 已安装并配置
- [ ] 项目文件完整
- [ ] 依赖库已安装 (`pip install -r requirements.txt`)

### 📁 关键文件检查
- [ ] `.github/workflows/daily_run.yml` - GitHub Actions 工作流
- [ ] `requirements.txt` - 完整依赖列表
- [ ] `scripts/telegram_push.py` - Telegram 推送脚本
- [ ] `analysis/run_analysis_simple.py` - 支持 latest 参数
- [ ] `analysis/export_notionsheet.py` - Notion 导出功能
- [ ] 所有分析模块文件 (keyword_analysis.py, competitor_analysis.py 等)

### 🤖 Telegram Bot 准备
- [ ] 已创建 Telegram Bot (@BotFather)
- [ ] 获得 Bot Token
- [ ] 获得 Chat ID
- [ ] 测试 Bot 连接成功

## 🚀 部署步骤

### 1️⃣ 推送代码到 GitHub
```bash
# 使用自动部署脚本 (推荐)
./deploy_to_github.sh    # Linux/Mac
deploy_to_github.bat     # Windows

# 或手动执行
git init
git remote add origin https://github.com/roccohia/xhshh.git
git add .
git commit -m "🎉 部署小红书数据分析自动化系统"
git push -u origin main
```

### 2️⃣ 配置 GitHub Secrets
访问: https://github.com/roccohia/xhshh/settings/secrets/actions

添加以下 Secrets:
- [ ] `BOT_TOKEN`: 你的 Telegram Bot Token
- [ ] `CHAT_ID`: 你的 Telegram Chat ID

### 3️⃣ 更新小红书 Cookie
编辑 `core/media_crawler/config/base_config.py`:
- [ ] 更新 COOKIES 字段为最新有效值
- [ ] 确认 SAVE_DATA_OPTION = "csv"
- [ ] 设置合适的 CRAWLER_MAX_NOTES_COUNT

### 4️⃣ 启用 GitHub Actions
- [ ] 访问 https://github.com/roccohia/xhshh/actions
- [ ] 确认工作流已启用
- [ ] 手动触发测试运行

## 🧪 测试验证

### 本地测试
```bash
# 测试 Telegram 连接
python scripts/test_telegram.py --token YOUR_TOKEN --chat-id YOUR_CHAT_ID

# 测试完整流程
python scripts/test_automation.py --skip-crawler --bot-token YOUR_TOKEN --chat-id YOUR_CHAT_ID

# 测试文件识别
python analysis/run_analysis_simple.py --input latest
```

### GitHub Actions 测试
- [ ] 手动触发工作流
- [ ] 检查所有步骤是否成功
- [ ] 确认 Telegram 收到推送消息
- [ ] 验证附件文件完整

## 📱 预期结果

### 每日自动运行
- [ ] 每天北京时间 9:00 自动触发
- [ ] 爬取指定关键词的小红书数据
- [ ] 运行 4 个分析模块
- [ ] 生成 Notion 内容日历
- [ ] 推送结果到 Telegram

### Telegram 推送内容
- [ ] 汇总消息 (文本)
- [ ] 词云图 (PNG)
- [ ] Notion 内容日历 (CSV)
- [ ] KOC 用户列表 (CSV)
- [ ] 选题建议 (CSV)
- [ ] 分析报告 (TXT)

## 🔧 故障排除

### 常见问题检查

#### 爬虫失败
- [ ] Cookie 是否过期
- [ ] 网络连接是否正常
- [ ] 关键词是否合适

#### 分析失败
- [ ] 数据文件是否存在
- [ ] 文件格式是否正确
- [ ] 依赖库是否完整

#### Telegram 推送失败
- [ ] Bot Token 是否正确
- [ ] Chat ID 是否正确
- [ ] 网络是否可达 Telegram API

#### GitHub Actions 失败
- [ ] Secrets 是否正确配置
- [ ] 工作流文件语法是否正确
- [ ] 依赖安装是否成功

### 调试方法
```bash
# 查看 GitHub Actions 日志
# 访问: https://github.com/roccohia/xhshh/actions

# 本地调试
python scripts/test_automation.py --help

# 检查文件权限
ls -la scripts/
chmod +x scripts/*.py
```

## 📊 监控指标

### 成功指标
- [ ] 每日成功运行 (GitHub Actions 绿色)
- [ ] Telegram 消息正常接收
- [ ] 分析文件正常生成
- [ ] 数据质量符合预期

### 性能指标
- [ ] 运行时间 < 20 分钟
- [ ] 爬取成功率 > 80%
- [ ] 文件生成完整率 100%
- [ ] Telegram 推送成功率 > 95%

## 🔄 维护计划

### 每周检查
- [ ] 查看 GitHub Actions 运行状态
- [ ] 检查 Telegram 推送是否正常
- [ ] 验证数据质量

### 每月维护
- [ ] 更新小红书 Cookie
- [ ] 检查依赖库版本
- [ ] 清理旧的分析文件
- [ ] 优化关键词配置

### 按需更新
- [ ] 调整爬取关键词
- [ ] 修改运行时间
- [ ] 增加新的分析功能
- [ ] 优化推送内容

## 🎯 优化建议

### 短期优化
- [ ] 增加错误重试机制
- [ ] 优化文件命名规则
- [ ] 添加更多可视化图表
- [ ] 改进 Telegram 消息格式

### 长期规划
- [ ] 支持多平台数据源
- [ ] 增加 AI 分析功能
- [ ] 开发 Web 界面
- [ ] 添加数据库存储

## ✅ 部署完成确认

完成以下所有项目即表示部署成功:

- [ ] 代码已推送到 GitHub
- [ ] GitHub Secrets 已配置
- [ ] Cookie 已更新
- [ ] GitHub Actions 已启用
- [ ] 本地测试通过
- [ ] GitHub Actions 测试通过
- [ ] Telegram 推送正常
- [ ] 所有文件正常生成

## 🎉 部署成功！

恭喜！你的小红书数据分析自动化系统已经成功部署！

从现在开始，你将每天早上 9:00 收到基于最新数据的分析报告，为内容创作和营销决策提供强有力的数据支持！

---

📞 **需要帮助？**
- 查看详细文档: [DEPLOY_TO_GITHUB.md](DEPLOY_TO_GITHUB.md)
- 提交 Issue: https://github.com/roccohia/xhshh/issues
- 查看运行日志: https://github.com/roccohia/xhshh/actions
