# 📱 Telegram 动态关键词管理指南

## 🎯 功能概览

通过 Telegram 命令动态管理小红书爬虫的关键词配置，无需修改代码即可更新爬取目标。

### ✨ 新增功能

1. **📱 Telegram 命令控制**: 通过聊天界面管理关键词
2. **🔄 动态配置更新**: 实时更新爬取关键词
3. **🎯 改进的 KOC 筛选**: 更精准的用户筛选标准
4. **🔒 安全权限控制**: 仅授权用户可操作

## 📋 可用命令

### `/set <关键词>` - 设置新关键词
```
/set 普拉提,瑜伽,健身
/set 产后修复,运动康复
/set 减肥,塑形,马甲线
```

### `/get` - 查看当前关键词
```
/get
```

### `/help` - 显示帮助信息
```
/help
```

## 🚀 使用流程

### 1️⃣ 启动命令监听器

#### 临时监听（60秒）
```bash
python scripts/telegram_command_listener.py --token YOUR_BOT_TOKEN --chat-id YOUR_CHAT_ID
```

#### 持续监听
```bash
python scripts/telegram_command_listener.py --token YOUR_BOT_TOKEN --chat-id YOUR_CHAT_ID --timeout 0
```

### 2️⃣ 发送 Telegram 命令

在 Telegram 中向你的 Bot 发送命令：

```
/set 普拉提,瑜伽,健身
```

Bot 会回复：
```
✅ 关键词已更新!

📝 新关键词 (3个):
  1. 普拉提
  2. 瑜伽
  3. 健身

🤖 下次 GitHub Actions 运行时将使用这些关键词
```

### 3️⃣ 验证配置

```
/get
```

Bot 会回复：
```
📋 当前关键词配置 (3个):

  1. 普拉提
  2. 瑜伽
  3. 健身

📁 配置文件: config/keywords.txt
⏰ 最后更新: 2025-07-02 15:30:00
```

### 4️⃣ 自动生效

下次 GitHub Actions 运行时会自动使用新关键词进行爬取。

## 🎯 KOC 筛选升级

### 新的筛选标准

- ✅ **点赞数**: ≥ 200（保持不变）
- ✅ **粉丝数**: 2000 ~ 10000 之间
- ✅ **粉丝数不可见**: 不排除（包容性更强）
- ✅ **关键词匹配**: 标题必须包含目标关键词
- ✅ **互动率**: 保留计算和显示

### 使用示例

```bash
# 使用新的筛选标准
python analysis/koc_filter.py --input latest --target-keywords 普拉提,健身

# 自定义筛选参数
python analysis/koc_filter.py \
  --input data.csv \
  --min-likes 300 \
  --min-followers 1000 \
  --max-followers 15000 \
  --target-keywords 瑜伽,普拉提
```

## 🔧 配置文件

### 关键词配置文件
**位置**: `config/keywords.txt`

**格式**: 逗号分隔的关键词
```
普拉提,健身,瑜伽
```

### 爬虫自动读取逻辑
1. **优先级1**: 命令行 `--keyword` 参数
2. **优先级2**: `config/keywords.txt` 文件
3. **优先级3**: 默认关键词 "普拉提,健身,瑜伽"

## 🔒 安全特性

### 权限控制
- 仅指定的 `chat_id` 可以发送命令
- 未授权用户会收到拒绝消息
- 所有操作都记录在日志中

### 日志记录
**位置**: `logs/telegram_command.log`

**内容**:
```
2025-07-02 15:30:00 - INFO - 授权用户访问: username (ID: 123456)
2025-07-02 15:30:05 - INFO - 关键词已更新: 普拉提,瑜伽,健身
2025-07-02 15:35:00 - WARNING - 未授权用户尝试访问: unknown_user (ID: 789012)
```

### 输入验证
- 关键词不能为空
- 最多支持 10 个关键词
- 每个关键词最多 20 个字符
- 自动过滤无效关键词

## 🧪 测试功能

### 测试脚本
```bash
# 测试文件功能
python scripts/test_telegram_commands.py --test-files-only

# 测试 Telegram 命令
python scripts/test_telegram_commands.py --token YOUR_TOKEN --chat-id YOUR_CHAT_ID
```

### 手动测试步骤

1. **启动监听器**:
   ```bash
   python scripts/telegram_command_listener.py --token TOKEN --chat-id CHAT_ID --timeout 60
   ```

2. **发送测试命令**:
   ```
   /help
   /get
   /set 测试关键词,普拉提
   /get
   ```

3. **验证文件更新**:
   ```bash
   cat config/keywords.txt
   ```

4. **测试爬虫读取**:
   ```bash
   python scripts/run_crawler_enhanced.py --limit 5
   ```

## 📊 GitHub Actions 集成

### 自动读取配置
GitHub Actions 工作流已更新，会自动：

1. 检查 `config/keywords.txt` 是否存在
2. 如果存在，使用文件中的关键词
3. 如果不存在，使用默认关键词

### 工作流更新
```yaml
- name: 运行数据爬取
  run: |
    if [ -f "config/keywords.txt" ]; then
      echo "使用配置文件中的关键词"
      python scripts/run_crawler_enhanced.py --limit 100
    else
      echo "使用默认关键词"
      python scripts/run_crawler_enhanced.py --keyword "普拉提,健身,瑜伽" --limit 100
    fi
```

## 💡 使用场景

### 1. 热点追踪
```
/set 夏日减肥,比基尼身材,马甲线
```

### 2. 季节性调整
```
/set 春季排毒,养生,瑜伽
```

### 3. 竞品监控
```
/set 某品牌名,竞品关键词
```

### 4. 用户需求分析
```
/set 产后修复,新手妈妈,育儿
```

## 🚨 注意事项

### 1. 监听器运行
- 命令监听器需要手动启动
- 建议在需要更新关键词时临时运行
- 可以设置超时时间避免长期占用资源

### 2. 关键词选择
- 选择相关性高的关键词
- 避免过于宽泛的词汇
- 考虑小红书用户的搜索习惯

### 3. 频率控制
- 不要频繁更改关键词
- 建议每次更新后观察几天效果
- 避免在 GitHub Actions 运行期间更改

## 🎉 效果预期

使用新功能后，你可以：

- 📱 **随时调整**: 通过手机即时更新关键词
- 🎯 **精准筛选**: 获得更相关的 KOC 用户
- 📊 **灵活分析**: 根据需求动态调整分析目标
- 🔄 **无缝集成**: 与现有自动化流程完美配合

**现在你可以通过 Telegram 轻松管理小红书数据分析的关键词了！** 🎊
