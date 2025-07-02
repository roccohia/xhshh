#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 推送脚本
将分析结果推送到 Telegram
"""

import os
import sys
import argparse
import glob
import asyncio
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/telegram_push.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def find_latest_files(output_dir="output"):
    """查找最新的分析文件"""
    if not os.path.exists(output_dir):
        logger.warning(f"输出目录不存在: {output_dir}")
        return {}
    
    files = {}
    
    # 查找各类文件
    patterns = {
        'keywords_csv': 'keywords_analysis_*.csv',
        'wordcloud': 'wordcloud_*.png',
        'competitor_csv': 'competitor_analysis_*.csv',
        'koc_csv': 'koc_users_*.csv',
        'topic_csv': 'topic_suggestions_*.csv',
        'notion_csv': 'notion_content_calendar.csv',
        'reports': '*_report_*.txt'
    }
    
    for file_type, pattern in patterns.items():
        file_pattern = os.path.join(output_dir, pattern)
        matching_files = glob.glob(file_pattern)
        
        if matching_files:
            if file_type == 'reports':
                # 对于报告文件，返回所有匹配的文件
                files[file_type] = sorted(matching_files, key=os.path.getmtime, reverse=True)
            else:
                # 对于其他文件，返回最新的
                latest_file = max(matching_files, key=os.path.getmtime)
                files[file_type] = latest_file
                logger.info(f"找到 {file_type}: {os.path.basename(latest_file)}")
    
    return files


def generate_summary_message(files):
    """生成汇总消息"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    message = f"🤖 小红书数据分析报告\n"
    message += f"📅 生成时间: {timestamp}\n\n"
    
    # 统计文件数量
    file_count = len([f for f in files.values() if f])
    message += f"📊 本次分析生成了 {file_count} 个文件:\n\n"
    
    # 文件详情
    file_descriptions = {
        'keywords_csv': '🔤 关键词分析',
        'wordcloud': '☁️ 词云图',
        'competitor_csv': '🏆 竞品分析',
        'koc_csv': '👥 KOC用户筛选',
        'topic_csv': '💡 选题建议',
        'notion_csv': '📅 Notion内容日历',
        'reports': '📋 分析报告'
    }
    
    for file_type, description in file_descriptions.items():
        if file_type in files and files[file_type]:
            if file_type == 'reports':
                message += f"{description}: {len(files[file_type])} 个文件\n"
            else:
                filename = os.path.basename(files[file_type])
                message += f"{description}: {filename}\n"
    
    message += f"\n🎯 分析完成，请查看附件获取详细结果！"
    
    return message


async def send_telegram_message(bot_token, chat_id, message):
    """发送文本消息"""
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
        logger.info("文本消息发送成功")
        return True
    except TelegramError as e:
        logger.error(f"发送文本消息失败: {e}")
        return False


async def send_telegram_file(bot_token, chat_id, file_path, caption=""):
    """发送文件"""
    try:
        bot = Bot(token=bot_token)
        
        with open(file_path, 'rb') as file:
            if file_path.lower().endswith('.png'):
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=file,
                    caption=caption
                )
            else:
                await bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    caption=caption
                )
        
        logger.info(f"文件发送成功: {os.path.basename(file_path)}")
        return True
    except TelegramError as e:
        logger.error(f"发送文件失败 {file_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"发送文件异常 {file_path}: {e}")
        return False


async def push_to_telegram(bot_token, chat_id, output_dir="output"):
    """推送分析结果到 Telegram"""
    logger.info("开始推送分析结果到 Telegram")
    
    # 查找文件
    files = find_latest_files(output_dir)
    
    if not files:
        # 检查是否有真实数据
        data_dir = "core/media_crawler/data/xhs"
        if os.path.exists(data_dir):
            csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
            if csv_files:
                error_msg = "❌ 找到数据文件但分析失败，请检查分析脚本"
            else:
                error_msg = "❌ 未获取到真实数据\n\n💡 可能原因:\n• Cookie 已过期\n• 小红书 API 变更\n• 网络连接问题\n• 反爬机制阻止\n\n🔧 建议:\n• 更新 Cookie 配置\n• 检查网络连接\n• 稍后重试\n\n🚫 系统不会生成模拟数据，只使用真实数据进行分析"
        else:
            error_msg = "❌ 数据目录不存在，爬虫可能未正常运行"

        await send_telegram_message(bot_token, chat_id, error_msg)
        return False
    
    # 发送汇总消息
    summary_message = generate_summary_message(files)
    await send_telegram_message(bot_token, chat_id, summary_message)
    
    # 发送重要文件
    priority_files = [
        ('wordcloud', '☁️ 关键词词云图'),
        ('notion_csv', '📅 Notion内容日历'),
        ('koc_csv', '👥 KOC用户列表'),
        ('topic_csv', '💡 选题建议')
    ]
    
    success_count = 0
    total_count = 0
    
    for file_type, description in priority_files:
        if file_type in files and files[file_type]:
            total_count += 1
            file_path = files[file_type]
            
            if os.path.exists(file_path):
                success = await send_telegram_file(
                    bot_token, chat_id, file_path, description
                )
                if success:
                    success_count += 1
                
                # 避免发送过快
                await asyncio.sleep(1)
    
    # 发送一个主要的分析报告
    if 'reports' in files and files['reports']:
        # 选择最新的报告
        latest_report = files['reports'][0]
        total_count += 1
        
        if os.path.exists(latest_report):
            success = await send_telegram_file(
                bot_token, chat_id, latest_report, "📋 详细分析报告"
            )
            if success:
                success_count += 1
    
    # 发送完成消息
    completion_msg = f"✅ 推送完成！成功发送 {success_count}/{total_count} 个文件"
    await send_telegram_message(bot_token, chat_id, completion_msg)
    
    logger.info(f"推送完成，成功率: {success_count}/{total_count}")
    return success_count > 0


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='推送分析结果到 Telegram',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python scripts/telegram_push.py --token YOUR_BOT_TOKEN --chat-id YOUR_CHAT_ID
  python scripts/telegram_push.py --token $BOT_TOKEN --chat-id $CHAT_ID --output-dir results
        """
    )
    
    parser.add_argument(
        '--token', '-t',
        type=str,
        required=True,
        help='Telegram Bot Token'
    )
    parser.add_argument(
        '--chat-id', '-c',
        type=str,
        required=True,
        help='Telegram Chat ID'
    )
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='output',
        help='分析结果目录 (默认: output)'
    )
    
    args = parser.parse_args()
    
    # 验证参数
    if not args.token:
        logger.error("Bot Token 不能为空")
        sys.exit(1)
    
    if not args.chat_id:
        logger.error("Chat ID 不能为空")
        sys.exit(1)
    
    # 创建日志目录
    os.makedirs('logs', exist_ok=True)
    
    logger.info("=" * 60)
    logger.info("📱 Telegram 推送服务")
    logger.info("=" * 60)
    logger.info(f"输出目录: {args.output_dir}")
    logger.info(f"Chat ID: {args.chat_id}")
    
    try:
        # 运行异步推送
        success = asyncio.run(push_to_telegram(
            args.token, args.chat_id, args.output_dir
        ))
        
        if success:
            logger.info("✅ Telegram 推送成功完成")
        else:
            logger.error("❌ Telegram 推送失败")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ 推送过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
