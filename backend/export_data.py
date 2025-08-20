"""
导出数据库数据到JSON文件的脚本
此脚本将导出所有省份和景点数据到JSON文件中，用于备份或迁移
"""

import json
from app import create_app
from models import Province, Attraction

def export_data():
    """导出所有省份和景点数据到JSON文件"""
    app = create_app()
    
    with app.app_context():
        # 导出省份数据
        provinces = Province.objects.all()
        provinces_data = []
        for province in provinces:
            provinces_data.append({
                'id': str(province.id),
                'name': province.name,
                'description': province.description,
                'created_at': province.created_at.isoformat() if province.created_at else None,
                'updated_at': province.updated_at.isoformat() if province.updated_at else None
            })
        
        # 导出景点数据
        attractions = Attraction.objects.all()
        attractions_data = []
        for attraction in attractions:
            attractions_data.append({
                'id': str(attraction.id),
                'name': attraction.name,
                'province_id': str(attraction.province.id) if attraction.province else None,
                'province_name': attraction.province.name if attraction.province else None,
                'description': attraction.description,
                'image_url': attraction.image_url,
                'video_url': attraction.video_url,
                'address': attraction.address,
                'created_at': attraction.created_at.isoformat() if attraction.created_at else None,
                'updated_at': attraction.updated_at.isoformat() if attraction.updated_at else None
            })
        
        # 保存到JSON文件
        export_data = {
            'provinces': provinces_data,
            'attractions': attractions_data
        }
        
        with open('exported_data.json', 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"导出完成!")
        print(f"导出省份数量: {len(provinces_data)}")
        print(f"导出景点数量: {len(attractions_data)}")
        print("数据已保存到 exported_data.json 文件中")

def main():
    """主函数"""
    print("数据库导出工具")
    print("=" * 30)
    export_data()

if __name__ == "__main__":
    main()