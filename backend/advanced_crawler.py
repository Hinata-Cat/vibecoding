"""
高级爬虫程序，用于爬取中国省份和景点信息
此脚本将爬取网络上的省份介绍、景点信息、图片和视频链接
"""

import requests
import json
import time
import random
from bs4 import BeautifulSoup
import urllib.parse

# 中国主要省份列表
PROVINCES = [
    "北京市", "上海市", "天津市", "重庆市",
    "河北省", "山西省", "辽宁省", "吉林省", "黑龙江省",
    "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省",
    "河南省", "湖北省", "湖南省", "广东省", "海南省",
    "四川省", "贵州省", "云南省", "陕西省", "甘肃省",
    "青海省", "台湾省", "内蒙古自治区", "广西壮族自治区", 
    "西藏自治区", "宁夏回族自治区", "新疆维吾尔自治区"
]

def get_random_headers():
    """
    获取随机请求头，模拟不同浏览器访问
    """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
    ]
    
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

def crawl_province_info(province_name):
    """
    爬取省份介绍信息
    """
    try:
        # 使用百度百科搜索省份信息
        search_url = f"https://baike.baidu.com/item/{province_name}"
        headers = get_random_headers()
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找省份介绍的段落
            intro_paragraphs = soup.find_all('div', class_='lemma-summary')
            if not intro_paragraphs:
                intro_paragraphs = soup.find_all('div', class_='para')
            
            if intro_paragraphs:
                # 提取前几个段落作为简介
                intro_text = ""
                for i, para in enumerate(intro_paragraphs[:3]):  # 取前3个段落
                    text = para.get_text().strip()
                    if text:
                        intro_text += text + "\n"
                        if len(intro_text) > 500:  # 限制长度
                            break
                
                intro_text = intro_text.strip()
                if intro_text:
                    print(f"成功爬取 {province_name} 的介绍")
                    return intro_text
            
            print(f"未找到 {province_name} 的详细介绍")
            return f"{province_name}是中国的一个省份，拥有丰富的历史文化和自然资源。"
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return f"{province_name}是中国的一个省份，拥有丰富的历史文化和自然资源。"
            
    except Exception as e:
        print(f"爬取 {province_name} 时出错: {e}")
        return f"{province_name}是中国的一个省份，拥有丰富的历史文化和自然资源。"

def search_bilibili_videos(province_name, keyword_suffix="旅游"):
    """
    在B站搜索与省份相关的视频，获取不同的视频链接
    """
    try:
        # 构造不同的搜索关键词组合
        keywords = [
            f"{province_name} {keyword_suffix}",
            f"{province_name} 景点",
            f"{province_name} 介绍",
            f"{province_name} 自驾游",
            f"{province_name} 攻略"
        ]
        
        # 随机选择一个关键词
        keyword = random.choice(keywords)
        
        # B站搜索页面URL
        search_url = "https://search.bilibili.com/all"
        headers = get_random_headers()
        
        params = {
            'keyword': keyword,
            'page': random.randint(1, 3),  # 随机选择页面
            'order': 'click'  # 按点击量排序
        }
        
        response = requests.get(search_url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找视频链接
            video_links = soup.find_all('a', href=True)
            bilibili_links = []
            
            for link in video_links:
                href = link['href']
                if href.startswith('//www.bilibili.com/video/') or '/video/' in href:
                    # 构造完整的B站视频链接
                    if href.startswith('//'):
                        full_url = 'https:' + href
                    elif href.startswith('/'):
                        full_url = 'https://www.bilibili.com' + href
                    else:
                        full_url = href
                        
                    # 提取BV号
                    if 'BV' in full_url:
                        bv_start = full_url.find('BV')
                        bv_end = full_url.find('?', bv_start)
                        if bv_end == -1:
                            bv_end = full_url.find('#', bv_start)
                        if bv_end == -1:
                            bv_end = len(full_url)
                        
                        bv_id = full_url[bv_start:bv_end]
                        clean_url = f"https://www.bilibili.com/video/{bv_id}"
                        bilibili_links.append(clean_url)
            
            # 去重并返回随机一个链接
            if bilibili_links:
                unique_links = list(set(bilibili_links))
                selected_link = random.choice(unique_links)
                print(f"找到 {province_name} 相关视频: {selected_link}")
                return selected_link
        
        print(f"未找到 {province_name} 的相关B站视频")
        return ""
        
    except Exception as e:
        print(f"搜索 {province_name} B站视频时出错: {e}")
        return ""

def search_images(province_name, count=3):
    """
    搜索省份相关图片链接
    """
    try:
        # 使用百度图片搜索
        search_url = "https://image.baidu.com/search/acjson"
        headers = get_random_headers()
        
        # 构造不同的搜索关键词组合
        keywords = [
            f"{province_name} 风景",
            f"{province_name} 旅游",
            f"{province_name} 景点",
            f"{province_name} 名胜"
        ]
        
        # 随机选择一个关键词
        keyword = random.choice(keywords)
        
        params = {
            'tn': 'resultjson_com',
            'ipn': 'rj',
            'ct': 201326592,
            'is': '',
            'fp': 'result',
            'queryWord': keyword,
            'cl': 2,
            'lm': -1,
            'ie': 'utf-8',
            'oe': 'utf-8',
            'adpicid': '',
            'st': -1,
            'z': '',
            'ic': 0,
            'hd': '',
            'latest': '',
            'copyright': '',
            'word': keyword,
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': 0,
            'istype': 2,
            'qc': '',
            'nc': 1,
            'fr': '',
            'expermode': '',
            'force': '',
            'pn': random.randint(1, 30),  # 随机页码
            'rn': count,  # 返回图片数量
            'gsm': '',
            '1603434983045': ''
        }
        
        response = requests.get(search_url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                image_urls = []
                
                if 'data' in data:
                    for item in data['data']:
                        if 'thumbURL' in item and item['thumbURL']:
                            image_urls.append(item['thumbURL'])
                
                if image_urls:
                    print(f"找到 {len(image_urls)} 张 {province_name} 相关图片")
                    return image_urls
            except json.JSONDecodeError:
                pass
        
        print(f"未找到 {province_name} 的相关图片")
        return []
        
    except Exception as e:
        print(f"搜索 {province_name} 图片时出错: {e}")
        return []

def crawl_top_attractions(province_name, count=3):
    """
    爬取省份的热门景点
    """
    try:
        # 搜索关键词
        search_query = f"{province_name} 热门景点"
        search_url = f"https://baike.baidu.com/item/{search_query}"
        headers = get_random_headers()
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        attractions = []
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找可能的景点列表
            list_items = soup.find_all('li')
            if not list_items:
                # 尝试查找段落中的景点信息
                paragraphs = soup.find_all('div', class_='para')
                for para in paragraphs:
                    text = para.get_text().strip()
                    # 简单的景点识别规则
                    if any(keyword in text for keyword in ['景区', '景点', '公园', '古镇', '名胜']):
                        # 提取景点名称（这里简化处理）
                        if len(text) < 50 and len(text) > 2:
                            attractions.append({
                                'name': text,
                                'description': f"{province_name}的著名景点"
                            })
                            if len(attractions) >= count:
                                break
            
            # 如果还是没有找到，使用预定义的景点名称
            if not attractions:
                common_attractions = [
                    f"{province_name}著名景点1",
                    f"{province_name}著名景点2", 
                    f"{province_name}著名景点3"
                ]
                
                for attr in common_attractions:
                    attractions.append({
                        'name': attr,
                        'description': f"{province_name}的著名景点，具有丰富的文化和自然价值"
                    })
            
            print(f"找到 {province_name} 的 {len(attractions)} 个景点")
            return attractions[:count]
        
        # 如果请求失败，返回预定义的景点
        return [
            {
                'name': f"{province_name}景点1",
                'description': f"{province_name}的著名景点"
            },
            {
                'name': f"{province_name}景点2", 
                'description': f"{province_name}的著名景点"
            },
            {
                'name': f"{province_name}景点3",
                'description': f"{province_name}的著名景点"
            }
        ]
        
    except Exception as e:
        print(f"爬取 {province_name} 景点时出错: {e}")
        # 返回预定义的景点
        return [
            {
                'name': f"{province_name}景点1",
                'description': f"{province_name}的著名景点"
            },
            {
                'name': f"{province_name}景点2", 
                'description': f"{province_name}的著名景点"
            },
            {
                'name': f"{province_name}景点3",
                'description': f"{province_name}的著名景点"
            }
        ]

def generate_province_data():
    """
    生成省份和景点数据
    """
    all_data = []
    
    print("开始生成省份和景点数据...")
    
    for i, province in enumerate(PROVINCES):
        print(f"正在处理 ({i+1}/{len(PROVINCES)}): {province}")
        
        # 获取省份信息
        province_description = crawl_province_info(province)
        
        # 获取省份相关视频链接
        province_video = search_bilibili_videos(province, "旅游")
        
        # 获取省份相关图片链接
        province_images = search_images(province, 1)
        province_image = province_images[0] if province_images else ""
        
        # 添加省份介绍作为第一个"景点"
        province_info = {
            "name": f"{province}简介",
            "province": province,
            "description": province_description,
            "image_url": province_image,
            "video_url": province_video,
            "address": province
        }
        
        all_data.append(province_info)
        
        # 获取该省份的热门景点
        attractions = crawl_top_attractions(province, 3)
        
        # 为每个景点获取独立的视频和图片
        for j, attraction in enumerate(attractions):
            # 为每个景点搜索不同的视频
            attraction_video = search_bilibili_videos(attraction['name'])
            
            # 为每个景点搜索不同的图片
            attraction_images = search_images(attraction['name'], 1)
            attraction_image = attraction_images[0] if attraction_images else ""
            
            attraction_info = {
                "name": attraction['name'],
                "province": province,
                "description": attraction['description'],
                "image_url": attraction_image,
                "video_url": attraction_video,
                "address": f"{province} {attraction['name']}"
            }
            
            all_data.append(attraction_info)
            print(f"  已添加景点: {attraction['name']}")
        
        # 添加延时，避免请求过于频繁
        time.sleep(2)
    
    return all_data

def save_to_json(data, filename):
    """
    将数据保存为JSON格式文件
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已保存到 {filename} 文件中")

def main():
    """
    主函数
    """
    print("高级省份和景点信息爬虫工具")
    print("=" * 50)
    
    # 生成数据
    all_data = generate_province_data()
    
    # 保存为JSON文件
    save_to_json(all_data, 'advanced_provinces_attractions.json')
    
    print("=" * 50)
    print(f"所有数据处理完成！共处理 {len(all_data)} 条记录")
    print("数据已保存到 advanced_provinces_attractions.json 文件中")

if __name__ == "__main__":
    main()