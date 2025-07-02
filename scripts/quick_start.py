#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书爬虫快速启动脚本
整合所有功能的一站式工具
"""

import os
import sys
import subprocess
import asyncio


def print_banner():
    """打印横幅"""
    print("=" * 70)
    print("🚀 小红书爬虫 - 快速启动工具")
    print("=" * 70)


def print_menu():
    """打印菜单"""
    print("\n📋 请选择操作:")
    print("1. 🍪 更新 Cookie")
    print("2. 🧪 测试 Cookie 有效性")
    print("3. 🕷️  运行爬虫 (基础版)")
    print("4. 🚀 运行爬虫 (增强版)")
    print("5. 📄 查看使用说明")
    print("6. 📁 查看输出文件")
    print("0. ❌ 退出")
    print()


def run_script(script_name: str, args: list = None):
    """运行脚本"""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ 脚本执行失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️  操作被用户中断")
        return False


def view_output_files():
    """查看输出文件"""
    data_dir = os.path.join(os.path.dirname(__file__), '../core/media_crawler/data/xhs')
    
    if not os.path.exists(data_dir):
        print(f"❌ 数据目录不存在: {data_dir}")
        return
    
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"📁 数据目录中没有 CSV 文件: {data_dir}")
        return
    
    print(f"📊 找到 {len(csv_files)} 个 CSV 文件:")
    print()
    
    # 按修改时间排序
    csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(data_dir, x)), reverse=True)
    
    for i, filename in enumerate(csv_files, 1):
        file_path = os.path.join(data_dir, filename)
        file_size = os.path.getsize(file_path)
        
        # 获取文件修改时间
        import datetime
        mtime = os.path.getmtime(file_path)
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        
        # 尝试统计行数
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                line_count = sum(1 for line in f) - 1  # 减去标题行
            line_info = f"{line_count} 条数据"
        except:
            line_info = "无法读取"
        
        print(f"{i:2d}. 📄 {filename}")
        print(f"     📅 修改时间: {mtime_str}")
        print(f"     📊 文件大小: {file_size:,} 字节")
        print(f"     📈 数据条数: {line_info}")
        print(f"     📁 完整路径: {file_path}")
        print()


def show_usage():
    """显示使用说明"""
    print("\n📖 使用说明:")
    print()
    print("🔧 首次使用:")
    print("1. 选择 '1. 更新 Cookie' 设置你的小红书 Cookie")
    print("2. 选择 '2. 测试 Cookie' 验证 Cookie 是否有效")
    print("3. 选择 '4. 运行爬虫 (增强版)' 开始爬取")
    print()
    print("🍪 获取 Cookie 步骤:")
    print("1. 打开浏览器，访问 https://www.xiaohongshu.com")
    print("2. 登录你的账号")
    print("3. 按 F12 打开开发者工具")
    print("4. 在 Network 标签页中刷新页面")
    print("5. 找到任意请求，复制 Cookie 值")
    print()
    print("🚀 爬虫使用:")
    print("- 基础版: 简单的爬取功能")
    print("- 增强版: 支持重试、验证码处理、更好的错误恢复")
    print()
    print("📁 输出文件:")
    print("- 数据保存在 core/media_crawler/data/xhs/ 目录")
    print("- 文件格式为 CSV，包含标题、点赞数、收藏数等信息")
    print()


def get_crawler_params():
    """获取爬虫参数"""
    print("\n🔤 请输入爬虫参数:")
    
    while True:
        keyword = input("🔍 搜索关键词 (必填): ").strip()
        if keyword:
            break
        print("❌ 关键词不能为空")
    
    while True:
        try:
            limit = input("📊 爬取数量 (默认 50): ").strip()
            if not limit:
                limit = 50
            else:
                limit = int(limit)
            if limit > 0:
                break
            else:
                print("❌ 数量必须大于 0")
        except ValueError:
            print("❌ 请输入有效的数字")
    
    return keyword, limit


def main():
    """主函数"""
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input("请选择操作 (0-6): ").strip()
        except KeyboardInterrupt:
            print("\n👋 再见!")
            break
        
        if choice == '0':
            print("👋 再见!")
            break
        
        elif choice == '1':
            print("\n🍪 启动 Cookie 更新工具...")
            run_script('update_cookie.py')
        
        elif choice == '2':
            print("\n🧪 测试 Cookie 有效性...")
            run_script('test_cookie.py')
        
        elif choice == '3':
            print("\n🕷️  启动基础版爬虫...")
            keyword, limit = get_crawler_params()
            run_script('run_crawler.py', ['--keyword', keyword, '--limit', str(limit)])
        
        elif choice == '4':
            print("\n🚀 启动增强版爬虫...")
            keyword, limit = get_crawler_params()
            run_script('run_crawler_enhanced.py', ['--keyword', keyword, '--limit', str(limit)])
        
        elif choice == '5':
            show_usage()
        
        elif choice == '6':
            print("\n📁 查看输出文件...")
            view_output_files()
        
        else:
            print("❌ 无效选择，请重新输入")
        
        if choice in ['1', '2', '3', '4']:
            input("\n⏸️  按回车键继续...")


if __name__ == '__main__':
    main()
