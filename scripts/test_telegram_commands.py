#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Telegram 命令功能
"""

import os
import sys
import argparse
import asyncio
from telegram import Bot
from telegram.error import TelegramError


async def test_telegram_commands(bot_token, chat_id):
    """测试 Telegram 命令功能"""
    try:
        bot = Bot(token=bot_token)
        
        print("🤖 测试 Telegram 命令功能...")
        
        # 测试 /get 命令
        print("\n1. 测试 /get 命令...")
        await bot.send_message(chat_id=chat_id, text="/get")
        
        # 等待一下
        await asyncio.sleep(2)
        
        # 测试 /help 命令
        print("2. 测试 /help 命令...")
        await bot.send_message(chat_id=chat_id, text="/help")
        
        # 等待一下
        await asyncio.sleep(2)
        
        # 测试 /set 命令
        print("3. 测试 /set 命令...")
        await bot.send_message(chat_id=chat_id, text="/set 测试关键词,普拉提,瑜伽")
        
        print("✅ 测试命令已发送，请检查 Telegram 消息")
        print("💡 如果没有收到回复，请确保命令监听器正在运行")
        
        return True
        
    except TelegramError as e:
        print(f"❌ Telegram 错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False


def test_keywords_file():
    """测试关键词文件功能"""
    print("📁 测试关键词文件功能...")
    
    keywords_file = 'config/keywords.txt'
    
    # 检查文件是否存在
    if os.path.exists(keywords_file):
        try:
            with open(keywords_file, 'r', encoding='utf-8') as f:
                keywords = f.read().strip()
                print(f"✅ 当前关键词: {keywords}")
        except Exception as e:
            print(f"❌ 读取关键词文件失败: {e}")
    else:
        print("⚠️  关键词文件不存在，将创建默认文件")
        os.makedirs('config', exist_ok=True)
        with open(keywords_file, 'w', encoding='utf-8') as f:
            f.write('普拉提,健身,瑜伽')
        print("✅ 已创建默认关键词文件")


def test_koc_filter():
    """测试新的 KOC 筛选功能"""
    print("🎯 测试新的 KOC 筛选功能...")
    
    # 检查是否有测试数据
    test_data_paths = [
        'core/media_crawler/data/xhs/',
        'output/'
    ]
    
    found_data = False
    for path in test_data_paths:
        if os.path.exists(path):
            csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
            if csv_files:
                print(f"✅ 找到测试数据: {path}")
                print(f"   文件: {csv_files[:3]}...")  # 显示前3个文件
                found_data = True
                break
    
    if not found_data:
        print("⚠️  未找到测试数据，请先运行爬虫获取数据")
        return False
    
    print("💡 可以使用以下命令测试新的 KOC 筛选:")
    print("   python analysis/koc_filter.py --input latest --target-keywords 普拉提,健身")
    
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='测试 Telegram 命令功能')
    parser.add_argument('--token', '-t', help='Telegram Bot Token')
    parser.add_argument('--chat-id', '-c', help='Telegram Chat ID')
    parser.add_argument('--test-files-only', action='store_true', help='仅测试文件功能')
    
    args = parser.parse_args()
    
    print("🧪 Telegram 命令功能测试")
    print("=" * 50)
    
    # 测试关键词文件
    test_keywords_file()
    
    print()
    
    # 测试 KOC 筛选
    test_koc_filter()
    
    if not args.test_files_only and args.token and args.chat_id:
        print()
        # 测试 Telegram 命令
        success = asyncio.run(test_telegram_commands(args.token, args.chat_id))
        
        if success:
            print("\n✅ Telegram 命令测试完成")
        else:
            print("\n❌ Telegram 命令测试失败")
    else:
        print("\n💡 要测试 Telegram 命令，请提供 --token 和 --chat-id 参数")
    
    print("\n📋 测试总结:")
    print("1. 关键词文件功能 - 已测试")
    print("2. KOC 筛选功能 - 已检查")
    print("3. Telegram 命令 - " + ("已测试" if args.token and args.chat_id else "需要参数"))
    
    print("\n🚀 下一步:")
    print("1. 启动命令监听器: python scripts/telegram_command_listener.py --token TOKEN --chat-id CHAT_ID")
    print("2. 在 Telegram 中发送命令测试")
    print("3. 运行爬虫测试关键词读取: python scripts/run_crawler_enhanced.py --limit 10")


if __name__ == '__main__':
    main()
