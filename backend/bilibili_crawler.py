"""
使用bilibili-api-python库的B站视频爬虫
此脚本可以正确爬取与景点相关的B站视频链接，避免爬取到无关内容
"""

import asyncio
import json
import time
import random
from bilibili_api import search, sync
import requests

# 景点数据
ATTRACTIONS = [
    # 北京市
    {"name": "故宫博物院", "province": "北京市"},
    {"name": "天坛公园", "province": "北京市"},
    {"name": "颐和园", "province": "北京市"},
    
    # 上海市
    {"name": "外滩", "province": "上海市"},
    {"name": "东方明珠塔", "province": "上海市"},
    {"name": "豫园", "province": "上海市"},
    
    # 天津市
    {"name": "天津之眼", "province": "天津市"},
    {"name": "五大道", "province": "天津市"},
    {"name": "古文化街", "province": "天津市"},
    
    # 重庆市
    {"name": "洪崖洞", "province": "重庆市"},
    {"name": "磁器口古镇", "province": "重庆市"},
    {"name": "武隆喀斯特", "province": "重庆市"},
    
    # 河北省
    {"name": "承德避暑山庄", "province": "河北省"},
    {"name": "北戴河", "province": "河北省"},
    {"name": "白洋淀", "province": "河北省"},
    
    # 山西省
    {"name": "五台山", "province": "山西省"},
    {"name": "平遥古城", "province": "山西省"},
    {"name": "云冈石窟", "province": "山西省"},
    
    # 辽宁省
    {"name": "沈阳故宫", "province": "辽宁省"},
    {"name": "大连海滨", "province": "辽宁省"},
    {"name": "金石滩", "province": "辽宁省"},
    
    # 吉林省
    {"name": "长白山天池", "province": "吉林省"},
    {"name": "伪满皇宫博物院", "province": "吉林省"},
    {"name": "净月潭", "province": "吉林省"},
    
    # 黑龙江省
    {"name": "哈尔滨冰雪大世界", "province": "黑龙江省"},
    {"name": "五大连池", "province": "黑龙江省"},
    {"name": "镜泊湖", "province": "黑龙江省"},
    
    # 江苏省
    {"name": "苏州园林", "province": "江苏省"},
    {"name": "南京中山陵", "province": "江苏省"},
    {"name": "瘦西湖", "province": "江苏省"},
    
    # 浙江省
    {"name": "西湖", "province": "浙江省"},
    {"name": "普陀山", "province": "浙江省"},
    {"name": "乌镇", "province": "浙江省"},
    
    # 安徽省
    {"name": "黄山", "province": "安徽省"},
    {"name": "九华山", "province": "安徽省"},
    {"name": "宏村", "province": "安徽省"},
    
    # 江西省
    {"name": "滕王阁旅游区", "province": "江西省"},
    {"name": "庐山风景名胜区", "province": "江西省"},
    {"name": "三清山风景名胜区", "province": "江西省"}
]

async def search_bilibili_video(attraction):
    """
    搜索与景点相关的B站视频
    """
    attraction_name = attraction["name"]
    province = attraction["province"]
    
    # 构造搜索关键词
    keywords = [
        f"{attraction_name} 旅游",
        f"{attraction_name} 介绍",
        f"{attraction_name} 宣传片",
        f"{province} {attraction_name}",
        f"{attraction_name} 4K"
    ]
    
    # 添加请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.bilibili.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # 尝试不同的关键词
    for keyword in keywords:
        try:
            print(f"正在搜索: {keyword}")
            
            # 使用B站搜索API
            result = await search.search_by_type(
                keyword=keyword,
                search_type=search.SearchObjectType.VIDEO,
                page=1,
                page_size=5  # 获取前5个结果
            )
            
            # 检查是否有搜索结果
            if result.get('result') and len(result['result']) > 0:
                # 遍历搜索结果，找到最相关的视频
                for video in result['result']:
                    title = video.get('title', '').lower()
                    # 检查视频标题是否包含景点名称
                    if attraction_name in title or \
                       (attraction_name == "天津之眼" and "天津" in title and "摩天轮" in title) or \
                       (attraction_name == "五大道" and "天津" in title and "五大道" in title) or \
                       (attraction_name == "磁器口古镇" and "磁器口" in title) or \
                       (attraction_name == "洪崖洞" and "洪崖洞" in title):
                        
                        # 构造完整的B站视频链接
                        bvid = video.get('bvid')
                        if bvid:
                            video_url = f"https://www.bilibili.com/video/{bvid}"
                            print(f"找到相关视频: {video_url}")
                            return {
                                "attraction": attraction_name,
                                "province": province,
                                "keyword": keyword,
                                "video_url": video_url,
                                "title": video.get('title', ''),
                                "play": video.get('play', 0),
                                "duration": video.get('duration', '')
                            }
            
            # 添加延时，避免触发风控
            await asyncio.sleep(random.uniform(1, 2))
            
        except Exception as e:
            print(f"搜索 {keyword} 时出错: {e}")
            # 如果遇到API错误，等待更长时间
            await asyncio.sleep(random.uniform(3, 5))
            continue
    
    # 如果没有找到相关视频，返回默认值
    print(f"未找到 {attraction_name} 的相关视频")
    return {
        "attraction": attraction_name,
        "province": province,
        "keyword": "",
        "video_url": "",  # 空链接表示未找到相关视频
        "title": "",
        "play": 0,
        "duration": ""
    }

async def crawl_all_videos():
    """
    爬取所有景点的B站视频链接
    """
    results = []
    
    print("开始爬取B站视频链接...")
    print("=" * 50)
    
    # 逐个处理每个景点
    for i, attraction in enumerate(ATTRACTIONS):
        print(f"\n处理进度: {i+1}/{len(ATTRACTIONS)} - {attraction['name']}")
        
        # 搜索相关视频
        result = await search_bilibili_video(attraction)
        results.append(result)
        
        # 显示结果
        if result["video_url"]:
            print(f"✓ 成功找到视频: {result['title']}")
        else:
            print(f"✗ 未找到相关视频")
        
        # 添加随机延时，模拟人工操作
        await asyncio.sleep(random.uniform(1, 3))
    
    return results

def save_results_to_json(results, filename):
    """
    将结果保存到JSON文件
    """
    # 过滤掉未找到视频的记录
    valid_results = [r for r in results if r["video_url"]]
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(valid_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n已保存 {len(valid_results)} 个视频链接到 {filename}")

def update_json_files_with_videos(video_data):
    """
    使用爬取到的视频链接更新JSON数据文件
    """
    # 创建一个字典，便于查找
    video_dict = {item["attraction"]: item["video_url"] for item in video_data if item["video_url"]}
    
    # 更新scenic_spots.json文件
    try:
        with open('scenic_spots.json', 'r', encoding='utf-8') as f:
            scenic_spots = json.load(f)
        
        updated_count = 0
        for spot in scenic_spots:
            attraction_name = spot.get("name")
            if attraction_name in video_dict and video_dict[attraction_name]:
                old_url = spot.get("video_url", "")
                new_url = video_dict[attraction_name]
                if old_url != new_url:
                    spot["video_url"] = new_url
                    updated_count += 1
                    print(f"更新 {attraction_name} 的视频链接: {new_url}")
        
        # 保存更新后的数据
        with open('scenic_spots.json', 'w', encoding='utf-8') as f:
            json.dump(scenic_spots, f, ensure_ascii=False, indent=2)
        
        print(f"\n成功更新 scenic_spots.json 中 {updated_count} 个视频链接")
        
    except Exception as e:
        print(f"更新 scenic_spots.json 时出错: {e}")
    
    # 更新testdata.json文件
    try:
        with open('testdata.json', 'r', encoding='utf-8') as f:
            testdata = json.load(f)
        
        updated_count = 0
        for spot in testdata:
            attraction_name = spot.get("name")
            if attraction_name in video_dict and video_dict[attraction_name]:
                old_url = spot.get("video_url", "")
                new_url = video_dict[attraction_name]
                if old_url != new_url:
                    spot["video_url"] = new_url
                    updated_count += 1
                    print(f"更新 {attraction_name} 的视频链接: {new_url}")
        
        # 保存更新后的数据
        with open('testdata.json', 'w', encoding='utf-8') as f:
            json.dump(testdata, f, ensure_ascii=False, indent=2)
        
        print(f"成功更新 testdata.json 中 {updated_count} 个视频链接")
        
    except Exception as e:
        print(f"更新 testdata.json 时出错: {e}")

async def main():
    """
    主函数
    """
    print("B站景点视频爬虫")
    print("=" * 50)
    
    # 爬取视频链接
    results = await crawl_all_videos()
    
    # 保存爬取结果
    save_results_to_json(results, 'bilibili_video_results.json')
    
    # 使用爬取到的视频链接更新数据文件
    valid_videos = [r for r in results if r["video_url"]]
    update_json_files_with_videos(valid_videos)
    
    # 统计结果
    total_count = len(ATTRACTIONS)
    found_count = len(valid_videos)
    not_found_count = total_count - found_count
    
    print("\n" + "=" * 50)
    print("爬取完成!")
    print(f"总计处理: {total_count} 个景点")
    print(f"找到视频: {found_count} 个")
    print(f"未找到视频: {not_found_count} 个")
    print(f"成功率: {found_count/total_count*100:.1f}%")

if __name__ == "__main__":
    # 运行异步主函数
    sync(main())