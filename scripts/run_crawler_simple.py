#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版小红书爬虫 - 专为 GitHub Actions 环境优化
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime


def get_default_keywords():
    """获取默认关键词"""
    default_keywords = "普拉提,健身,瑜伽"
    print(f"📋 使用默认关键词: {default_keywords}")
    return default_keywords


def create_main_py_if_missing():
    """如果 main.py 不存在，创建一个简化版本"""
    media_crawler_dir = 'core/media_crawler'
    main_py = os.path.join(media_crawler_dir, 'main.py')

    if not os.path.exists(main_py):
        print(f"🔧 创建 main.py 文件: {main_py}")

        main_py_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaCrawler 主程序 - GitHub Actions 简化版
"""

import argparse
import sys
import os
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='MediaCrawler')
    parser.add_argument('--platform', default='xhs')
    parser.add_argument('--lt', default='cookie')
    parser.add_argument('--type', default='search')
    parser.add_argument('--keywords', required=True)

    args = parser.parse_args()

    print(f"MediaCrawler 启动参数:")
    print(f"  平台: {args.platform}")
    print(f"  登录类型: {args.lt}")
    print(f"  类型: {args.type}")
    print(f"  关键词: {args.keywords}")

    # 在 GitHub Actions 环境中，我们无法真正运行爬虫
    # 所以这里只是模拟运行
    print("⚠️  在 GitHub Actions 环境中无法运行真实爬虫")
    print("💡 将在后续步骤中创建示例数据")

    return 0

if __name__ == '__main__':
    sys.exit(main())
'''

        try:
            os.makedirs(media_crawler_dir, exist_ok=True)
            with open(main_py, 'w', encoding='utf-8') as f:
                f.write(main_py_content)
            print(f"✅ main.py 已创建")
            return True
        except Exception as e:
            print(f"❌ 创建 main.py 失败: {e}")
            return False

    return True


def run_mediacrawler(keywords, limit=100):
    """运行 MediaCrawler（GitHub Actions 优化版）"""
    print(f"🚀 启动 MediaCrawler...")
    print(f"   关键词: {keywords}")
    print(f"   数量限制: {limit}")

    # 在 GitHub Actions 环境中，先尝试真实爬取
    # 如果失败再使用备用数据
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        print("🔧 检测到 GitHub Actions 环境")
        print("🚀 尝试真实爬取（如果 Cookie 有效）")
        # 继续执行，不直接返回 False

    # 本地环境尝试运行 MediaCrawler
    media_crawler_dir = 'core/media_crawler'

    if not os.path.exists(media_crawler_dir):
        print(f"❌ MediaCrawler 目录不存在: {media_crawler_dir}")
        return False

    # 确保 main.py 存在
    if not create_main_py_if_missing():
        return False

    # 检查 main.py 是否存在
    main_py = os.path.join(media_crawler_dir, 'main.py')
    if not os.path.exists(main_py):
        print(f"❌ main.py 仍然不存在: {main_py}")
        return False
    
    try:
        # 构建命令 (根据 MediaCrawler 的实际参数)
        cmd = [
            sys.executable, 'main.py',
            '--platform', 'xhs',
            '--lt', 'cookie',
            '--type', 'search',
            '--keywords', keywords
            # 注意：MediaCrawler 可能不支持 --crawl-count 参数
            # 数量限制可能需要在配置文件中设置
        ]
        
        print(f"🔧 执行命令: {' '.join(cmd)}")
        print(f"🔧 工作目录: {os.path.abspath(media_crawler_dir)}")
        
        # 运行命令
        result = subprocess.run(
            cmd,
            cwd=media_crawler_dir,
            capture_output=True,
            text=True,
            timeout=600  # 10分钟超时
        )
        
        print(f"📊 返回码: {result.returncode}")
        
        if result.stdout:
            print("📤 标准输出:")
            print(result.stdout)
        
        if result.stderr:
            print("📤 错误输出:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ MediaCrawler 运行成功")
            return True
        else:
            print(f"❌ MediaCrawler 运行失败，返回码: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ MediaCrawler 运行超时")
        return False
    except Exception as e:
        print(f"❌ 运行 MediaCrawler 时出错: {e}")
        return False


def check_output_files():
    """检查输出文件"""
    print("📁 检查输出文件...")
    
    data_dirs = [
        'core/media_crawler/data/xhs',
        'data/xhs',
        'output'
    ]
    
    found_files = []
    
    for data_dir in data_dirs:
        if os.path.exists(data_dir):
            files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
            if files:
                print(f"✅ 在 {data_dir} 找到 {len(files)} 个 CSV 文件:")
                for file in sorted(files)[-3:]:  # 显示最新的3个文件
                    file_path = os.path.join(data_dir, file)
                    file_size = os.path.getsize(file_path)
                    print(f"   📄 {file} ({file_size} bytes)")
                    found_files.append(file_path)
    
    if found_files:
        print(f"✅ 总共找到 {len(found_files)} 个输出文件")
        return True
    else:
        print("⚠️  未找到任何输出文件")
        return False





def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='简化版小红书爬虫 - GitHub Actions 优化版',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--keyword',
        type=str,
        help='搜索关键词 (如不提供则从 config/keywords.txt 读取)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=50,
        help='爬取数量限制 (默认: 50)'
    )

    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🕷️  小红书爬虫 (GitHub Actions 简化版)")
    print("=" * 60)
    
    # 处理关键词
    if args.keyword:
        keywords = args.keyword
        print(f"🎯 使用命令行关键词: {keywords}")
    else:
        keywords = get_default_keywords()
    
    print(f"📋 配置信息:")
    print(f"   关键词: {keywords}")
    print(f"   数量限制: {args.limit}")
    print(f"   当前目录: {os.getcwd()}")
    print()
    
    # 尝试运行爬虫
    success = run_mediacrawler(keywords, args.limit)
    
    # 检查输出文件
    has_output = check_output_files()
    
    if not success or not has_output:
        print("❌ 爬取失败，没有获取到任何真实数据")
        print("💡 可能的原因:")
        print("   - Cookie 已过期，需要更新")
        print("   - 小红书 API 端点已变更")
        print("   - 网络连接问题")
        print("   - 反爬机制阻止了请求")
    
    if has_output:
        print("\n✅ 爬虫任务完成!")
        print("📁 数据文件已准备就绪，可以进行后续分析")
        return True
    else:
        print("\n❌ 爬虫任务失败!")
        print("💡 请检查网络连接和 Cookie 配置")
        print("🚫 不会生成模拟数据，只使用真实数据进行分析")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
