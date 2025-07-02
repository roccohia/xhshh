#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KOC 用户筛选模块
筛选高互动、中等粉丝量的 KOC (Key Opinion Consumer) 用户
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


def estimate_follower_count(nickname, liked_count, collected_count, comment_count):
    """
    估算用户粉丝数
    基于用户昵称特征和互动数据进行估算
    """
    # 基础互动数
    total_engagement = liked_count + collected_count + comment_count
    
    # 昵称特征分析
    nickname_score = 0
    nickname = str(nickname).lower()
    
    # 机构/品牌特征 (通常粉丝较多)
    brand_keywords = [
        '官方', '旗舰店', '品牌', '工作室', '机构', '中心',
        '学院', '培训', '教育', '健身房', '瑜伽馆', '普拉提馆'
    ]
    
    # 个人博主特征
    personal_keywords = [
        '老师', '教练', '博主', '达人', '分享', '记录',
        '日记', '生活', '小', '爱', '喜欢'
    ]
    
    # 新手特征 (通常粉丝较少)
    newbie_keywords = [
        '新手', '小白', '初学', '菜鸟', '学习中', '努力',
        '加油', '坚持', '第一次', '尝试'
    ]
    
    if any(keyword in nickname for keyword in brand_keywords):
        nickname_score = 3  # 机构类，粉丝可能较多
    elif any(keyword in nickname for keyword in personal_keywords):
        nickname_score = 2  # 个人博主
    elif any(keyword in nickname for keyword in newbie_keywords):
        nickname_score = 1  # 新手用户
    else:
        nickname_score = 1.5  # 普通用户
    
    # 基于互动数估算粉丝数
    # 假设互动率在 2%-8% 之间
    if total_engagement > 0:
        # 使用不同的互动率估算
        estimated_followers_low = total_engagement / 0.08  # 8% 互动率
        estimated_followers_high = total_engagement / 0.02  # 2% 互动率
        estimated_followers = (estimated_followers_low + estimated_followers_high) / 2
        
        # 根据昵称特征调整
        estimated_followers *= nickname_score
        
        return int(estimated_followers)
    else:
        return 0


def classify_user_type(nickname, estimated_followers, avg_engagement):
    """分类用户类型"""
    nickname = str(nickname).lower()
    
    # 机构/品牌账号
    brand_keywords = [
        '官方', '旗舰店', '品牌', '工作室', '机构', '中心',
        '学院', '培训', '教育', '健身房', '瑜伽馆', '普拉提馆'
    ]
    
    if any(keyword in nickname for keyword in brand_keywords):
        return '机构/品牌'
    
    # 根据粉丝数和互动数分类
    if estimated_followers >= 100000:  # 10万+
        return '头部KOL'
    elif estimated_followers >= 50000:  # 5-10万
        return '腰部KOL'
    elif estimated_followers >= 10000:  # 1-5万
        if avg_engagement >= 500:
            return '优质KOC'
        else:
            return '普通KOL'
    elif estimated_followers >= 1000:  # 1千-1万
        if avg_engagement >= 200:
            return '潜力KOC'
        else:
            return '普通用户'
    else:  # 1千以下
        if avg_engagement >= 100:
            return '新兴KOC'
        else:
            return '普通用户'


def calculate_koc_score(row):
    """计算 KOC 评分"""
    # 基础分数
    score = 0
    
    # 互动数评分 (40%)
    engagement_score = min(row['avg_total_engagement'] / 1000 * 40, 40)
    score += engagement_score
    
    # 互动率评分 (30%)
    engagement_rate_score = min(row['avg_engagement_rate'] / 10 * 30, 30)
    score += engagement_rate_score
    
    # 发布频率评分 (20%)
    post_frequency_score = min(row['post_count'] / 10 * 20, 20)
    score += post_frequency_score
    
    # 粉丝数适中性评分 (10%)
    followers = row['estimated_followers']
    if 1000 <= followers <= 50000:  # 理想的 KOC 粉丝范围
        follower_score = 10
    elif followers < 1000:
        follower_score = followers / 1000 * 10
    else:  # followers > 50000
        follower_score = max(10 - (followers - 50000) / 10000, 0)
    
    score += follower_score
    
    return min(score, 100)  # 最高100分


def filter_koc_users(df, min_likes=200, max_followers=50000, min_engagement_rate=2.0):
    """筛选 KOC 用户"""
    print(f"🔍 筛选 KOC 用户 (点赞>{min_likes}, 粉丝<{max_followers}, 互动率>{min_engagement_rate}%)...")
    
    # 按用户聚合数据
    user_stats = df.groupby(['user_id', 'nickname']).agg({
        'liked_count': ['mean', 'max', 'sum'],
        'collected_count': ['mean', 'max', 'sum'],
        'comment_count': ['mean', 'max', 'sum'],
        'share_count': ['mean', 'max', 'sum'],
        'title': 'count'  # 发布数量
    }).round(2)
    
    # 重命名列
    user_stats.columns = [
        'avg_liked', 'max_liked', 'total_liked',
        'avg_collected', 'max_collected', 'total_collected',
        'avg_comment', 'max_comment', 'total_comment',
        'avg_share', 'max_share', 'total_share',
        'post_count'
    ]
    
    # 重置索引
    user_stats = user_stats.reset_index()
    
    # 计算总互动数
    user_stats['avg_total_engagement'] = (
        user_stats['avg_liked'] + user_stats['avg_collected'] + 
        user_stats['avg_comment'] + user_stats['avg_share']
    )
    
    user_stats['max_total_engagement'] = (
        user_stats['max_liked'] + user_stats['max_collected'] + 
        user_stats['max_comment'] + user_stats['max_share']
    )
    
    # 估算粉丝数
    user_stats['estimated_followers'] = user_stats.apply(
        lambda row: estimate_follower_count(
            row['nickname'], row['avg_liked'], 
            row['avg_collected'], row['avg_comment']
        ), axis=1
    )
    
    # 计算互动率
    user_stats['avg_engagement_rate'] = (
        user_stats['avg_total_engagement'] / 
        (user_stats['estimated_followers'] * 0.05)  # 假设5%的曝光率
    ).fillna(0) * 100
    
    # 分类用户类型
    user_stats['user_type'] = user_stats.apply(
        lambda row: classify_user_type(
            row['nickname'], row['estimated_followers'], row['avg_total_engagement']
        ), axis=1
    )
    
    # 计算 KOC 评分
    user_stats['koc_score'] = user_stats.apply(calculate_koc_score, axis=1)
    
    # 筛选条件
    koc_filter = (
        (user_stats['avg_liked'] >= min_likes) &
        (user_stats['estimated_followers'] <= max_followers) &
        (user_stats['avg_engagement_rate'] >= min_engagement_rate) &
        (user_stats['post_count'] >= 2)  # 至少发布2篇
    )
    
    koc_users = user_stats[koc_filter].copy()
    
    # 按 KOC 评分排序
    koc_users = koc_users.sort_values('koc_score', ascending=False)
    
    print(f"✅ 筛选出 {len(koc_users)} 个 KOC 用户")
    
    return koc_users, user_stats


def analyze_koc_characteristics(koc_users, all_users):
    """分析 KOC 用户特征"""
    print("📊 分析 KOC 用户特征...")
    
    analysis = {}
    
    # 基础统计
    analysis['total_koc'] = len(koc_users)
    analysis['total_users'] = len(all_users)
    analysis['koc_ratio'] = len(koc_users) / len(all_users) * 100
    
    # KOC 用户的平均指标
    analysis['avg_koc_followers'] = koc_users['estimated_followers'].mean()
    analysis['avg_koc_engagement'] = koc_users['avg_total_engagement'].mean()
    analysis['avg_koc_posts'] = koc_users['post_count'].mean()
    analysis['avg_koc_score'] = koc_users['koc_score'].mean()
    
    # 用户类型分布
    analysis['user_type_dist'] = koc_users['user_type'].value_counts().to_dict()
    
    # 粉丝数分布
    follower_ranges = [
        (0, 1000, '1K以下'),
        (1000, 5000, '1K-5K'),
        (5000, 10000, '5K-1W'),
        (10000, 30000, '1W-3W'),
        (30000, 50000, '3W-5W')
    ]
    
    follower_dist = {}
    for min_f, max_f, label in follower_ranges:
        count = len(koc_users[
            (koc_users['estimated_followers'] >= min_f) & 
            (koc_users['estimated_followers'] < max_f)
        ])
        follower_dist[label] = count
    
    analysis['follower_dist'] = follower_dist
    
    return analysis


def create_koc_visualizations(koc_users, all_users, output_dir):
    """创建 KOC 分析可视化图表"""
    print("📈 生成 KOC 分析图表...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建图表
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. KOC 评分分布
    axes[0, 0].hist(koc_users['koc_score'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('KOC 评分分布')
    axes[0, 0].set_xlabel('KOC 评分')
    axes[0, 0].set_ylabel('用户数量')
    axes[0, 0].axvline(koc_users['koc_score'].mean(), color='red', linestyle='--', 
                       label=f'平均分: {koc_users["koc_score"].mean():.1f}')
    axes[0, 0].legend()
    
    # 2. 粉丝数 vs 互动数散点图
    scatter = axes[0, 1].scatter(koc_users['estimated_followers'], koc_users['avg_total_engagement'], 
                                c=koc_users['koc_score'], cmap='viridis', alpha=0.7)
    axes[0, 1].set_title('粉丝数 vs 平均互动数')
    axes[0, 1].set_xlabel('估算粉丝数')
    axes[0, 1].set_ylabel('平均互动数')
    plt.colorbar(scatter, ax=axes[0, 1], label='KOC评分')
    
    # 3. 用户类型分布
    user_type_counts = koc_users['user_type'].value_counts()
    axes[1, 0].pie(user_type_counts.values, labels=user_type_counts.index, autopct='%1.1f%%')
    axes[1, 0].set_title('KOC 用户类型分布')
    
    # 4. 发布数量 vs KOC 评分
    axes[1, 1].scatter(koc_users['post_count'], koc_users['koc_score'], alpha=0.7, color='orange')
    axes[1, 1].set_title('发布数量 vs KOC 评分')
    axes[1, 1].set_xlabel('发布数量')
    axes[1, 1].set_ylabel('KOC 评分')
    
    # 添加趋势线
    z = np.polyfit(koc_users['post_count'], koc_users['koc_score'], 1)
    p = np.poly1d(z)
    axes[1, 1].plot(koc_users['post_count'], p(koc_users['post_count']), "r--", alpha=0.8)
    
    plt.tight_layout()
    
    chart_path = os.path.join(output_dir, f'koc_analysis_{timestamp}.png')
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📈 KOC 分析图表已保存到: {chart_path}")
    
    return chart_path


def generate_koc_report(analysis, output_dir):
    """生成 KOC 分析报告"""
    print("📋 生成 KOC 分析报告...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f'koc_analysis_report_{timestamp}.txt')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("小红书 KOC 用户分析报告\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("📊 基础统计\n")
        f.write("-" * 30 + "\n")
        f.write(f"总用户数: {analysis['total_users']}\n")
        f.write(f"KOC 用户数: {analysis['total_koc']}\n")
        f.write(f"KOC 占比: {analysis['koc_ratio']:.2f}%\n\n")
        
        f.write("📈 KOC 用户平均指标\n")
        f.write("-" * 30 + "\n")
        f.write(f"平均粉丝数: {analysis['avg_koc_followers']:.0f}\n")
        f.write(f"平均互动数: {analysis['avg_koc_engagement']:.1f}\n")
        f.write(f"平均发布数: {analysis['avg_koc_posts']:.1f}\n")
        f.write(f"平均 KOC 评分: {analysis['avg_koc_score']:.1f}\n\n")
        
        f.write("👥 用户类型分布\n")
        f.write("-" * 30 + "\n")
        for user_type, count in analysis['user_type_dist'].items():
            percentage = count / analysis['total_koc'] * 100
            f.write(f"{user_type}: {count}人 ({percentage:.1f}%)\n")
        
        f.write("\n📊 粉丝数分布\n")
        f.write("-" * 30 + "\n")
        for range_label, count in analysis['follower_dist'].items():
            percentage = count / analysis['total_koc'] * 100 if analysis['total_koc'] > 0 else 0
            f.write(f"{range_label}: {count}人 ({percentage:.1f}%)\n")
        
        f.write(f"\n\n报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"📋 KOC 分析报告已保存到: {report_path}")
    
    return report_path


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='小红书 KOC 用户筛选工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python analysis/koc_filter.py --input core/media_crawler/data/xhs/1_search_contents_2025-07-02.csv
  python analysis/koc_filter.py --input data.csv --min-likes 300 --max-followers 30000
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
        '--min-likes',
        type=int,
        default=200,
        help='最小平均点赞数 (默认: 200)'
    )
    parser.add_argument(
        '--max-followers',
        type=int,
        default=50000,
        help='最大粉丝数 (默认: 50000)'
    )
    parser.add_argument(
        '--min-engagement-rate',
        type=float,
        default=2.0,
        help='最小互动率百分比 (默认: 2.0)'
    )
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"❌ 输入文件不存在: {args.input}")
        sys.exit(1)
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 60)
    print("🎯 小红书 KOC 用户筛选")
    print("=" * 60)
    
    try:
        # 读取数据
        print(f"📖 读取数据文件: {args.input}")
        df = pd.read_csv(args.input)
        
        print(f"📊 数据概览: {len(df)} 条笔记")
        
        # 数据清理
        numeric_columns = ['liked_count', 'collected_count', 'comment_count', 'share_count']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # 筛选 KOC 用户
        koc_users, all_users = filter_koc_users(
            df, args.min_likes, args.max_followers, args.min_engagement_rate
        )
        
        if len(koc_users) == 0:
            print("⚠️  没有找到符合条件的 KOC 用户，请调整筛选条件")
            sys.exit(0)
        
        # 分析 KOC 特征
        analysis = analyze_koc_characteristics(koc_users, all_users)
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存 KOC 用户列表
        koc_output = os.path.join(args.output_dir, f'koc_users_{timestamp}.csv')
        
        # 选择输出列
        output_columns = [
            'nickname', 'user_type', 'estimated_followers', 'post_count',
            'avg_liked', 'avg_collected', 'avg_comment', 'avg_total_engagement',
            'avg_engagement_rate', 'koc_score', 'max_total_engagement'
        ]
        
        koc_users[output_columns].to_csv(koc_output, index=False, encoding='utf-8-sig')
        print(f"📄 KOC 用户列表已保存到: {koc_output}")
        
        # 保存所有用户统计
        all_users_output = os.path.join(args.output_dir, f'all_users_stats_{timestamp}.csv')
        all_users[output_columns].to_csv(all_users_output, index=False, encoding='utf-8-sig')
        print(f"📄 所有用户统计已保存到: {all_users_output}")
        
        # 生成可视化
        create_koc_visualizations(koc_users, all_users, args.output_dir)
        
        # 生成报告
        generate_koc_report(analysis, args.output_dir)
        
        # 输出统计信息
        print("\n" + "=" * 60)
        print("📊 KOC 筛选结果统计")
        print("=" * 60)
        print(f"📝 总用户数: {analysis['total_users']}")
        print(f"🎯 KOC 用户数: {analysis['total_koc']}")
        print(f"📊 KOC 占比: {analysis['koc_ratio']:.2f}%")
        print(f"👥 平均粉丝数: {analysis['avg_koc_followers']:.0f}")
        print(f"💬 平均互动数: {analysis['avg_koc_engagement']:.1f}")
        print(f"⭐ 平均 KOC 评分: {analysis['avg_koc_score']:.1f}")
        
        print("\n🏆 TOP 10 KOC 用户:")
        top_koc = koc_users.head(10)
        for i, (_, user) in enumerate(top_koc.iterrows(), 1):
            print(f"  {i:2d}. {user['nickname']} (评分: {user['koc_score']:.1f}, "
                  f"粉丝: {user['estimated_followers']:.0f}, 互动: {user['avg_total_engagement']:.1f})")
        
        print("\n✅ KOC 筛选完成!")
        
    except Exception as e:
        print(f"❌ 筛选过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
