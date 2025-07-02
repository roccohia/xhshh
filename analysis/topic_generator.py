#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容选题辅助模块
分析高互动标题，使用 AI 生成选题建议和标题模板
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np
from datetime import datetime
import json
import re
from collections import Counter
import openai
from typing import List, Dict, Any


def setup_openai_client(api_key=None, base_url=None):
    """设置 OpenAI 客户端"""
    if api_key:
        openai.api_key = api_key
    else:
        # 尝试从环境变量获取
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️  未设置 OpenAI API Key")
            print("请设置环境变量 OPENAI_API_KEY 或使用 --api-key 参数")
            return None
        openai.api_key = api_key
    
    if base_url:
        openai.api_base = base_url
    
    return openai


def analyze_title_patterns(titles):
    """分析标题模式"""
    print("🔍 分析标题模式...")
    
    patterns = {
        '数字型': [],
        '疑问型': [],
        '感叹型': [],
        '对比型': [],
        '体验型': [],
        '教程型': [],
        '种草型': [],
        '时间型': []
    }
    
    # 定义模式识别规则
    pattern_rules = {
        '数字型': [r'\d+', r'[一二三四五六七八九十]+', r'第\d+', r'\d+个', r'\d+种', r'\d+天'],
        '疑问型': [r'[？?]', r'什么', r'怎么', r'如何', r'为什么', r'哪个', r'哪里'],
        '感叹型': [r'[！!]', r'太', r'超', r'绝了', r'爱了', r'哇', r'天啊'],
        '对比型': [r'vs', r'对比', r'区别', r'哪个好', r'还是', r'or'],
        '体验型': [r'体验', r'试用', r'测评', r'亲测', r'真实', r'感受', r'心得'],
        '教程型': [r'教程', r'教学', r'入门', r'新手', r'零基础', r'学会', r'掌握'],
        '种草型': [r'推荐', r'安利', r'种草', r'必买', r'好用', r'值得', r'不踩雷'],
        '时间型': [r'\d+天', r'\d+周', r'\d+月', r'每天', r'坚持', r'第\d+天']
    }
    
    for title in titles:
        title_lower = title.lower()
        for pattern_type, rules in pattern_rules.items():
            for rule in rules:
                if re.search(rule, title_lower):
                    patterns[pattern_type].append(title)
                    break
    
    # 统计各类型数量
    pattern_stats = {k: len(v) for k, v in patterns.items()}
    
    return patterns, pattern_stats


def extract_high_engagement_titles(df, top_n=50):
    """提取高互动标题"""
    print(f"📊 提取前 {top_n} 个高互动标题...")
    
    # 计算总互动数
    numeric_columns = ['liked_count', 'collected_count', 'comment_count', 'share_count']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    df['total_engagement'] = (
        df.get('liked_count', 0) + 
        df.get('collected_count', 0) + 
        df.get('comment_count', 0) + 
        df.get('share_count', 0)
    )
    
    # 按总互动数排序
    high_engagement_df = df.nlargest(top_n, 'total_engagement')
    
    titles = high_engagement_df['title'].fillna('').astype(str).tolist()
    titles = [title.strip() for title in titles if title.strip()]
    
    return titles, high_engagement_df


def generate_ai_analysis(titles, client, model="gpt-3.5-turbo"):
    """使用 AI 分析标题并生成建议"""
    print("🤖 使用 AI 分析标题模式...")
    
    if not client:
        print("⚠️  OpenAI 客户端未配置，跳过 AI 分析")
        return None
    
    # 准备提示词
    titles_text = '\n'.join(titles[:30])  # 限制标题数量避免超出 token 限制
    
    prompt = f"""
请分析以下小红书高互动标题，并提供内容选题建议：

标题列表：
{titles_text}

请从以下几个维度进行分析：

1. 标题结构模板分析
   - 识别常见的标题结构模式
   - 总结高互动标题的共同特征

2. 内容类型分类
   - 体验分享类
   - 教程指导类
   - 种草推荐类
   - 对比测评类
   - 知识科普类
   - 其他类型

3. 选题方向建议
   - 基于分析结果，提供5-10个具体的选题方向
   - 每个选题包含标题模板和内容要点

4. 标题优化建议
   - 提供标题写作的具体技巧
   - 推荐使用的关键词和表达方式

请以 JSON 格式返回分析结果，包含以上四个部分的详细内容。
"""
    
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个专业的内容营销分析师，擅长分析社交媒体内容趋势和用户行为。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        ai_analysis = response.choices[0].message.content
        
        # 尝试解析 JSON
        try:
            ai_result = json.loads(ai_analysis)
        except json.JSONDecodeError:
            # 如果不是有效的 JSON，返回原始文本
            ai_result = {"raw_analysis": ai_analysis}
        
        print("✅ AI 分析完成")
        return ai_result
        
    except Exception as e:
        print(f"❌ AI 分析失败: {e}")
        return None


def generate_topic_suggestions(patterns, pattern_stats, ai_analysis=None):
    """生成选题建议"""
    print("💡 生成选题建议...")
    
    suggestions = []
    
    # 基于模式分析的建议
    for pattern_type, count in sorted(pattern_stats.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            if pattern_type == '数字型':
                suggestions.append({
                    'type': '数字型内容',
                    'template': 'X个/X种/X天 + 核心内容 + 效果描述',
                    'examples': ['5个普拉提动作让你告别小肚腩', '30天普拉提挑战，我的身材变化'],
                    'tips': '使用具体数字增加可信度，数字建议在3-10之间',
                    'engagement_potential': '高',
                    'count': count
                })
            
            elif pattern_type == '体验型':
                suggestions.append({
                    'type': '体验分享类',
                    'template': '亲测/体验 + 产品/方法 + 真实感受',
                    'examples': ['亲测这家普拉提馆，效果超出预期', '30天普拉提体验，我的真实感受'],
                    'tips': '强调真实性和个人体验，增加可信度',
                    'engagement_potential': '高',
                    'count': count
                })
            
            elif pattern_type == '疑问型':
                suggestions.append({
                    'type': '疑问引导类',
                    'template': '疑问词 + 核心问题 + 解答预期',
                    'examples': ['普拉提真的能减肥吗？我来告诉你', '为什么明星都在练普拉提？'],
                    'tips': '提出用户关心的问题，激发好奇心',
                    'engagement_potential': '中高',
                    'count': count
                })
            
            elif pattern_type == '对比型':
                suggestions.append({
                    'type': '对比测评类',
                    'template': 'A vs B + 对比维度 + 结论建议',
                    'examples': ['普拉提 vs 瑜伽，哪个更适合减肥？', '器械普拉提 vs 垫上普拉提对比'],
                    'tips': '选择用户关心的对比点，给出明确建议',
                    'engagement_potential': '高',
                    'count': count
                })
    
    # 如果有 AI 分析结果，整合建议
    if ai_analysis and isinstance(ai_analysis, dict):
        if 'topic_suggestions' in ai_analysis:
            ai_suggestions = ai_analysis['topic_suggestions']
            if isinstance(ai_suggestions, list):
                for suggestion in ai_suggestions:
                    suggestions.append({
                        'type': 'AI推荐',
                        'template': suggestion.get('template', ''),
                        'examples': suggestion.get('examples', []),
                        'tips': suggestion.get('tips', ''),
                        'engagement_potential': 'AI预测',
                        'count': 0
                    })
    
    return suggestions


def create_content_calendar(suggestions, days=30):
    """创建内容日历"""
    print(f"📅 创建 {days} 天内容日历...")
    
    calendar = []
    
    # 内容类型权重（基于互动潜力）
    type_weights = {
        '数字型内容': 0.25,
        '体验分享类': 0.25,
        '对比测评类': 0.20,
        '疑问引导类': 0.15,
        '教程指导类': 0.10,
        'AI推荐': 0.05
    }
    
    # 生成内容日历
    for day in range(1, days + 1):
        # 根据权重选择内容类型
        available_types = [s for s in suggestions if s['count'] > 0 or s['type'] == 'AI推荐']
        
        if available_types:
            # 简单的轮换策略
            suggestion = available_types[(day - 1) % len(available_types)]
            
            calendar_item = {
                'day': day,
                'date': (datetime.now() + pd.Timedelta(days=day-1)).strftime('%Y-%m-%d'),
                'content_type': suggestion['type'],
                'template': suggestion['template'],
                'example': suggestion['examples'][0] if suggestion['examples'] else '',
                'tips': suggestion['tips'],
                'engagement_potential': suggestion['engagement_potential']
            }
            
            calendar.append(calendar_item)
    
    return calendar


def save_analysis_results(patterns, pattern_stats, suggestions, calendar, ai_analysis, output_dir):
    """保存分析结果"""
    print("💾 保存分析结果...")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 1. 保存标题模式分析
    pattern_output = os.path.join(output_dir, f'title_patterns_{timestamp}.json')
    pattern_data = {
        'pattern_stats': pattern_stats,
        'pattern_examples': {k: v[:5] for k, v in patterns.items()},  # 只保存前5个例子
        'analysis_time': datetime.now().isoformat()
    }

    with open(pattern_output, 'w', encoding='utf-8') as f:
        json.dump(pattern_data, f, ensure_ascii=False, indent=2)

    print(f"📄 标题模式分析已保存到: {pattern_output}")

    # 2. 保存选题建议
    suggestions_output = os.path.join(output_dir, f'topic_suggestions_{timestamp}.csv')
    suggestions_df = pd.DataFrame(suggestions)
    suggestions_df.to_csv(suggestions_output, index=False, encoding='utf-8-sig')

    print(f"📄 选题建议已保存到: {suggestions_output}")

    # 3. 保存内容日历
    calendar_output = os.path.join(output_dir, f'content_calendar_{timestamp}.csv')
    calendar_df = pd.DataFrame(calendar)
    calendar_df.to_csv(calendar_output, index=False, encoding='utf-8-sig')

    print(f"📄 内容日历已保存到: {calendar_output}")

    # 4. 保存 AI 分析结果
    if ai_analysis:
        ai_output = os.path.join(output_dir, f'ai_analysis_{timestamp}.json')
        with open(ai_output, 'w', encoding='utf-8') as f:
            json.dump(ai_analysis, f, ensure_ascii=False, indent=2)

        print(f"📄 AI 分析结果已保存到: {ai_output}")

    return {
        'patterns': pattern_output,
        'suggestions': suggestions_output,
        'calendar': calendar_output,
        'ai_analysis': ai_output if ai_analysis else None
    }


def generate_comprehensive_report(pattern_stats, suggestions, calendar, ai_analysis, output_dir):
    """生成综合报告"""
    print("📋 生成综合分析报告...")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f'topic_analysis_report_{timestamp}.txt')

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("小红书内容选题分析报告\n")
        f.write("=" * 60 + "\n\n")

        f.write("📊 标题模式分析\n")
        f.write("-" * 30 + "\n")
        total_titles = sum(pattern_stats.values())
        for pattern_type, count in sorted(pattern_stats.items(), key=lambda x: x[1], reverse=True):
            percentage = count / total_titles * 100 if total_titles > 0 else 0
            f.write(f"{pattern_type}: {count}个 ({percentage:.1f}%)\n")

        f.write(f"\n💡 选题建议 ({len(suggestions)}个)\n")
        f.write("-" * 30 + "\n")
        for i, suggestion in enumerate(suggestions, 1):
            f.write(f"{i}. {suggestion['type']}\n")
            f.write(f"   模板: {suggestion['template']}\n")
            f.write(f"   示例: {suggestion['examples'][0] if suggestion['examples'] else 'N/A'}\n")
            f.write(f"   建议: {suggestion['tips']}\n")
            f.write(f"   互动潜力: {suggestion['engagement_potential']}\n\n")

        f.write(f"📅 内容日历 (未来{len(calendar)}天)\n")
        f.write("-" * 30 + "\n")
        for item in calendar[:10]:  # 只显示前10天
            f.write(f"第{item['day']}天 ({item['date']}): {item['content_type']}\n")
            f.write(f"   {item['example']}\n\n")

        if ai_analysis:
            f.write("🤖 AI 分析摘要\n")
            f.write("-" * 30 + "\n")
            if isinstance(ai_analysis, dict):
                if 'summary' in ai_analysis:
                    f.write(f"{ai_analysis['summary']}\n")
                else:
                    f.write("AI 分析结果已保存到单独的 JSON 文件中\n")
            else:
                f.write("AI 分析结果格式异常\n")

        f.write(f"\n\n报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"📋 综合分析报告已保存到: {report_path}")

    return report_path


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='小红书内容选题辅助工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python analysis/topic_generator.py --input core/media_crawler/data/xhs/1_search_contents_2025-07-02.csv
  python analysis/topic_generator.py --input data.csv --top-n 100 --api-key your_openai_key
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
        default=50,
        help='分析前 N 个高互动标题 (默认: 50)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='OpenAI API Key (可选，用于 AI 分析)'
    )
    parser.add_argument(
        '--base-url',
        type=str,
        help='OpenAI API Base URL (可选，用于自定义 API 端点)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='gpt-3.5-turbo',
        help='OpenAI 模型名称 (默认: gpt-3.5-turbo)'
    )
    parser.add_argument(
        '--calendar-days',
        type=int,
        default=30,
        help='生成内容日历的天数 (默认: 30)'
    )

    args = parser.parse_args()

    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"❌ 输入文件不存在: {args.input}")
        sys.exit(1)

    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 60)
    print("💡 小红书内容选题辅助分析")
    print("=" * 60)

    try:
        # 读取数据
        print(f"📖 读取数据文件: {args.input}")
        df = pd.read_csv(args.input)

        print(f"📊 数据概览: {len(df)} 条笔记")

        # 提取高互动标题
        high_engagement_titles, high_engagement_df = extract_high_engagement_titles(df, args.top_n)

        if not high_engagement_titles:
            print("❌ 没有找到有效的标题数据")
            sys.exit(1)

        print(f"✅ 提取到 {len(high_engagement_titles)} 个高互动标题")

        # 分析标题模式
        patterns, pattern_stats = analyze_title_patterns(high_engagement_titles)

        # 设置 OpenAI 客户端
        openai_client = None
        ai_analysis = None

        if args.api_key or os.getenv('OPENAI_API_KEY'):
            openai_client = setup_openai_client(args.api_key, args.base_url)
            if openai_client:
                ai_analysis = generate_ai_analysis(high_engagement_titles, openai_client, args.model)

        # 生成选题建议
        suggestions = generate_topic_suggestions(patterns, pattern_stats, ai_analysis)

        # 创建内容日历
        calendar = create_content_calendar(suggestions, args.calendar_days)

        # 保存分析结果
        output_files = save_analysis_results(
            patterns, pattern_stats, suggestions, calendar, ai_analysis, args.output_dir
        )

        # 生成综合报告
        report_path = generate_comprehensive_report(
            pattern_stats, suggestions, calendar, ai_analysis, args.output_dir
        )

        # 输出统计信息
        print("\n" + "=" * 60)
        print("📊 分析结果统计")
        print("=" * 60)
        print(f"📝 分析标题数量: {len(high_engagement_titles)}")
        print(f"📋 标题模式类型: {len([k for k, v in pattern_stats.items() if v > 0])}")
        print(f"💡 生成选题建议: {len(suggestions)}")
        print(f"📅 内容日历天数: {len(calendar)}")

        print("\n🏆 热门标题模式:")
        for pattern_type, count in sorted(pattern_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
            if count > 0:
                percentage = count / len(high_engagement_titles) * 100
                print(f"  {pattern_type}: {count}个 ({percentage:.1f}%)")

        print("\n💡 推荐选题类型:")
        for i, suggestion in enumerate(suggestions[:5], 1):
            print(f"  {i}. {suggestion['type']} (互动潜力: {suggestion['engagement_potential']})")

        print(f"\n📄 详细结果已保存到:")
        for key, path in output_files.items():
            if path:
                print(f"  {key}: {path}")
        print(f"  综合报告: {report_path}")

        print("\n✅ 选题分析完成!")

    except Exception as e:
        print(f"❌ 分析过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
