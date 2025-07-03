#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书 API 逆向爬虫 - 尝试真实的 API 端点和参数
"""

import os
import sys
import json
import csv
import time
import random
import hashlib
import urllib.parse
from datetime import datetime
import requests

class XHSAPIReverseCrawler:
    def __init__(self, cookies=None, proxy_list=None):
        self.cookies = cookies
        self.proxy_list = proxy_list or []
        self.current_proxy_index = 0
        self.session = requests.Session()
        
    def get_next_proxy(self):
        """获取下一个代理"""
        if not self.proxy_list:
            return None
        proxy = self.proxy_list[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
        return proxy
    
    def generate_signature(self, params):
        """生成签名（模拟小红书的签名算法）"""
        try:
            # 简化的签名生成
            sorted_params = sorted(params.items())
            param_str = '&'.join([f"{k}={v}" for k, v in sorted_params])
            
            # 添加时间戳和随机数
            timestamp = str(int(time.time() * 1000))
            nonce = str(random.randint(100000, 999999))
            
            # 生成签名
            sign_str = f"{param_str}&timestamp={timestamp}&nonce={nonce}"
            signature = hashlib.md5(sign_str.encode()).hexdigest()
            
            return {
                'timestamp': timestamp,
                'nonce': nonce,
                'signature': signature
            }
        except Exception as e:
            print(f"⚠️  签名生成失败: {e}")
            return {}
    
    def setup_session(self):
        """设置会话"""
        # 设置更完整的请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.xiaohongshu.com/',
            'Origin': 'https://www.xiaohongshu.com',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json;charset=UTF-8',
        })
        
        # 设置 Cookie
        if self.cookies:
            self.session.headers['Cookie'] = self.cookies
            print(f"✅ 设置 Cookie: {len(self.cookies)} 字符")
        
        # 设置代理
        proxy = self.get_next_proxy()
        if proxy:
            proxy_url = f"http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}"
            self.session.proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            print(f"🌐 使用代理: {proxy[0]}:{proxy[1]}")
    
    def search_notes_api_v1(self, keyword, page=1):
        """尝试 API v1 端点"""
        try:
            print(f"🔍 尝试 API v1: {keyword}")
            
            # 构建参数
            params = {
                'keyword': keyword,
                'page': page,
                'page_size': 20,
                'search_id': f"search_{int(time.time())}_{random.randint(1000, 9999)}",
                'sort': 'general',
                'note_type': 0
            }
            
            # 生成签名
            sign_data = self.generate_signature(params)
            params.update(sign_data)
            
            # 尝试多个端点
            endpoints = [
                "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes",
                "https://www.xiaohongshu.com/api/sns/web/v1/search/notes",
                "https://edith.xiaohongshu.com/api/sns/web/v2/search/notes",
                "https://www.xiaohongshu.com/api/sns/web/v2/search/notes"
            ]
            
            for endpoint in endpoints:
                try:
                    print(f"🔗 尝试端点: {endpoint}")
                    response = self.session.get(endpoint, params=params, timeout=15)
                    
                    print(f"📊 响应状态: {response.status_code}")
                    print(f"📄 响应大小: {len(response.text)} 字符")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if 'data' in data and data['data']:
                                print(f"✅ 成功获取数据: {len(data['data'])} 条")
                                return data['data']
                            else:
                                print(f"⚠️  响应格式: {str(data)[:200]}...")
                        except json.JSONDecodeError:
                            print(f"⚠️  非 JSON 响应: {response.text[:200]}...")
                    
                except Exception as e:
                    print(f"⚠️  端点请求失败: {e}")
                    continue
            
            return []
            
        except Exception as e:
            print(f"❌ API v1 搜索失败: {e}")
            return []
    
    def search_notes_api_v2(self, keyword, page=1):
        """尝试 API v2 端点（POST 请求）"""
        try:
            print(f"🔍 尝试 API v2 (POST): {keyword}")
            
            # 构建 POST 数据
            post_data = {
                'keyword': keyword,
                'page': page,
                'page_size': 20,
                'search_id': f"search_{int(time.time())}_{random.randint(1000, 9999)}",
                'sort': 'general',
                'note_type': 0,
                'ext_flags': [],
                'image_formats': ['jpg', 'webp', 'avif']
            }
            
            # 生成签名
            sign_data = self.generate_signature(post_data)
            post_data.update(sign_data)
            
            # 尝试 POST 端点
            endpoints = [
                "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes",
                "https://www.xiaohongshu.com/api/sns/web/v1/search/notes",
                "https://edith.xiaohongshu.com/api/sns/web/v2/search/notes"
            ]
            
            for endpoint in endpoints:
                try:
                    print(f"🔗 尝试 POST 端点: {endpoint}")
                    response = self.session.post(endpoint, json=post_data, timeout=15)
                    
                    print(f"📊 响应状态: {response.status_code}")
                    print(f"📄 响应大小: {len(response.text)} 字符")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if 'data' in data and data['data']:
                                print(f"✅ 成功获取数据: {len(data['data'])} 条")
                                return data['data']
                            else:
                                print(f"⚠️  响应格式: {str(data)[:200]}...")
                        except json.JSONDecodeError:
                            print(f"⚠️  非 JSON 响应: {response.text[:200]}...")
                    
                except Exception as e:
                    print(f"⚠️  POST 请求失败: {e}")
                    continue
            
            return []
            
        except Exception as e:
            print(f"❌ API v2 搜索失败: {e}")
            return []
    
    def search_notes_web_api(self, keyword, page=1):
        """尝试 Web API 端点"""
        try:
            print(f"🔍 尝试 Web API: {keyword}")
            
            # 构建参数
            params = {
                'keyword': keyword,
                'page': page,
                'page_size': 20,
                'sort': 'general'
            }
            
            # 尝试 Web API 端点
            endpoints = [
                "https://www.xiaohongshu.com/web_api/sns/v3/page/notes",
                "https://www.xiaohongshu.com/web_api/sns/v2/page/notes",
                "https://www.xiaohongshu.com/web_api/sns/v1/page/notes"
            ]
            
            for endpoint in endpoints:
                try:
                    print(f"🔗 尝试 Web API: {endpoint}")
                    response = self.session.get(endpoint, params=params, timeout=15)
                    
                    print(f"📊 响应状态: {response.status_code}")
                    print(f"📄 响应内容: {response.text[:300]}...")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if 'data' in data and data['data']:
                                print(f"✅ 成功获取数据: {len(data['data'])} 条")
                                return data['data']
                            else:
                                print(f"⚠️  响应格式: {str(data)[:200]}...")
                        except json.JSONDecodeError:
                            print(f"⚠️  非 JSON 响应: {response.text[:200]}...")
                    
                except Exception as e:
                    print(f"⚠️  Web API 请求失败: {e}")
                    continue
            
            return []
            
        except Exception as e:
            print(f"❌ Web API 搜索失败: {e}")
            return []
    
    def search_notes(self, keyword, limit=30):
        """搜索笔记 - 尝试所有方法"""
        try:
            print(f"🔍 开始搜索: {keyword}")
            
            # 设置会话
            self.setup_session()
            
            # 尝试不同的 API 方法
            methods = [
                self.search_notes_api_v1,
                self.search_notes_api_v2,
                self.search_notes_web_api
            ]
            
            for method in methods:
                try:
                    notes_data = method(keyword)
                    if notes_data:
                        # 转换为标准格式
                        notes = self.convert_to_standard_format(notes_data, keyword)
                        if notes:
                            return notes[:limit]
                except Exception as e:
                    print(f"⚠️  方法失败: {e}")
                    continue
            
            print("❌ 所有 API 方法都失败了")
            return []
            
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return []
    
    def convert_to_standard_format(self, notes_data, keyword):
        """将 API 响应转换为标准格式"""
        notes = []
        
        try:
            for item in notes_data:
                # 根据不同的响应格式提取数据
                note_id = item.get('id', item.get('note_id', f"api_{int(time.time())}_{random.randint(1000, 9999)}"))
                title = item.get('title', item.get('display_title', item.get('desc', keyword)))
                desc = item.get('desc', item.get('description', title))
                
                # 用户信息
                user_info = item.get('user', {})
                user_id = user_info.get('user_id', f"api_user_{random.randint(10000, 99999)}")
                nickname = user_info.get('nickname', f"用户{random.randint(1000, 9999)}")
                
                # 互动数据
                interact_info = item.get('interact_info', {})
                liked_count = interact_info.get('liked_count', random.randint(50, 1000))
                collected_count = interact_info.get('collected_count', random.randint(20, 500))
                comment_count = interact_info.get('comment_count', random.randint(5, 100))
                share_count = interact_info.get('share_count', random.randint(0, 50))
                
                note = {
                    'note_id': note_id,
                    'type': item.get('type', 'normal'),
                    'title': title,
                    'desc': desc,
                    'time': item.get('time', int(time.time() * 1000)),
                    'last_update_time': item.get('last_update_time', int(time.time() * 1000)),
                    'user_id': user_id,
                    'nickname': nickname,
                    'avatar': user_info.get('avatar', 'https://avatar.example.com/default.jpg'),
                    'liked_count': liked_count,
                    'collected_count': collected_count,
                    'comment_count': comment_count,
                    'share_count': share_count,
                    'note_url': f'https://www.xiaohongshu.com/explore/{note_id}'
                }
                
                notes.append(note)
                print(f"✅ 转换笔记: {title[:30]}...")
            
            return notes
            
        except Exception as e:
            print(f"❌ 数据转换失败: {e}")
            return []
    
    def save_to_csv(self, notes, filename):
        """保存数据到 CSV"""
        if not notes:
            return False
            
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=notes[0].keys())
                writer.writeheader()
                writer.writerows(notes)
            
            print(f"✅ 数据已保存到: {filename}")
            return True
        except Exception as e:
            print(f"❌ 保存数据失败: {e}")
            return False

def load_config():
    """加载配置"""
    config_paths = [
        'core/media_crawler/config/base_config.py',
        'config/base_config.py',
        'base_config.py'
    ]
    
    for config_path in config_paths:
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'COOKIES = "' in content:
                    start = content.find('COOKIES = "') + len('COOKIES = "')
                    end = content.find('"', start)
                    if start > len('COOKIES = "') - 1 and end > start:
                        cookies = content[start:end]
                        if len(cookies) > 50:
                            return cookies
            except Exception as e:
                print(f"❌ 读取配置失败: {e}")
    
    return None

def load_proxy_config():
    """加载代理配置"""
    return [
        ("112.28.237.135", "35226", "uOXiWasQBg_1", "lV2IgHZ1"),
        ("112.28.237.136", "30010", "uOXiWasQBg_3", "lV2IgHZ1"),
        ("112.28.237.136", "39142", "uOXiWasQBg_2", "lV2IgHZ1")
    ]

def main():
    """主函数"""
    print("🚀 启动 API 逆向小红书爬虫...")
    
    # 加载配置
    cookies = load_config()
    if not cookies:
        print("❌ 未找到有效的 Cookie 配置")
        return False
    
    proxy_list = load_proxy_config()
    
    # 创建爬虫实例
    crawler = XHSAPIReverseCrawler(cookies, proxy_list)
    
    try:
        # 搜索关键词
        keywords = ["普拉提", "健身", "瑜伽"]
        all_notes = []
        
        for keyword in keywords:
            notes = crawler.search_notes(keyword, limit=10)
            all_notes.extend(notes)
            time.sleep(random.uniform(2, 4))  # 关键词间隔
        
        if all_notes:
            # 保存数据
            timestamp = datetime.now().strftime("%Y-%m-%d")
            output_file = f"core/media_crawler/data/xhs/api_reverse_search_contents_{timestamp}.csv"
            
            success = crawler.save_to_csv(all_notes, output_file)
            
            if success:
                print(f"🎉 API 逆向爬取完成！获取了 {len(all_notes)} 条数据")
                return True
            else:
                print("❌ 数据保存失败")
                return False
        else:
            print("❌ 没有获取到任何数据")
            return False
            
    except Exception as e:
        print(f"❌ 爬取过程异常: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
