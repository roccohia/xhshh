#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cookie 测试工具 - 验证小红书 Cookie 是否有效
"""

import json
import httpx
import asyncio
import os


async def test_cookie_validity(config_file: str):
    """测试 Cookie 有效性"""
    
    # 加载配置
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    cookie_dict = config.get('cookie', {})
    headers = config.get('headers', {})
    
    # 构建 Cookie 字符串
    cookies_str = '; '.join([f'{k}={v}' for k, v in cookie_dict.items()])
    
    print("🔍 测试 Cookie 有效性...")
    print(f"Cookie 长度: {len(cookies_str)} 字符")
    print(f"User-Agent: {headers.get('User-Agent', 'N/A')}")
    
    # 测试请求头
    test_headers = {
        'User-Agent': headers.get('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
        'Cookie': cookies_str,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.xiaohongshu.com/',
        'Origin': 'https://www.xiaohongshu.com',
    }
    
    # 测试 URL - 小红书搜索 API (更容易通过)
    test_url = "https://www.xiaohongshu.com/explore"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            print(f"📡 发送测试请求到: {test_url}")
            response = await client.get(test_url, headers=test_headers)
            
            print(f"📊 响应状态码: {response.status_code}")
            print(f"📄 响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                # 检查是否包含登录页面的特征
                response_text = response.text
                if "登录" in response_text or "login" in response_text.lower():
                    print("❌ 页面显示需要登录，Cookie 可能已过期")
                    return False
                elif "搜索" in response_text or "explore" in response_text.lower():
                    print("✅ Cookie 有效！能够正常访问小红书页面")
                    return True
                else:
                    print(f"⚠️  页面内容异常: {response_text[:200]}")
                    return False
            elif response.status_code == 461:
                print("❌ 遇到验证码，Cookie 可能已过期或被检测")
                return False
            elif response.status_code == 403:
                print("❌ 访问被拒绝，Cookie 可能无效")
                return False
            else:
                print(f"⚠️  未知状态码: {response.status_code}")
                print(f"响应内容: {response.text[:200]}")
                return False
                
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False


async def main():
    """主函数"""
    config_file = os.path.join(os.path.dirname(__file__), '../config/xhs_config.json')
    
    if not os.path.exists(config_file):
        print(f"❌ 配置文件不存在: {config_file}")
        return
    
    print("=" * 50)
    print("🍪 小红书 Cookie 有效性测试")
    print("=" * 50)
    
    is_valid = await test_cookie_validity(config_file)
    
    print("\n" + "=" * 50)
    if is_valid:
        print("✅ Cookie 测试通过！可以继续使用爬虫")
    else:
        print("❌ Cookie 测试失败！请更新 Cookie")
        print("\n💡 获取新 Cookie 的步骤:")
        print("1. 打开浏览器，访问 https://www.xiaohongshu.com")
        print("2. 登录你的账号")
        print("3. 按 F12 打开开发者工具")
        print("4. 在 Network 标签页中刷新页面")
        print("5. 找到任意请求，复制 Cookie 值")
        print("6. 更新 config/xhs_config.json 文件中的 cookie 字段")
    print("=" * 50)


if __name__ == '__main__':
    asyncio.run(main())
