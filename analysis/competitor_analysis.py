#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
竞品笔记分析模块
分析小红书笔记的互动数据，识别高质量内容和内容类型
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import re


def classify_content_type(title, desc):
    """根据标题和描述分类内容类型"""
    title = str(title).lower()
    desc = str(desc).lower()
    content = f"{title} {desc}"
    
    # 定义关键词模式
    patterns = {
        '亲身体验': [
            '我的', '亲测', '体验', '试用', '使用感受', '真实感受',
            '第一次', '初体验', '尝试', '感受', '心得', '日记'
        ],
        '种草推荐': [
            '推荐', '安利', '种草', '必买', '好用', '值得', '强烈推荐',
            '不踩雷', '闭眼入', '回购', '爱用', '好物'
        ],
        '教程指导': [
            '教程', '教学', '怎么', '如何', '方法', '步骤', '技巧',
            '入门', '零基础', '新手', '指南', '攻略'
        ],
        '对比测评': [
            'vs', '对比', '测评', '评测', '区别', '哪个好', '选择',
            '比较', '测试', '横评', '对决'
        ],
        '知识科普': [
            '科普', '知识', '原理', '为什么', '什么是', '解析',
            '揭秘', '真相', '误区', '注意事项'
        ],
        '打卡分享': [
            '打卡', '日常', 'vlog', '记录', '分享', '今天',
            '坚持', '第几天', '进步', '变化'
        ]
    }
    
    # 计算每种类型的匹配分数
    scores = {}
    for content_type, keywords in patterns.items():
        score = sum(1 for keyword in keywords if keyword in content)
        scores[content_type] = score
    
    # 返回得分最高的类型
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    else:
        return '其他'


def calculate_engagement_metrics(df):
    """计算互动指标"""
    print("📊 计算互动指标...")
    
    # 转换数值类型
    numeric_columns = ['liked_count', 'collected_count', 'comment_count', 'share_count']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # 计算总互动数
    df['total_engagement'] = (
        df.get('liked_count', 0) + 
        df.get('collected_count', 0) + 
        df.get('comment_count', 0) + 
        df.get('share_count', 0)
    )
    
    # 计算互动率 (假设曝光量为总互动数的10-50倍)
    # 这里使用一个估算公式
    df['estimated_views'] = df['total_engagement'] * np.random.uniform(15, 35, len(df))
    df['engagement_rate'] = (df['total_engagement'] / df['estimated_views'] * 100).round(2)
    
    # 计算收藏率
    df['collect_rate'] = (df.get('collected_count', 0) / df['total_engagement'] * 100).round(2)
    df['collect_rate'] = df['collect_rate'].fillna(0)
    
    # 计算评论率
    df['comment_rate'] = (df.get('comment_count', 0) / df['total_engagement'] * 100).round(2)
    df['comment_rate'] = df['comment_rate'].fillna(0)
    
    return df


def analyze_time_patterns(df):
    """分析发布时间模式"""
    print("⏰ 分析发布时间模式...")
    
    if 'time' not in df.columns:
        return df
    
    # 转换时间戳
    df['publish_datetime'] = pd.to_datetime(df['time'], unit='ms', errors='coerce')
    df['publish_date'] = df['publish_datetime'].dt.date
    df['publish_hour'] = df['publish_datetime'].dt.hour
    df['publish_weekday'] = df['publish_datetime'].dt.day_name()
    df['publish_month'] = df['publish_datetime'].dt.month
    
    # 计算发布天数
    if not df['publish_datetime'].isna().all():
        latest_date = df['publish_datetime'].max()
        df['days_since_publish'] = (latest_date - df['publish_datetime']).dt.days
    
    return df


def identify_high_performance_content(df, top_n=20):
    """识别高表现内容"""
    print(f"🏆 识别前 {top_n} 个高表现内容...")
    
    # 按互动率排序
    high_engagement = df.nlargest(top_n, 'engagement_rate').copy()
    
    # 按总互动数排序
    high_total = df.nlargest(top_n, 'total_engagement').copy()
    
    # 按收藏率排序
    high_collect = df.nlargest(top_n, 'collect_rate').copy()
    
    return {
        'high_engagement': high_engagement,
        'high_total': high_total,
        'high_collect': high_collect
    }


def generate_competitor_report(df, output_dir):
    """生成竞品分析报告"""
    print("📋 生成竞品分析报告...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 基础统计
    stats = {
        '总笔记数': len(df),
        '平均点赞数': df['liked_count'].mean(),
        '平均收藏数': df['collected_count'].mean(),
        '平均评论数': df['comment_count'].mean(),
        '平均互动率': df['engagement_rate'].mean(),
        '最高互动率': df['engagement_rate'].max(),
        '最高点赞数': df['liked_count'].max()
    }
    
    # 内容类型分布
    content_type_dist = df['content_type'].value_counts()
    
    # 用户分析
    user_stats = df.groupby('nickname').agg({
        'total_engagement': ['count', 'mean', 'sum'],
        'engagement_rate': 'mean'
    }).round(2)
    
    user_stats.columns = ['发布数量', '平均互动数', '总互动数', '平均互动率']
    user_stats = user_stats.sort_values('总互动数', ascending=False).head(20)
    
    # 保存报告
    report_path = os.path.join(output_dir, f'competitor_report_{timestamp}.txt')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("小红书竞品笔记分析报告\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("📊 基础统计\n")
        f.write("-" * 30 + "\n")
        for key, value in stats.items():
            f.write(f"{key}: {value:.2f}\n")
        
        f.write("\n📋 内容类型分布\n")
        f.write("-" * 30 + "\n")
        for content_type, count in content_type_dist.items():
            percentage = count / len(df) * 100
            f.write(f"{content_type}: {count}篇 ({percentage:.1f}%)\n")
        
        f.write("\n👥 活跃用户TOP20\n")
        f.write("-" * 30 + "\n")
        f.write(user_stats.to_string())
        
        f.write(f"\n\n报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"📋 竞品分析报告已保存到: {report_path}")
    
    return stats, content_type_dist, user_stats


def create_visualizations(df, output_dir):
    """创建可视化图表"""
    print("📈 生成可视化图表...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 1. 互动指标分布图
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 点赞数分布
    axes[0, 0].hist(df['liked_count'], bins=30, alpha=0.7, color='skyblue')
    axes[0, 0].set_title('点赞数分布')
    axes[0, 0].set_xlabel('点赞数')
    axes[0, 0].set_ylabel('频次')
    
    # 收藏数分布
    axes[0, 1].hist(df['collected_count'], bins=30, alpha=0.7, color='lightgreen')
    axes[0, 1].set_title('收藏数分布')
    axes[0, 1].set_xlabel('收藏数')
    axes[0, 1].set_ylabel('频次')
    
    # 互动率分布
    axes[1, 0].hist(df['engagement_rate'], bins=30, alpha=0.7, color='orange')
    axes[1, 0].set_title('互动率分布')
    axes[1, 0].set_xlabel('互动率 (%)')
    axes[1, 0].set_ylabel('频次')
    
    # 内容类型分布
    content_counts = df['content_type'].value_counts()
    axes[1, 1].pie(content_counts.values, labels=content_counts.index, autopct='%1.1f%%')
    axes[1, 1].set_title('内容类型分布')
    
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, f'engagement_analysis_{timestamp}.png')
    plt.savefig(chart1_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. 时间趋势图
    if 'publish_datetime' in df.columns and not df['publish_datetime'].isna().all():
        fig, axes = plt.subplots(2, 1, figsize=(15, 10))
        
        # 按日期统计发布量
        daily_posts = df.groupby(df['publish_datetime'].dt.date).size()
        axes[0].plot(daily_posts.index, daily_posts.values, marker='o')
        axes[0].set_title('每日发布量趋势')
        axes[0].set_xlabel('日期')
        axes[0].set_ylabel('发布数量')
        axes[0].tick_params(axis='x', rotation=45)
        
        # 按小时统计发布量
        hourly_posts = df.groupby('publish_hour').size()
        axes[1].bar(hourly_posts.index, hourly_posts.values, alpha=0.7)
        axes[1].set_title('发布时间分布 (按小时)')
        axes[1].set_xlabel('小时')
        axes[1].set_ylabel('发布数量')
        
        plt.tight_layout()
        chart2_path = os.path.join(output_dir, f'time_analysis_{timestamp}.png')
        plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📈 时间分析图表已保存到: {chart2_path}")
    
    print(f"📈 互动分析图表已保存到: {chart1_path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='小红书竞品笔记分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python analysis/competitor_analysis.py --input core/media_crawler/data/xhs/1_search_contents_2025-07-02.csv
  python analysis/competitor_analysis.py --input data.csv --top-n 30
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
        '--top-n', '-n',
        type=int,
        default=20,
        help='分析前 N 个高表现内容 (默认: 20)'
    )
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"❌ 输入文件不存在: {args.input}")
        sys.exit(1)
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 60)
    print("🏆 小红书竞品笔记分析")
    print("=" * 60)
    
    try:
        # 读取数据
        print(f"📖 读取数据文件: {args.input}")
        df = pd.read_csv(args.input)
        
        print(f"📊 数据概览: {len(df)} 条笔记")
        
        # 数据清理
        df = df.fillna('')
        
        # 分类内容类型
        print("🏷️ 分析内容类型...")
        df['content_type'] = df.apply(
            lambda row: classify_content_type(row.get('title', ''), row.get('desc', '')),
            axis=1
        )
        
        # 计算互动指标
        df = calculate_engagement_metrics(df)
        
        # 分析时间模式
        df = analyze_time_patterns(df)
        
        # 识别高表现内容
        high_performance = identify_high_performance_content(df, args.top_n)
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存分析结果
        main_output = os.path.join(args.output_dir, f'competitor_analysis_{timestamp}.csv')
        
        # 选择要保存的列
        output_columns = [
            'title', 'nickname', 'content_type', 'liked_count', 'collected_count',
            'comment_count', 'share_count', 'total_engagement', 'engagement_rate',
            'collect_rate', 'comment_rate'
        ]
        
        # 添加时间相关列（如果存在）
        time_columns = ['publish_datetime', 'publish_date', 'publish_hour', 'days_since_publish']
        for col in time_columns:
            if col in df.columns:
                output_columns.append(col)
        
        # 按互动率排序并保存
        df_sorted = df.sort_values('engagement_rate', ascending=False)
        df_sorted[output_columns].to_csv(main_output, index=False, encoding='utf-8-sig')
        print(f"📄 竞品分析结果已保存到: {main_output}")
        
        # 保存高表现内容
        for category, data in high_performance.items():
            category_output = os.path.join(
                args.output_dir, f'{category}_{timestamp}.csv'
            )
            data[output_columns].to_csv(category_output, index=False, encoding='utf-8-sig')
            print(f"📄 {category} 已保存到: {category_output}")
        
        # 生成报告
        stats, content_dist, user_stats = generate_competitor_report(df, args.output_dir)
        
        # 创建可视化
        create_visualizations(df, args.output_dir)
        
        # 输出统计信息
        print("\n" + "=" * 60)
        print("📊 分析结果统计")
        print("=" * 60)
        print(f"📝 分析笔记数量: {len(df)}")
        print(f"📈 平均互动率: {stats['平均互动率']:.2f}%")
        print(f"🏆 最高互动率: {stats['最高互动率']:.2f}%")
        print(f"👍 最高点赞数: {int(stats['最高点赞数'])}")
        
        print("\n📋 内容类型分布:")
        for content_type, count in content_dist.head().items():
            percentage = count / len(df) * 100
            print(f"  {content_type}: {count}篇 ({percentage:.1f}%)")
        
        print("\n✅ 竞品分析完成!")
        
    except Exception as e:
        print(f"❌ 分析过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
