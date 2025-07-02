@echo off
chcp 65001 >nul
echo 🚀 开始部署到 GitHub 仓库...
echo 📁 仓库地址: https://github.com/roccohia/xhshh

REM 检查是否在正确的目录
if not exist "requirements.txt" (
    echo ❌ 错误: 请在项目根目录运行此脚本
    pause
    exit /b 1
)

REM 检查 git 是否已初始化
if not exist ".git" (
    echo 🔧 初始化 Git 仓库...
    git init
    git remote add origin https://github.com/roccohia/xhshh.git
) else (
    echo ✅ Git 仓库已存在
)

REM 检查关键文件
echo 📋 检查关键文件...
set "missing_files="

if exist ".github\workflows\daily_run.yml" (
    echo ✅ .github\workflows\daily_run.yml
) else (
    echo ❌ .github\workflows\daily_run.yml ^(缺失^)
    set "missing_files=1"
)

if exist "requirements.txt" (
    echo ✅ requirements.txt
) else (
    echo ❌ requirements.txt ^(缺失^)
    set "missing_files=1"
)

if exist "scripts\telegram_push.py" (
    echo ✅ scripts\telegram_push.py
) else (
    echo ❌ scripts\telegram_push.py ^(缺失^)
    set "missing_files=1"
)

if exist "analysis\run_analysis_simple.py" (
    echo ✅ analysis\run_analysis_simple.py
) else (
    echo ❌ analysis\run_analysis_simple.py ^(缺失^)
    set "missing_files=1"
)

if exist "analysis\export_notionsheet.py" (
    echo ✅ analysis\export_notionsheet.py
) else (
    echo ❌ analysis\export_notionsheet.py ^(缺失^)
    set "missing_files=1"
)

if defined missing_files (
    echo ⚠️  警告: 发现缺失文件，但继续部署...
)

REM 创建 .gitignore 文件
echo 📝 创建 .gitignore...
(
echo # Python
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo build/
echo develop-eggs/
echo dist/
echo downloads/
echo eggs/
echo .eggs/
echo lib/
echo lib64/
echo parts/
echo sdist/
echo var/
echo wheels/
echo *.egg-info/
echo .installed.cfg
echo *.egg
echo.
echo # 虚拟环境
echo venv/
echo env/
echo ENV/
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo.
echo # 日志文件
echo logs/
echo *.log
echo.
echo # 数据文件
echo core/media_crawler/data/
echo output/
echo *.csv
echo *.json
echo *.png
echo.
echo # 配置文件中的敏感信息
echo *_user_data_dir/
echo.
echo # 系统文件
echo .DS_Store
echo Thumbs.db
echo.
echo # 临时文件
echo *.tmp
echo *.temp
) > .gitignore

REM 添加所有文件
echo 📦 添加文件到 Git...
git add .

REM 提交变更
echo 💾 提交变更...
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

REM 推送到 GitHub
echo 🚀 推送到 GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo ✅ 成功推送到 GitHub!
) else (
    echo ⚠️  推送可能遇到问题，请检查网络连接和权限
)

echo.
echo 🎉 部署完成!
echo.
echo 📋 接下来的步骤:
echo 1. 访问 https://github.com/roccohia/xhshh/settings/secrets/actions
echo 2. 添加 GitHub Secrets:
echo    - BOT_TOKEN: 你的 Telegram Bot Token
echo    - CHAT_ID: 你的 Telegram Chat ID
echo 3. 创建 Telegram Bot ^(如果还没有^):
echo    - 找 @BotFather 创建 Bot
echo    - 获取 Token 和 Chat ID
echo 4. 更新小红书 Cookie ^(core/media_crawler/config/base_config.py^)
echo 5. 测试运行:
echo    - 访问 https://github.com/roccohia/xhshh/actions
echo    - 手动触发工作流测试
echo.
echo 📖 详细说明请查看 DEPLOY_TO_GITHUB.md
echo 🎯 系统将在每天北京时间 9:00 自动运行!
echo.
pause
