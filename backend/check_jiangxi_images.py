"""
检查江西省景点图片情况的脚本
"""

from app import create_app
from models import Province, Attraction

def check_jiangxi_images():
    """检查江西省景点的图片情况"""
    app = create_app()
    
    with app.app_context():
        # 查找江西省
        province = Province.objects(name='江西省').first()
        if not province:
            print("未找到江西省")
            return
        
        # 获取江西省所有景点
        jiangxi_attractions = Attraction.objects(province=province)
        print(f"江西省共有 {jiangxi_attractions.count()} 个景点")
        
        # 统计没有图片的景点
        no_image_attractions = []
        for attraction in jiangxi_attractions:
            if not attraction.image_url:
                no_image_attractions.append(attraction)
        
        print(f"其中没有图片的景点有 {len(no_image_attractions)} 个")
        
        # 显示没有图片的景点列表
        if no_image_attractions:
            print("\n没有图片的景点列表:")
            for attraction in no_image_attractions:
                print(f"  - {attraction.name}")
        
        # 显示有图片的景点列表
        print("\n有图片的景点列表:")
        has_image_count = 0
        for attraction in jiangxi_attractions:
            if attraction.image_url:
                has_image_count += 1
                print(f"  - {attraction.name}: {attraction.image_url}")

if __name__ == "__main__":
    check_jiangxi_images()