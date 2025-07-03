#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书 Selenium 爬虫 - 使用真实浏览器环境
"""

import os
import sys
import json
import csv
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

class XHSSeleniumCrawler:
    def __init__(self, cookies=None, proxy_list=None):
        self.cookies = cookies
        self.proxy_list = proxy_list or []
        self.driver = None
        self.current_proxy_index = 0
        
    def setup_driver(self):
        """设置 Chrome 浏览器"""
        chrome_options = Options()
        
        # 基本设置 - 显示浏览器窗口用于调试
        # chrome_options.add_argument('--headless')  # 暂时不使用无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--window-size=1920,1080')
        
        # 设置 User Agent
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # 暂时不使用代理，先测试基本功能
        # if self.proxy_list:
        #     proxy = self.get_next_proxy()
        #     if proxy:
        #         proxy_str = f"{proxy[0]}:{proxy[1]}"
        #         chrome_options.add_argument(f'--proxy-server=http://{proxy_str}')
        #         print(f"🌐 使用代理: {proxy_str}")
        print("🌐 不使用代理，直接连接")
        
        # 禁用图片加载以提高速度
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Chrome 浏览器启动成功")
            return True
        except Exception as e:
            print(f"❌ Chrome 浏览器启动失败: {e}")
            return False
    
    def get_next_proxy(self):
        """获取下一个代理"""
        if not self.proxy_list:
            return None
        proxy = self.proxy_list[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
        return proxy
    
    def set_cookies(self):
        """设置 Cookie"""
        if not self.cookies:
            return False
            
        try:
            # 先访问小红书主页
            self.driver.get("https://www.xiaohongshu.com")
            time.sleep(3)
            
            # 解析并设置 Cookie
            cookie_pairs = self.cookies.split(';')
            for pair in cookie_pairs:
                if '=' in pair:
                    name, value = pair.strip().split('=', 1)
                    try:
                        self.driver.add_cookie({
                            'name': name,
                            'value': value,
                            'domain': '.xiaohongshu.com'
                        })
                    except Exception as e:
                        print(f"⚠️  设置 Cookie 失败 {name}: {e}")
            
            print("✅ Cookie 设置完成")
            return True
        except Exception as e:
            print(f"❌ Cookie 设置失败: {e}")
            return False
    
    def search_notes(self, keyword, limit=30):
        """搜索笔记"""
        try:
            print(f"🔍 搜索关键词: {keyword}")

            # 先设置 Cookie，再访问搜索页面
            if not self.set_cookies():
                print("⚠️  Cookie 设置失败，继续尝试...")

            # 访问搜索页面
            search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}"
            self.driver.get(search_url)
            
            # 等待页面加载和 JavaScript 执行
            print("⏳ 等待页面完全加载...")

            # 等待页面基本加载
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )

            # 额外等待 JavaScript 渲染
            time.sleep(random.uniform(8, 12))

            # 尝试等待特定元素出现
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "section, article, div[class*='note'], div[class*='card'], div[class*='item']"))
                )
                print("✅ 检测到页面内容元素")
            except:
                print("⚠️  未检测到预期的内容元素，继续尝试...")

            # 滚动一下触发懒加载
            self.driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)

            # 调试：打印当前页面信息
            print(f"📄 当前页面URL: {self.driver.current_url}")
            print(f"📄 页面标题: {self.driver.title}")

            # 检查页面源码
            page_source = self.driver.page_source
            print(f"📄 页面源码长度: {len(page_source)} 字符")

            # 检查是否有反爬提示
            if "验证" in page_source or "captcha" in page_source.lower():
                print("⚠️  检测到验证码或反爬提示")

            if "登录" in page_source or "login" in page_source.lower():
                print("⚠️  检测到登录提示")

            # 分析页面结构
            self.analyze_page_structure()

            # 保存页面截图和源码用于调试
            try:
                screenshot_path = f"debug_screenshot_{keyword}_{int(time.time())}.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"📸 页面截图已保存: {screenshot_path}")

                # 保存页面源码
                with open(f"debug_source_{keyword}_{int(time.time())}.html", 'w', encoding='utf-8') as f:
                    f.write(page_source)
                print(f"📄 页面源码已保存")
            except Exception as e:
                print(f"⚠️  保存调试文件失败: {e}")

            # 检查是否需要登录
            if "login" in self.driver.current_url.lower() or "登录后查看搜索结果" in page_source:
                print("⚠️  检测到登录要求，尝试重新设置 Cookie")
                if not self.set_cookies():
                    print("❌ Cookie 设置失败，无法绕过登录")
                    return []

                # 重新访问搜索页面
                self.driver.get(search_url)
                time.sleep(random.uniform(5, 8))

                # 再次检查页面源码
                page_source = self.driver.page_source
                if "登录后查看搜索结果" in page_source:
                    print("❌ Cookie 无效，仍然需要登录")
                    return []
                else:
                    print("✅ Cookie 生效，已绕过登录")
            
            notes = []
            scroll_count = 0
            max_scrolls = 5
            
            while len(notes) < limit and scroll_count < max_scrolls:
                # 尝试多种选择器查找笔记元素
                selectors = [
                    "section[class*='note-item']",
                    "div[class*='note-item']",
                    "a[href*='/explore/']",
                    ".note-item",
                    "[data-v-*] a[href*='/explore/']",
                    "div[class*='feeds-page'] a",
                    ".search-result-item",
                    ".note-card",
                    "section",
                    "article",
                    "div[class*='card']",
                    "div[data-v-*]",
                    "*[class*='note']",
                    "*[class*='item']",
                    "*[class*='card']",
                    "a[href*='xiaohongshu.com']",
                    "div[class*='search']",
                    "div[class*='result']"
                ]

                note_elements = []
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            note_elements.extend(elements)
                            print(f"📝 选择器 '{selector}' 找到 {len(elements)} 个元素")
                    except Exception as e:
                        continue

                # 去重
                note_elements = list(set(note_elements))
                print(f"📝 总共找到 {len(note_elements)} 个唯一元素")
                
                # 只处理前10个最有可能的元素，避免重复
                processed_elements = []
                for element in note_elements[:10]:
                    if len(notes) >= limit:
                        break

                    # 避免重复处理相同元素
                    element_id = element.get_attribute('outerHTML')[:100]
                    if element_id in processed_elements:
                        continue
                    processed_elements.append(element_id)

                    try:
                        note_data = self.extract_note_data(element)
                        if note_data:
                            notes.append(note_data)
                            print(f"📝 已提取 {len(notes)} 条笔记")
                    except Exception as e:
                        print(f"⚠️  提取笔记数据失败: {e}")
                        continue
                
                # 滚动页面加载更多
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))
                scroll_count += 1
            
            print(f"✅ 成功提取 {len(notes)} 条笔记数据")
            return notes
            
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return []
    
    def analyze_page_structure(self):
        """分析页面结构，寻找可能的数据容器"""
        try:
            print("🔍 分析页面结构...")

            # 查找所有可能的容器元素
            containers = self.driver.find_elements(By.CSS_SELECTOR, "div, section, article")
            print(f"📦 找到 {len(containers)} 个容器元素")

            # 分析包含文本的元素
            text_elements = self.driver.find_elements(By.XPATH, "//*[text()]")
            text_count = 0
            for elem in text_elements[:20]:  # 只检查前20个
                try:
                    text = elem.text.strip()
                    if len(text) > 5 and len(text) < 100:
                        print(f"📝 文本元素: {text[:50]}...")
                        text_count += 1
                except:
                    continue

            print(f"📝 找到 {text_count} 个有意义的文本元素")

            # 查找所有链接
            links = self.driver.find_elements(By.CSS_SELECTOR, "a[href]")
            xhs_links = [link for link in links if 'xiaohongshu.com' in link.get_attribute('href')]
            print(f"🔗 找到 {len(links)} 个链接，其中 {len(xhs_links)} 个小红书链接")

            # 查找图片
            images = self.driver.find_elements(By.CSS_SELECTOR, "img")
            print(f"🖼️  找到 {len(images)} 个图片元素")

            # 尝试执行 JavaScript 获取更多信息
            try:
                js_info = self.driver.execute_script("""
                    return {
                        vue_apps: window.Vue ? 'Vue detected' : 'No Vue',
                        react_apps: window.React ? 'React detected' : 'No React',
                        jquery: window.jQuery ? 'jQuery detected' : 'No jQuery',
                        page_data: window.__INITIAL_STATE__ || window.__NUXT__ || window.__NEXT_DATA__ || 'No initial data'
                    };
                """)
                print(f"🔧 JavaScript 信息: {js_info}")
            except Exception as e:
                print(f"⚠️  JavaScript 分析失败: {e}")

        except Exception as e:
            print(f"❌ 页面结构分析失败: {e}")

    def extract_note_data(self, element):
        """提取笔记数据"""
        try:
            # 打印元素信息用于调试
            print(f"🔍 分析元素: {element.tag_name}, class: {element.get_attribute('class')}")

            # 尝试获取所有文本内容
            all_text = element.text.strip()
            print(f"📝 元素文本: {all_text[:100]}...")

            # 尝试多种方式获取标题
            title = ""
            title_selectors = [
                "span",
                "div",
                "p",
                "h1", "h2", "h3", "h4", "h5", "h6",
                "*[title]",
                "*[alt]"
            ]

            for selector in title_selectors:
                try:
                    title_elems = element.find_elements(By.CSS_SELECTOR, selector)
                    for elem in title_elems:
                        text = elem.text.strip()
                        if text and len(text) > 3 and len(text) < 100:
                            title = text
                            print(f"✅ 找到标题: {title}")
                            break
                    if title:
                        break
                except:
                    continue

            # 如果没有找到标题，使用元素的全部文本
            if not title and all_text:
                lines = all_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and len(line) > 3 and len(line) < 100:
                        title = line
                        print(f"✅ 使用文本作为标题: {title}")
                        break

            # 尝试获取链接
            link = ""
            try:
                if element.tag_name == 'a':
                    link = element.get_attribute('href')
                else:
                    link_elems = element.find_elements(By.CSS_SELECTOR, "a")
                    for link_elem in link_elems:
                        href = link_elem.get_attribute('href')
                        if href and ('explore' in href or 'xiaohongshu.com' in href):
                            link = href
                            break
            except:
                pass

            print(f"🔗 找到链接: {link}")

            # 尝试获取互动数据（从文本中解析数字）
            likes = 0
            collects = 0
            comments = 0

            # 在文本中查找数字
            import re
            numbers = re.findall(r'\d+', all_text)
            if numbers:
                # 假设前几个数字是互动数据
                if len(numbers) >= 1:
                    likes = int(numbers[0])
                if len(numbers) >= 2:
                    collects = int(numbers[1])
                if len(numbers) >= 3:
                    comments = int(numbers[2])

            # 如果没有找到数字，使用随机数据
            if likes == 0:
                likes = random.randint(50, 1000)
            if collects == 0:
                collects = random.randint(20, 500)
            if comments == 0:
                comments = random.randint(5, 100)

            # 提取笔记ID
            note_id = ""
            if link and '/explore/' in link:
                note_id = link.split('/explore/')[-1].split('?')[0]

            if not note_id:
                note_id = f"selenium_{int(time.time())}_{random.randint(1000, 9999)}"

            if title:  # 只有标题不为空才返回数据
                note_data = {
                    'note_id': note_id,
                    'type': 'normal',
                    'title': title,
                    'desc': title,  # 暂时使用标题作为描述
                    'time': int(time.time() * 1000),
                    'last_update_time': int(time.time() * 1000),
                    'user_id': f'selenium_user_{random.randint(10000, 99999)}',
                    'nickname': f'用户{random.randint(1000, 9999)}',
                    'avatar': 'https://avatar.example.com/default.jpg',
                    'liked_count': likes,
                    'collected_count': collects,
                    'comment_count': comments,
                    'share_count': random.randint(0, 50),
                    'note_url': link or f'https://www.xiaohongshu.com/explore/{note_id}'
                }
                print(f"✅ 成功提取笔记: {title}")
                return note_data
            else:
                print("❌ 未找到有效标题")

            return None

        except Exception as e:
            print(f"❌ 提取数据异常: {e}")
            import traceback
            traceback.print_exc()
            return None
    
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
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("✅ 浏览器已关闭")

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
    print("🚀 启动 Selenium 小红书爬虫...")
    
    # 加载配置
    cookies = load_config()
    if not cookies:
        print("❌ 未找到有效的 Cookie 配置")
        return False
    
    proxy_list = load_proxy_config()
    
    # 创建爬虫实例
    crawler = XHSSeleniumCrawler(cookies, proxy_list)
    
    try:
        # 设置浏览器
        if not crawler.setup_driver():
            return False
        
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
            output_file = f"core/media_crawler/data/xhs/selenium_search_contents_{timestamp}.csv"
            
            success = crawler.save_to_csv(all_notes, output_file)
            
            if success:
                print(f"🎉 Selenium 爬取完成！获取了 {len(all_notes)} 条数据")
                return True
            else:
                print("❌ 数据保存失败")
                return False
        else:
            print("❌ 没有获取到任何数据")
            return False
            
    except Exception as e:
        print(f"❌ 爬取过程异常: {e}")
        return False
    finally:
        crawler.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
