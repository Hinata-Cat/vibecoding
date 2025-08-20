"""
合并的数据导入脚本
此脚本整合了init_data.py、import_jiangxi_data.py和import_scenic_spots.py的功能
用于一次性导入所有示例数据到数据库中
"""

import json
from app import create_app
from models import Province, Attraction

def import_init_data():
    """
    导入初始数据（来自init_data.py）
    """
    app = create_app()
    
    with app.app_context():
        # 初始景点数据
        attractions_data = [
            {
                "name": "故宫博物院",
                "province": "北京市",
                "description": "明清两代的皇家宫殿，世界上现存规模最大、保存最完整的木质结构古建筑之一",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Beijing_-_Forbidden_City_-_Courtyard_-_P1060396.JPG/800px-Beijing_-_Forbidden_City_-_Courtyard_-_P1060396.JPG",
                "video_url": "https://www.bilibili.com/video/BV1Vs411W7PT",
                "address": "北京市东城区景山前街4号"
            },
            {
                "name": "天坛公园",
                "province": "北京市",
                "description": "明清两朝皇帝祭天的场所，中国现存最大的古代祭祀性建筑群",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Temple_of_Heaven_Park_in_spring.jpg/800px-Temple_of_Heaven_Park_in_spring.jpg",
                "video_url": "https://www.bilibili.com/video/BV1Gx411d7w7",
                "address": "北京市东城区天坛路甲1号"
            },
            {
                "name": "颐和园",
                "province": "北京市",
                "description": "中国清朝时期皇家园林，以昆明湖、万寿山为基础，汲取江南园林的设计手法而建成",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Summer_Palace_in_Beijing_13.jpg/800px-Summer_Palace_in_Beijing_13.jpg",
                "video_url": "https://www.bilibili.com/video/BV1bx411P7sW",
                "address": "北京市海淀区新建宫门路19号"
            },
            {
                "name": "西湖",
                "province": "浙江省",
                "description": "中国著名的旅游胜地，以'西湖十景'闻名于世",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/West_Lake_in_Hangzhou_11.jpg/800px-West_Lake_in_Hangzhou_11.jpg",
                "video_url": "https://www.bilibili.com/video/BV1yt41137Pq",
                "address": "浙江省杭州市西湖区"
            },
            {
                "name": "黄山",
                "province": "安徽省",
                "description": "以奇松、怪石、云海、温泉'四绝'著称于世",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Mountain_View_at_Huangshan_01.jpg/800px-Mountain_View_at_Huangshan_01.jpg",
                "video_url": "https://www.bilibili.com/video/BV1Mt41137Pq",
                "address": "安徽省黄山市"
            }
        ]
        
        imported_count = 0
        for attraction_data in attractions_data:
            # 查找或创建省份
            province = Province.objects(name=attraction_data["province"]).first()
            if not province:
                province = Province(name=attraction_data["province"], description=f"{attraction_data['province']}是中国的一个省份")
                province.save()
                print(f"已创建省份: {province.name}")
            
            # 检查景点是否已存在
            existing_attraction = Attraction.objects(
                name=attraction_data["name"],
                province=province
            ).first()
            
            if not existing_attraction:
                # 创建新景点
                attraction = Attraction(
                    name=attraction_data["name"],
                    province=province,
                    description=attraction_data["description"],
                    image_url=attraction_data["image_url"],
                    video_url=attraction_data["video_url"],
                    address=attraction_data["address"]
                )
                attraction.save()
                print(f"已导入景点: {attraction.name}")
                imported_count += 1
            else:
                print(f"景点已存在，跳过: {attraction_data['name']}")
        
        print(f"初始数据导入完成，共导入 {imported_count} 个景点")

def import_jiangxi_data():
    """
    导入江西省景点数据（来自import_jiangxi_data.py）
    """
    app = create_app()
    
    with app.app_context():
        # 读取JSON文件
        try:
            with open('testdata.json', 'r', encoding='utf-8') as f:
                attractions_data = json.load(f)
        except FileNotFoundError:
            print("错误: 找不到 testdata.json 文件")
            return
        except json.JSONDecodeError:
            print("错误: testdata.json 文件格式不正确")
            return
        
        # 查找或创建江西省
        province = Province.objects(name="江西省").first()
        if not province:
            province = Province(name="江西省", description="华东地区省份，革命老区")
            province.save()
            print(f"已创建省份: {province.name}")
        else:
            print(f"省份已存在: {province.name}")
        
        # 导入江西省景点数据
        imported_count = 0
        for attraction_data in attractions_data:
            if attraction_data.get("province") == "江西省":
                # 检查景点是否已存在
                existing_attraction = Attraction.objects(
                    name=attraction_data["name"],
                    province=province
                ).first()
                
                if not existing_attraction:
                    # 创建新景点
                    attraction = Attraction(
                        name=attraction_data["name"],
                        province=province,
                        description=attraction_data["description"],
                        image_url=attraction_data["image_url"],
                        video_url=attraction_data["video_url"],
                        address=attraction_data["address"]
                    )
                    attraction.save()
                    print(f"已导入景点: {attraction.name}")
                    imported_count += 1
                else:
                    print(f"景点已存在，跳过: {attraction_data['name']}")
        
        print(f"江西省景点数据导入完成，共导入 {imported_count} 个景点")

def import_scenic_spots_data():
    """
    导入风景名胜数据（来自import_scenic_spots.py）
    """
    app = create_app()
    
    with app.app_context():
        # 读取风景名胜JSON文件
        try:
            with open('scenic_spots.json', 'r', encoding='utf-8') as f:
                scenic_spots_data = json.load(f)
        except FileNotFoundError:
            print("错误: 找不到 scenic_spots.json 文件")
            return
        except json.JSONDecodeError:
            print("错误: scenic_spots.json 文件格式不正确")
            return
        
        print(f"开始导入 {len(scenic_spots_data)} 个景点信息...")
        
        imported_count = 0
        updated_count = 0
        
        for spot_data in scenic_spots_data:
            try:
                # 获取或创建省份
                province_name = spot_data['province']
                province = Province.objects(name=province_name).first()
                
                if not province:
                    # 如果省份不存在，则创建一个新省份
                    province = Province(name=province_name, description=f"{province_name}是中国的一个省份")
                    province.save()
                    print(f"已创建新省份: {province_name}")
                
                # 检查景点是否已存在
                existing_attraction = Attraction.objects(
                    name=spot_data['name'],
                    province=province
                ).first()
                
                if existing_attraction:
                    # 更新已存在的景点信息
                    existing_attraction.description = spot_data['description']
                    existing_attraction.image_url = spot_data['image_url']
                    existing_attraction.video_url = spot_data['video_url']
                    existing_attraction.address = spot_data['address']
                    existing_attraction.save()
                    updated_count += 1
                    print(f"已更新景点信息: {spot_data['name']}")
                else:
                    # 创建新的景点记录
                    attraction = Attraction(
                        name=spot_data['name'],
                        province=province,
                        description=spot_data['description'],
                        image_url=spot_data['image_url'],
                        video_url=spot_data['video_url'],
                        address=spot_data['address']
                    )
                    attraction.save()
                    imported_count += 1
                    print(f"已导入新景点: {spot_data['name']}")
                    
            except Exception as e:
                print(f"导入 {spot_data.get('name', '未知景点')} 时出错: {e}")
        
        print(f"风景名胜数据导入完成，新增 {imported_count} 个景点，更新 {updated_count} 个景点")

def main():
    """
    主函数 - 执行所有数据导入操作
    """
    print("数据导入工具")
    print("=" * 50)
    
    print("\n1. 导入初始数据...")
    import_init_data()
    
    print("\n2. 导入江西省景点数据...")
    import_jiangxi_data()
    
    print("\n3. 导入风景名胜数据...")
    import_scenic_spots_data()
    
    print("\n" + "=" * 50)
    print("所有数据导入完成!")

if __name__ == "__main__":
    main()