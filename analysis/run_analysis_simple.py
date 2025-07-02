#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版数据分析启动脚本 - 解决编码问题
"""

import os
import sys
import argparse
import subprocess
import glob
from datetime import datetime

# 设置环境变量解决 Windows 编码问题
os.environ['PYTHONIOENCODING'] = 'utf-8'


def find_latest_csv_file():
    """查找最新的爬取数据文件"""
    data_dir = "core/media_crawler/data/xhs"

    if not os.path.exists(data_dir):
        return None

    # 查找所有内容文件
    pattern = os.path.join(data_dir, "*_search_contents_*.csv")
    csv_files = glob.glob(pattern)

    if not csv_files:
        return None

    # 按修改时间排序，返回最新的
    latest_file = max(csv_files, key=os.path.getmtime)
    return latest_file


def print_banner():
    """打印横幅"""
    print("=" * 70)
    print("小红书数据分析套件 - 简化版")
    print("=" * 70)


def run_analysis_module(module_name, input_file, output_dir, extra_args=None):
    """运行分析模块"""
    print(f"\n运行 {module_name}...")
    print("-" * 50)
    
    script_path = os.path.join(os.path.dirname(__file__), f'{module_name}.py')
    
    if not os.path.exists(script_path):
        print(f"错误: 模块文件不存在: {script_path}")
        return False
    
    # 构建命令
    cmd = [sys.executable, script_path, '--input', input_file, '--output-dir', output_dir]
    
    if extra_args:
        cmd.extend(extra_args)
    
    try:
        # 设置环境变量
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(cmd, check=True, env=env)
        print(f"成功: {module_name} 运行完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"失败: {module_name} 运行失败")
        print(f"返回码: {e.returncode}")
        return False
    except Exception as e:
        print(f"异常: {module_name} 运行异常: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='小红书数据分析套件 - 简化版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python analysis/run_analysis_simple.py --input core/media_crawler/data/xhs/1_search_contents_2025-07-02.csv
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
    
    args = parser.parse_args()

    # 处理 latest 参数
    if args.input == "latest":
        latest_file = find_latest_csv_file()
        if latest_file:
            args.input = latest_file
            print(f"自动识别最新文件: {latest_file}")
        else:
            print("错误: 未找到任何数据文件")
            sys.exit(1)

    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}")
        sys.exit(1)
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    print_banner()
    
    print(f"输入文件: {args.input}")
    print(f"输出目录: {args.output_dir}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 定义分析模块
    modules = [
        {
            'name': 'keyword_analysis',
            'description': '关键词分析',
            'extra_args': ['--top-n', '20']
        },
        {
            'name': 'competitor_analysis',
            'description': '竞品笔记分析',
            'extra_args': ['--top-n', '15']
        },
        {
            'name': 'koc_filter',
            'description': 'KOC 用户筛选',
            'extra_args': ['--min-likes', '150']
        },
        {
            'name': 'topic_generator',
            'description': '内容选题辅助',
            'extra_args': ['--top-n', '30']
        },
        {
            'name': 'export_notionsheet',
            'description': 'Notion 内容日历导出',
            'extra_args': ['--days', '30', '--input-dir', args.output_dir]
        }
    ]
    
    # 运行分析模块
    results = {}
    
    for module in modules:
        success = run_analysis_module(
            module['name'],
            args.input,
            args.output_dir,
            module['extra_args']
        )
        
        results[module['name']] = 'success' if success else 'failed'
    
    # 输出总结
    print("\n" + "=" * 70)
    print("分析结果总结")
    print("=" * 70)
    
    success_count = sum(1 for status in results.values() if status == 'success')
    failed_count = sum(1 for status in results.values() if status == 'failed')
    
    print(f"成功: {success_count} 个模块")
    print(f"失败: {failed_count} 个模块")
    
    print("\n详细结果:")
    for module in modules:
        name = module['name']
        desc = module['description']
        status = results[name]
        
        if status == 'success':
            icon = "[成功]"
        else:
            icon = "[失败]"
        
        print(f"  {icon} {desc} ({name}): {status}")
    
    # 输出文件位置
    print(f"\n所有结果已保存到: {os.path.abspath(args.output_dir)}")
    
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed_count > 0:
        print(f"\n警告: 有 {failed_count} 个模块运行失败")
        sys.exit(1)
    else:
        print("\n所有分析模块运行完成!")


if __name__ == '__main__':
    main()
