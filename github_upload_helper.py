#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 文件上传助手
"""

import base64
import os

def encode_file_to_base64(filepath):
    """将文件编码为 base64"""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        encoded = base64.b64encode(content).decode('utf-8')
        return encoded
    except Exception as e:
        print(f"编码文件失败: {e}")
        return None

def main():
    """主函数"""
    # 编码 README.md
    readme_content = encode_file_to_base64('README.md')
    if readme_content:
        print("README.md base64 编码 (前100字符):")
        print(readme_content[:100] + "...")
        print(f"总长度: {len(readme_content)} 字符")
        
        # 保存到文件
        with open('readme_base64.txt', 'w') as f:
            f.write(readme_content)
        print("✅ README.md base64 内容已保存到 readme_base64.txt")
    
    # 编码其他关键文件
    files_to_encode = [
        'requirements.txt',
        '.gitignore',
        '.github/workflows/daily_run.yml'
    ]
    
    for filepath in files_to_encode:
        if os.path.exists(filepath):
            content = encode_file_to_base64(filepath)
            if content:
                filename = filepath.replace('/', '_').replace('\\', '_')
                output_file = f"{filename}_base64.txt"
                with open(output_file, 'w') as f:
                    f.write(content)
                print(f"✅ {filepath} 已编码保存到 {output_file}")

if __name__ == "__main__":
    main()
