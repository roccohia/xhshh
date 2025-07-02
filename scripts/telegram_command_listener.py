#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 命令监听器
接收 Telegram 消息并动态更新爬取关键词配置
"""

import os
import sys
import argparse
import asyncio
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError


# 设置日志
def setup_logging():
    """设置日志配置"""
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/telegram_command.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


logger = setup_logging()


def load_keywords():
    """加载当前关键词配置"""
    keywords_file = 'config/keywords.txt'
    
    if os.path.exists(keywords_file):
        try:
            with open(keywords_file, 'r', encoding='utf-8') as f:
                keywords = f.read().strip()
                return keywords if keywords else "普拉提,健身,瑜伽"
        except Exception as e:
            logger.error(f"读取关键词文件失败: {e}")
            return "普拉提,健身,瑜伽"
    else:
        # 创建默认配置文件
        os.makedirs('config', exist_ok=True)
        default_keywords = "普拉提,健身,瑜伽"
        save_keywords(default_keywords)
        return default_keywords


def save_keywords(keywords):
    """保存关键词配置"""
    keywords_file = 'config/keywords.txt'
    
    try:
        os.makedirs('config', exist_ok=True)
        with open(keywords_file, 'w', encoding='utf-8') as f:
            f.write(keywords.strip())
        logger.info(f"关键词已保存: {keywords}")
        return True
    except Exception as e:
        logger.error(f"保存关键词失败: {e}")
        return False


def validate_keywords(keywords):
    """验证关键词格式"""
    if not keywords or not keywords.strip():
        return False, "关键词不能为空"
    
    # 分割关键词
    keyword_list = [kw.strip() for kw in keywords.split(',')]
    
    # 过滤空关键词
    keyword_list = [kw for kw in keyword_list if kw]
    
    if not keyword_list:
        return False, "没有有效的关键词"
    
    if len(keyword_list) > 10:
        return False, "关键词数量不能超过10个"
    
    # 检查关键词长度
    for kw in keyword_list:
        if len(kw) > 20:
            return False, f"关键词 '{kw}' 过长（最多20个字符）"
    
    return True, ','.join(keyword_list)


async def check_permission(update: Update, authorized_chat_id: str) -> bool:
    """检查用户权限"""
    user_chat_id = str(update.effective_chat.id)
    user_id = update.effective_user.id
    username = update.effective_user.username or "未知用户"
    
    if user_chat_id != authorized_chat_id:
        logger.warning(f"未授权用户尝试访问: {username} (ID: {user_id}, Chat: {user_chat_id})")
        await update.message.reply_text("❌ 您没有权限使用此功能")
        return False
    
    logger.info(f"授权用户访问: {username} (ID: {user_id})")
    return True


async def set_keywords_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /set 命令"""
    authorized_chat_id = context.bot_data.get('authorized_chat_id')
    
    if not await check_permission(update, authorized_chat_id):
        return
    
    # 获取关键词参数
    if not context.args:
        await update.message.reply_text(
            "❌ 请提供关键词\n\n"
            "使用方法: `/set 普拉提,瑜伽,健身`\n"
            "多个关键词用逗号分隔"
        )
        return
    
    keywords = ' '.join(context.args)
    
    # 验证关键词
    is_valid, result = validate_keywords(keywords)
    
    if not is_valid:
        await update.message.reply_text(f"❌ 关键词格式错误: {result}")
        return
    
    # 保存关键词
    if save_keywords(result):
        keyword_list = result.split(',')
        response = f"✅ 关键词已更新!\n\n"
        response += f"📝 新关键词 ({len(keyword_list)}个):\n"
        for i, kw in enumerate(keyword_list, 1):
            response += f"  {i}. {kw}\n"
        response += f"\n🤖 下次 GitHub Actions 运行时将使用这些关键词"
        
        await update.message.reply_text(response)
        
        logger.info(f"关键词已更新: {result}")
    else:
        await update.message.reply_text("❌ 保存关键词失败，请稍后重试")


async def get_keywords_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /get 命令"""
    authorized_chat_id = context.bot_data.get('authorized_chat_id')
    
    if not await check_permission(update, authorized_chat_id):
        return
    
    # 加载当前关键词
    current_keywords = load_keywords()
    keyword_list = current_keywords.split(',')
    
    response = f"📋 当前关键词配置 ({len(keyword_list)}个):\n\n"
    for i, kw in enumerate(keyword_list, 1):
        response += f"  {i}. {kw.strip()}\n"
    
    response += f"\n📁 配置文件: config/keywords.txt"
    response += f"\n⏰ 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    await update.message.reply_text(response)
    
    logger.info(f"查询当前关键词: {current_keywords}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /help 命令"""
    authorized_chat_id = context.bot_data.get('authorized_chat_id')
    
    if not await check_permission(update, authorized_chat_id):
        return
    
    help_text = """
🤖 小红书爬虫关键词管理

📋 可用命令:

/set <关键词> - 设置新的关键词
  示例: /set 普拉提,瑜伽,健身

/get - 查看当前关键词配置

/help - 显示此帮助信息

📝 说明:
• 多个关键词用逗号分隔
• 最多支持10个关键词
• 每个关键词最多20个字符
• 设置后下次 GitHub Actions 运行时生效

🔒 安全:
• 仅授权用户可使用
• 所有操作都会记录日志
"""
    
    await update.message.reply_text(help_text)


async def handle_unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理未知消息"""
    authorized_chat_id = context.bot_data.get('authorized_chat_id')
    
    if not await check_permission(update, authorized_chat_id):
        return
    
    await update.message.reply_text(
        "❓ 未知命令\n\n"
        "请使用 /help 查看可用命令"
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """错误处理器"""
    logger.error(f"处理更新时出错: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ 处理命令时出现错误，请稍后重试"
        )


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Telegram 关键词管理命令监听器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python scripts/telegram_command_listener.py --token YOUR_BOT_TOKEN --chat-id YOUR_CHAT_ID
  python scripts/telegram_command_listener.py --token $BOT_TOKEN --chat-id $CHAT_ID --timeout 30
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
        help='授权的 Telegram Chat ID'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=60,
        help='监听超时时间（秒），0表示持续监听 (默认: 60)'
    )
    
    args = parser.parse_args()
    
    if not args.token:
        logger.error("Bot Token 不能为空")
        sys.exit(1)
    
    if not args.chat_id:
        logger.error("Chat ID 不能为空")
        sys.exit(1)
    
    logger.info("=" * 60)
    logger.info("🤖 Telegram 关键词管理服务启动")
    logger.info("=" * 60)
    logger.info(f"授权 Chat ID: {args.chat_id}")
    logger.info(f"监听超时: {args.timeout}秒 {'(持续监听)' if args.timeout == 0 else ''}")
    
    try:
        # 创建应用
        application = Application.builder().token(args.token).build()
        
        # 存储授权的 chat_id
        application.bot_data['authorized_chat_id'] = args.chat_id
        
        # 添加命令处理器
        application.add_handler(CommandHandler("set", set_keywords_command))
        application.add_handler(CommandHandler("get", get_keywords_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("start", help_command))
        
        # 添加未知消息处理器
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unknown_message))
        
        # 添加错误处理器
        application.add_error_handler(error_handler)
        
        logger.info("✅ Telegram Bot 启动成功")
        logger.info("📱 等待命令...")
        
        # 运行 Bot
        if args.timeout > 0:
            # 运行指定时间后停止
            async def run_with_timeout():
                async with application:
                    await application.start()
                    await asyncio.sleep(args.timeout)
                    await application.stop()
            
            asyncio.run(run_with_timeout())
        else:
            # 持续运行
            application.run_polling()
        
        logger.info("🛑 Telegram Bot 已停止")
        
    except Exception as e:
        logger.error(f"❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
