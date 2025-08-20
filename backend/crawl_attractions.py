import requests
from bs4 import BeautifulSoup
import json
import time

# 省份及其ID映射（需根据你的数据库实际ID填写）
PROVINCES = {
    "北京市": "60a8a1c1b1a8d92b6c123456",
    "上海市": "60a8a1c1b1a8d92b6c123457",
    # ...其他省份...
}

def get_mfw_attractions(province, limit=3):
    """
    爬取马蜂窝省份景点榜单
    """
    url = f"https://www.mafengwo.cn/jd/{province}/gonglve.html"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    attractions = []
    for item in soup.select('.scenic-list .item')[:limit]:
        name = item.select_one('.title').get_text(strip=True)
        desc = item.select_one('.detail').get_text(strip=True) if item.select_one('.detail') else ""
        img = item.select_one('img')['data-original'] if item.select_one('img') else ""
        address = province
        # 这里只能爬到图片和简介，视频需后续补充
        attractions.append({
            "name": name,
            "province_id": PROVINCES[province],
            "description": desc,
            "image_url": img,
            "video_url": "",  # 后续补充
            "address": address
        })
    return attractions

def main():
    all_attractions = []
    for province in PROVINCES:
        print(f"正在爬取{province}...")
        try:
            # 省份拼音或ID需根据马蜂窝URL规则调整
            attractions = get_mfw_attractions(province)
            all_attractions.extend(attractions)
            time.sleep(2)  # 防止被封IP
        except Exception as e:
            print(f"{province} 爬取失败: {e}")
    # 保存到json
    with open("attractions_seed.json", "w", encoding="utf-8") as f:
        json.dump(all_attractions, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
