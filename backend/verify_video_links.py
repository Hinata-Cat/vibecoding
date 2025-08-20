"""
验证数据库中视频链接是否已更新为新的B站链接的脚本
"""

import json
from app import create_app
from models import Province, Attraction

def verify_video_links():
    """
    验证数据库中的视频链接
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
        
        # 创建一个字典以便快速查找
        video_dict = {item["attraction"]: item["video_url"] for item in bilibili_data if item["video_url"]}
        
        print("验证数据库中的视频链接...")
        print("=" * 50)
        
        # 获取所有景点
        attractions = Attraction.objects()
        
        verified_count = 0
        mismatch_count = 0
        missing_count = 0
        
        for attraction in attractions:
            attraction_name = attraction.name
            current_video_url = attraction.video_url
            
            if attraction_name in video_dict:
                expected_video_url = video_dict[attraction_name]
                
                if current_video_url == expected_video_url:
                    print(f"✓ {attraction_name}: 视频链接正确")
                    verified_count += 1
                else:
                    print(f"✗ {attraction_name}: 视频链接不匹配")
                    print(f"  数据库中的链接: {current_video_url}")
                    print(f"  应该是: {expected_video_url}")
                    mismatch_count += 1
            else:
                if current_video_url and "bilibili.com" in current_video_url:
                    print(f"? {attraction_name}: 使用了B站链接，但未在爬取结果中找到")
                    verified_count += 1
                elif not current_video_url:
                    print(f"- {attraction_name}: 没有视频链接")
                    missing_count += 1
                else:
                    print(f"? {attraction_name}: 使用了非B站链接")
                    missing_count += 1
        
        print("\n" + "=" * 50)
        print("验证结果:")
        print(f"  正确链接: {verified_count} 个")
        print(f"  错误链接: {mismatch_count} 个")
        print(f"  缺失链接: {missing_count} 个")
        print(f"  总计检查: {attractions.count()} 个景点")
        
        if mismatch_count == 0:
            print("\n恭喜: 所有视频链接都已正确更新!")
        else:
            print(f"\n警告: 发现 {mismatch_count} 个链接不匹配，请检查数据库!")

def main():
    """
    主函数
    """
    print("视频链接验证工具")
    print("=" * 50)
    
    verify_video_links()

if __name__ == "__main__":
    main()