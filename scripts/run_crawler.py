#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书笔记爬虫启动脚本
使用 MediaCrawler 进行小红书内容爬取
"""

import sys
import os
import argparse
import asyncio
from datetime import datetime

# 添加当前脚本目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from config_manager import create_config_manager


def print_banner():
    """打印启动横幅"""
    print("=" * 60)
    print("🕷️  小红书笔记爬虫 (基于 MediaCrawler)")
    print("=" * 60)


async def run_crawler(keyword: str, limit: int, config_file: str):
    """
    运行小红书爬虫

    Args:
        keyword: 搜索关键词
        limit: 爬取数量限制
        config_file: 配置文件路径
    """
    try:
        print(f"🚀 开始爬取关键词: '{keyword}', 数量限制: {limit}")

        # 创建配置管理器
        config_manager = create_config_manager(config_file)

        # 设置 MediaCrawler 配置
        config = config_manager.setup_mediacrawler_config(keyword, limit)

        # 导入并运行爬虫
        from media_platform.xhs import XiaoHongShuCrawler

        print("🔧 初始化爬虫...")
        crawler = XiaoHongShuCrawler()

        print("🌐 开始爬取数据...")
        await crawler.start()

        print("✅ 爬取完成!")

        # 查找输出文件
        data_dir = os.path.join(current_dir, '../core/media_crawler/data/xhs')
        if os.path.exists(data_dir):
            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
            if csv_files:
                latest_file = max(csv_files, key=lambda x: os.path.getctime(os.path.join(data_dir, x)))
                print(f"📄 数据已保存到: {os.path.join(data_dir, latest_file)}")
            else:
                print(f"📁 请检查数据目录: {data_dir}")
        else:
            print(f"⚠️  数据目录不存在: {data_dir}")

    except Exception as e:
        print(f"❌ 爬取过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        raise


def main():
    """主函数"""
    print_banner()

    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='小红书笔记爬虫 - 基于 MediaCrawler',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python run_crawler.py --keyword "普拉提" --limit 50
  python run_crawler.py --keyword "瑜伽,健身" --limit 100
        """
    )
    parser.add_argument(
        '--keyword',
        type=str,
        required=True,
        help='搜索关键词 (支持多个关键词用逗号分隔)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=50,
        help='抓取数量限制 (默认: 50)'
    )
    parser.add_argument(
        '--config',
        type=str,
        default=os.path.join(current_dir, '../config/xhs_config.json'),
        help='配置文件路径 (默认: ../config/xhs_config.json)'
    )

    args = parser.parse_args()

    # 验证配置文件存在
    if not os.path.exists(args.config):
        print(f"❌ 配置文件不存在: {args.config}")
        sys.exit(1)

    # 运行爬虫
    try:
        asyncio.run(run_crawler(args.keyword, args.limit, args.config))
    except KeyboardInterrupt:
        print("\n⏹️  用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 程序执行失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()