"""
生成中国所有省份介绍信息的脚本
此脚本使用预定义数据生成与testdata.json格式相同的省份介绍信息
"""

import json

# 中国省份列表
PROVINCES = [
    "北京市", "上海市", "天津市", "重庆市",
    "河北省", "山西省", "辽宁省", "吉林省", "黑龙江省",
    "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省",
    "河南省", "湖北省", "湖南省", "广东省", "海南省",
    "四川省", "贵州省", "云南省", "陕西省", "甘肃省",
    "青海省", "台湾省", "内蒙古自治区", "广西壮族自治区", 
    "西藏自治区", "宁夏回族自治区", "新疆维吾尔自治区", "香港特别行政区", "澳门特别行政区"
]

# 省份介绍数据
PROVINCE_DESCRIPTIONS = {
    "北京市": "中国的首都，政治、文化和国际交往中心，拥有故宫、天坛等众多历史文化遗产，是世界著名的旅游城市。",
    "上海市": "中国最大的城市和经济中心，被誉为'东方明珠'，以外滩、东方明珠塔等现代建筑和豫园等古典园林闻名于世。",
    "天津市": "中国北方重要的港口城市和工业基地，拥有丰富的历史文化遗产和独特的津门文化，以狗不理包子等特色美食著称。",
    "重庆市": "中国西南地区的工商业重镇和交通枢纽，以山城地貌、火锅美食和三峡工程闻名，是长江上游的重要城市。",
    "河北省": "华北地区的重要省份，环绕北京和天津，拥有承德避暑山庄、北戴河等著名景点，是连接东北和华北的交通要道。",
    "山西省": "中华文明的重要发源地之一，以煤炭资源丰富著称，拥有平遥古城、五台山等历史文化遗迹。",
    "辽宁省": "东北地区的经济大省，以重工业闻名，拥有沈阳故宫、大连海滨等丰富的旅游资源。",
    "吉林省": "东北地区的重要农业和工业基地，以长春电影制片厂、长白山天池等文化自然景观著称。",
    "黑龙江省": "中国最北端的省份，以冰雕艺术、五大连池火山地貌和大兴安岭森林资源闻名。",
    "江苏省": "华东地区的经济强省，以苏州园林、南京中山陵等历史文化景观和发达的水乡风光著称。",
    "浙江省": "中国东南沿海的经济强省，以杭州西湖、普陀山等自然人文景观和民营经济发达闻名。",
    "安徽省": "华东地区连接长三角与中西部的省份，以黄山、九华山等自然风光和徽派建筑文化著称。",
    "福建省": "中国东南沿海的省份，以厦门鼓浪屿、武夷山等自然人文景观和闽南文化闻名。",
    "江西省": "华东地区的革命老区，以庐山、井冈山等红色旅游资源和鄱阳湖自然风光著称。",
    "山东省": "孔孟之乡，中华文明的重要发源地之一，以泰山、曲阜三孔等历史文化遗迹闻名。",
    "河南省": "中华文明的重要发源地，人口大省，以少林寺、龙门石窟等历史文化遗迹著称。",
    "湖北省": "中部地区的交通枢纽，以武汉黄鹤楼、武当山等历史文化和自然景观闻名。",
    "湖南省": "中部地区的农业和工业大省，以张家界奇峰、岳阳楼等自然人文景观著称。",
    "广东省": "中国改革开放的前沿阵地，以广州、深圳等现代化城市和丰富的岭南文化闻名。",
    "海南省": "中国唯一的热带海岛省份，以三亚热带海滨风光和丰富的海洋旅游资源著称。",
    "四川省": "中国西南地区的文化大省，以成都大熊猫基地、九寨沟等自然风光和川菜文化闻名。",
    "贵州省": "中国西南地区的山区省份，以黄果树瀑布、荔波小七孔等自然景观和苗族侗族文化著称。",
    "云南省": "中国西南边陲的多民族省份，以丽江古城、大理洱海等自然人文景观和丰富的民族文化闻名。",
    "陕西省": "中华文明的重要发源地，以西安兵马俑、华山等历史文化遗产和丝绸之路起点闻名。",
    "甘肃省": "连接中原与西域的要道，以敦煌莫高窟、嘉峪关等丝绸之路文化遗产著称。",
    "青海省": "中国西北地区的高原省份，以青海湖、三江源等高原自然景观和藏族文化闻名。",
    "台湾省": "中国不可分割的一部分，以台北101大楼、日月潭等现代都市和自然风光闻名。",
    "内蒙古自治区": "中国面积最大的省级行政区，以呼伦贝尔大草原、成吉思汗陵等草原文化和历史遗迹著称。",
    "广西壮族自治区": "中国南部的多民族自治区，以桂林山水、北海银滩等自然风光和壮族文化闻名。",
    "西藏自治区": "中国西南边陲的少数民族自治区，以布达拉宫、珠穆朗玛峰等宗教文化和自然景观闻名。",
    "宁夏回族自治区": "中国西北地区的少数民族自治区，以银川西夏王陵、沙湖等历史文化和自然景观著称。",
    "新疆维吾尔自治区": "中国陆地面积最大的省级行政区，以天山天池、喀纳斯湖等自然风光和维吾尔族文化闻名。",
    "香港特别行政区": "中国的特别行政区，以维多利亚港、迪士尼乐园等现代都市景观和购物天堂闻名。",
    "澳门特别行政区": "中国的特别行政区，以大三巴牌坊、威尼斯人度假村等中西文化融合景观和博彩业闻名。"
}

# 省份相关B站视频链接
PROVINCE_VIDEOS = {
    "北京市": "https://www.bilibili.com/video/BV1Vs411W7PT",
    "上海市": "https://www.bilibili.com/video/BV1GJ411V7wk",
    "天津市": "https://www.bilibili.com/video/BV1YE411v7Gn",
    "重庆市": "https://www.bilibili.com/video/BV15E411x7QT",
    "河北省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "山西省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "辽宁省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "吉林省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "黑龙江省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "江苏省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "浙江省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "安徽省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "福建省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "江西省": "https://www.bilibili.com/video/BV1kx411Q7fN",
    "山东省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "河南省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "湖北省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "湖南省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "广东省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "海南省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "四川省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "贵州省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "云南省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "陕西省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "甘肃省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "青海省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "台湾省": "https://www.bilibili.com/video/BV1WE411o7zd",
    "内蒙古自治区": "https://www.bilibili.com/video/BV1WE411o7zd",
    "广西壮族自治区": "https://www.bilibili.com/video/BV1WE411o7zd",
    "西藏自治区": "https://www.bilibili.com/video/BV1WE411o7zd",
    "宁夏回族自治区": "https://www.bilibili.com/video/BV1WE411o7zd",
    "新疆维吾尔自治区": "https://www.bilibili.com/video/BV1WE411o7zd",
    "香港特别行政区": "https://www.bilibili.com/video/BV1WE411o7zd",
    "澳门特别行政区": "https://www.bilibili.com/video/BV1WE411o7zd"
}

# 省份相关图片链接
PROVINCE_IMAGES = {
    "北京市": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Beijing_city_view_%28Zhongnanhai%29.jpg/800px-Beijing_city_view_%28Zhongnanhai%29.jpg",
    "上海市": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Shanghai_Skyline_2019.jpg/800px-Shanghai_Skyline_2019.jpg",
    "天津市": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Tianjin_eye_in_night.jpg/800px-Tianjin_eye_in_night.jpg",
    "重庆市": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Chongqing_skyline_from_Jiangbei.jpg/800px-Chongqing_skyline_from_Jiangbei.jpg",
    "河北省": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Chengde_Summer_Palace_%281%29.jpg/800px-Chengde_Summer_Palace_%281%29.jpg",
    "山西省": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Taiyuan_satellite_map.jpg/800px-Taiyuan_satellite_map.jpg",
    "辽宁省": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Shenyang_downtown_skyline.jpg/800px-Shenyang_downtown_skyline.jpg",
    "吉林省": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Changbai_Mountain_Tianchi.jpg/800px-Changbai_Mountain_Tianchi.jpg",
    "黑龙江省": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Harbin_Ice_and_Snow_World.jpg/800px-Harbin_Ice_and_Snow_World.jpg",
    "江苏省": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Nanjing_skyline_from_Yangtze_river.jpg/800px-Nanjing_skyline_from_Yangtze_river.jpg",
    "浙江省": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/West_Lake_in_Hangzhou.jpg/800px-West_Lake_in_Hangzhou.jpg",
    "安徽省": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Yellow_Mountain_in_Anqing.jpg/800px-Yellow_Mountain_in_Anqing.jpg",
    "福建省": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Gulangyu_island_from_the_sea.jpg/800px-Gulangyu_island_from_the_sea.jpg",
    "江西省": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Poyang_Lake_in_Winter.jpg/800px-Poyang_Lake_in_Winter.jpg",
    "山东省": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Mount_Tai_skyline.jpg/800px-Mount_Tai_skyline.jpg",
    "河南省": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Shaolin_Temple_gate.jpg/800px-Shaolin_Temple_gate.jpg",
    "湖北省": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Yellow_Crane_Tower_in_Wuhan.jpg/800px-Yellow_Crane_Tower_in_Wuhan.jpg",
    "湖南省": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Zhangjiajie_national_forest_park.jpg/800px-Zhangjiajie_national_forest_park.jpg",
    "广东省": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Guangzhou_skyline_from_Pearl_River.jpg/800px-Guangzhou_skyline_from_Pearl_River.jpg",
    "海南省": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Sanya_beach_with_palms.jpg/800px-Sanya_beach_with_palms.jpg",
    "四川省": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Jiuzhaigou_Valley_scenery.jpg/800px-Jiuzhaigou_Valley_scenery.jpg",
    "贵州省": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Huangguoshu_Waterfall.jpg/800px-Huangguoshu_Waterfall.jpg",
    "云南省": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Kunming_Lake_in_the_Summer_Palace.jpg/800px-Kunming_Lake_in_the_Summer_Palace.jpg",
    "陕西省": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Terracotta_Army_Pit_1.jpg/800px-Terracotta_Army_Pit_1.jpg",
    "甘肃省": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Mogao_Caves_exterior.jpg/800px-Mogao_Caves_exterior.jpg",
    "青海省": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Qinghai_Lake_from_space.jpg/800px-Qinghai_Lake_from_space.jpg",
    "台湾省": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Taipei_101_skyline.jpg/800px-Taipei_101_skyline.jpg",
    "内蒙古自治区": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Hulunbuir_grassland.jpg/800px-Hulunbuir_grassland.jpg",
    "广西壮族自治区": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Li_River_scenery_near_Guilin.jpg/800px-Li_River_scenery_near_Guilin.jpg",
    "西藏自治区": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Potala_Palace_in_Lhasa.jpg/800px-Potala_Palace_in_Lhasa.jpg",
    "宁夏回族自治区": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Xixia_Tomb_complex.jpg/800px-Xixia_Tomb_complex.jpg",
    "新疆维吾尔自治区": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Tianchi_Lake_on_Tianshan.jpg/800px-Tianchi_Lake_on_Tianshan.jpg",
    "香港特别行政区": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Hong_Kong_Skyline_from_the_air.jpg/800px-Hong_Kong_Skyline_from_the_air.jpg",
    "澳门特别行政区": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Macau_skyline_from_Guia_Hill.jpg/800px-Macau_skyline_from_Guia_Hill.jpg"
}

def generate_province_data():
    """
    生成省份数据，格式与testdata.json类似
    """
    provinces_data = []
    
    print("开始生成省份介绍数据...")
    
    for i, province in enumerate(PROVINCES):
        print(f"正在处理 ({i+1}/{len(PROVINCES)}): {province}")
        
        # 获取省份信息
        description = PROVINCE_DESCRIPTIONS.get(province, f"{province}是中国的一个省份，拥有丰富的历史文化和自然资源。")
        video_url = PROVINCE_VIDEOS.get(province, "")
        image_url = PROVINCE_IMAGES.get(province, "")
        
        # 创建与testdata.json格式相似的数据结构
        province_info = {
            "name": f"{province}简介",
            "province": province,
            "description": description,
            "image_url": image_url,
            "video_url": video_url,
            "address": province
        }
        
        provinces_data.append(province_info)
    
    return provinces_data

def save_to_json(data, filename):
    """
    将数据保存为JSON格式文件
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已保存到 {filename} 文件中")

def main():
    """
    主函数
    """
    print("中国省份介绍信息生成工具")
    print("=" * 40)
    
    # 生成省份数据
    provinces_data = generate_province_data()
    
    # 保存为JSON文件
    save_to_json(provinces_data, 'provinces_info.json')
    
    print("=" * 40)
    print("所有省份信息处理完成！")

if __name__ == "__main__":
    main()