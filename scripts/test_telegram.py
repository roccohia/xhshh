#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 推送测试脚本
用于测试 Telegram Bot 配置是否正确
"""

import asyncio
import argparse
import sys
from telegram import Bot
from telegram.error import TelegramError


async def test_telegram_connection(bot_token, chat_id):
    """测试 Telegram 连接"""
    try:
        bot = Bot(token=bot_token)
        
        # 获取 bot 信息
        bot_info = await bot.get_me()
        print(f"✅ Bot 连接成功!")
        print(f"Bot 名称: {bot_info.first_name}")
        print(f"Bot 用户名: @{bot_info.username}")
        
        # 发送测试消息
        test_message = "🤖 测试消息：小红书数据分析系统连接成功！"
        await bot.send_message(chat_id=chat_id, text=test_message)
        print(f"✅ 测试消息发送成功到 Chat ID: {chat_id}")
        
        return True
        
    except TelegramError as e:
        print(f"❌ Telegram 错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 连接异常: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='测试 Telegram Bot 连接')
    parser.add_argument('--token', '-t', required=True, help='Telegram Bot Token')
    parser.add_argument('--chat-id', '-c', required=True, help='Telegram Chat ID')
    
    args = parser.parse_args()
    
    print("🔧 测试 Telegram Bot 连接...")
    
    success = asyncio.run(test_telegram_connection(args.token, args.chat_id))
    
    if success:
        print("\n🎉 Telegram 配置测试成功！")
        print("现在可以运行完整的自动化流程了。")
    else:
        print("\n❌ Telegram 配置测试失败！")
        print("请检查 Bot Token 和 Chat ID 是否正确。")
        sys.exit(1)


if __name__ == '__main__':
    main()
