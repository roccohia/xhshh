#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检查工具 - 验证所有依赖是否正确安装
"""

import sys
import os
import subprocess
import importlib


def check_python_version():
    """检查 Python 版本"""
    print("🐍 检查 Python 版本...")
    version = sys.version_info
    print(f"   当前版本: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("   ✅ Python 版本符合要求 (>= 3.7)")
        return True
    else:
        print("   ❌ Python 版本过低，需要 3.7 或更高版本")
        return False


def check_required_packages():
    """检查必需的 Python 包"""
    print("\n📦 检查必需的 Python 包...")
    
    required_packages = [
        'httpx', 'playwright', 'tenacity', 'aiofiles', 
        'pandas', 'opencv-python', 'aiomysql', 'redis',
        'pydantic', 'fastapi', 'uvicorn', 'python-dotenv',
        'jieba', 'wordcloud', 'matplotlib', 'requests',
        'parsel', 'pyexecjs'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            # 特殊处理一些包名
            import_name = package
            if package == 'opencv-python':
                import_name = 'cv2'
            elif package == 'python-dotenv':
                import_name = 'dotenv'
            elif package == 'pyexecjs':
                import_name = 'execjs'
            
            importlib.import_module(import_name)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  缺少 {len(missing_packages)} 个包:")
        for pkg in missing_packages:
            print(f"     - {pkg}")
        print("\n💡 安装命令:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    else:
        print("   🎉 所有必需包都已安装!")
        return True


def check_playwright_browsers():
    """检查 Playwright 浏览器"""
    print("\n🌐 检查 Playwright 浏览器...")
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'playwright', 'install', '--dry-run'],
            capture_output=True, text=True, timeout=30
        )
        
        if 'chromium' in result.stdout.lower():
            print("   ✅ Chromium 浏览器已安装")
            return True
        else:
            print("   ❌ Chromium 浏览器未安装")
            print("   💡 安装命令: python -m playwright install chromium")
            return False
    except Exception as e:
        print(f"   ⚠️  无法检查浏览器状态: {e}")
        print("   💡 尝试安装: python -m playwright install chromium")
        return False


def check_config_file():
    """检查配置文件"""
    print("\n📄 检查配置文件...")
    
    config_path = os.path.join(os.path.dirname(__file__), '../config/xhs_config.json')
    
    if not os.path.exists(config_path):
        print(f"   ❌ 配置文件不存在: {config_path}")
        return False
    
    try:
        import json
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查必要字段
        required_fields = ['platform', 'cookie', 'headers']
        missing_fields = []
        
        for field in required_fields:
            if field not in config:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"   ❌ 配置文件缺少字段: {missing_fields}")
            return False
        
        # 检查 Cookie 字段
        cookie_fields = config.get('cookie', {})
        important_cookies = ['web_session', 'webId']
        
        has_important = any(key in cookie_fields for key in important_cookies)
        
        if not has_important:
            print("   ⚠️  配置文件中没有重要的 Cookie 字段")
            print("   💡 请运行: python scripts/update_cookie.py")
            return False
        
        print("   ✅ 配置文件格式正确")
        print(f"   📊 Cookie 字段数量: {len(cookie_fields)}")
        return True
        
    except json.JSONDecodeError:
        print("   ❌ 配置文件 JSON 格式错误")
        return False
    except Exception as e:
        print(f"   ❌ 读取配置文件失败: {e}")
        return False


def check_project_structure():
    """检查项目结构"""
    print("\n📁 检查项目结构...")
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    required_paths = [
        'config/xhs_config.json',
        'scripts/run_crawler.py',
        'scripts/run_crawler_enhanced.py',
        'scripts/config_manager.py',
        'core/media_crawler/main.py',
        'core/media_crawler/media_platform/xhs/core.py'
    ]
    
    missing_paths = []
    
    for path in required_paths:
        full_path = os.path.join(base_dir, path)
        if os.path.exists(full_path):
            print(f"   ✅ {path}")
        else:
            print(f"   ❌ {path}")
            missing_paths.append(path)
    
    if missing_paths:
        print(f"\n⚠️  缺少 {len(missing_paths)} 个文件")
        return False
    else:
        print("   🎉 项目结构完整!")
        return True


def main():
    """主函数"""
    print("=" * 60)
    print("🔍 小红书爬虫环境检查")
    print("=" * 60)
    
    checks = [
        ("Python 版本", check_python_version),
        ("Python 包", check_required_packages),
        ("Playwright 浏览器", check_playwright_browsers),
        ("配置文件", check_config_file),
        ("项目结构", check_project_structure)
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ 检查失败: {e}")
            results.append((name, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 检查结果总结")
    print("=" * 60)
    
    passed = 0
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:20s} {status}")
        if result:
            passed += 1
    
    print(f"\n📈 通过率: {passed}/{len(results)} ({passed/len(results)*100:.1f}%)")
    
    if passed == len(results):
        print("\n🎉 环境检查全部通过！可以开始使用爬虫了")
        print("\n🚀 下一步:")
        print("   1. python scripts/test_cookie.py")
        print("   2. python scripts/quick_start.py")
    else:
        print("\n⚠️  请先解决上述问题，然后重新运行检查")
        print("\n💡 常见解决方案:")
        print("   - 安装缺失的包: pip install -r core/media_crawler/requirements.txt")
        print("   - 安装浏览器: python -m playwright install chromium")
        print("   - 更新 Cookie: python scripts/update_cookie.py")


if __name__ == '__main__':
    main()
