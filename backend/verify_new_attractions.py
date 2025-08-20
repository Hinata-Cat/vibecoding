"""
验证新爬取的景点数据脚本
此脚本用于验证刚刚爬取并导入数据库的景点数据
"""

from app import create_app
from models import Province, Attraction
import json

def verify_new_attractions():
    """
    验证新爬取的景点数据
    """
    app = create_app()
    
    with app.app_context():
        print("验证新爬取的景点数据...")
        print("=" * 50)
        
        # 读取爬取的数据文件
        try:
            with open('province_attractions_data.json', 'r', encoding='utf-8') as f:
                crawled_data = json.load(f)
        except FileNotFoundError:
            print("错误: 找不到 province_attractions_data.json 文件")
            return
        except json.JSONDecodeError:
            print("错误: province_attractions_data.json 文件格式不正确")
            return
        
        print(f"总共爬取了 {len(crawled_data)} 个景点")
        
        # 验证数据库中的数据
        verified_count = 0
        missing_count = 0
        mismatch_count = 0
        
        # 创建一个字典以便快速查找
        crawled_dict = {item["name"]: item for item in crawled_data}
        
        # 检查数据库中的所有景点
        attractions = Attraction.objects()
        print(f"\n数据库中共有 {attractions.count()} 个景点")
        
        for attraction in attractions:
            name = attraction.name
            
            if name in crawled_dict:
                crawled_item = crawled_dict[name]
                
                # 验证各项数据
                mismatches = []
                
                if attraction.description != crawled_item["description"]:
                    mismatches.append("描述不匹配")
                
                if attraction.image_url != crawled_item["image_url"]:
                    mismatches.append("图片链接不匹配")
                
                if attraction.video_url != crawled_item["video_url"]:
                    mismatches.append("视频链接不匹配")
                
                if attraction.address != crawled_item["address"]:
                    mismatches.append("地址不匹配")
                
                if mismatches:
                    print(f"✗ {name}: {', '.join(mismatches)}")
                    mismatch_count += 1
                else:
                    print(f"✓ {name}: 数据一致")
                    verified_count += 1
            else:
                # 这些是之前已存在的景点
                print(f"? {name}: 之前已存在的景点")
                missing_count += 1
        
        print("\n" + "=" * 50)
        print("验证结果:")
        print(f"  数据一致: {verified_count} 个")
        print(f"  数据不一致: {mismatch_count} 个")
        print(f"  之前已存在: {missing_count} 个")
        
        if mismatch_count == 0:
            print("\n恭喜: 所有新爬取的景点数据都已正确导入数据库!")
        else:
            print(f"\n警告: 发现 {mismatch_count} 个数据不一致，请检查数据库!")

def show_new_attractions():
    """
    显示新添加的景点信息
    """
    app = create_app()
    
    with app.app_context():
        print("新添加的景点信息:")
        print("=" * 50)
        
        # 读取爬取的数据文件
        try:
            with open('province_attractions_data.json', 'r', encoding='utf-8') as f:
                crawled_data = json.load(f)
        except FileNotFoundError:
            print("错误: 找不到 province_attractions_data.json 文件")
            return
        except json.JSONDecodeError:
            print("错误: province_attractions_data.json 文件格式不正确")
            return
        
        # 显示每个新景点的信息
        for i, attraction in enumerate(crawled_data, 1):
            print(f"{i}. {attraction['name']} ({attraction['province']})")
            print(f"   描述: {attraction['description']}")
            print(f"   图片链接: {attraction['image_url']}")
            print(f"   视频链接: {attraction['video_url']}")
            print(f"   地址: {attraction['address']}")
            print()

def main():
    """
    主函数
    """
    print("新景点数据验证工具")
    print("=" * 50)
    
    # 显示新添加的景点信息
    show_new_attractions()
    
    # 验证数据
    verify_new_attractions()

if __name__ == "__main__":
    main()