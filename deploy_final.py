#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终部署脚本 - 推送完整的小红书数据分析系统到 GitHub
"""

import os
import subprocess
import sys
from datetime import datetime

def run_command(command, description):
    """运行命令并返回结果"""
    print(f"\n🔧 {description}")
    print(f"📝 执行: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print("📤 输出:")
            print(result.stdout)
        
        if result.stderr and result.returncode != 0:
            print("⚠️  错误:")
            print(result.stderr)
        
        success = result.returncode == 0
        print(f"{'✅' if success else '❌'} {description} {'成功' if success else '失败'}")
        return success
        
    except Exception as e:
        print(f"❌ {description} 异常: {e}")
        return False

def main():
    """主部署函数"""
    print("🚀 开始最终部署到 GitHub")
    print(f"⏰ 部署时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 检查是否在正确的目录
    if not os.path.exists('.github/workflows/daily_run.yml'):
        print("❌ 错误: 请在项目根目录运行此脚本")
        return False
    
    # 步骤1: 配置 Git 用户信息
    print("\n📋 步骤1: 配置 Git 用户信息")
    run_command('git config user.name "roccohia"', "设置 Git 用户名")
    run_command('git config user.email "yurongxin@yahoo.com"', "设置 Git 邮箱")
    
    # 步骤2: 添加所有文件
    print("\n📋 步骤2: 添加文件到 Git")
    if not run_command('git add .', "添加所有文件"):
        print("❌ 添加文件失败")
        return False
    
    # 步骤3: 检查状态
    print("\n📋 步骤3: 检查 Git 状态")
    run_command('git status', "检查 Git 状态")
    
    # 步骤4: 创建提交
    print("\n📋 步骤4: 创建提交")
    commit_message = f"🚀 完整小红书数据分析系统 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    if not run_command(f'git commit -m "{commit_message}"', "创建提交"):
        print("⚠️  可能没有新的更改需要提交")
    
    # 步骤5: 推送到远程仓库
    print("\n📋 步骤5: 推送到 GitHub")
    if not run_command('git push origin main', "推送到 GitHub"):
        print("❌ 推送失败，可能需要设置远程仓库")
        
        # 尝试设置远程仓库
        print("\n🔧 尝试设置远程仓库...")
        run_command('git remote add origin https://github.com/roccohia/xhshh.git', "添加远程仓库")
        
        # 再次尝试推送
        if not run_command('git push -u origin main', "强制推送到 GitHub"):
            print("❌ 推送仍然失败")
            return False
    
    # 步骤6: 验证推送结果
    print("\n📋 步骤6: 验证推送结果")
    run_command('git log --oneline -5', "查看最近提交")
    
    print("\n" + "=" * 80)
    print("🎉 部署完成！")
    print("✅ 代码已成功推送到 GitHub")
    print("🔗 仓库地址: https://github.com/roccohia/xhshh")
    print("\n📋 下一步操作:")
    print("1. 访问 GitHub 仓库确认代码已上传")
    print("2. 设置 GitHub Secrets (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)")
    print("3. 启用 GitHub Actions")
    print("4. 监控每日自动运行结果")
    print("=" * 80)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
