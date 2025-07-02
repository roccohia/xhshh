#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cookie 更新工具 - 简化 Cookie 更新流程
"""

import json
import os
import re
from datetime import datetime


def parse_cookie_string(cookie_string: str) -> dict:
    """
    解析 Cookie 字符串为字典
    支持多种格式的 Cookie 输入
    """
    cookie_dict = {}
    
    # 处理不同格式的 Cookie 字符串
    if ';' in cookie_string:
        # 格式: key1=value1; key2=value2
        pairs = cookie_string.split(';')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.strip().split('=', 1)
                cookie_dict[key.strip()] = value.strip()
    elif '\n' in cookie_string:
        # 格式: 多行，每行一个 key=value
        lines = cookie_string.strip().split('\n')
        for line in lines:
            if '=' in line and not line.strip().startswith('#'):
                key, value = line.strip().split('=', 1)
                cookie_dict[key.strip()] = value.strip()
    else:
        print("⚠️  无法识别的 Cookie 格式")
        return {}
    
    return cookie_dict


def extract_important_cookies(cookie_dict: dict) -> dict:
    """提取重要的 Cookie 字段"""
    important_keys = [
        'a1', 'web_session', 'webId', 'gid', 'acw_tc', 
        'abRequestId', 'sec_poison_id', 'websectiga', 
        'webBuild', 'xsecappid'
    ]
    
    extracted = {}
    for key in important_keys:
        if key in cookie_dict:
            extracted[key] = cookie_dict[key]
    
    return extracted


def update_config_file(config_path: str, new_cookies: dict, user_agent: str = None):
    """更新配置文件"""
    try:
        # 读取现有配置
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 备份原配置
        backup_path = config_path + f'.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print(f"📁 原配置已备份到: {backup_path}")
        
        # 更新 Cookie
        config['cookie'] = new_cookies
        
        # 更新 User-Agent (如果提供)
        if user_agent:
            config['headers']['User-Agent'] = user_agent
        
        # 保存新配置
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        print(f"✅ 配置文件已更新: {config_path}")
        return True
        
    except Exception as e:
        print(f"❌ 更新配置文件失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("🍪 小红书 Cookie 更新工具")
    print("=" * 60)
    
    config_path = os.path.join(os.path.dirname(__file__), '../config/xhs_config.json')
    
    print("📋 请按照以下步骤获取 Cookie:")
    print("1. 打开浏览器，访问 https://www.xiaohongshu.com")
    print("2. 登录你的账号")
    print("3. 按 F12 打开开发者工具")
    print("4. 在 Application/Storage 标签页中找到 Cookies")
    print("5. 复制所有 Cookie 或者复制请求头中的 Cookie 字符串")
    print()
    
    print("💡 支持的输入格式:")
    print("   格式1: key1=value1; key2=value2; key3=value3")
    print("   格式2: 多行格式，每行一个 key=value")
    print()
    
    # 获取 Cookie 输入
    print("🔤 请粘贴你的 Cookie (输入完成后按两次回车):")
    cookie_lines = []
    while True:
        try:
            line = input()
            if line.strip() == "" and cookie_lines:
                break
            if line.strip():
                cookie_lines.append(line.strip())
        except KeyboardInterrupt:
            print("\n⏹️  操作已取消")
            return
    
    if not cookie_lines:
        print("❌ 没有输入 Cookie")
        return
    
    cookie_string = '\n'.join(cookie_lines)
    
    # 解析 Cookie
    print("\n🔍 解析 Cookie...")
    cookie_dict = parse_cookie_string(cookie_string)
    
    if not cookie_dict:
        print("❌ Cookie 解析失败")
        return
    
    print(f"📊 解析到 {len(cookie_dict)} 个 Cookie 字段")
    
    # 提取重要字段
    important_cookies = extract_important_cookies(cookie_dict)
    print(f"🎯 提取到 {len(important_cookies)} 个重要字段:")
    for key in important_cookies:
        value = important_cookies[key]
        display_value = value[:20] + "..." if len(value) > 20 else value
        print(f"   {key}: {display_value}")
    
    if not important_cookies:
        print("⚠️  没有找到重要的 Cookie 字段")
        print("🔍 所有解析到的字段:")
        for key, value in cookie_dict.items():
            display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"   {key}: {display_value}")
        
        use_all = input("\n❓ 是否使用所有字段? (y/N): ").lower().strip()
        if use_all == 'y':
            important_cookies = cookie_dict
        else:
            print("❌ 操作已取消")
            return
    
    # 询问是否更新 User-Agent
    print("\n🌐 是否需要更新 User-Agent? (可选)")
    update_ua = input("❓ 输入新的 User-Agent (直接回车跳过): ").strip()
    
    # 更新配置文件
    print(f"\n💾 更新配置文件: {config_path}")
    success = update_config_file(
        config_path, 
        important_cookies, 
        update_ua if update_ua else None
    )
    
    if success:
        print("\n🎉 Cookie 更新完成!")
        print("💡 建议运行以下命令测试:")
        print("   python scripts/test_cookie.py")
        print("   python scripts/run_crawler_enhanced.py --keyword \"测试\" --limit 5")
    else:
        print("\n💔 Cookie 更新失败!")


if __name__ == '__main__':
    main()
