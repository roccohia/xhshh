#!/bin/bash
# 快速部署到 GitHub 脚本

echo "🚀 开始部署到 GitHub 仓库..."
echo "📁 仓库地址: https://github.com/roccohia/xhshh"

# 检查是否在正确的目录
if [ ! -f "requirements.txt" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查 git 是否已初始化
if [ ! -d ".git" ]; then
    echo "🔧 初始化 Git 仓库..."
    git init
    git remote add origin https://github.com/roccohia/xhshh.git
else
    echo "✅ Git 仓库已存在"
fi

# 检查关键文件
echo "📋 检查关键文件..."
files=(
    ".github/workflows/daily_run.yml"
    "requirements.txt"
    "scripts/telegram_push.py"
    "analysis/run_analysis_simple.py"
    "analysis/export_notionsheet.py"
)

missing_files=()
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (缺失)"
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "⚠️  警告: 发现缺失文件，但继续部署..."
fi

# 创建 .gitignore 文件
echo "📝 创建 .gitignore..."
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 虚拟环境
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 日志文件
logs/
*.log

# 数据文件
core/media_crawler/data/
output/
*.csv
*.json
*.png

# 配置文件中的敏感信息
*_user_data_dir/

# 系统文件
.DS_Store
Thumbs.db

# 临时文件
*.tmp
*.temp
EOF

# 添加所有文件
echo "📦 添加文件到 Git..."
git add .

# 检查是否有变更
if git diff --staged --quiet; then
    echo "ℹ️  没有新的变更需要提交"
else
    # 提交变更
    echo "💾 提交变更..."
    git commit -m "🎉 部署小红书数据分析自动化系统

✨ 新增功能:
- 🤖 GitHub Actions 自动化工作流
- 📊 完整的数据分析模块 (关键词、竞品、KOC、选题)
- 📱 Telegram 自动推送
- 📅 Notion 内容日历导出
- 🔧 完整的测试套件

🚀 系统特性:
- 每天北京时间 9:00 自动运行
- 支持多关键词爬取
- 智能数据分析和可视化
- 自动推送分析结果到 Telegram
- 生成可直接导入 Notion 的内容日历

📋 部署说明:
1. 配置 GitHub Secrets (BOT_TOKEN, CHAT_ID)
2. 创建 Telegram Bot
3. 更新小红书 Cookie
4. 启用 GitHub Actions

详细部署指南请查看 DEPLOY_TO_GITHUB.md"
fi

# 推送到 GitHub
echo "🚀 推送到 GitHub..."
if git push -u origin main; then
    echo "✅ 成功推送到 GitHub!"
else
    echo "⚠️  推送可能遇到问题，请检查网络连接和权限"
fi

echo ""
echo "🎉 部署完成!"
echo ""
echo "📋 接下来的步骤:"
echo "1. 访问 https://github.com/roccohia/xhshh/settings/secrets/actions"
echo "2. 添加 GitHub Secrets:"
echo "   - BOT_TOKEN: 你的 Telegram Bot Token"
echo "   - CHAT_ID: 你的 Telegram Chat ID"
echo "3. 创建 Telegram Bot (如果还没有):"
echo "   - 找 @BotFather 创建 Bot"
echo "   - 获取 Token 和 Chat ID"
echo "4. 更新小红书 Cookie (core/media_crawler/config/base_config.py)"
echo "5. 测试运行:"
echo "   - 访问 https://github.com/roccohia/xhshh/actions"
echo "   - 手动触发工作流测试"
echo ""
echo "📖 详细说明请查看 DEPLOY_TO_GITHUB.md"
echo "🎯 系统将在每天北京时间 9:00 自动运行!"
