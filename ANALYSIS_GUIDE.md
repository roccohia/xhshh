# 📊 小红书数据分析模块使用指南

基于爬取的小红书笔记数据，提供4个专业的数据分析功能模块。

## 🎯 功能概览

| 模块 | 功能 | 输出文件 |
|------|------|----------|
| 🔍 关键词分析 | 分析标题关键词频率，生成词云图 | CSV + PNG + 趋势分析 |
| 🏆 竞品分析 | 分析互动数据，识别高质量内容 | CSV + PNG + 报告 |
| 👥 KOC 筛选 | 筛选高互动中等粉丝的 KOC 用户 | CSV + PNG + 报告 |
| 💡 选题辅助 | 分析标题模式，生成选题建议 | CSV + JSON + 内容日历 |

## 🚀 快速开始

### 一键运行所有分析 (推荐)

```bash
# 运行所有分析模块
python analysis/run_analysis_simple.py --input core/media_crawler/data/xhs/1_search_contents_2025-07-02.csv

# 自定义输出目录
python analysis/run_analysis_simple.py --input data.csv --output-dir my_analysis
```

### 单独运行各模块

```bash
# 1. 关键词分析
python analysis/keyword_analysis.py --input data.csv --top-n 30

# 2. 竞品分析
python analysis/competitor_analysis.py --input data.csv --top-n 20

# 3. KOC 筛选
python analysis/koc_filter.py --input data.csv --min-likes 200 --max-followers 50000

# 4. 选题辅助 (支持 OpenAI)
python analysis/topic_generator.py --input data.csv --api-key your_openai_key
```

## 📋 详细功能说明

### 1️⃣ 关键词分析 (keyword_analysis.py)

**功能：**
- 使用 jieba 分词分析笔记标题
- 统计关键词出现频率
- 生成词云图可视化
- 分析关键词时间趋势

**输出文件：**
- `keywords_analysis_*.csv` - 关键词频率排行
- `wordcloud_*.png` - 词云图
- `keyword_trends.csv` - 关键词趋势分析

**示例结果：**
```
排名  关键词    出现次数
1     普拉提    30
2     运动      6
3     区别      5
4     瑜伽      4
```

### 2️⃣ 竞品分析 (competitor_analysis.py)

**功能：**
- 计算互动率、收藏率等指标
- 自动分类内容类型（体验/教程/种草等）
- 识别高表现内容
- 分析发布时间模式

**输出文件：**
- `competitor_analysis_*.csv` - 完整竞品分析
- `high_engagement_*.csv` - 高互动内容
- `engagement_analysis_*.png` - 互动分析图表
- `competitor_report_*.txt` - 分析报告

**内容类型分类：**
- 亲身体验类
- 教程指导类
- 种草推荐类
- 对比测评类
- 知识科普类
- 打卡分享类

### 3️⃣ KOC 筛选 (koc_filter.py)

**功能：**
- 估算用户粉丝数
- 计算 KOC 评分
- 筛选高互动中等粉丝用户
- 分析用户类型分布

**筛选条件：**
- 平均点赞数 > 200 (可调)
- 估算粉丝数 < 50000 (可调)
- 互动率 > 2% (可调)
- 发布数量 >= 2

**输出文件：**
- `koc_users_*.csv` - KOC 用户列表
- `all_users_stats_*.csv` - 所有用户统计
- `koc_analysis_*.png` - KOC 分析图表
- `koc_analysis_report_*.txt` - KOC 分析报告

**示例结果：**
```
昵称                    用户类型    粉丝数    KOC评分    平均互动
普拉提视频搬运工        优质KOC     40687     83.0       976.0
皓东潜制序体态控制学    优质KOC     22406     65.5       537.0
```

### 4️⃣ 选题辅助 (topic_generator.py)

**功能：**
- 分析高互动标题模式
- 识别标题结构类型
- 生成选题建议模板
- 创建30天内容日历
- 支持 OpenAI GPT 深度分析

**标题模式类型：**
- 数字型：包含具体数字
- 疑问型：包含疑问词
- 对比型：包含对比元素
- 体验型：强调亲身体验
- 教程型：提供指导内容

**输出文件：**
- `topic_suggestions_*.csv` - 选题建议
- `content_calendar_*.csv` - 30天内容日历
- `title_patterns_*.json` - 标题模式分析
- `topic_analysis_report_*.txt` - 选题分析报告
- `ai_analysis_*.json` - AI 分析结果 (如果启用)

**示例选题建议：**
```
类型          模板                              互动潜力
数字型内容    X个/X种/X天 + 核心内容 + 效果描述    高
对比测评类    A vs B + 对比维度 + 结论建议        高
疑问引导类    疑问词 + 核心问题 + 解答预期        中高
体验分享类    亲测/体验 + 产品/方法 + 真实感受    高
```

## 📁 输出文件结构

```
output/
├── keywords_analysis_*.csv      # 关键词分析
├── wordcloud_*.png             # 词云图
├── keyword_trends.csv          # 关键词趋势
├── competitor_analysis_*.csv   # 竞品分析
├── high_engagement_*.csv       # 高互动内容
├── engagement_analysis_*.png   # 互动图表
├── koc_users_*.csv            # KOC 用户列表
├── koc_analysis_*.png         # KOC 分析图表
├── topic_suggestions_*.csv    # 选题建议
├── content_calendar_*.csv     # 内容日历
└── *_report_*.txt            # 各种分析报告
```

## ⚙️ 高级配置

### OpenAI 集成 (选题分析)

```bash
# 设置环境变量
export OPENAI_API_KEY="your_api_key"

# 或使用参数
python analysis/topic_generator.py --input data.csv --api-key your_key --model gpt-4
```

### 自定义参数

```bash
# 关键词分析 - 提取更多关键词
python analysis/keyword_analysis.py --input data.csv --top-n 50 --max-words 200

# 竞品分析 - 分析更多高表现内容
python analysis/competitor_analysis.py --input data.csv --top-n 30

# KOC 筛选 - 调整筛选条件
python analysis/koc_filter.py --input data.csv --min-likes 300 --max-followers 30000 --min-engagement-rate 3.0

# 选题分析 - 生成更长的内容日历
python analysis/topic_generator.py --input data.csv --calendar-days 60
```

## 📊 实际应用场景

### 1. 内容策划
- 使用关键词分析了解热门话题
- 通过选题辅助生成内容日历
- 参考高互动标题模式

### 2. 竞品研究
- 分析竞品内容类型分布
- 识别高表现内容特征
- 了解发布时间规律

### 3. KOC 合作
- 筛选优质 KOC 用户
- 评估 KOC 影响力
- 制定合作策略

### 4. 数据驱动决策
- 基于数据优化内容策略
- 跟踪关键词趋势变化
- 监控竞品动态

## 🔧 依赖安装

```bash
# 安装必需依赖
pip install pandas jieba wordcloud matplotlib seaborn numpy

# 可选：OpenAI 支持
pip install openai
```

## 💡 使用建议

1. **数据质量**：确保输入的 CSV 文件包含完整的字段
2. **参数调优**：根据实际需求调整各模块的参数
3. **定期分析**：建议定期运行分析，跟踪趋势变化
4. **结合使用**：多个模块结合使用效果更佳
5. **AI 增强**：有条件建议使用 OpenAI 进行深度分析

## 🎉 总结

这套数据分析模块为小红书内容运营提供了完整的数据支持，从关键词洞察到选题建议，从竞品分析到 KOC 筛选，帮助你做出更明智的内容决策！
