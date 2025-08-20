"""
初始化示例数据脚本
此脚本将添加中国省份和一些热门景点的示例数据
"""

from app import create_app
from models import Province, Attraction

def init_sample_data():
    app = create_app()
    
    with app.app_context():
        # 清空现有数据
        Province.objects.delete()
        Attraction.objects.delete()
        
        # 创建省份数据
        provinces_data = [
            {"name": "北京市", "description": "中国的首都，政治、文化中心"},
            {"name": "上海市", "description": "中国最大的城市，经济金融中心"},
            {"name": "广东省", "description": "中国南部沿海省份，经济发达"},
            {"name": "四川省", "description": "中国西南内陆省份，以美食和自然风光闻名"},
            {"name": "浙江省", "description": "中国东南沿海省份，经济活跃，风景秀丽"},
        ]
        
        provinces = []
        for prov_data in provinces_data:
            province = Province(**prov_data)
            province.save()
            provinces.append(province)
            print(f"已创建省份: {province.name}")
        
        # 创建景点数据
        attractions_data = [
            {
                "name": "故宫博物院",
                "province": provinces[0],  # 北京市
                "description": "明清两代的皇家宫殿，世界上现存规模最大、保存最完整的木质结构古建筑之一",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Forbidden_City_Beijing_July_2008_01.jpg/800px-Forbidden_City_Beijing_July_2008_01.jpg",
                "video_url": "https://www.bilibili.com/video/BV1Vs411W7PT",
                "address": "北京市东城区景山前街4号"
            },
            {
                "name": "天坛公园",
                "province": provinces[0],  # 北京市
                "description": "明清两朝皇帝祭天的场所，中国现存最大的古代祭祀性建筑群",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Temple_of_Heaven_Park_in_autumn.jpg/800px-Temple_of_Heaven_Park_in_autumn.jpg",
                "video_url": "https://www.bilibili.com/video/BV1Gx411d7w7",
                "address": "北京市东城区天坛路甲1号"
            },
            {
                "name": "外滩",
                "province": provinces[1],  # 上海市
                "description": "上海的标志性景观，拥有众多历史建筑和现代摩天大楼",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Shanghai_-_The_Bund_edit.jpg/800px-Shanghai_-_The_Bund_edit.jpg",
                "video_url": "https://www.bilibili.com/video/BV1yW411x7Eb",
                "address": "上海市黄浦区中山东一路"
            },
            {
                "name": "东方明珠广播电视塔",
                "province": provinces[1],  # 上海市
                "description": "上海的标志性建筑之一，塔高468米",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Oriental_Pearl_Tower_in_Pudong_from_the_Bund_in_Shanghai_2017.jpg/400px-Oriental_Pearl_Tower_in_Pudong_from_the_Bund_in_Shanghai_2017.jpg",
                "video_url": "https://www.bilibili.com/video/BV1xs411B7qh",
                "address": "上海市浦东新区陆家嘴世纪大道1号"
            },
            {
                "name": "大熊猫繁育研究基地",
                "province": provinces[3],  # 四川省
                "description": "致力于大熊猫保护和研究的基地，可近距离观察大熊猫",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Giant_Panda_-_Chengdu_Giant_Panda_Breeding_Research_Station_%289559533718%29.jpg/800px-Giant_Panda_-_Chengdu_Giant_Panda_Breeding_Research_Station_%289559533718%29.jpg",
                "video_url": "https://www.bilibili.com/video/BV1GJ411W7IE",
                "address": "四川省成都市成华区熊猫大道1375号"
            }
        ]
        
        for attr_data in attractions_data:
            attraction = Attraction(**attr_data)
            attraction.save()
            print(f"已创建景点: {attraction.name}")
        
        print("示例数据初始化完成!")

if __name__ == "__main__":
    init_sample_data()