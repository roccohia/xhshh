#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理器 - 用于动态设置 MediaCrawler 配置而不修改源码文件
"""

import os
import sys
import json
from typing import Dict, Any


class ConfigManager:
    """配置管理器，用于动态覆盖 MediaCrawler 的配置"""
    
    def __init__(self, config_file_path: str):
        """
        初始化配置管理器
        
        Args:
            config_file_path: xhs_config.json 文件路径
        """
        self.config_file_path = config_file_path
        self.config_data = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load config file {self.config_file_path}: {e}")
    
    def setup_mediacrawler_config(self, keyword: str, limit: int):
        """
        设置 MediaCrawler 配置

        Args:
            keyword: 搜索关键词
            limit: 爬取数量限制
        """
        # 添加 MediaCrawler 路径到 sys.path
        mediacrawler_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../core/media_crawler')
        )
        if mediacrawler_path not in sys.path:
            sys.path.insert(0, mediacrawler_path)

        # 切换到 MediaCrawler 目录，确保相对路径正确
        original_cwd = os.getcwd()
        os.chdir(mediacrawler_path)

        # 导入配置模块
        import config
        
        # 动态设置配置
        config.PLATFORM = "xhs"
        config.KEYWORDS = keyword
        config.LOGIN_TYPE = "cookie"
        config.CRAWLER_TYPE = "search"
        config.CRAWLER_MAX_NOTES_COUNT = limit
        config.SAVE_DATA_OPTION = "csv"  # 强制使用 CSV 输出
        config.ENABLE_GET_COMMENTS = True
        config.ENABLE_GET_SUB_COMMENTS = False
        config.HEADLESS = False  # 使用有头浏览器，便于处理验证码
        config.ENABLE_CDP_MODE = False
        config.ENABLE_IP_PROXY = False
        config.MAX_CONCURRENCY_NUM = 1
        config.START_PAGE = 1
        config.SORT_TYPE = ""
        
        # 设置 Cookie
        cookie_dict = self.config_data.get('cookie', {})
        cookies_str = '; '.join([f'{k}={v}' for k, v in cookie_dict.items()])
        config.COOKIES = cookies_str
        
        # 设置 User Agent
        headers = self.config_data.get('headers', {})
        config.UA = headers.get('User-Agent', 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')
        
        print(f"[ConfigManager] 配置已设置:")
        print(f"  - 关键词: {keyword}")
        print(f"  - 数量限制: {limit}")
        print(f"  - 登录类型: cookie")
        print(f"  - 输出格式: csv")
        print(f"  - Cookie已设置: {len(cookies_str)} 字符")
        print(f"  - 工作目录: {os.getcwd()}")

        # 禁用词云功能，避免文件路径问题
        config.ENABLE_GET_WORDCLOUD = False

        return config
    
    def get_cookie_dict(self) -> Dict[str, str]:
        """获取 Cookie 字典"""
        return self.config_data.get('cookie', {})
    
    def get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return self.config_data.get('headers', {})


def create_config_manager(config_file_path: str) -> ConfigManager:
    """创建配置管理器实例"""
    return ConfigManager(config_file_path)
