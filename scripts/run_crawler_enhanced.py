#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版小红书笔记爬虫启动脚本
支持手动验证码处理和更好的错误恢复机制
"""

import sys
import os
import argparse
import asyncio
import time
from datetime import datetime

# 添加必要的路径到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # 项目根目录
media_crawler_dir = os.path.join(project_root, 'core', 'media_crawler')

# 添加路径到 sys.path
sys.path.insert(0, current_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, media_crawler_dir)

print(f"🔧 Python 路径设置:")
print(f"   当前目录: {current_dir}")
print(f"   项目根目录: {project_root}")
print(f"   MediaCrawler 目录: {media_crawler_dir}")

from config_manager import create_config_manager


def load_keywords_from_config():
    """从配置文件加载关键词"""
    keywords_file = 'config/keywords.txt'

    if os.path.exists(keywords_file):
        try:
            with open(keywords_file, 'r', encoding='utf-8') as f:
                keywords = f.read().strip()
                if keywords:
                    print(f"📋 从配置文件加载关键词: {keywords}")
                    return keywords
        except Exception as e:
            print(f"⚠️  读取关键词配置文件失败: {e}")

    # 返回默认关键词
    default_keywords = "普拉提,健身,瑜伽"
    print(f"📋 使用默认关键词: {default_keywords}")
    return default_keywords


def print_banner():
    """打印启动横幅"""
    print("=" * 70)
    print("🕷️  小红书笔记爬虫 (增强版 - 支持验证码处理)")
    print("=" * 70)


async def run_crawler_with_retry(keyword: str, limit: int, config_file: str, max_retries: int = 3):
    """
    运行小红书爬虫，支持重试机制
    
    Args:
        keyword: 搜索关键词
        limit: 爬取数量限制
        config_file: 配置文件路径
        max_retries: 最大重试次数
    """
    for attempt in range(max_retries):
        try:
            print(f"🚀 第 {attempt + 1} 次尝试爬取关键词: '{keyword}', 数量限制: {limit}")
            
            # 创建配置管理器
            config_manager = create_config_manager(config_file)
            
            # 设置 MediaCrawler 配置
            config = config_manager.setup_mediacrawler_config(keyword, limit)
            
            # 导入并运行爬虫
            from media_platform.xhs import XiaoHongShuCrawler
            
            print("🔧 初始化爬虫...")
            crawler = XiaoHongShuCrawler()
            
            print("🌐 开始爬取数据...")
            print("💡 如果遇到验证码，请在打开的浏览器窗口中手动完成验证")
            
            await crawler.start()
            
            print("✅ 爬取完成!")
            
            # 查找输出文件
            data_dir = os.path.join(current_dir, '../core/media_crawler/data/xhs')
            if os.path.exists(data_dir):
                csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
                if csv_files:
                    # 按修改时间排序，获取最新文件
                    csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(data_dir, x)), reverse=True)
                    latest_file = csv_files[0]
                    file_path = os.path.join(data_dir, latest_file)
                    file_size = os.path.getsize(file_path)
                    print(f"📄 数据已保存到: {file_path}")
                    print(f"📊 文件大小: {file_size} 字节")
                    
                    # 简单统计行数
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            line_count = sum(1 for line in f) - 1  # 减去标题行
                        print(f"📈 爬取到 {line_count} 条数据")
                    except:
                        pass
                else:
                    print(f"📁 数据目录存在但无 CSV 文件: {data_dir}")
            else:
                print(f"⚠️  数据目录不存在: {data_dir}")
            
            return True  # 成功完成
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ 第 {attempt + 1} 次尝试失败: {error_msg}")
            
            # 分析错误类型并给出建议
            if "验证码" in error_msg or "461" in error_msg:
                print("🔍 检测到验证码问题")
                if attempt < max_retries - 1:
                    print("💡 建议:")
                    print("   1. 在浏览器中完成验证码")
                    print("   2. 等待几分钟后重试")
                    print("   3. 或者更新 Cookie")
                    
                    wait_time = (attempt + 1) * 30  # 递增等待时间
                    print(f"⏳ 等待 {wait_time} 秒后重试...")
                    await asyncio.sleep(wait_time)
                    continue
            elif "Cookie" in error_msg or "登录" in error_msg:
                print("🍪 检测到 Cookie 问题")
                print("💡 请更新 config/xhs_config.json 中的 Cookie")
                break
            elif "网络" in error_msg or "连接" in error_msg:
                print("🌐 检测到网络问题")
                if attempt < max_retries - 1:
                    wait_time = 10
                    print(f"⏳ 等待 {wait_time} 秒后重试...")
                    await asyncio.sleep(wait_time)
                    continue
            
            if attempt == max_retries - 1:
                print(f"💥 所有重试都失败了，最后错误: {error_msg}")
                import traceback
                traceback.print_exc()
                return False
    
    return False


def main():
    """主函数"""
    print_banner()
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='小红书笔记爬虫 (增强版) - 基于 MediaCrawler',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python run_crawler_enhanced.py --keyword "普拉提" --limit 50
  python run_crawler_enhanced.py --keyword "瑜伽,健身" --limit 100 --retries 5
        """
    )
    parser.add_argument(
        '--keyword',
        type=str,
        required=False,  # 改为非必需，可以从配置文件读取
        help='搜索关键词 (支持多个关键词用逗号分隔，如不提供则从 config/keywords.txt 读取)'
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
    parser.add_argument(
        '--retries', 
        type=int, 
        default=3,
        help='最大重试次数 (默认: 3)'
    )
    
    args = parser.parse_args()

    # 处理关键词参数
    if args.keyword:
        # 使用命令行提供的关键词
        keywords = args.keyword
        print(f"🎯 使用命令行关键词: {keywords}")
    else:
        # 从配置文件读取关键词
        keywords = load_keywords_from_config()

    # 验证配置文件存在
    if not os.path.exists(args.config):
        print(f"❌ 配置文件不存在: {args.config}")
        sys.exit(1)

    print(f"📋 配置信息:")
    print(f"   关键词: {keywords}")
    print(f"   数量限制: {args.limit}")
    print(f"   配置文件: {args.config}")
    print(f"   最大重试: {args.retries}")
    print()

    # 运行爬虫
    try:
        success = asyncio.run(run_crawler_with_retry(
            keywords,
            args.limit,
            args.config,
            args.retries
        ))
        
        if success:
            print("\n🎉 爬虫任务完成!")
        else:
            print("\n💔 爬虫任务失败!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序执行失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
