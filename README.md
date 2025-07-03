# 🚀 小红书数据分析系统

一个功能完整、技术先进的小红书数据爬取和分析系统，支持关键词搜索、KOC筛选、数据可视化和全自动化报告推送。

## ✨ 核心特色

### 🔥 强大的数据爬取能力
- **多策略爬虫**: requests + selenium + API逆向，确保数据获取成功率
- **智能代理轮换**: 3个国内高速代理服务器，避免IP封禁
- **反爬虫对抗**: User-Agent轮换、随机请求间隔、Cookie自动管理
- **容错机制**: 完善的异常处理和自动重试，确保系统稳定运行

### 📊 专业的数据分析功能
- **中文关键词分析**: jieba分词 + 自定义词典，精准提取热门关键词
- **KOC智能筛选**: 基于粉丝数和互动数的精确分级系统
- **竞品深度分析**: 多维度数据对比和趋势分析
- **数据可视化**: 高质量词云图、互动分析图表、KOC分布图

### 🤖 全自动化工作流
- **GitHub Actions**: 每日北京时间9:00自动运行，无需人工干预
- **Telegram智能推送**: 实时推送分析报告和系统状态
- **多格式输出**: CSV数据、PNG图片、TXT报告，满足不同需求

## 🏗️ 系统架构

```
📦 xhs_source/
├── 🔄 .github/workflows/          # 自动化工作流
│   └── daily_run.yml             # 每日定时任务配置
├── 📈 analysis/                   # 数据分析核心模块
│   ├── keyword_analysis.py       # 关键词分析引擎
│   ├── koc_filter.py             # KOC智能筛选器
│   ├── competitor_analysis.py    # 竞品分析工具
│   └── topic_generator.py        # AI话题生成器
├── 🕷️ scripts/                    # 爬虫脚本集合
│   ├── xhs_crawler_direct.py     # 主力爬虫引擎
│   ├── telegram_push.py          # Telegram推送服务
│   └── config_manager.py         # 配置管理工具
├── ⚙️ core/media_crawler/         # 核心爬虫框架
│   └── config/                   # 系统配置中心
├── 📊 output/                     # 分析结果输出
└── 📋 requirements.txt           # 依赖管理
```

## 🚀 快速部署

### 第1步: 环境准备

```bash
# 克隆项目到本地
git clone https://github.com/roccohia/xhshh.git
cd xhshh

# 安装Python依赖
pip install -r requirements.txt
```

### 第2步: 配置设置

编辑 `core/media_crawler/config/base_config.py`:

```python
# 🍪 更新小红书Cookie（重要！）
COOKIES = "你的最新小红书Cookie"

# 🔍 配置搜索关键词
KEYWORDS = ["普拉提", "健身", "瑜伽", "减肥", "运动"]

# 📊 设置分析参数
MIN_LIKES = 200        # KOC筛选最低点赞数
MAX_FOLLOWERS = 10000  # KOC最大粉丝数
```

### 第3步: 本地测试

```bash
# 🕷️ 测试数据爬取
python scripts/xhs_crawler_direct.py

# 📊 测试关键词分析
python analysis/keyword_analysis.py --input core/media_crawler/data/xhs/latest.csv

# 👥 测试KOC分析
python analysis/koc_filter.py --input core/media_crawler/data/xhs/latest.csv --min-likes 200
```

### 第4步: 自动化部署

1. **设置GitHub Secrets**:
   - `TELEGRAM_BOT_TOKEN`: 你的Telegram Bot Token
   - `TELEGRAM_CHAT_ID`: 接收报告的Chat ID

2. **启用GitHub Actions**:
   - 推送代码后自动启用
   - 每日北京时间9:00自动运行
   - 支持手动触发执行

## 📊 核心分析功能

### 🔍 关键词分析引擎
- **智能分词**: 使用jieba分词，支持自定义词典
- **热度排序**: 按出现频率和重要性排序
- **词云生成**: 生成高质量中文词云图
- **趋势分析**: 跟踪关键词热度变化

### 👥 KOC智能筛选系统
- **🥉 KOC级别**: <1,000粉丝，高互动率
- **🥈 Nano KOL**: 1,000-3,999粉丝 + 10K-49K总互动
- **🥇 Micro KOL**: 4,000-10,000粉丝 + 50K-99K总互动  
- **💎 Macro KOL**: 10,000+粉丝 + 100K+总互动

### 📈 数据可视化
- **词云图**: 美观的中文词云，支持自定义颜色
- **互动分析图**: 点赞、收藏、评论数据对比
- **KOC分布图**: 用户等级分布可视化
- **趋势图表**: 时间序列数据分析

## 🤖 自动化特性

### ⏰ 定时任务
- **每日执行**: 北京时间9:00自动运行
- **智能重试**: 失败时自动重试3次
- **状态监控**: 实时监控运行状态

### 📱 Telegram推送
系统每日自动推送：
- 📊 **数据分析报告**: 关键词热度、KOC发现
- 📈 **趋势变化**: 热门话题变化趋势
- 👥 **用户洞察**: 新发现的优质KOC
- ⚠️ **系统状态**: 运行状态和错误提醒

### 📁 输出管理
- **自动分类**: 按日期和类型自动分类文件
- **格式丰富**: CSV数据、PNG图片、TXT报告
- **云端存储**: 自动上传到GitHub，永久保存

## 📈 输出文件详解

### 📊 数据文件 (CSV)
- `keywords_analysis_YYYYMMDD_HHMMSS.csv`: 关键词分析结果
- `koc_users_YYYYMMDD_HHMMSS.csv`: 筛选出的KOC用户列表
- `competitor_analysis_YYYYMMDD_HHMMSS.csv`: 竞品对比数据

### 🖼️ 图片文件 (PNG)
- `wordcloud_YYYYMMDD_HHMMSS.png`: 关键词词云图
- `engagement_analysis_YYYYMMDD_HHMMSS.png`: 互动数据分析图
- `koc_analysis_YYYYMMDD_HHMMSS.png`: KOC分布分析图

### 📄 报告文件 (TXT)
- `koc_analysis_report_YYYYMMDD_HHMMSS.txt`: 详细KOC分析报告
- `competitor_report_YYYYMMDD_HHMMSS.txt`: 竞品分析报告

## ⚙️ 高级配置

### 🌐 代理服务器
系统内置3个高速国内代理，自动轮换：
```python
PROXY_SERVERS = [
    ("112.28.237.135", "35226", "username", "password"),
    ("112.28.237.136", "30010", "username", "password"),
    ("112.28.237.136", "39142", "username", "password")
]
```

### 🍪 Cookie管理
定期更新Cookie保持系统有效性：
```python
# 获取最新Cookie的方法：
# 1. 打开小红书网页版
# 2. 登录账号
# 3. F12打开开发者工具
# 4. 复制Cookie字符串
COOKIES = "a1=xxx; web_session=xxx; ..."
```

## 🔧 故障排除

### 常见问题解决

1. **Cookie失效**:
   ```bash
   # 更新Cookie后重新运行
   python scripts/update_cookie.py
   ```

2. **代理连接失败**:
   ```bash
   # 测试代理连接
   python scripts/test_proxy.py
   ```

3. **分析结果为空**:
   ```bash
   # 检查数据文件
   python scripts/check_data.py
   ```

## 📝 使用须知

⚠️ **重要提醒**:
1. **合规使用**: 严格遵守小红书平台使用条款
2. **频率控制**: 合理控制爬取频率，避免对平台造成压力
3. **数据保护**: 妥善保护用户隐私，不得滥用数据
4. **商业用途**: 商业使用前请确保符合相关法律法规

## 🤝 贡献指南

欢迎贡献代码和建议！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

## 📞 技术支持

- 🐛 **Bug报告**: [GitHub Issues](https://github.com/roccohia/xhshh/issues)
- 💡 **功能建议**: [GitHub Discussions](https://github.com/roccohia/xhshh/discussions)
- 📧 **技术交流**: 通过GitHub Issues联系

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个Star支持一下！ ⭐**

Made with ❤️ by [roccohia](https://github.com/roccohia)

</div>
