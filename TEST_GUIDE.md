# 🧪 小红书爬虫测试指南

完整的测试流程，确保爬虫能够正常工作。

## 📋 测试步骤

### 第一步：环境检查 ✅

```bash
# 运行环境检查工具
python scripts/check_environment.py
```

这个工具会检查：
- ✅ Python 版本 (>= 3.7)
- ✅ 必需的 Python 包
- ✅ Playwright 浏览器
- ✅ 配置文件格式
- ✅ 项目结构完整性

**如果检查失败，请按照提示解决问题。**

### 第二步：更新 Cookie 🍪

```bash
# 方法1: 使用 Cookie 更新工具 (推荐)
python scripts/update_cookie.py

# 方法2: 手动编辑配置文件
# 编辑 config/xhs_config.json
```

#### 获取 Cookie 的详细步骤：

1. **打开浏览器**，访问 https://www.xiaohongshu.com
2. **登录你的账号**
3. **按 F12** 打开开发者工具
4. **切换到 Network 标签页**
5. **刷新页面**
6. **找到任意请求**，右键选择 "Copy" → "Copy as cURL"
7. **从 cURL 中提取 Cookie** 或直接复制 Cookie 头

#### Cookie 格式示例：
```
a1=xxx; web_session=xxx; webId=xxx; gid=xxx; acw_tc=xxx
```

### 第三步：测试 Cookie 有效性 🧪

```bash
# 测试 Cookie 是否有效
python scripts/test_cookie.py
```

**期望结果：**
- ✅ Cookie 有效！能够正常访问小红书页面

**如果失败：**
- ❌ 重新获取 Cookie
- ❌ 检查网络连接

### 第四步：小规模测试 🔬

```bash
# 使用增强版爬虫进行小规模测试
python scripts/run_crawler_enhanced.py --keyword "测试" --limit 5
```

**期望结果：**
- 🌐 浏览器自动打开
- 📊 成功爬取 5 条数据
- 📄 生成 CSV 文件

**可能遇到的问题：**

#### 1. 验证码问题 🤖
```
❌ 出现验证码，请求失败，Verifytype: 102
```
**解决方案：**
- 在自动打开的浏览器中手动完成验证码
- 等待几分钟后重试
- 更新 Cookie

#### 2. Cookie 过期 🍪
```
❌ Cookie 可能已过期
```
**解决方案：**
- 重新获取 Cookie
- 运行 `python scripts/update_cookie.py`

#### 3. 网络问题 🌐
```
❌ 网络连接失败
```
**解决方案：**
- 检查网络连接
- 尝试使用代理
- 稍后重试

### 第五步：正式测试 🚀

```bash
# 测试你想要的关键词
python scripts/run_crawler_enhanced.py --keyword "普拉提" --limit 50
```

### 第六步：检查结果 📊

```bash
# 方法1: 使用快速启动工具查看
python scripts/quick_start.py
# 选择 "6. 查看输出文件"

# 方法2: 直接查看文件夹
ls core/media_crawler/data/xhs/
```

**检查内容：**
- 📄 CSV 文件是否生成
- 📊 数据条数是否正确
- 📋 字段是否完整

## 🎯 一键测试 (推荐)

如果你想要最简单的测试方式：

```bash
# 运行快速启动工具
python scripts/quick_start.py
```

然后按照菜单操作：
1. 选择 "1. 更新 Cookie"
2. 选择 "2. 测试 Cookie 有效性"  
3. 选择 "4. 运行爬虫 (增强版)"
4. 选择 "6. 查看输出文件"

## 📋 测试检查清单

### 环境准备 ✅
- [ ] Python 3.7+ 已安装
- [ ] 所有依赖包已安装
- [ ] Playwright 浏览器已安装
- [ ] 项目结构完整

### Cookie 配置 ✅
- [ ] 已获取最新 Cookie
- [ ] 配置文件格式正确
- [ ] Cookie 测试通过

### 功能测试 ✅
- [ ] 小规模测试成功 (5条数据)
- [ ] 验证码处理正常
- [ ] CSV 文件正确生成
- [ ] 数据字段完整

### 正式使用 ✅
- [ ] 目标关键词测试成功
- [ ] 数据量符合预期
- [ ] 输出格式满足需求

## 🐛 常见问题排查

### 问题1: 依赖安装失败
```bash
# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r core/media_crawler/requirements.txt
```

### 问题2: 浏览器启动失败
```bash
# 重新安装浏览器
python -m playwright install --force chromium
```

### 问题3: 权限问题
```bash
# Windows 用户可能需要管理员权限
# 或者使用 --user 参数
pip install --user package_name
```

### 问题4: 编码问题
- 确保终端支持 UTF-8 编码
- Windows 用户建议使用 PowerShell 或 Git Bash

## 📞 获取帮助

如果测试过程中遇到问题：

1. **查看错误日志**：仔细阅读错误信息
2. **检查网络**：确保能正常访问小红书
3. **更新 Cookie**：Cookie 是最常见的问题源
4. **重启程序**：有时重启能解决临时问题

## 🎉 测试成功标志

当你看到以下输出时，说明测试成功：

```
✅ 爬取完成!
📄 数据已保存到: core/media_crawler/data/xhs/1_xhs_search_posts_20250702.csv
📊 文件大小: 15,234 字节
📈 爬取到 50 条数据
```

恭喜！你的小红书爬虫已经可以正常使用了！🎊
