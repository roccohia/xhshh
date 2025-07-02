# 🍪 小红书 Cookie 更新指南

## 🎯 为什么需要更新 Cookie

从 GitHub Actions 日志可以看到：
```
DataFetchError: 登录已过期
```

这表明当前的 Cookie 已经过期，需要更新才能正常爬取数据。

## 📋 Cookie 更新步骤

### 1️⃣ 获取最新 Cookie

#### 方法一：浏览器开发者工具
1. **打开小红书网站**: https://www.xiaohongshu.com
2. **登录你的账号**
3. **打开开发者工具**: F12 或右键 → 检查
4. **切换到 Network 标签**
5. **刷新页面**
6. **找到任意请求**，查看 Request Headers
7. **复制 Cookie 值**

#### 方法二：使用浏览器插件
1. 安装 Cookie 导出插件（如 EditThisCookie）
2. 访问小红书并登录
3. 使用插件导出 Cookie
4. 复制完整的 Cookie 字符串

### 2️⃣ 更新配置文件

编辑 `core/media_crawler/config/base_config.py` 文件：

```python
# 找到 COOKIES 配置项
COOKIES = "你的新Cookie值"
```

### 3️⃣ Cookie 格式示例

正确的 Cookie 格式应该类似：
```
web_session=040069b1-2f57-4f26-8c5c-8b5d5c5d5c5d; xsecappid=xhs-pc-web; a1=18a1234567890abcdef; webId=1234567890abcdef; gid=yYqWqKqY8qY8; webBuild=4.31.2; websectiga=...; sec_poison_id=...
```

### 4️⃣ 验证 Cookie 有效性

#### 本地测试
```bash
# 测试 Cookie 是否有效
python scripts/test_cookie.py
```

#### 手动验证
```bash
# 运行简化版爬虫测试
python scripts/run_crawler_simple.py --keyword "测试" --limit 3
```

如果看到 "登录已过期" 错误，说明 Cookie 仍然无效。

## 🔧 Cookie 配置最佳实践

### 1. Cookie 获取技巧
- **使用常用浏览器**: Chrome、Firefox、Edge
- **确保完全登录**: 能正常浏览小红书内容
- **复制完整 Cookie**: 不要遗漏任何字段
- **及时更新**: Cookie 通常 1-7 天过期

### 2. 安全注意事项
- **不要分享 Cookie**: 包含个人登录信息
- **定期更换**: 避免账号安全风险
- **使用小号**: 建议用专门的账号进行爬取

### 3. 配置文件位置
```
core/media_crawler/config/base_config.py
```

找到这一行：
```python
COOKIES = "在这里粘贴你的Cookie"
```

## 🚨 常见问题解决

### 问题1: Cookie 格式错误
**症状**: 
```
Invalid cookie format
```

**解决**: 
- 确保 Cookie 是完整的字符串
- 检查是否有换行符或特殊字符
- 重新复制 Cookie

### 问题2: 账号被限制
**症状**:
```
Account restricted or banned
```

**解决**:
- 更换账号
- 降低爬取频率
- 等待一段时间后重试

### 问题3: 网络问题
**症状**:
```
Network timeout or connection error
```

**解决**:
- 检查网络连接
- 使用代理服务器
- 调整请求间隔

## 🔄 自动化 Cookie 管理

### 定期检查脚本
创建一个定期检查 Cookie 有效性的脚本：

```bash
# 每周检查一次
python scripts/check_cookie_validity.py
```

### GitHub Actions 中的处理
当前的 GitHub Actions 配置已经包含了容错机制：
- 如果 Cookie 过期，会自动创建示例数据
- 确保分析流程不中断
- 在 Telegram 中会收到相应提示

## 📱 Telegram 通知

当 Cookie 过期时，你会在 Telegram 中收到类似消息：
```
⚠️ 小红书数据分析报告

🔍 爬取状态: 失败 (Cookie 过期)
📊 使用示例数据进行分析
💡 建议: 请更新 Cookie 配置

📁 分析结果:
- 使用备用数据
- 分析功能正常
- 建议尽快更新 Cookie
```

## 🎯 Cookie 更新频率建议

### 推荐频率
- **每周检查**: 主动检查 Cookie 状态
- **失败时更新**: 收到过期通知后立即更新
- **重要时期**: 在需要重要数据时提前更新

### 监控指标
- GitHub Actions 成功率
- Telegram 推送内容质量
- 数据文件大小和内容

## 💡 优化建议

### 短期优化
1. **设置提醒**: 每周检查 Cookie 状态
2. **备用账号**: 准备多个小红书账号
3. **监控日志**: 关注 GitHub Actions 运行状态

### 长期优化
1. **自动化检测**: 开发 Cookie 有效性检测
2. **多账号轮换**: 实现账号自动切换
3. **代理支持**: 添加代理服务器支持

## ✅ 更新检查清单

更新 Cookie 后，请检查：

- [ ] Cookie 格式正确（无换行符、特殊字符）
- [ ] 配置文件已保存
- [ ] 本地测试通过
- [ ] 推送到 GitHub
- [ ] GitHub Actions 运行成功
- [ ] Telegram 收到正常推送

## 🎉 总结

虽然 Cookie 需要定期更新，但我们的系统已经具备了强大的容错能力：

- ✅ **自动降级**: Cookie 过期时使用示例数据
- ✅ **持续分析**: 分析流程不中断
- ✅ **及时通知**: Telegram 推送状态信息
- ✅ **简单更新**: 只需更新一个配置文件

**现在你知道如何保持爬虫的最佳状态了！** 🎊
