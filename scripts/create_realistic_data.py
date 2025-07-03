#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建高质量的真实格式数据用于测试分析功能
基于真实小红书数据格式和内容特征
"""

import os
import csv
import random
import time
from datetime import datetime, timedelta

def create_realistic_xhs_data():
    """创建真实的小红书数据"""
    
    # 真实的小红书笔记标题和内容
    realistic_notes = [
        {
            "title": "普拉提新手入门｜30天改变体态的秘密",
            "desc": "分享我30天普拉提练习的真实体验，从驼背到挺拔，从松垮到紧致！附详细动作教程",
            "keywords": ["普拉提", "体态", "新手", "教程"],
            "user_type": "fitness_blogger",
            "engagement_level": "high"
        },
        {
            "title": "健身房普拉提课程体验｜值得报名吗？",
            "desc": "试了3家健身房的普拉提课程，来给大家测评一下哪家最值得！价格、教练、环境全方位对比",
            "keywords": ["健身房", "普拉提", "课程", "测评"],
            "user_type": "reviewer",
            "engagement_level": "medium"
        },
        {
            "title": "瑜伽vs普拉提｜选择困难症看这里",
            "desc": "练了5年瑜伽又转普拉提的我，来告诉你两者的区别和如何选择适合自己的运动方式",
            "keywords": ["瑜伽", "普拉提", "对比", "选择"],
            "user_type": "experienced_user",
            "engagement_level": "high"
        },
        {
            "title": "居家健身装备推荐｜小空间大效果",
            "desc": "租房党的健身装备清单！不到500块打造完美居家健身角落，瑜伽垫、弹力带、泡沫轴...",
            "keywords": ["居家健身", "装备", "推荐", "租房"],
            "user_type": "lifestyle_blogger",
            "engagement_level": "medium"
        },
        {
            "title": "瑜伽冥想入门｜找回内心平静的方法",
            "desc": "焦虑症患者的自救指南，通过瑜伽冥想重新找回生活的平衡，分享我的练习心得和方法",
            "keywords": ["瑜伽", "冥想", "焦虑", "心理健康"],
            "user_type": "wellness_advocate",
            "engagement_level": "high"
        },
        {
            "title": "普拉提核心训练｜告别小肚腩",
            "desc": "专门针对核心的普拉提动作合集，每天15分钟，坚持一个月腰围减了5cm！动作详解+注意事项",
            "keywords": ["普拉提", "核心训练", "减肚子", "动作"],
            "user_type": "fitness_coach",
            "engagement_level": "high"
        },
        {
            "title": "健身新手避坑指南｜我踩过的那些坑",
            "desc": "健身3年的血泪史，从盲目跟风到科学训练，分享新手最容易犯的错误和正确的开始方式",
            "keywords": ["健身", "新手", "避坑", "经验"],
            "user_type": "fitness_enthusiast",
            "engagement_level": "medium"
        },
        {
            "title": "瑜伽体式详解｜下犬式的正确打开方式",
            "desc": "最基础也最重要的瑜伽体式，90%的人都做错了！详细分解动作要领，避免手腕疼痛",
            "keywords": ["瑜伽", "体式", "下犬式", "教学"],
            "user_type": "yoga_teacher",
            "engagement_level": "high"
        },
        {
            "title": "普拉提垫子怎么选？｜5款热门测评",
            "desc": "从材质到厚度，从防滑到便携，全方位测评5款热门普拉提垫，帮你选出最适合的那一款",
            "keywords": ["普拉提", "垫子", "测评", "选购"],
            "user_type": "product_reviewer",
            "engagement_level": "medium"
        },
        {
            "title": "健身饮食搭配｜增肌减脂这样吃",
            "desc": "健身教练的一日三餐分享，增肌期和减脂期的饮食差异，简单易做的健康餐食谱",
            "keywords": ["健身", "饮食", "增肌", "减脂"],
            "user_type": "fitness_coach",
            "engagement_level": "high"
        },
        {
            "title": "瑜伽服穿搭｜运动也要美美的",
            "desc": "瑜伽服不只是运动装！分享我的瑜伽服穿搭心得，从材质选择到颜色搭配，运动时尚两不误",
            "keywords": ["瑜伽", "穿搭", "瑜伽服", "时尚"],
            "user_type": "fashion_blogger",
            "engagement_level": "medium"
        },
        {
            "title": "普拉提工作室探店｜魔都最美的5家",
            "desc": "上海最值得打卡的普拉提工作室，从环境到服务，从价格到效果，全方位探店报告",
            "keywords": ["普拉提", "工作室", "上海", "探店"],
            "user_type": "lifestyle_blogger",
            "engagement_level": "medium"
        },
        {
            "title": "健身打卡100天｜我的身材变化记录",
            "desc": "从120斤到105斤，从体脂28%到18%，100天健身打卡的真实记录，附前后对比照",
            "keywords": ["健身", "打卡", "减肥", "变化"],
            "user_type": "transformation_story",
            "engagement_level": "high"
        },
        {
            "title": "瑜伽初学者常见问题｜老师不会告诉你的事",
            "desc": "瑜伽老师的私房话，初学者最容易遇到的问题和解决方法，让你的瑜伽之路更顺畅",
            "keywords": ["瑜伽", "初学者", "问题", "技巧"],
            "user_type": "yoga_teacher",
            "engagement_level": "high"
        },
        {
            "title": "普拉提私教课值得上吗？｜性价比分析",
            "desc": "上了50节普拉提私教课的真实感受，从效果到价格，帮你分析私教课的性价比",
            "keywords": ["普拉提", "私教", "性价比", "体验"],
            "user_type": "experienced_user",
            "engagement_level": "medium"
        }
    ]
    
    # 用户类型对应的粉丝数和互动数据
    user_profiles = {
        "fitness_blogger": {"followers": (5000, 15000), "engagement_rate": (0.08, 0.15)},
        "reviewer": {"followers": (2000, 8000), "engagement_rate": (0.05, 0.12)},
        "experienced_user": {"followers": (500, 3000), "engagement_rate": (0.03, 0.08)},
        "lifestyle_blogger": {"followers": (8000, 25000), "engagement_rate": (0.06, 0.12)},
        "wellness_advocate": {"followers": (3000, 10000), "engagement_rate": (0.04, 0.10)},
        "fitness_coach": {"followers": (10000, 30000), "engagement_rate": (0.10, 0.20)},
        "fitness_enthusiast": {"followers": (800, 4000), "engagement_rate": (0.03, 0.07)},
        "yoga_teacher": {"followers": (6000, 18000), "engagement_rate": (0.08, 0.16)},
        "product_reviewer": {"followers": (4000, 12000), "engagement_rate": (0.06, 0.14)},
        "fashion_blogger": {"followers": (15000, 50000), "engagement_rate": (0.05, 0.10)},
        "transformation_story": {"followers": (1000, 5000), "engagement_rate": (0.12, 0.25)}
    }
    
    # 生成数据
    notes_data = []
    base_time = int(time.time() * 1000)
    
    for i, note_template in enumerate(realistic_notes):
        # 基础信息
        note_id = f"real_{int(time.time())}_{i:04d}"
        
        # 用户信息
        user_type = note_template["user_type"]
        profile = user_profiles.get(user_type, user_profiles["experienced_user"])
        
        followers = random.randint(*profile["followers"])
        engagement_rate = random.uniform(*profile["engagement_rate"])
        
        # 根据粉丝数和互动率计算互动数据
        base_views = followers * random.uniform(0.3, 0.8)  # 30-80% 的粉丝会看到
        liked_count = int(base_views * engagement_rate * random.uniform(0.8, 1.2))
        collected_count = int(liked_count * random.uniform(0.3, 0.6))
        comment_count = int(liked_count * random.uniform(0.05, 0.15))
        share_count = int(liked_count * random.uniform(0.02, 0.08))
        
        # 时间信息（最近30天内的随机时间）
        days_ago = random.randint(0, 30)
        note_time = base_time - (days_ago * 24 * 60 * 60 * 1000)
        
        # 用户昵称
        user_nicknames = [
            "普拉提小仙女", "健身达人Lily", "瑜伽老师Emma", "运动博主小王",
            "健身教练Mike", "瑜伽导师Anna", "普拉提爱好者", "健身小白兔",
            "瑜伽生活家", "运动美少女", "健身励志姐", "普拉提教练",
            "瑜伽修行者", "健身变美记", "运动达人"
        ]
        
        note_data = {
            'note_id': note_id,
            'type': 'normal',
            'title': note_template["title"],
            'desc': note_template["desc"],
            'time': note_time,
            'last_update_time': note_time,
            'user_id': f'user_{note_id}',
            'nickname': random.choice(user_nicknames),
            'avatar': f'https://avatar.xiaohongshu.com/{note_id}.jpg',
            'liked_count': liked_count,
            'collected_count': collected_count,
            'comment_count': comment_count,
            'share_count': share_count,
            'note_url': f'https://www.xiaohongshu.com/explore/{note_id}'
        }
        
        notes_data.append(note_data)
    
    return notes_data

def save_realistic_data():
    """保存真实数据到文件"""
    try:
        # 创建数据
        notes = create_realistic_xhs_data()
        
        # 确保目录存在
        data_dir = "core/media_crawler/data/xhs"
        os.makedirs(data_dir, exist_ok=True)
        
        # 保存到文件
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join(data_dir, f"realistic_search_contents_{timestamp}.csv")
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if notes:
                writer = csv.DictWriter(f, fieldnames=notes[0].keys())
                writer.writeheader()
                writer.writerows(notes)
        
        print(f"✅ 已创建 {len(notes)} 条真实格式数据")
        print(f"📁 文件保存至: {filename}")
        
        # 显示数据统计
        total_likes = sum(note['liked_count'] for note in notes)
        total_collects = sum(note['collected_count'] for note in notes)
        total_comments = sum(note['comment_count'] for note in notes)
        
        print(f"📊 数据统计:")
        print(f"   总点赞数: {total_likes:,}")
        print(f"   总收藏数: {total_collects:,}")
        print(f"   总评论数: {total_comments:,}")
        print(f"   平均点赞: {total_likes//len(notes):,}")
        
        return filename
        
    except Exception as e:
        print(f"❌ 创建数据失败: {e}")
        return None

def main():
    """主函数"""
    print("🎨 创建高质量真实格式数据...")
    
    filename = save_realistic_data()
    
    if filename:
        print("🎉 真实数据创建完成！")
        print("💡 现在可以用这些数据测试分析功能了")
        return True
    else:
        print("❌ 数据创建失败")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
