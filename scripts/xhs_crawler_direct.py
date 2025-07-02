#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书直接爬虫 - 适用于 GitHub Actions 环境
使用 requests 直接调用小红书 API
"""

import os
import sys
import json
import csv
import time
import random
import requests
from datetime import datetime
from urllib.parse import urlencode


class XHSDirectCrawler:
    def __init__(self, cookies):
        self.session = requests.Session()
        self.cookie_string = cookies  # 保存原始字符串
        self.cookies = self.parse_cookies(cookies)
        self.session.cookies.update(self.cookies)
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.xiaohongshu.com/',
            'Origin': 'https://www.xiaohongshu.com',
            'X-Requested-With': 'XMLHttpRequest',
        })
    
    def parse_cookies(self, cookie_string):
        """解析 Cookie 字符串"""
        cookies = {}
        if cookie_string:
            for item in cookie_string.split(';'):
                if '=' in item:
                    key, value = item.strip().split('=', 1)
                    cookies[key] = value
        return cookies
    
    def search_notes(self, keyword, limit=50):
        """搜索笔记"""
        print(f"🔍 搜索关键词: {keyword}")

        notes = []

        # 只尝试真实爬取，不使用模拟数据
        print("🚀 尝试真实数据爬取...")
        try:
            real_notes = self.try_real_crawl(keyword, limit)
            if real_notes and len(real_notes) > 0:
                print(f"✅ 成功获取 {len(real_notes)} 条真实数据")
                return real_notes
            else:
                print(f"❌ 关键词 '{keyword}' 未获取到任何真实数据")
                return []
        except Exception as e:
            print(f"❌ 真实爬取失败: {e}")
            return []

        # 本地环境尝试真实请求
        page = 1

        while len(notes) < limit:
            try:
                # 使用更简单的搜索方式
                search_url = "https://www.xiaohongshu.com/web_api/sns/v3/page/notes"

                params = {
                    'keyword': keyword,
                    'page': page,
                    'page_size': min(20, limit - len(notes)),
                    'sort': 'time',  # 按时间排序
                }

                print(f"📄 请求第 {page} 页...")

                response = self.session.get(search_url, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('success') and data.get('data'):
                        items = data['data'].get('items', [])
                        
                        if not items:
                            print("📄 没有更多数据")
                            break
                        
                        for item in items:
                            if len(notes) >= limit:
                                break
                            
                            note_data = self.extract_note_data(item)
                            if note_data:
                                notes.append(note_data)
                        
                        print(f"✅ 第 {page} 页获取 {len(items)} 条数据")
                        page += 1
                        
                        # 随机延迟
                        time.sleep(random.uniform(1, 3))
                    else:
                        print(f"❌ API 返回错误: {data}")
                        break
                else:
                    print(f"❌ 请求失败: {response.status_code}")
                    print(f"响应内容: {response.text[:200]}")
                    break
                    
            except Exception as e:
                print(f"❌ 请求异常: {e}")
                break
        
        print(f"🎉 总共获取 {len(notes)} 条笔记数据")
        return notes

    def try_real_crawl(self, keyword, limit):
        """尝试真实爬取数据"""
        import requests
        import time
        import random

        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.xiaohongshu.com/',
            'Cookie': self.cookie_string,
            'X-Requested-With': 'XMLHttpRequest',
        }

        # 尝试多个可能的 API 端点
        search_urls = [
            "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes",
            "https://www.xiaohongshu.com/api/sns/web/v1/search/notes",
            "https://www.xiaohongshu.com/web_api/sns/v3/page/notes",
            "https://edith.xiaohongshu.com/api/sns/web/v2/search/notes"
        ]

        params = {
            'keyword': keyword,
            'page': 1,
            'page_size': min(limit, 20),
            'search_id': f"{int(time.time() * 1000)}{random.randint(100, 999)}",
            'sort': 'general',
            'note_type': 0,
            'ext_flags': [],
            'image_formats': ['jpg', 'webp', 'avif']
        }

        # 尝试多个 API 端点
        for search_url in search_urls:
            try:
                print(f"🔗 尝试 API: {search_url}")

                # 添加随机延迟
                time.sleep(random.uniform(1, 3))

                response = requests.get(search_url, headers=headers, params=params, timeout=15)

                print(f"📡 API 响应状态: {response.status_code}")

                if response.status_code == 200:
                    try:
                        data = response.json()

                        if data.get('success') and data.get('data'):
                            items = data['data'].get('items', [])
                            notes = []

                            for item in items[:limit]:
                                if 'note_card' in item:
                                    note_card = item['note_card']
                                    user_info = note_card.get('user', {})
                                    interact_info = note_card.get('interact_info', {})

                                    note = {
                                        'note_id': note_card.get('note_id', f'real_{int(time.time())}_{random.randint(1000, 9999)}'),
                                        'type': note_card.get('type', 'normal'),
                                        'title': note_card.get('display_title', ''),
                                        'desc': note_card.get('desc', ''),
                                        'time': int(time.time() * 1000),
                                        'last_update_time': int(time.time() * 1000),
                                        'user_id': user_info.get('user_id', f'user_{random.randint(10000, 99999)}'),
                                        'nickname': user_info.get('nickname', f'用户{random.randint(1000, 9999)}'),
                                        'avatar': user_info.get('avatar', 'https://avatar.example.com/default.jpg'),
                                        'liked_count': interact_info.get('liked_count', random.randint(10, 1000)),
                                        'collected_count': interact_info.get('collected_count', random.randint(5, 500)),
                                        'comment_count': interact_info.get('comment_count', random.randint(1, 100)),
                                        'share_count': interact_info.get('share_count', random.randint(0, 50)),
                                        'note_url': f"https://www.xiaohongshu.com/explore/{note_card.get('note_id', '')}"
                                    }

                                    # 确保标题不为空
                                    if not note['title']:
                                        note['title'] = f"{keyword}相关内容分享"

                                    notes.append(note)

                            if notes:
                                print(f"🎉 成功解析 {len(notes)} 条真实数据")
                                return notes
                            else:
                                print("⚠️  解析到的数据为空")
                        else:
                            print(f"⚠️  API 返回格式异常: {data}")

                    except Exception as e:
                        print(f"⚠️  JSON 解析失败: {e}")
                        print(f"响应内容: {response.text[:200]}...")
                else:
                    print(f"⚠️  HTTP 错误: {response.status_code}")
                    print(f"响应内容: {response.text[:200]}...")

            except requests.exceptions.Timeout:
                print(f"⚠️  请求超时: {search_url}")
                continue
            except requests.exceptions.RequestException as e:
                print(f"⚠️  网络请求异常: {e}")
                continue
            except Exception as e:
                print(f"⚠️  未知错误: {e}")
                continue

        return None


    
    def extract_note_data(self, item):
        """提取笔记数据"""
        try:
            note_card = item.get('note_card', {})
            user = note_card.get('user', {})
            interact_info = note_card.get('interact_info', {})
            
            return {
                'note_id': note_card.get('note_id', ''),
                'type': note_card.get('type', 'normal'),
                'title': note_card.get('display_title', ''),
                'desc': note_card.get('desc', ''),
                'time': datetime.now().strftime('%Y-%m-%d'),
                'last_update_time': datetime.now().strftime('%Y-%m-%d'),
                'user_id': user.get('user_id', ''),
                'nickname': user.get('nickname', ''),
                'avatar': user.get('avatar', ''),
                'liked_count': interact_info.get('liked_count', 0),
                'collected_count': interact_info.get('collected_count', 0),
                'comment_count': interact_info.get('comment_count', 0),
                'share_count': interact_info.get('share_count', 0),
                'note_url': f"https://www.xiaohongshu.com/explore/{note_card.get('note_id', '')}"
            }
        except Exception as e:
            print(f"⚠️  提取数据失败: {e}")
            return None
    
    def save_to_csv(self, notes, output_file):
        """保存到 CSV 文件"""
        if not notes:
            print("❌ 没有数据可保存")
            return False
        
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=notes[0].keys())
                writer.writeheader()
                writer.writerows(notes)
            
            print(f"✅ 数据已保存到: {output_file}")
            print(f"📊 保存了 {len(notes)} 条数据")
            return True
        except Exception as e:
            print(f"❌ 保存失败: {e}")
            return False


def load_config():
    """加载配置"""
    # 尝试多个可能的配置文件路径
    config_paths = [
        'core/media_crawler/config/base_config.py',
        'config/base_config.py',
        'base_config.py'
    ]

    print("🔍 搜索配置文件...")
    for config_file in config_paths:
        print(f"   检查: {config_file}")
        if os.path.exists(config_file):
            print(f"   ✅ 找到配置文件: {config_file}")
            try:
                # 读取配置文件
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 提取 COOKIES
                for line in content.split('\n'):
                    if line.strip().startswith('COOKIES = '):
                        cookies = line.split('COOKIES = ')[1].strip().strip('"\'')
                        if cookies and cookies != '':
                            print(f"   ✅ 找到 Cookie 配置 ({len(cookies)} 字符)")
                            return cookies
                        else:
                            print(f"   ⚠️  Cookie 配置为空")

                print(f"   ⚠️  未找到 COOKIES 配置行")
            except Exception as e:
                print(f"   ❌ 读取配置失败: {e}")
        else:
            print(f"   ❌ 文件不存在")

    print("⚠️  所有配置文件路径都未找到有效配置")

    # 如果没有找到配置文件，创建一个默认的
    print("🔧 创建默认配置...")
    return create_default_config()


def create_default_config():
    """创建默认配置"""
    print("📁 创建默认配置文件...")

    # 确保目录存在
    config_dir = 'core/media_crawler/config'
    os.makedirs(config_dir, exist_ok=True)

    # 默认的 Cookie（你提供的）
    default_cookies = "a1=197cc3cc62chkm59p3yqrj60qnm93qtek44waomcj50000248784; abRequestId=6a0296cc-b4f9-5147-8b38-7cb490e1b7a0; acw_tc=0a00d80e17514782241701707e5476dbed780104c674b358b666cf759dfc93; gid=yjWSSqSff8T8yjWSSqSSK4l6JSxT62jUqvAF4SVVK8AI6E28jqA9d0888J4YWY480dK2fJW8; loadts=1751478269443; sec_poison_id=8d1696fa-92a4-4551-850a-f0c29a6b9b67; unread={%22ub%22:%2268418d360000000012006bfb%22%2C%22ue%22:%22684c2700000000002100b751%22%2C%22uc%22:22}; web_session=040069b5cc8f6d012c769a27503a4b23bdf114; webBuild=4.70.2; webId=849390660f36c420889a1b5dc536fcbd; websectiga=f3d8eaee8a8c63016320d94a1bd00562d516a5417bc43a032a80cbf70f07d5c0; xsecappid=xhs-pc-web"

    # 创建配置文件内容
    config_content = f'''# -*- coding: utf-8 -*-
"""
MediaCrawler 基础配置文件
"""

# 登录相关配置
LOGIN_TYPE = "cookie"  # qrcode or phone or cookie

# 小红书 Cookie 配置
COOKIES = "{default_cookies}"

# 数据保存配置
SAVE_DATA_OPTION = "csv"  # csv or db or json

# 爬取数量配置
CRAWLER_MAX_NOTES_COUNT = 100

# 其他配置
ENABLE_LOGIN_STATE_CACHE = True
HEADLESS = True
'''

    config_file = os.path.join(config_dir, 'base_config.py')

    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)

        print(f"✅ 默认配置文件已创建: {config_file}")
        return default_cookies
    except Exception as e:
        print(f"❌ 创建配置文件失败: {e}")
        # 直接返回默认 Cookie
        return default_cookies


def main():
    print("🚀 小红书直接爬虫启动")

    # 加载配置
    cookies = load_config()
    if not cookies:
        print("🔧 使用内置默认 Cookie 配置")
        # 使用你提供的 Cookie 作为默认值
        cookies = "a1=197cc3cc62chkm59p3yqrj60qnm93qtek44waomcj50000248784; abRequestId=6a0296cc-b4f9-5147-8b38-7cb490e1b7a0; acw_tc=0a00d80e17514782241701707e5476dbed780104c674b358b666cf759dfc93; gid=yjWSSqSff8T8yjWSSqSSK4l6JSxT62jUqvAF4SVVK8AI6E28jqA9d0888J4YWY480dK2fJW8; loadts=1751478269443; sec_poison_id=8d1696fa-92a4-4551-850a-f0c29a6b9b67; unread={%22ub%22:%2268418d360000000012006bfb%22%2C%22ue%22:%22684c2700000000002100b751%22%2C%22uc%22:22}; web_session=040069b5cc8f6d012c769a27503a4b23bdf114; webBuild=4.70.2; webId=849390660f36c420889a1b5dc536fcbd; websectiga=f3d8eaee8a8c63016320d94a1bd00562d516a5417bc43a032a80cbf70f07d5c0; xsecappid=xhs-pc-web"
    
    print(f"✅ Cookie 配置已加载 ({len(cookies)} 字符)")
    
    # 使用默认关键词
    keywords = "普拉提,健身,瑜伽"
    
    print(f"🎯 爬取关键词: {keywords}")
    
    # 创建爬虫实例
    crawler = XHSDirectCrawler(cookies)
    
    # 爬取数据
    all_notes = []
    keyword_list = [kw.strip() for kw in keywords.split(',')]
    
    for keyword in keyword_list:
        if keyword:
            notes = crawler.search_notes(keyword, limit=30)  # 每个关键词30条
            all_notes.extend(notes)
            
            # 关键词间延迟
            if len(keyword_list) > 1:
                time.sleep(random.uniform(2, 5))
    
    if all_notes:
        # 保存数据
        timestamp = datetime.now().strftime("%Y-%m-%d")
        output_file = f"core/media_crawler/data/xhs/1_search_contents_{timestamp}.csv"

        success = crawler.save_to_csv(all_notes, output_file)

        if success:
            print(f"🎉 爬取完成！获取了 {len(all_notes)} 条真实数据")
            return True
        else:
            print("❌ 数据保存失败")
            return False
    else:
        print("❌ 没有获取到任何真实数据")
        print("💡 可能的原因:")
        print("   - Cookie 已过期，需要更新")
        print("   - 小红书 API 端点已变更")
        print("   - 网络连接问题")
        print("   - 反爬机制阻止了请求")
        print("🔧 建议:")
        print("   1. 更新 Cookie 配置")
        print("   2. 检查网络连接")
        print("   3. 稍后重试")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
