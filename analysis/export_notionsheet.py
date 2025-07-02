#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion 内容日历导出模块
生成适用于 Notion 导入的内容日历 CSV 文件
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import glob
import re


def find_latest_analysis_files(output_dir):
    """查找最新的分析文件"""
    files = {}
    
    # 查找各类分析文件
    patterns = {
        'topic_suggestions': 'topic_suggestions_*.csv',
        'high_engagement': 'high_engagement_*.csv',
        'keywords_analysis': 'keywords_analysis_*.csv'
    }
    
    for file_type, pattern in patterns.items():
        file_pattern = os.path.join(output_dir, pattern)
        matching_files = glob.glob(file_pattern)
        
        if matching_files:
            # 选择最新的文件（按文件名排序，通常包含时间戳）
            latest_file = sorted(matching_files)[-1]
            files[file_type] = latest_file
            print(f"✅ 找到 {file_type}: {os.path.basename(latest_file)}")
        else:
            print(f"⚠️  未找到 {file_type} 文件")
            files[file_type] = None
    
    return files


def load_analysis_data(files):
    """加载分析数据"""
    data = {}
    
    # 加载选题建议
    if files['topic_suggestions']:
        try:
            data['topics'] = pd.read_csv(files['topic_suggestions'])
            print(f"📊 加载选题建议: {len(data['topics'])} 条")
        except Exception as e:
            print(f"❌ 加载选题建议失败: {e}")
            data['topics'] = None
    
    # 加载高互动内容
    if files['high_engagement']:
        try:
            data['high_engagement'] = pd.read_csv(files['high_engagement'])
            print(f"📊 加载高互动内容: {len(data['high_engagement'])} 条")
        except Exception as e:
            print(f"❌ 加载高互动内容失败: {e}")
            data['high_engagement'] = None
    
    # 加载关键词分析
    if files['keywords_analysis']:
        try:
            data['keywords'] = pd.read_csv(files['keywords_analysis'])
            print(f"📊 加载关键词分析: {len(data['keywords'])} 条")
        except Exception as e:
            print(f"❌ 加载关键词分析失败: {e}")
            data['keywords'] = None
    
    return data


def extract_content_highlights(title, desc=""):
    """从标题和描述中提取内容亮点"""
    if not title or pd.isna(title):
        return ""
    
    title = str(title)
    desc = str(desc) if desc and not pd.isna(desc) else ""
    content = f"{title} {desc}".lower()
    
    # 定义亮点关键词模式
    highlight_patterns = {
        '数字亮点': [r'\d+天', r'\d+个', r'\d+种', r'\d+分钟', r'\d+次'],
        '效果亮点': ['减肥', '塑形', '瘦身', '变化', '效果', '改善', '提升'],
        '体验亮点': ['亲测', '真实', '体验', '感受', '心得', '分享'],
        '专业亮点': ['教程', '教学', '技巧', '方法', '指导', '专业'],
        '对比亮点': ['vs', '对比', '区别', '哪个好', '选择'],
        '情感亮点': ['爱了', '绝了', '太好', '超棒', '推荐', '必看']
    }
    
    highlights = []
    
    for category, patterns in highlight_patterns.items():
        for pattern in patterns:
            if re.search(pattern, content):
                highlights.append(category.replace('亮点', ''))
                break
    
    # 如果没有找到特定亮点，尝试提取数字或关键词
    if not highlights:
        # 提取数字
        numbers = re.findall(r'\d+', title)
        if numbers:
            highlights.append(f"{numbers[0]}个要点")
        
        # 提取动词
        action_words = ['学会', '掌握', '了解', '体验', '尝试', '练习']
        for word in action_words:
            if word in content:
                highlights.append(f"{word}方法")
                break
    
    return "、".join(highlights[:2]) if highlights else ""


def generate_content_calendar(data, days=30):
    """生成内容日历"""
    print(f"📅 生成 {days} 天内容日历...")
    
    calendar_entries = []
    
    # 生成日期列表（从今天开始的未来30天）
    start_date = datetime.now().date()
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    # 准备数据源
    topics = data.get('topics')
    high_engagement = data.get('high_engagement')
    keywords = data.get('keywords')
    
    # 获取前5个高频关键词
    top_keywords = []
    if keywords is not None and len(keywords) > 0:
        top_keywords = keywords.head(5)['关键词'].tolist()
    
    # 默认目标人群
    target_audiences = ['宝妈', '健身初学者', '上班族', '学生党', '新手妈妈', '职场女性']
    
    # 生成内容日历条目
    for i, date in enumerate(dates):
        entry = {}
        
        # 日期
        entry['Date'] = date.strftime('%Y-%m-%d')
        
        # 主题方向
        if topics is not None and len(topics) > 0:
            topic_idx = i % len(topics)
            topic_row = topics.iloc[topic_idx]
            entry['主题方向'] = topic_row.get('type', '通用内容')
        else:
            # 默认主题方向
            default_topics = ['体验分享', '教程指导', '对比测评', '知识科普', '打卡记录']
            entry['主题方向'] = default_topics[i % len(default_topics)]
        
        # 标题草稿
        if high_engagement is not None and len(high_engagement) > 0:
            title_idx = i % len(high_engagement)
            title_row = high_engagement.iloc[title_idx]
            original_title = title_row.get('title', '')
            
            # 对原标题进行简单改写，避免完全重复
            if original_title:
                # 简单的标题变化策略
                variations = [
                    f"我的{original_title}",
                    f"{original_title}｜真实体验",
                    f"分享：{original_title}",
                    f"{original_title}（详细版）",
                    original_title  # 保留原标题
                ]
                entry['标题草稿'] = random.choice(variations)
                
                # 提取内容亮点
                desc = title_row.get('desc', '') if 'desc' in title_row else ''
                entry['内容亮点'] = extract_content_highlights(original_title, desc)
                
                # 笔记链接
                entry['笔记链接'] = title_row.get('note_url', '') if 'note_url' in title_row else ''
            else:
                entry['标题草稿'] = f"第{i+1}天内容分享"
                entry['内容亮点'] = ""
                entry['笔记链接'] = ""
        else:
            entry['标题草稿'] = f"第{i+1}天内容分享"
            entry['内容亮点'] = ""
            entry['笔记链接'] = ""
        
        # 关键词标签
        if top_keywords:
            # 随机选择2-3个关键词
            selected_keywords = random.sample(top_keywords, min(3, len(top_keywords)))
            entry['关键词标签'] = "、".join(selected_keywords)
        else:
            entry['关键词标签'] = "普拉提、运动、健身"
        
        # 目标人群（随机选择1-2个）
        num_audiences = random.randint(1, 2)
        selected_audiences = random.sample(target_audiences, num_audiences)
        entry['目标人群'] = "、".join(selected_audiences)
        
        # 发布状态
        entry['发布状态'] = "待写"
        
        calendar_entries.append(entry)
    
    return pd.DataFrame(calendar_entries)


def optimize_calendar_distribution(calendar_df):
    """优化内容日历分布"""
    print("🔧 优化内容分布...")
    
    # 确保主题方向分布均匀
    unique_topics = calendar_df['主题方向'].unique()
    
    # 重新分配主题，确保分布更均匀
    for i, topic in enumerate(unique_topics):
        # 每个主题分配到对应的日期
        topic_indices = list(range(i, len(calendar_df), len(unique_topics)))
        calendar_df.loc[topic_indices, '主题方向'] = topic
    
    # 确保周末有更轻松的内容
    for idx, row in calendar_df.iterrows():
        date_obj = datetime.strptime(row['Date'], '%Y-%m-%d')
        weekday = date_obj.weekday()
        
        # 周末（周六日）安排轻松内容
        if weekday >= 5:  # 5=周六, 6=周日
            if '教程' in row['主题方向'] or '对比' in row['主题方向']:
                calendar_df.loc[idx, '主题方向'] = '打卡分享'
                calendar_df.loc[idx, '标题草稿'] = f"周末放松｜{row['标题草稿']}"
    
    return calendar_df


def add_content_suggestions(calendar_df):
    """添加内容建议"""
    print("💡 添加内容建议...")
    
    # 为每个条目添加内容建议
    suggestions = []
    
    for _, row in calendar_df.iterrows():
        topic = row['主题方向']
        
        if '体验' in topic:
            suggestion = "分享个人真实体验，包含前后对比"
        elif '教程' in topic:
            suggestion = "提供详细步骤，配图或视频演示"
        elif '对比' in topic:
            suggestion = "客观分析优缺点，给出明确建议"
        elif '科普' in topic:
            suggestion = "用通俗易懂的语言解释专业知识"
        elif '打卡' in topic:
            suggestion = "记录日常练习，展示坚持过程"
        else:
            suggestion = "结合个人经验，提供实用价值"
        
        suggestions.append(suggestion)
    
    calendar_df['内容建议'] = suggestions
    
    return calendar_df


def save_notion_calendar(calendar_df, output_path):
    """保存 Notion 内容日历"""
    print(f"💾 保存 Notion 内容日历到: {output_path}")
    
    # 确保列顺序符合 Notion 导入要求
    column_order = [
        'Date', '主题方向', '标题草稿', '关键词标签', 
        '目标人群', '内容亮点', '内容建议', '笔记链接', '发布状态'
    ]
    
    # 重新排列列顺序
    calendar_df = calendar_df[column_order]
    
    # 保存为 CSV
    calendar_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"✅ 成功生成 {len(calendar_df)} 条内容日历记录")
    
    return calendar_df


def generate_summary_report(calendar_df, output_dir):
    """生成汇总报告"""
    print("📋 生成汇总报告...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f'notion_calendar_report_{timestamp}.txt')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("Notion 内容日历生成报告\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"日历条目数量: {len(calendar_df)}\n")
        f.write(f"日期范围: {calendar_df['Date'].min()} 到 {calendar_df['Date'].max()}\n\n")
        
        # 主题方向分布
        f.write("📊 主题方向分布:\n")
        f.write("-" * 30 + "\n")
        topic_counts = calendar_df['主题方向'].value_counts()
        for topic, count in topic_counts.items():
            percentage = count / len(calendar_df) * 100
            f.write(f"{topic}: {count}条 ({percentage:.1f}%)\n")
        
        # 目标人群分布
        f.write("\n👥 目标人群分布:\n")
        f.write("-" * 30 + "\n")
        all_audiences = []
        for audiences in calendar_df['目标人群']:
            all_audiences.extend(audiences.split('、'))
        
        from collections import Counter
        audience_counts = Counter(all_audiences)
        for audience, count in audience_counts.most_common():
            f.write(f"{audience}: {count}次\n")
        
        # 关键词使用情况
        f.write("\n🔤 关键词使用情况:\n")
        f.write("-" * 30 + "\n")
        all_keywords = []
        for keywords in calendar_df['关键词标签']:
            all_keywords.extend(keywords.split('、'))
        
        keyword_counts = Counter(all_keywords)
        for keyword, count in keyword_counts.most_common(10):
            f.write(f"{keyword}: {count}次\n")
        
        f.write(f"\n\n报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"📋 汇总报告已保存到: {report_path}")
    
    return report_path


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='生成 Notion 内容日历导入用的 CSV 文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python analysis/export_notionsheet.py
  python analysis/export_notionsheet.py --output-dir output --days 45
  python analysis/export_notionsheet.py --input-dir analysis_results
        """
    )

    parser.add_argument(
        '--input-dir', '-i',
        type=str,
        default='output',
        help='分析结果输入目录 (默认: output)'
    )
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='output',
        help='输出目录 (默认: output)'
    )
    parser.add_argument(
        '--days', '-d',
        type=int,
        default=30,
        help='生成日历的天数 (默认: 30)'
    )
    parser.add_argument(
        '--filename',
        type=str,
        default='notion_content_calendar.csv',
        help='输出文件名 (默认: notion_content_calendar.csv)'
    )

    args = parser.parse_args()

    # 检查输入目录
    if not os.path.exists(args.input_dir):
        print(f"❌ 输入目录不存在: {args.input_dir}")
        sys.exit(1)

    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 60)
    print("📅 Notion 内容日历生成器")
    print("=" * 60)

    try:
        # 查找分析文件
        print(f"🔍 在目录中查找分析文件: {args.input_dir}")
        analysis_files = find_latest_analysis_files(args.input_dir)

        # 检查是否找到必要文件
        if not any(analysis_files.values()):
            print("❌ 未找到任何分析文件")
            print("请先运行数据分析模块生成必要的文件")
            sys.exit(1)

        # 加载分析数据
        print("\n📖 加载分析数据...")
        data = load_analysis_data(analysis_files)

        # 生成内容日历
        print(f"\n📅 生成 {args.days} 天内容日历...")
        calendar_df = generate_content_calendar(data, args.days)

        # 优化内容分布
        calendar_df = optimize_calendar_distribution(calendar_df)

        # 添加内容建议
        calendar_df = add_content_suggestions(calendar_df)

        # 保存 Notion 日历
        output_path = os.path.join(args.output_dir, args.filename)
        calendar_df = save_notion_calendar(calendar_df, output_path)

        # 生成汇总报告
        report_path = generate_summary_report(calendar_df, args.output_dir)

        # 输出统计信息
        print("\n" + "=" * 60)
        print("📊 生成结果统计")
        print("=" * 60)
        print(f"📅 日历条目数量: {len(calendar_df)}")
        print(f"📆 日期范围: {calendar_df['Date'].min()} 到 {calendar_df['Date'].max()}")
        print(f"📁 输出文件: {output_path}")
        print(f"📋 汇总报告: {report_path}")

        # 显示主题分布
        print("\n📊 主题方向分布:")
        topic_counts = calendar_df['主题方向'].value_counts()
        for topic, count in topic_counts.head().items():
            percentage = count / len(calendar_df) * 100
            print(f"  {topic}: {count}条 ({percentage:.1f}%)")

        # 显示前几条示例
        print("\n📝 前5条内容预览:")
        for i, (_, row) in enumerate(calendar_df.head().iterrows(), 1):
            print(f"  {i}. {row['Date']} | {row['主题方向']} | {row['标题草稿'][:30]}...")

        print(f"\n✅ Notion 内容日历生成完成!")
        print(f"💡 可直接将 {args.filename} 导入到 Notion 数据库中")

    except Exception as e:
        print(f"❌ 生成过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
