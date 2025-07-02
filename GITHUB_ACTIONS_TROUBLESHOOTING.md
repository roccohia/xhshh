# 🔧 GitHub Actions 故障排除指南

## ✅ 已修复的问题

### 1. Actions 版本弃用问题 ✅
**问题**: `actions/upload-artifact@v3` 已弃用
**解决**: 已更新到 `v4` 版本

**问题**: `actions/setup-python@v4` 可能过时
**解决**: 已更新到 `v5` 版本

## 🔍 常见问题排查

### 1. Secrets 配置问题

#### 症状
```
Error: Input required and not supplied: token
```

#### 解决方案
1. 访问: https://github.com/roccohia/xhshh/settings/secrets/actions
2. 确认已添加以下 Secrets:
   - `BOT_TOKEN`: Telegram Bot Token
   - `CHAT_ID`: Telegram Chat ID

#### 验证方法
```bash
# 本地测试 Telegram 连接
python scripts/test_telegram.py --token YOUR_TOKEN --chat-id YOUR_CHAT_ID
```

### 2. 依赖安装失败

#### 症状
```
ERROR: Could not find a version that satisfies the requirement
```

#### 解决方案
检查 `requirements.txt` 文件格式：
```txt
# 确保没有重复的依赖
# 确保版本号格式正确
pandas>=1.3.0
requests>=2.25.0
```

### 3. 爬虫失败

#### 症状
```
未找到爬取数据，将使用示例数据
```

#### 可能原因
- Cookie 过期
- 网络连接问题
- 反爬机制触发

#### 解决方案
1. 更新 `core/media_crawler/config/base_config.py` 中的 Cookie
2. 调整爬取参数（减少 limit 数量）
3. 检查关键词是否合适

### 4. Python 路径问题

#### 症状
```
ModuleNotFoundError: No module named 'analysis'
```

#### 解决方案
确保工作流中设置了正确的 PYTHONPATH：
```yaml
env:
  PYTHONPATH: ${{ github.workspace }}
```

### 5. 文件权限问题

#### 症状
```
Permission denied
```

#### 解决方案
在工作流中添加权限设置：
```yaml
permissions:
  contents: read
  actions: write
```

## 🧪 测试步骤

### 1. 本地测试
```bash
# 测试完整流程
python scripts/test_automation.py --skip-crawler

# 测试 Telegram 推送
python scripts/telegram_push.py --token TOKEN --chat-id CHAT_ID
```

### 2. GitHub Actions 测试
1. 访问: https://github.com/roccohia/xhshh/actions
2. 点击 "小红书数据分析自动化任务"
3. 点击 "Run workflow"
4. 选择 "main" 分支
5. 点击 "Run workflow" 按钮

### 3. 查看日志
1. 在 Actions 页面点击运行记录
2. 展开各个步骤查看详细日志
3. 重点检查红色（失败）的步骤

## 📊 成功指标

### 工作流成功运行的标志
- ✅ 所有步骤显示绿色勾号
- ✅ Telegram 收到推送消息
- ✅ Artifacts 中包含分析结果
- ✅ 没有错误日志

### 预期输出
```
🤖 小红书数据分析报告
📅 生成时间: 2025-07-02 09:00:00

📊 本次分析生成了 5 个文件:
🔤 关键词分析: keywords_analysis_*.csv
☁️ 词云图: wordcloud_*.png
...
```

## 🔧 调试技巧

### 1. 启用调试模式
在工作流中添加：
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

### 2. 添加调试输出
```yaml
- name: 调试信息
  run: |
    echo "当前目录: $(pwd)"
    echo "Python 版本: $(python --version)"
    echo "文件列表: $(ls -la)"
    echo "环境变量: $(env | grep -E '(BOT_TOKEN|CHAT_ID)')"
```

### 3. 检查文件结构
```yaml
- name: 检查项目结构
  run: |
    find . -name "*.py" | head -20
    ls -la scripts/
    ls -la analysis/
```

## 🚨 紧急修复

### 如果工作流完全失败
1. 检查 YAML 语法是否正确
2. 确认所有必需的 Secrets 已配置
3. 验证文件路径是否正确
4. 检查 Python 版本兼容性

### 如果只有部分步骤失败
1. 查看具体失败步骤的日志
2. 检查该步骤的依赖是否满足
3. 验证环境变量是否正确设置
4. 确认文件是否存在

## 📞 获取帮助

### 查看文档
- [GitHub Actions 官方文档](https://docs.github.com/en/actions)
- [项目部署指南](DEPLOY_TO_GITHUB.md)
- [完整使用指南](README.md)

### 提交 Issue
如果遇到无法解决的问题：
1. 访问: https://github.com/roccohia/xhshh/issues
2. 点击 "New issue"
3. 提供详细的错误信息和日志
4. 描述复现步骤

## ✅ 当前状态

### 已修复的版本问题
- ✅ `actions/checkout@v4` - 最新版本
- ✅ `actions/setup-python@v5` - 最新版本  
- ✅ `actions/upload-artifact@v4` - 最新版本

### 工作流配置
- ✅ 定时任务: 每天北京时间 9:00
- ✅ 手动触发: 支持
- ✅ 错误处理: continue-on-error
- ✅ 文件上传: Artifacts 保留 7 天

现在你的 GitHub Actions 应该可以正常运行了！🎉
