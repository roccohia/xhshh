#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键运行所有数据分析模块
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime


def print_banner():
    """打印横幅"""
    print("=" * 70)
    print("📊 小红书数据分析套件 - 一键运行")
    print("=" * 70)


def run_analysis_module(module_name, input_file, output_dir, extra_args=None):
    """运行分析模块"""
    print(f"\n🔄 运行 {module_name}...")
    print("-" * 50)
    
    script_path = os.path.join(os.path.dirname(__file__), f'{module_name}.py')
    
    if not os.path.exists(script_path):
        print(f"❌ 模块文件不存在: {script_path}")
        return False
    
    # 构建命令
    cmd = [sys.executable, script_path, '--input', input_file, '--output-dir', output_dir]
    
    if extra_args:
        cmd.extend(extra_args)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {module_name} 运行成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {module_name} 运行失败:")
        print(f"错误信息: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ {module_name} 运行异常: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='小红书数据分析套件 - 一键运行所有分析模块',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python analysis/run_all_analysis.py --input core/media_crawler/data/xhs/1_search_contents_2025-07-02.csv
  python analysis/run_all_analysis.py --input data.csv --api-key your_openai_key
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        required=True,
        help='输入的 CSV 文件路径'
    )
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='output',
        help='输出目录 (默认: output)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='OpenAI API Key (用于选题分析)'
    )
    parser.add_argument(
        '--skip-modules',
        type=str,
        nargs='*',
        default=[],
        help='跳过的模块 (keyword_analysis, competitor_analysis, koc_filter, topic_generator)'
    )
    parser.add_argument(
        '--keyword-top-n',
        type=int,
        default=30,
        help='关键词分析：提取前 N 个关键词 (默认: 30)'
    )
    parser.add_argument(
        '--competitor-top-n',
        type=int,
        default=20,
        help='竞品分析：分析前 N 个高表现内容 (默认: 20)'
    )
    parser.add_argument(
        '--koc-min-likes',
        type=int,
        default=200,
        help='KOC筛选：最小平均点赞数 (默认: 200)'
    )
    parser.add_argument(
        '--topic-top-n',
        type=int,
        default=50,
        help='选题分析：分析前 N 个高互动标题 (默认: 50)'
    )
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"❌ 输入文件不存在: {args.input}")
        sys.exit(1)
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    print_banner()
    
    print(f"📁 输入文件: {args.input}")
    print(f"📁 输出目录: {args.output_dir}")
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 定义分析模块
    modules = [
        {
            'name': 'keyword_analysis',
            'description': '关键词分析',
            'extra_args': ['--top-n', str(args.keyword_top_n)]
        },
        {
            'name': 'competitor_analysis',
            'description': '竞品笔记分析',
            'extra_args': ['--top-n', str(args.competitor_top_n)]
        },
        {
            'name': 'koc_filter',
            'description': 'KOC 用户筛选',
            'extra_args': ['--min-likes', str(args.koc_min_likes)]
        },
        {
            'name': 'topic_generator',
            'description': '内容选题辅助',
            'extra_args': ['--top-n', str(args.topic_top_n)]
        }
    ]
    
    # 添加 API Key 到选题分析
    if args.api_key:
        for module in modules:
            if module['name'] == 'topic_generator':
                module['extra_args'].extend(['--api-key', args.api_key])
    
    # 运行分析模块
    results = {}
    
    for module in modules:
        if module['name'] in args.skip_modules:
            print(f"\n⏭️  跳过 {module['description']} ({module['name']})")
            results[module['name']] = 'skipped'
            continue
        
        success = run_analysis_module(
            module['name'],
            args.input,
            args.output_dir,
            module['extra_args']
        )
        
        results[module['name']] = 'success' if success else 'failed'
    
    # 输出总结
    print("\n" + "=" * 70)
    print("📊 分析结果总结")
    print("=" * 70)
    
    success_count = sum(1 for status in results.values() if status == 'success')
    failed_count = sum(1 for status in results.values() if status == 'failed')
    skipped_count = sum(1 for status in results.values() if status == 'skipped')
    
    print(f"✅ 成功: {success_count} 个模块")
    print(f"❌ 失败: {failed_count} 个模块")
    print(f"⏭️  跳过: {skipped_count} 个模块")
    
    print("\n📋 详细结果:")
    for module in modules:
        name = module['name']
        desc = module['description']
        status = results[name]
        
        if status == 'success':
            icon = "✅"
        elif status == 'failed':
            icon = "❌"
        else:
            icon = "⏭️"
        
        print(f"  {icon} {desc} ({name}): {status}")
    
    # 输出文件位置
    print(f"\n📁 所有结果已保存到: {os.path.abspath(args.output_dir)}")
    
    # 生成分析报告索引
    generate_analysis_index(args.output_dir, results)
    
    print(f"⏰ 完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed_count > 0:
        print(f"\n⚠️  有 {failed_count} 个模块运行失败，请检查错误信息")
        sys.exit(1)
    else:
        print("\n🎉 所有分析模块运行完成!")


def generate_analysis_index(output_dir, results):
    """生成分析结果索引"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    index_path = os.path.join(output_dir, f'analysis_index_{timestamp}.txt')
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("小红书数据分析结果索引\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"输出目录: {output_dir}\n\n")
        
        f.write("📊 分析模块运行状态:\n")
        f.write("-" * 30 + "\n")
        
        module_descriptions = {
            'keyword_analysis': '关键词分析',
            'competitor_analysis': '竞品笔记分析',
            'koc_filter': 'KOC 用户筛选',
            'topic_generator': '内容选题辅助'
        }
        
        for module_name, status in results.items():
            desc = module_descriptions.get(module_name, module_name)
            f.write(f"{desc}: {status}\n")
        
        f.write("\n📁 输出文件说明:\n")
        f.write("-" * 30 + "\n")
        f.write("关键词分析:\n")
        f.write("  - keywords_analysis_*.csv: 关键词频率统计\n")
        f.write("  - wordcloud_*.png: 词云图\n")
        f.write("  - keyword_trends.csv: 关键词趋势分析\n\n")
        
        f.write("竞品分析:\n")
        f.write("  - competitor_analysis_*.csv: 竞品分析结果\n")
        f.write("  - high_engagement_*.csv: 高互动内容\n")
        f.write("  - engagement_analysis_*.png: 互动分析图表\n")
        f.write("  - competitor_report_*.txt: 竞品分析报告\n\n")
        
        f.write("KOC 筛选:\n")
        f.write("  - koc_users_*.csv: KOC 用户列表\n")
        f.write("  - all_users_stats_*.csv: 所有用户统计\n")
        f.write("  - koc_analysis_*.png: KOC 分析图表\n")
        f.write("  - koc_analysis_report_*.txt: KOC 分析报告\n\n")
        
        f.write("选题分析:\n")
        f.write("  - topic_suggestions_*.csv: 选题建议\n")
        f.write("  - content_calendar_*.csv: 内容日历\n")
        f.write("  - title_patterns_*.json: 标题模式分析\n")
        f.write("  - topic_analysis_report_*.txt: 选题分析报告\n")
        f.write("  - ai_analysis_*.json: AI 分析结果 (如果启用)\n")
    
    print(f"📋 分析结果索引已保存到: {index_path}")


if __name__ == '__main__':
    main()
