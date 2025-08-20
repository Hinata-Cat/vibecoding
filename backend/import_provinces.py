"""
导入省份信息到数据库的脚本
此脚本将provinces_info.json中的省份信息导入到MongoDB数据库中
"""

import json
from app import create_app
from models import Province

def import_provinces_data():
    """
    将省份信息导入到数据库中
    """
    app = create_app()
    
    with app.app_context():
        # 读取省份信息JSON文件
        try:
            with open('provinces_info.json', 'r', encoding='utf-8') as f:
                provinces_data = json.load(f)
        except FileNotFoundError:
            print("错误: 找不到 provinces_info.json 文件")
            return
        except json.JSONDecodeError:
            print("错误: provinces_info.json 文件格式不正确")
            return
        
        print(f"开始导入 {len(provinces_data)} 个省份信息...")
        
        imported_count = 0
        updated_count = 0
        error_count = 0
        
        for province_data in provinces_data:
            try:
                province_name = province_data['province']
                
                # 查找是否已存在该省份
                existing_province = Province.objects(name=province_name).first()
                
                if existing_province:
                    # 更新已存在的省份信息
                    existing_province.description = province_data['description']
                    existing_province.save()
                    updated_count += 1
                    print(f"已更新省份信息: {province_name}")
                else:
                    # 创建新的省份记录
                    province = Province(
                        name=province_name,
                        description=province_data['description']
                    )
                    province.save()
                    imported_count += 1
                    print(f"已导入新省份: {province_name}")
                    
            except Exception as e:
                error_count += 1
                print(f"导入 {province_data.get('province', '未知省份')} 时出错: {e}")
        
        print("=" * 40)
        print(f"导入完成!")
        print(f"新增省份: {imported_count} 个")
        print(f"更新省份: {updated_count} 个")
        print(f"错误数量: {error_count} 个")

def main():
    """
    主函数
    """
    print("省份信息导入工具")
    print("=" * 40)
    
    import_provinces_data()

if __name__ == "__main__":
    main()