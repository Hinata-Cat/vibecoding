"""
为江西省景点添加图片的脚本
使用Bing图片搜索为没有图片的江西省景点获取相关图片
"""

import time
import random
import urllib.parse
import requests
from bs4 import BeautifulSoup
from app import create_app
from models import Province, Attraction

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

def search_images(query, count=1):
    """
    使用Bing图片搜索获取相关图片
    """
    print(f"正在搜索 '{query}' 的相关图片...")
    
    # 对查询词进行URL编码
    encoded_query = urllib.parse.quote(query)
    
    # 构造搜索URL（按相关性排序，过滤大尺寸图片）
    search_url = f"https://www.bing.com/images/search?q={encoded_query}&qft=+filterui:imagesize-large&first=1"
    
    try:
        # 随机延迟避免过于频繁的请求
        time.sleep(random.uniform(0.5, 1.5))
        
        # 创建新的请求
        response = requests.get(
            search_url, 
            headers=HEADERS, 
            timeout=15,
            verify=True
        )
        response.raise_for_status()
        
        # 检查是否触发了反爬验证
        if "验证" in response.text or "captcha" in response.text.lower():
            print("  警告：可能触发了反爬验证")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        image_links = []
        
        # 解析结构化数据获取图片链接
        for meta in soup.find_all('a', {'class': 'iusc'}):
            m = meta.get('m')
            if m:
                try:
                    # 安全地解析JSON数据
                    m = m.replace('\\"', '"')
                    import json
                    image_data = json.loads(m)
                    if image_data.get('murl'):
                        orig_url = image_data['murl']
                        # 验证URL是否有效
                        if orig_url.startswith(('http://', 'https://')):
                            image_links.append(orig_url)
                            if len(image_links) >= count:
                                break
                except Exception as e:
                    continue
        
        print(f"  找到 {len(image_links)} 张相关图片")
        return image_links[:count]
        
    except Exception as e:
        print(f"  搜索图片时出错: {e}")
        return []

def update_jiangxi_attraction_images():
    """
    更新江西省景点的图片
    """
    app = create_app()
    
    with app.app_context():
        # 查找江西省
        province = Province.objects(name='江西省').first()
        if not province:
            print("未找到江西省")
            return
        
        # 获取江西省所有景点
        jiangxi_attractions = Attraction.objects(province=province)
        print(f"江西省共有 {jiangxi_attractions.count()} 个景点")
        
        # 统计没有图片的景点
        no_image_attractions = [a for a in jiangxi_attractions if not a.image_url]
        print(f"其中没有图片的景点有 {len(no_image_attractions)} 个")
        
        updated_count = 0
        
        # 为没有图片的景点搜索图片
        for attraction in no_image_attractions:
            print(f"\n正在处理: {attraction.name}")
            
            # 搜索图片
            images = search_images(f"{attraction.name} 风景", count=1)
            
            if images:
                # 更新数据库
                old_url = attraction.image_url
                attraction.image_url = images[0]
                attraction.save()
                print(f"  ✓ 已更新 {attraction.name} 的图片链接")
                print(f"    原链接: {old_url}")
                print(f"    新链接: {images[0]}")
                updated_count += 1
            else:
                print(f"  ✗ 未能找到 {attraction.name} 的相关图片")
            
            # 添加延时
            time.sleep(random.uniform(1, 2))
        
        print(f"\n处理完成! 成功为 {updated_count} 个景点添加了图片")

def main():
    """
    主函数
    """
    print("江西省景点图片更新工具")
    print("=" * 50)
    update_jiangxi_attraction_images()

if __name__ == "__main__":
    main()