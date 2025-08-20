"""
百度百科图片爬虫
此脚本从百度百科搜索景点相关图片，并导入到数据库中
"""

import asyncio
import json
import time
import random
import re
import os
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from app import create_app
from models import Attraction

# 请求头信息，模拟浏览器访问
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# 百度百科基础URL
BAIDU_BAIKE_BASE = "https://baike.baidu.com"

class BaiduBaikeImageCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        
    def get_baidu_baike_page(self, keyword):
        """
        获取百度百科页面
        """
        try:
            # 搜索百度百科
            search_url = f"https://baike.baidu.com/search/word"
            params = {
                'word': keyword,
                'pic': 1  # 启用图片模式
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            # 检查是否重定向到词条页面
            if '/item/' in response.url:
                return response.url, response.text
            else:
                # 解析搜索结果页面，找到第一个词条链接
                soup = BeautifulSoup(response.text, 'html.parser')
                first_result = soup.find('a', class_='result-title')
                if first_result and first_result.get('href'):
                    item_url = BAIDU_BAIKE_BASE + first_result['href']
                    # 获取词条页面内容
                    item_response = self.session.get(item_url, timeout=10)
                    item_response.raise_for_status()
                    return item_url, item_response.text
            
            return None, None
        except Exception as e:
            print(f"获取百度百科页面 {keyword} 时出错: {e}")
            return None, None
    
    def extract_images_from_page(self, html_content, keyword):
        """
        从百度百科页面提取图片
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            images = []
            
            # 方法1: 查找相册中的图片
            album_items = soup.find_all('div', class_='album-item')
            for item in album_items:
                img_tag = item.find('img')
                if img_tag:
                    # 获取真实图片URL，百度百科使用懒加载，真实URL在data-src或data-original等属性中
                    img_url = (img_tag.get('data-src') or 
                              img_tag.get('data-original') or 
                              img_tag.get('data-lazyload') or 
                              img_tag.get('src'))
                    
                    if img_url and not img_url.endswith('new.png'):
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        elif img_url.startswith('/'):
                            img_url = BAIDU_BAIKE_BASE + img_url
                        
                        title = img_tag.get('alt', f"{keyword}相关图片") or f"{keyword}图片"
                        images.append({
                            'url': img_url,
                            'title': title,
                            'source': '百度百科相册',
                            'description': title
                        })
            
            # 方法2: 查找summary-pic中的主图
            summary_pic = soup.find('div', class_='summary-pic')
            if summary_pic:
                img_tag = summary_pic.find('img')
                if img_tag:
                    img_url = (img_tag.get('data-src') or 
                              img_tag.get('data-original') or 
                              img_tag.get('data-lazyload') or 
                              img_tag.get('src'))
                    
                    if img_url and not img_url.endswith('new.png'):
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        elif img_url.startswith('/'):
                            img_url = BAIDU_BAIKE_BASE + img_url
                        
                        images.append({
                            'url': img_url,
                            'title': f"{keyword} - 百度百科主图",
                            'source': '百度百科主图',
                            'description': f"{keyword}的百度百科主图"
                        })
            
            # 方法3: 查找正文中的图片
            content_bodies = soup.find_all('div', class_='lemma-summary') or soup.find_all('div', class_='main-content')
            for content_body in content_bodies:
                img_tags = content_body.find_all('img')
                for img_tag in img_tags:
                    img_url = (img_tag.get('data-src') or 
                              img_tag.get('data-original') or 
                              img_tag.get('data-lazyload') or 
                              img_tag.get('src'))
                    
                    if img_url and not img_url.endswith('new.png'):
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        elif img_url.startswith('/'):
                            img_url = BAIDU_BAIKE_BASE + img_url
                        
                        title = img_tag.get('alt', f"{keyword}内容图片") or f"{keyword}内容图片"
                        images.append({
                            'url': img_url,
                            'title': title,
                            'source': '百度百科内容',
                            'description': title
                        })
            
            # 方法4: 查找所有可能包含图片的元素
            all_imgs = soup.find_all('img')
            for img_tag in all_imgs:
                img_src = (img_tag.get('data-src') or 
                          img_tag.get('data-original') or 
                          img_tag.get('data-lazyload') or 
                          img_tag.get('src'))
                
                if (img_src and 
                    not img_src.endswith('new.png') and
                    'logo' not in img_src):
                    
                    if img_src.startswith('//'):
                        img_url = 'https:' + img_src
                    elif img_src.startswith('/'):
                        img_url = BAIDU_BAIKE_BASE + img_src
                    else:
                        img_url = img_src
                    
                    # 检查是否是有效的图片链接
                    if any(ext in img_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                        title = img_tag.get('alt', f"{keyword}相关图片") or f"{keyword}图片"
                        images.append({
                            'url': img_url,
                            'title': title,
                            'source': '百度百科通用',
                            'description': title
                        })
            
            # 方法5: 特殊处理：尝试从JavaScript中提取图片URL
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # 查找可能包含图片URL的JavaScript代码
                    # 匹配更多可能的图片URL模式
                    patterns = [
                        r'"picUrl"\s*:\s*"([^"]+)"',
                        r'"url"\s*:\s*"([^"]+)"',
                        r'https?://[^\s"\']*\.(?:jpg|jpeg|png|gif)[^\s"\']*'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, script.string)
                        for match in matches:
                            if isinstance(match, str) and ('baike' in match or 'bdimg' in match):
                                # 清理URL，移除可能的引号或逗号
                                img_url = re.sub(r'[",\'}].*', '', match)
                                if not img_url.endswith('new.png'):
                                    if img_url.startswith('//'):
                                        img_url = 'https:' + img_url
                                    elif img_url.startswith('/'):
                                        img_url = BAIDU_BAIKE_BASE + img_url
                                    
                                    images.append({
                                        'url': img_url,
                                        'title': f"{keyword} JS图片",
                                        'source': '百度百科JS',
                                        'description': f"{keyword}从JS中提取的图片"
                                    })
            
            # 方法6: 通过API获取图片（如果页面中有picGroupUid）
            # 查找picGroupUid
            pic_group_match = re.search(r'picGroupUid\s*[:=]\s*["\']([^"\']+)["\']', html_content)
            if pic_group_match:
                pic_group_uid = pic_group_match.group(1)
                # 构造API请求URL
                api_url = f"https://baike.baidu.com/api/wikiui/getpics?picGroupUid={pic_group_uid}"
                try:
                    api_response = self.session.get(api_url, timeout=10)
                    api_response.raise_for_status()
                    api_data = api_response.json()
                    if 'data' in api_data and 'picList' in api_data['data']:
                        for pic in api_data['data']['picList']:
                            if 'url' in pic:
                                img_url = pic['url']
                                if img_url.startswith('//'):
                                    img_url = 'https:' + img_url
                                
                                title = pic.get('title', f"{keyword} API图片") or f"{keyword} API图片"
                                images.append({
                                    'url': img_url,
                                    'title': title,
                                    'source': '百度百科API',
                                    'description': title
                                })
                except Exception as e:
                    print(f"通过API获取图片时出错: {e}")
            
            return images
        except Exception as e:
            print(f"从页面提取图片时出错: {e}")
            return []
    
    def filter_and_sort_images(self, images, keyword):
        """
        过滤和排序图片，选择最相关的高质量图片
        """
        if not images:
            return []
        
        # 过滤有效的图片URL
        valid_images = []
        for img in images:
            url = img['url']
            # 检查是否是有效的图片URL
            if url and (url.endswith(('.jpg', '.jpeg', '.png', '.gif')) or 'pic' in url or 'image' in url):
                # 检查是否为占位符图片
                if url.endswith('new.png'):
                    continue
                    
                # 检查图片标题是否与关键词相关
                title = img['title'].lower()
                description = img['description'].lower()
                keyword_lower = keyword.lower()
                
                # 计算相关性分数
                score = 0
                if keyword_lower in title or keyword_lower in description:
                    score += 50
                elif any(word in title or word in description for word in keyword_lower.split()):
                    score += 30
                
                # 根据来源评分
                source = img['source']
                if '主图' in source:
                    score += 25
                elif '相册' in source:
                    score += 20
                elif '内容' in source:
                    score += 15
                elif 'API' in source:
                    score += 12
                elif 'JS' in source:
                    score += 10
                else:
                    score += 5
                
                img['score'] = score
                valid_images.append(img)
        
        # 去重：根据URL去重
        seen_urls = set()
        unique_images = []
        for img in valid_images:
            if img['url'] not in seen_urls:
                seen_urls.add(img['url'])
                unique_images.append(img)
        
        # 按分数排序
        unique_images.sort(key=lambda x: x['score'], reverse=True)
        return unique_images
    
    def crawl_images_for_attraction(self, attraction_name):
        """
        为特定景点爬取图片
        """
        print(f"正在为景点 '{attraction_name}' 爬取百度百科图片...")
        
        # 获取百度百科页面
        page_url, html_content = self.get_baidu_baike_page(attraction_name)
        if not html_content:
            print(f"  未能找到 {attraction_name} 的百度百科页面")
            return []
        
        print(f"  找到百度百科页面: {page_url}")
        
        # 提取图片
        images = self.extract_images_from_page(html_content, attraction_name)
        print(f"  从页面提取到 {len(images)} 张图片")
        
        # 过滤和排序图片
        filtered_images = self.filter_and_sort_images(images, attraction_name)
        print(f"  过滤后剩余 {len(filtered_images)} 张有效图片")
        
        return filtered_images[:5]  # 返回前5张最相关的图片
    
    def update_database_with_images(self, attraction_name, images):
        """
        将图片信息更新到数据库
        """
        if not images:
            return False
        
        app = create_app()
        with app.app_context():
            # 查找景点
            attraction = Attraction.objects(name=attraction_name).first()
            if not attraction:
                print(f"  数据库中未找到景点: {attraction_name}")
                return False
            
            # 使用第一张图片作为主图
            best_image = images[0]
            if not attraction.image_url or attraction.image_url != best_image['url']:
                old_url = attraction.image_url
                attraction.image_url = best_image['url']
                attraction.save()
                print(f"  ✓ 已更新 {attraction_name} 的图片链接")
                print(f"    原链接: {old_url}")
                print(f"    新链接: {best_image['url']}")
                return True
            else:
                print(f"  图片链接未变化，无需更新")
                return False

def process_attractions_from_db():
    """
    从数据库中获取所有景点并为其爬取图片
    """
    crawler = BaiduBaikeImageCrawler()
    
    app = create_app()
    with app.app_context():
        # 获取所有景点
        attractions = Attraction.objects()
        print(f"数据库中共有 {attractions.count()} 个景点")
        
        results = []
        updated_count = 0
        
        for i, attraction in enumerate(attractions):
            attraction_name = attraction.name
            print(f"\n处理进度: {i+1}/{attractions.count()} - {attraction_name}")
            
            # 爬取图片
            images = crawler.crawl_images_for_attraction(attraction_name)
            
            if images:
                # 更新数据库
                updated = crawler.update_database_with_images(attraction_name, images)
                if updated:
                    updated_count += 1
                
                results.append({
                    'attraction': attraction_name,
                    'images': images
                })
            else:
                print(f"  未找到相关图片")
            
            # 添加延时，避免请求过于频繁
            time.sleep(random.uniform(2, 4))
        
        # 保存结果到JSON文件
        with open('baidu_baike_images.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n处理完成!")
        print(f"总共处理 {attractions.count()} 个景点")
        print(f"成功更新 {updated_count} 个景点的图片")
        print("详细结果已保存到 baidu_baike_images.json")

def main():
    """
    主函数
    """
    print("百度百科图片爬虫")
    print("=" * 50)
    print("注意事项:")
    print("1. 请遵守robots.txt协议")
    print("2. 注意图片版权问题")
    print("3. 已添加请求延时避免过于频繁")
    print("4. 仅用于学习和非商业用途")
    print("=" * 50)
    
    process_attractions_from_db()

if __name__ == "__main__":
    main()