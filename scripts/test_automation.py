#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化流程测试脚本
模拟 GitHub Actions 的完整流程
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime


def run_command(command, description, continue_on_error=True):
    """运行命令并处理结果"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"执行命令: {command}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        print("✅ 命令执行成功")
        if result.stdout:
            print("输出:")
            print(result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败 (返回码: {e.returncode})")
        if e.stdout:
            print("标准输出:")
            print(e.stdout)
        if e.stderr:
            print("错误输出:")
            print(e.stderr)
        
        if not continue_on_error:
            sys.exit(1)
        
        return False
    
    except Exception as e:
        print(f"❌ 命令执行异常: {e}")
        if not continue_on_error:
            sys.exit(1)
        
        return False


def setup_environment():
    """设置环境"""
    print("🔧 设置测试环境...")
    
    # 创建必要目录
    directories = [
        "core/media_crawler/data/xhs",
        "output",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ 创建目录: {directory}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='测试完整的自动化流程',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python scripts/test_automation.py
  python scripts/test_automation.py --skip-crawler --bot-token YOUR_TOKEN --chat-id YOUR_CHAT_ID
        """
    )
    
    parser.add_argument(
        '--skip-crawler',
        action='store_true',
        help='跳过爬虫步骤（使用现有数据）'
    )
    parser.add_argument(
        '--bot-token',
        type=str,
        help='Telegram Bot Token（用于测试推送）'
    )
    parser.add_argument(
        '--chat-id',
        type=str,
        help='Telegram Chat ID（用于测试推送）'
    )
    parser.add_argument(
        '--keywords',
        type=str,
        default='普拉提,健身,瑜伽',
        help='爬取关键词（默认：普拉提,健身,瑜伽）'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=50,
        help='爬取数量限制（默认：50）'
    )
    
    args = parser.parse_args()
    
    print("🚀 开始测试自动化流程")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 设置环境
    setup_environment()
    
    # 步骤1: 数据爬取
    if not args.skip_crawler:
        crawler_cmd = f'python scripts/run_crawler_enhanced.py --keyword "{args.keywords}" --limit {args.limit}'
        run_command(
            crawler_cmd,
            "步骤1: 爬取小红书数据",
            continue_on_error=True
        )
    else:
        print("\n⏭️ 跳过爬虫步骤")
    
    # 步骤2: 数据分析
    analysis_cmd = 'python analysis/run_analysis_simple.py --input latest'
    run_command(
        analysis_cmd,
        "步骤2: 运行数据分析",
        continue_on_error=True
    )
    
    # 步骤3: 生成 Notion 日历
    notion_cmd = 'python analysis/export_notionsheet.py --days 30'
    run_command(
        notion_cmd,
        "步骤3: 生成 Notion 内容日历",
        continue_on_error=True
    )
    
    # 步骤4: Telegram 推送（如果提供了参数）
    if args.bot_token and args.chat_id:
        telegram_cmd = f'python scripts/telegram_push.py --token "{args.bot_token}" --chat-id "{args.chat_id}"'
        run_command(
            telegram_cmd,
            "步骤4: 推送到 Telegram",
            continue_on_error=True
        )
    else:
        print("\n⏭️ 跳过 Telegram 推送（未提供 Bot Token 和 Chat ID）")
        print("💡 如需测试推送功能，请使用 --bot-token 和 --chat-id 参数")
    
    # 检查输出文件
    print(f"\n{'='*60}")
    print("📊 检查输出文件")
    print(f"{'='*60}")
    
    output_dir = "output"
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        if files:
            print(f"✅ 找到 {len(files)} 个输出文件:")
            for file in sorted(files):
                file_path = os.path.join(output_dir, file)
                file_size = os.path.getsize(file_path)
                print(f"  📄 {file} ({file_size} bytes)")
        else:
            print("⚠️ 输出目录为空")
    else:
        print("❌ 输出目录不存在")
    
    print(f"\n🎉 自动化流程测试完成!")
    print(f"⏰ 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 结果文件位置: {os.path.abspath(output_dir)}")


if __name__ == '__main__':
    main()
