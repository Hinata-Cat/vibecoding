"""
导入B站视频数据到数据库的脚本
此脚本将bilibili_video_results.json中的数据导入到数据库中，替换原有的视频链接
"""

import json
from app import create_app
from models import Province, Attraction

def import_bilibili_data():
    """
    导入B站视频数据到数据库
    """
    app = create_app()
    
    with app.app_context():
        # 读取B站爬取结果
        try:
            with open('bilibili_video_results.json', 'r', encoding='utf-8') as f:
                bilibili_data = json.load(f)
        except FileNotFoundError:
            print("错误: 找不到 bilibili_video_results.json 文件")
            return
        except json.JSONDecodeError:
            print("错误: bilibili_video_results.json 文件格式不正确")
            return
        
        print(f"开始导入 {len(bilibili_data)} 个B站视频数据...")
        
        updated_count = 0
        not_found_count = 0
        
        # 创建一个字典以便快速查找
        video_dict = {item["attraction"]: item["video_url"] for item in bilibili_data}
        
        # 更新scenic_spots.json中的景点数据
        try:
            with open('scenic_spots.json', 'r', encoding='utf-8') as f:
                scenic_spots = json.load(f)
            
            for spot in scenic_spots:
                attraction_name = spot.get("name")
                if attraction_name in video_dict:
                    old_url = spot.get("video_url", "")
                    new_url = video_dict[attraction_name]
                    if old_url != new_url and new_url:  # 只有当新链接不为空且不同时才更新
                        spot["video_url"] = new_url
                        print(f"更新 {attraction_name} 的视频链接: {new_url}")
            
            # 保存更新后的数据
            with open('scenic_spots.json', 'w', encoding='utf-8') as f:
                json.dump(scenic_spots, f, ensure_ascii=False, indent=2)
            
            print(f"\n成功更新 scenic_spots.json 中的视频链接")
            
        except Exception as e:
            print(f"更新 scenic_spots.json 时出错: {e}")
        
        # 更新testdata.json中的景点数据
        try:
            with open('testdata.json', 'r', encoding='utf-8') as f:
                testdata = json.load(f)
            
            for spot in testdata:
                attraction_name = spot.get("name")
                if attraction_name in video_dict:
                    old_url = spot.get("video_url", "")
                    new_url = video_dict[attraction_name]
                    if old_url != new_url and new_url:  # 只有当新链接不为空且不同时才更新
                        spot["video_url"] = new_url
                        print(f"更新 {attraction_name} 的视频链接: {new_url}")
            
            # 保存更新后的数据
            with open('testdata.json', 'w', encoding='utf-8') as f:
                json.dump(testdata, f, ensure_ascii=False, indent=2)
            
            print(f"成功更新 testdata.json 中的视频链接")
            
        except Exception as e:
            print(f"更新 testdata.json 时出错: {e}")
        
        # 更新数据库中的景点数据
        for item in bilibili_data:
            attraction_name = item["attraction"]
            video_url = item["video_url"]
            
            if not video_url:
                continue
                
            # 查找数据库中的景点
            attraction = Attraction.objects(name=attraction_name).first()
            
            if attraction:
                # 更新视频链接
                old_url = attraction.video_url
                if old_url != video_url:
                    attraction.video_url = video_url
                    attraction.save()
                    updated_count += 1
                    print(f"数据库中已更新 {attraction_name} 的视频链接")
            else:
                not_found_count += 1
                print(f"数据库中未找到景点: {attraction_name}")
        
        print("\n" + "=" * 50)
        print("数据导入完成!")
        print(f"成功更新: {updated_count} 个景点的视频链接")
        print(f"未找到景点: {not_found_count} 个")
        print(f"总共处理: {len(bilibili_data)} 个视频链接")

def main():
    """
    主函数
    """
    print("B站视频数据导入工具")
    print("=" * 50)
    
    import_bilibili_data()

if __name__ == "__main__":
    main()