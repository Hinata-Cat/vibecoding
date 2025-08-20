"""
导入江西省景点数据脚本
此脚本将testdata.json中江西省的景点数据导入到数据库中
"""

import json
from app import create_app
from models import Province, Attraction

def import_jiangxi_data():
    app = create_app()
    
    with app.app_context():
        # 读取JSON文件
        with open('testdata.json', 'r', encoding='utf-8') as f:
            attractions_data = json.load(f)
        
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
        
        print(f"成功导入 {imported_count} 个江西省景点")

if __name__ == "__main__":
    import_jiangxi_data()