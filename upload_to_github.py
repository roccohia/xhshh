#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 GitHub API 上传文件到仓库
"""

import os
import base64
import json

# 需要上传的关键文件列表
CRITICAL_FILES = [
    "README.md",
    "requirements.txt", 
    ".gitignore",
    ".github/workflows/daily_run.yml",
    "core/media_crawler/config/base_config.py",
    "scripts/xhs_crawler_direct.py",
    "scripts/telegram_push.py",
    "analysis/keyword_analysis.py",
    "analysis/koc_filter.py",
    "analysis/competitor_analysis.py",
    "analysis/topic_generator.py",
    "core/media_crawler/data/xhs/realistic_search_contents_2025-07-03.csv"
]

def get_file_content(filepath):
    """读取文件内容并编码为 base64"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                content = f.read()
            return base64.b64encode(content).decode('utf-8')
        else:
            print(f"⚠️  文件不存在: {filepath}")
            return None
    except Exception as e:
        print(f"❌ 读取文件失败 {filepath}: {e}")
        return None

def main():
    """主函数"""
    print("📋 准备上传的关键文件:")
    
    upload_list = []
    
    for filepath in CRITICAL_FILES:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✅ {filepath} ({size:,} 字节)")
            
            content = get_file_content(filepath)
            if content:
                upload_list.append({
                    'path': filepath,
                    'content': content,
                    'size': size
                })
        else:
            print(f"❌ {filepath} (文件不存在)")
    
    print(f"\n📊 总计: {len(upload_list)} 个文件准备上传")
    
    # 保存上传列表到文件
    with open('upload_list.json', 'w', encoding='utf-8') as f:
        json.dump(upload_list, f, indent=2, ensure_ascii=False)
    
    print("✅ 上传列表已保存到 upload_list.json")
    print("💡 请使用 GitHub API 工具上传这些文件")

if __name__ == "__main__":
    main()
