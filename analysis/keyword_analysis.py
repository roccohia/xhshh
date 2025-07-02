#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关键词分析模块
读取小红书笔记数据，分析标题中的关键词频率，生成词云图
"""

import os
import sys
import argparse
import pandas as pd
import jieba
import jieba.analyse
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np


def setup_jieba():
    """设置 jieba 分词"""
    # 添加自定义词典
    custom_words = [
        '普拉提', '瑜伽', '健身', '减肥', '塑形', '体态', '核心',
        '小红书', '种草', '测评', '推荐', '分享', '体验',
        '教程', '入门', '进阶', '专业', '器械', '垫上',
        '私教', '课程', '训练', '运动', '康复'
    ]
    
    for word in custom_words:
        jieba.add_word(word)
    
    # 设置停用词
    stop_words = {
        '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
        '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
        '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '里',
        '就是', '还是', '比较', '非常', '特别', '真的', '可以', '但是',
        '因为', '所以', '如果', '虽然', '然后', '还有', '或者', '以及',
        '以为', '觉得', '感觉', '应该', '可能', '一定', '肯定', '绝对',
        '完全', '基本', '主要', '重要', '关键', '核心', '基础', '简单',
        '复杂', '困难', '容易', '方便', '麻烦', '问题', '方法', '方式',
        '时候', '开始', '结束', '过程', '结果', '效果', '作用', '功能',
        '特点', '优点', '缺点', '好处', '坏处', '影响', '变化', '提高',
        '增加', '减少', '保持', '维持', '继续', '停止', '开始', '结束'
    }
    
    return stop_words


def extract_keywords_from_titles(titles, stop_words, top_n=30):
    """从标题中提取关键词"""
    print(f"📊 开始分析 {len(titles)} 个标题...")
    
    # 合并所有标题
    all_text = ' '.join(titles)
    
    # 使用 jieba 分词
    words = jieba.cut(all_text)
    
    # 过滤停用词和单字符
    filtered_words = [
        word.strip() for word in words 
        if len(word.strip()) > 1 and word.strip() not in stop_words
    ]
    
    # 统计词频
    word_counter = Counter(filtered_words)
    
    # 获取前 N 个关键词
    top_keywords = word_counter.most_common(top_n)
    
    print(f"✅ 提取到 {len(top_keywords)} 个关键词")
    
    return top_keywords, word_counter


def save_keywords_csv(keywords, output_path):
    """保存关键词分析结果到 CSV"""
    df = pd.DataFrame(keywords, columns=['关键词', '出现次数'])
    df['排名'] = range(1, len(df) + 1)
    df = df[['排名', '关键词', '出现次数']]
    
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"📄 关键词分析结果已保存到: {output_path}")
    
    return df


def generate_wordcloud(word_counter, output_path, max_words=100):
    """生成词云图"""
    print("🎨 生成词云图...")
    
    # 设置中文字体
    font_path = None
    possible_fonts = [
        'C:/Windows/Fonts/simhei.ttf',  # Windows 黑体
        'C:/Windows/Fonts/msyh.ttf',    # Windows 微软雅黑
        '/System/Library/Fonts/PingFang.ttc',  # macOS
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'  # Linux
    ]
    
    for font in possible_fonts:
        if os.path.exists(font):
            font_path = font
            break
    
    # 创建词云
    wordcloud = WordCloud(
        width=1200,
        height=800,
        background_color='white',
        font_path=font_path,
        max_words=max_words,
        colormap='viridis',
        relative_scaling=0.5,
        random_state=42
    ).generate_from_frequencies(word_counter)
    
    # 保存词云图
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('小红书笔记标题关键词词云图', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"🎨 词云图已保存到: {output_path}")


def analyze_keyword_trends(df, keywords_df, output_dir):
    """分析关键词趋势"""
    print("📈 分析关键词趋势...")
    
    # 转换时间戳
    df['publish_date'] = pd.to_datetime(df['time'], unit='ms')
    df['month'] = df['publish_date'].dt.to_period('M')
    
    # 获取前10个关键词
    top_10_keywords = keywords_df.head(10)['关键词'].tolist()
    
    # 分析每个月的关键词出现情况
    monthly_trends = []
    
    for month in df['month'].unique():
        month_data = df[df['month'] == month]
        month_titles = ' '.join(month_data['title'].fillna(''))
        
        month_row = {'月份': str(month)}
        for keyword in top_10_keywords:
            count = month_titles.count(keyword)
            month_row[keyword] = count
        
        monthly_trends.append(month_row)
    
    trends_df = pd.DataFrame(monthly_trends)
    trends_output = os.path.join(output_dir, 'keyword_trends.csv')
    trends_df.to_csv(trends_output, index=False, encoding='utf-8-sig')
    
    print(f"📈 关键词趋势分析已保存到: {trends_output}")
    
    return trends_df


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='小红书笔记关键词分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python analysis/keyword_analysis.py --input core/media_crawler/data/xhs/1_search_contents_2025-07-02.csv
  python analysis/keyword_analysis.py --input data.csv --top-n 50 --max-words 150
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
        default=30,
        help='提取前 N 个关键词 (默认: 30)'
    )
    parser.add_argument(
        '--max-words',
        type=int,
        default=100,
        help='词云图最大词数 (默认: 100)'
    )
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"❌ 输入文件不存在: {args.input}")
        sys.exit(1)
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 60)
    print("🔍 小红书笔记关键词分析")
    print("=" * 60)
    
    try:
        # 读取数据
        print(f"📖 读取数据文件: {args.input}")
        df = pd.read_csv(args.input)
        
        if 'title' not in df.columns:
            print("❌ CSV 文件中没有找到 'title' 列")
            sys.exit(1)
        
        # 清理标题数据
        titles = df['title'].fillna('').astype(str).tolist()
        titles = [title.strip() for title in titles if title.strip()]
        
        if not titles:
            print("❌ 没有找到有效的标题数据")
            sys.exit(1)
        
        # 设置 jieba
        stop_words = setup_jieba()
        
        # 提取关键词
        top_keywords, word_counter = extract_keywords_from_titles(
            titles, stop_words, args.top_n
        )
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存关键词 CSV
        keywords_output = os.path.join(
            args.output_dir, f'keywords_analysis_{timestamp}.csv'
        )
        keywords_df = save_keywords_csv(top_keywords, keywords_output)
        
        # 生成词云图
        wordcloud_output = os.path.join(
            args.output_dir, f'wordcloud_{timestamp}.png'
        )
        generate_wordcloud(word_counter, wordcloud_output, args.max_words)
        
        # 分析关键词趋势
        if 'time' in df.columns:
            analyze_keyword_trends(df, keywords_df, args.output_dir)
        
        # 输出统计信息
        print("\n" + "=" * 60)
        print("📊 分析结果统计")
        print("=" * 60)
        print(f"📝 分析笔记数量: {len(titles)}")
        print(f"🔤 提取关键词数量: {len(top_keywords)}")
        print(f"📄 关键词 CSV: {keywords_output}")
        print(f"🎨 词云图: {wordcloud_output}")
        
        print("\n🏆 前10个热门关键词:")
        for i, (word, count) in enumerate(top_keywords[:10], 1):
            print(f"  {i:2d}. {word} ({count}次)")
        
        print("\n✅ 关键词分析完成!")
        
    except Exception as e:
        print(f"❌ 分析过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
