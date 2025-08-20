"""
将风景名胜数据导入到数据库的脚本
此脚本将scenic_spots.json中的数据导入到MongoDB数据库中
"""

import json
from app import create_app
from models import Province, Attraction

def import_scenic_spots():
    """
    将风景名胜数据导入到数据库中
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
        error_count = 0
        
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
                error_count += 1
                print(f"导入 {spot_data.get('name', '未知景点')} 时出错: {e}")
        
        print("=" * 40)
        print(f"导入完成!")
        print(f"新增景点: {imported_count} 个")
        print(f"更新景点: {updated_count} 个")
        print(f"错误数量: {error_count} 个")

def main():
    """
    主函数
    """
    print("风景名胜数据导入工具")
    print("=" * 40)
    
    import_scenic_spots()

if __name__ == "__main__":
    main()