"""
从JSON文件导入数据到数据库的脚本
此脚本将从exported_data.json文件中导入省份和景点数据到数据库
"""

import json
from app import create_app
from models import Province, Attraction

def import_data():
    """从JSON文件导入省份和景点数据到数据库"""
    app = create_app()
    
    with app.app_context():
        # 清空现有数据
        print("清空现有数据...")
        Province.objects.delete()
        Attraction.objects.delete()
        
        # 读取导出的数据
        try:
            with open('exported_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("错误: 找不到 exported_data.json 文件")
            return
        except json.JSONDecodeError:
            print("错误: exported_data.json 文件格式不正确")
            return
        
        # 导入省份数据
        provinces_data = data.get('provinces', [])
        province_id_map = {}  # 用于映射旧ID到新ID
        
        print(f"导入 {len(provinces_data)} 个省份...")
        for province_data in provinces_data:
            # 创建新的省份对象
            province = Province(
                name=province_data['name'],
                description=province_data['description']
            )
            province.save()
            
            # 保存ID映射关系
            old_id = province_data['id']
            province_id_map[old_id] = province.id
            
            print(f"  ✓ 已导入省份: {province.name}")
        
        # 导入景点数据
        attractions_data = data.get('attractions', [])
        print(f"导入 {len(attractions_data)} 个景点...")
        
        for attraction_data in attractions_data:
            # 查找关联的省份
            province = None
            if attraction_data['province_id'] in province_id_map:
                province_id = province_id_map[attraction_data['province_id']]
                province = Province.objects(id=province_id).first()
            elif attraction_data['province_name']:
                province = Province.objects(name=attraction_data['province_name']).first()
            
            if not province:
                print(f"  ! 跳过景点 {attraction_data['name']}，未找到关联的省份")
                continue
            
            # 创建新的景点对象
            attraction = Attraction(
                name=attraction_data['name'],
                province=province,
                description=attraction_data['description'],
                image_url=attraction_data['image_url'],
                video_url=attraction_data['video_url'],
                address=attraction_data['address']
            )
            attraction.save()
            
            print(f"  ✓ 已导入景点: {attraction.name}")
        
        print(f"\n导入完成!")
        print(f"导入省份数量: {len(provinces_data)}")
        print(f"导入景点数量: {len(attractions_data)}")

def main():
    """主函数"""
    print("数据库导入工具")
    print("=" * 30)
    print("注意: 此操作将清空现有数据库中的所有数据!")
    confirm = input("是否继续? (输入 'yes' 确认): ")
    
    if confirm.lower() == 'yes':
        import_data()
    else:
        print("操作已取消")

if __name__ == "__main__":
    main()