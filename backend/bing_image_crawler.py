"""
Bing图片搜索爬虫
此脚本使用Bing图片搜索为景点获取相关图片链接
"""

import asyncio
import json
import time
import random
import re
import urllib.parse
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
    'Referer': 'https://www.bing.com/',
}

class BingImageCrawler:
    def __init__(self):
        # 不使用session，避免代理问题
        pass
        
    def search_images(self, query, count=5):
        """
        使用Bing图片搜索获取相关图片
        """
        print(f"正在搜索 '{query}' 的相关图片...")
        
        # 对查询词进行URL编码
        encoded_query = urllib.parse.quote(query)
        
        # 构造搜索URL（按相关性排序，过滤大尺寸图片）
        search_url = f"https://www.bing.com/images/search?q={encoded_query}&qft=+filterui:imagesize-large&first=1"
        
        # 尝试多次连接，避免网络问题
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # 减少延迟时间，但仍保持随机性避免被封
                time.sleep(random.uniform(0.5, 1.5))
                
                # 创建新的请求，不使用session避免代理问题
                response = requests.get(
                    search_url, 
                    headers=HEADERS, 
                    timeout=15,
                    verify=True  # 验证SSL证书
                )
                response.raise_for_status()
                
                # 检查是否触发了反爬验证
                if "验证" in response.text or "captcha" in response.text.lower():
                    print("  警告：可能触发了反爬验证")
                    return []
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                image_links = []
                
                # 方法1: 解析结构化数据（最可靠方式）
                for meta in soup.find_all('a', {'class': 'iusc'}):
                    m = meta.get('m')
                    if m:
                        try:
                            # 安全地解析JSON数据
                            # 替换转义引号
                            m = m.replace('\\"', '"')
                            # 使用正则表达式提取JSON对象
                            image_data = json.loads(m)
                            if image_data.get('murl'):
                                orig_url = image_data['murl']
                                # 验证URL是否有效
                                if orig_url.startswith(('http://', 'https://')):
                                    image_links.append(orig_url)
                                    if len(image_links) >= count:
                                        break
                        except Exception as e:
                            # 如果JSON解析失败，尝试其他方法
                            continue
                
                # 方法2: 如果方法1没有获取到足够图片，则尝试其他方式
                if len(image_links) < count:
                    # 查找包含图片信息的其他元素
                    img_containers = soup.find_all('div', class_='img_cont')
                    for container in img_containers:
                        img_tag = container.find('img')
                        if img_tag:
                            # 尝试从data-src或src获取图片链接
                            src = img_tag.get('data-src') or img_tag.get('src')
                            if src and src.startswith('http'):
                                # 如果是缩略图URL，尝试获取原始URL
                                if 'th?id=' in src:
                                    # 尝试构建原始图片URL
                                    # 对于Bing，我们直接使用缩略图URL，因为原始URL可能难以提取
                                    image_links.append(src)
                                else:
                                    image_links.append(src)
                            
                            if len(image_links) >= count:
                                break
                
                # 方法3: 从m属性中直接提取图片链接
                if len(image_links) < count:
                    # 查找所有具有m属性的元素
                    media_items = soup.find_all(attrs={"m": True})
                    for item in media_items:
                        m_data = item.get("m")
                        if m_data:
                            # 尝试提取murl
                            murl_match = re.search(r'"murl":"([^"]+)"', m_data)
                            if murl_match:
                                url = murl_match.group(1).replace("\\", "")
                                if url.startswith(('http://', 'https://')):
                                    image_links.append(url)
                                    if len(image_links) >= count:
                                        break
                
                print(f"  找到 {len(image_links)} 张相关图片")
                return image_links[:count]
                
            except requests.exceptions.ProxyError as e:
                print(f"  代理错误: 无法连接到代理服务器，请检查网络设置 (尝试 {attempt+1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                continue
            except requests.exceptions.ConnectionError as e:
                print(f"  连接错误: 无法连接到服务器，请检查网络连接 (尝试 {attempt+1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                continue
            except requests.exceptions.Timeout as e:
                print(f"  超时错误: 请求超时，请检查网络连接 (尝试 {attempt+1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                continue
            except requests.exceptions.RequestException as e:
                print(f"  请求错误: {e} (尝试 {attempt+1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                continue
            except Exception as e:
                print(f"  搜索图片时出错: {e} (尝试 {attempt+1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                continue
        
        return []
    
    def crawl_images_for_attraction(self, attraction_name):
        """
        为特定景点爬取相关图片
        """
        print(f"正在为景点 '{attraction_name}' 爬取相关图片...")
        
        # 构造多个搜索关键词以提高相关性
        search_queries = [
            f"{attraction_name}",
            f"{attraction_name} 风景",
        ]
        
        all_images = []
        
        for query in search_queries:
            images = self.search_images(query, count=3)
            all_images.extend(images)
            
            # 减少延迟时间
            time.sleep(random.uniform(0.5, 1))
            
            # 如果已经获取到足够多的图片，就停止搜索
            if len(all_images) >= 5:
                break
        
        # 去重并限制数量
        unique_images = list(dict.fromkeys(all_images))[:5]
        
        # 构造完整的结果
        results = []
        for i, url in enumerate(unique_images):
            results.append({
                'url': url,
                'title': f"{attraction_name} 相关图片 {i+1}",
                'source': 'Bing图片搜索',
                'description': f"通过Bing搜索'{attraction_name}'获取的相关图片"
            })
        
        return results
    
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
    crawler = BingImageCrawler()
    
    app = create_app()
    with app.app_context():
        # 获取所有景点
        attractions = Attraction.objects()
        print(f"数据库中共有 {attractions.count()} 个景点")
        
        results = []
        updated_count = 0
        
        # 处理所有景点，不再限制数量
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
            
            # 减少延迟时间，但仍保持随机性避免被封
            time.sleep(random.uniform(1, 2))
        
        # 保存结果到JSON文件
        with open('bing_images.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n处理完成!")
        print(f"总共处理 {attractions.count()} 个景点")
        print(f"成功更新 {updated_count} 个景点的图片")
        print("详细结果已保存到 bing_images.json")

def main():
    """
    主函数
    """
    print("Bing图片搜索爬虫")
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