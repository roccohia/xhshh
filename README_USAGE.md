# 小红书笔记爬虫使用指南

基于 MediaCrawler 改造的小红书笔记爬虫，支持通过命令行传入关键词和数量，使用 Cookie 模拟登录，输出 CSV 格式数据。

## 🚀 快速开始

### 🎯 一键启动 (推荐)

```bash
# 运行快速启动工具，包含所有功能
python scripts/quick_start.py
```

这个工具提供了图形化菜单，包括：
- 🍪 Cookie 更新
- 🧪 Cookie 测试
- 🕷️ 爬虫运行
- 📁 结果查看

### 1. 环境准备

确保已安装 Python 3.7+ 和必要的依赖：

```bash
# 安装依赖
pip install -r core/media_crawler/requirements.txt

# 安装 Playwright 浏览器
python -m playwright install chromium
```

### 2. 配置 Cookie

编辑 `config/xhs_config.json` 文件，更新你的小红书 Cookie：

```json
{
    "platform": "xiaohongshu",
    "cookie": {
        "a1": "你的a1值",
        "web_session": "你的web_session值",
        "webId": "你的webId值",
        "gid": "你的gid值",
        "acw_tc": "你的acw_tc值"
    },
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
}
```

#### 获取 Cookie 的步骤：
1. 打开浏览器，访问 https://www.xiaohongshu.com
2. 登录你的账号
3. 按 F12 打开开发者工具
4. 在 Application/Storage 标签页中找到 Cookies
5. 复制需要的 Cookie 值到配置文件

### 3. 更新 Cookie (简化方式)

```bash
# 使用 Cookie 更新工具
python scripts/update_cookie.py
```

按照提示粘贴你的 Cookie 字符串即可自动更新配置。

### 4. 运行爬虫

```bash
# 基础版爬虫
python scripts/run_crawler.py --keyword "普拉提" --limit 50

# 增强版爬虫 (推荐，支持重试和验证码处理)
python scripts/run_crawler_enhanced.py --keyword "普拉提" --limit 50 --retries 5

# 多关键词搜索
python scripts/run_crawler_enhanced.py --keyword "普拉提,瑜伽,健身" --limit 100
```

### 5. 测试 Cookie 有效性

```bash
python scripts/test_cookie.py
```

## 📁 项目结构

```
xhs_source/
├── config/
│   └── xhs_config.json          # 配置文件
├── scripts/
│   ├── quick_start.py           # 🎯 快速启动工具 (推荐)
│   ├── run_crawler.py           # 基础版爬虫
│   ├── run_crawler_enhanced.py  # 增强版爬虫 (支持重试)
│   ├── update_cookie.py         # Cookie 更新工具
│   ├── test_cookie.py           # Cookie 测试工具
│   └── config_manager.py        # 配置管理器
├── core/
│   └── media_crawler/           # MediaCrawler 核心代码
└── README_USAGE.md              # 使用说明
```

## 🔧 核心功能

### ✅ 已实现功能

1. **命令行参数支持**：通过 `--keyword` 和 `--limit` 传入搜索参数
2. **Cookie 登录**：使用配置文件中的 Cookie 模拟登录状态
3. **配置管理**：动态配置 MediaCrawler，避免修改源码文件
4. **CSV 输出**：爬取的数据自动保存为 CSV 格式
5. **错误处理**：完善的错误提示和异常处理
6. **Cookie 验证**：提供 Cookie 有效性测试工具

### 📊 输出数据字段

CSV 文件包含以下字段：
- 标题 (title)
- 点赞数 (liked_count)
- 收藏数 (collected_count)
- 评论数 (comment_count)
- 分享数 (share_count)
- 用户ID (user_id)
- 用户昵称 (nickname)
- 发布时间 (time)
- 笔记链接 (note_url)

## ⚠️ 注意事项

### Cookie 管理
- Cookie 有时效性，需要定期更新
- 如果遇到验证码，说明 Cookie 可能已过期
- 建议使用最新的浏览器获取 Cookie

### 反爬虫应对
- 程序会自动打开浏览器窗口，便于手动处理验证码
- 如果遇到滑动验证码，请在浏览器中手动完成
- 建议控制爬取频率，避免触发反爬虫机制

### 数据输出
- 数据保存在 `core/media_crawler/data/xhs/` 目录
- 文件名格式：`{序号}_xhs_search_posts_{时间戳}.csv`
- 每次运行会生成新的文件，避免数据覆盖

## 🐛 常见问题

### 1. 依赖安装失败
```bash
# 如果 pip 安装失败，尝试使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r core/media_crawler/requirements.txt
```

### 2. 浏览器启动失败
```bash
# 重新安装 Playwright 浏览器
python -m playwright install --force chromium
```

### 3. Cookie 验证失败
- 确保 Cookie 是最新的
- 检查是否包含所有必要字段
- 尝试重新登录获取新的 Cookie

### 4. 验证码问题
- 程序会自动打开浏览器
- 在浏览器中手动完成验证码
- 验证完成后程序会自动继续

## 📈 使用建议

1. **首次使用**：先运行 `test_cookie.py` 验证 Cookie 有效性
2. **小批量测试**：建议先用小数量（如 5-10）测试
3. **定期更新**：定期更新 Cookie 和 User-Agent
4. **合理使用**：遵守平台规则，控制爬取频率

## 🔄 更新日志

- ✅ 修复了 base_config.py 语法错误
- ✅ 重构了配置管理机制
- ✅ 优化了 run_crawler.py 脚本
- ✅ 添加了 Cookie 验证工具
- ✅ 完善了错误处理和用户提示
