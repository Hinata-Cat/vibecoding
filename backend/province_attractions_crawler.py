"""
省份景点推荐和数据爬取脚本
此脚本为每个省份推荐热门景点，并爬取相关数据（描述、图片、B站视频等）
"""

import asyncio
import json
import time
import random
from bilibili_api import search, sync
from app import create_app
from models import Province, Attraction

# 各省份的热门景点推荐
PROVINCE_ATTRACTIONS = {
    "北京市": [
        "故宫博物院", "天坛公园", "颐和园", "八达岭长城", "北海公园", 
        "景山公园", "雍和宫", "恭王府", "圆明园", "慕田峪长城"
    ],
    "上海市": [
        "外滩", "东方明珠塔", "豫园", "上海迪士尼乐园", "田子坊", 
        "新天地", "上海博物馆", "朱家角古镇", "陆家嘴", "上海野生动物园"
    ],
    "天津市": [
        "天津之眼", "五大道", "古文化街", "意式风情区", "盘山风景区", 
        "独乐寺", "天津博物馆", "石家大院", "周恩来邓颖超纪念馆", "天津水上公园"
    ],
    "重庆市": [
        "洪崖洞", "磁器口古镇", "武隆喀斯特", "大足石刻", "三峡博物馆", 
        "重庆动物园", "南山风景区", "重庆科技馆", "白公馆", "渣滓洞"
    ],
    "河北省": [
        "承德避暑山庄", "北戴河", "白洋淀", "清东陵", "清西陵", 
        "山海关", "金山岭长城", "娲皇宫", "广府古城", "白石山"
    ],
    "山西省": [
        "五台山", "平遥古城", "云冈石窟", "乔家大院", "王家大院", 
        "恒山", "应县木塔", "晋祠", "雁门关", "壶口瀑布"
    ],
    "辽宁省": [
        "沈阳故宫", "大连海滨", "金石滩", "鞍山千山", "抚顺雷锋纪念馆", 
        "本溪水洞", "丹东鸭绿江", "锦州古塔", "朝阳凤凰山", "葫芦岛龙湾海滨"
    ],
    "吉林省": [
        "长白山天池", "伪满皇宫博物院", "净月潭", "长春电影制片厂", "吉林雾凇岛", 
        "查干湖", "敦化六顶山", "通化五女峰", "集安高句丽文物古迹", "松花湖"
    ],
    "黑龙江省": [
        "哈尔滨冰雪大世界", "五大连池", "镜泊湖", "漠河北极村", "大庆铁人王进喜纪念馆", 
        "齐齐哈尔扎龙自然保护区", "牡丹江威虎山", "佳木斯黑瞎子岛", "伊春汤旺河林海奇石", "绥化海伦大峡谷"
    ],
    "江苏省": [
        "苏州园林", "南京中山陵", "瘦西湖", "鼋头渚", "周庄古镇", 
        "同里古镇", "灵山大佛", "夫子庙", "拙政园", "留园"
    ],
    "浙江省": [
        "西湖", "普陀山", "乌镇", "横店影视城", "千岛湖", 
        "西塘古镇", "南浔古镇", "雁荡山", "天台山", "莫干山"
    ],
    "安徽省": [
        "黄山", "九华山", "宏村", "西递古村", "天柱山", 
        "琅琊山", "采石矶", "巢湖", "花山迷窟", "太极洞"
    ],
    "福建省": [
        "鼓浪屿", "武夷山", "土楼", "太姥山", "湄洲岛", 
        "清源山", "冠豸山", "福州三坊七巷", "泉州清源山", "厦门环岛路"
    ],
    "江西省": [
        "滕王阁旅游区", "庐山风景名胜区", "三清山风景名胜区", "龙虎山", "井冈山", 
        "婺源", "鄱阳湖", "景德镇古窑", "赣州古城", "明月山"
    ],
    "山东省": [
        "泰山", "趵突泉", "孔府孔庙孔林", "青岛海滨", "蓬莱阁", 
        "崂山", "威海刘公岛", "潍坊风筝博物馆", "烟台蓬莱阁", "枣庄台儿庄古城"
    ],
    "河南省": [
        "少林寺", "龙门石窟", "云台山", "清明上河园", "嵩山", 
        "白马寺", "开封府", "嵖岈山", "鸡公山", "殷墟"
    ],
    "湖北省": [
        "黄鹤楼", "武当山", "神农架", "三峡大坝", "东湖风景区", 
        "荆州古城", "襄阳古隆中", "恩施大峡谷", "宜昌三峡人家", "咸宁九宫山"
    ],
    "湖南省": [
        "张家界", "岳阳楼", "凤凰古城", "橘子洲头", "崀山", 
        "衡山", "韶山", "岳麓山", "桃花源", "德夯苗寨"
    ],
    "广东省": [
        "广州长隆", "深圳世界之窗", "丹霞山", "珠海长隆", "白云山", 
        "佛山祖庙", "肇庆七星岩", "惠州西湖", "汕头南澳岛", "韶关丹霞山"
    ],
    "海南省": [
        "三亚亚龙湾", "天涯海角", "蜈支洲岛", "南山文化旅游区", "大小洞天", 
        "呀诺达热带雨林", "分界洲岛", "三亚湾", "博鳌亚洲论坛永久会址", "海口骑楼老街"
    ],
    "四川省": [
        "成都大熊猫繁育研究基地", "九寨沟", "峨眉山", "乐山大佛", "都江堰", 
        "青城山", "稻城亚丁", "阆中古城", "海螺沟", "四姑娘山"
    ],
    "贵州省": [
        "黄果树瀑布", "荔波小七孔", "西江千户苗寨", "梵净山", "赤水丹霞", 
        "织金洞", "马岭河峡谷", "青岩古镇", "镇远古镇", "兴义万峰林"
    ],
    "云南省": [
        "丽江古城", "大理古城", "石林", "玉龙雪山", "洱海", 
        "西双版纳", "香格里拉", "腾冲火山热海", "昆明世博园", "泸沽湖"
    ],
    "陕西省": [
        "秦始皇兵马俑", "华山", "西安古城墙", "大雁塔", "华清池", 
        "法门寺", "延安革命纪念馆", "黄帝陵", "太白山", "壶口瀑布"
    ],
    "甘肃省": [
        "敦煌莫高窟", "嘉峪关", "张掖丹霞", "麦积山石窟", "崆峒山", 
        "鸣沙山月牙泉", "拉卜楞寺", "炳灵寺石窟", "雅丹魔鬼城", "祁连山草原"
    ],
    "青海省": [
        "青海湖", "塔尔寺", "茶卡盐湖", "门源油菜花海", "坎布拉国家森林公园", 
        "可可西里自然保护区", "同仁历史文化名城", "互助土族故土园", "贵德国家地质公园", "玉树三江源"
    ],
    "台湾省": [
        "日月潭", "阿里山", "台北101", "垦丁国家公园", "故宫博物院", 
        "太鲁阁峡谷", "九份", "平溪", "花莲", "台中逢甲夜市"
    ],
    "内蒙古自治区": [
        "呼伦贝尔大草原", "成吉思汗陵", "响沙湾", "阿尔山国家森林公园", "额济纳胡杨林", 
        "希拉穆仁草原", "满洲里中俄边境", "赤峰克什克腾石阵", "通辽大青沟", "鄂尔多斯响沙湾"
    ],
    "广西壮族自治区": [
        "桂林漓江", "北海银滩", "德天瀑布", "龙脊梯田", "涠洲岛", 
        "象鼻山", "芦笛岩", "七星公园", "阳朔西街", "南宁青秀山"
    ],
    "西藏自治区": [
        "布达拉宫", "大昭寺", "珠穆朗玛峰", "纳木错", "色拉寺", 
        "扎什伦布寺", "雅鲁藏布大峡谷", "巴松措", "羊卓雍错", "南迦巴瓦峰"
    ],
    "宁夏回族自治区": [
        "沙湖", "沙坡头", "西夏王陵", "镇北堡西部影城", "水洞沟", 
        "贺兰山岩画", "六盘山", "须弥山石窟", "火石寨", "青铜峡黄河大峡谷"
    ],
    "新疆维吾尔自治区": [
        "天山天池", "喀纳斯湖", "吐鲁番葡萄沟", "那拉提草原", "巴音布鲁克草原", 
        "喀什老城", "塔克拉玛干沙漠", "可可托海", "博斯腾湖", "赛里木湖"
    ]
}

async def search_bilibili_video(attraction_name, province_name):
    """
    搜索与景点相关的B站视频
    """
    # 构造搜索关键词
    keywords = [
        f"{attraction_name} 旅游",
        f"{attraction_name} 介绍",
        f"{attraction_name} 宣传片",
        f"{province_name} {attraction_name}",
        f"{attraction_name} 4K"
    ]
    
    # 尝试不同的关键词
    for keyword in keywords:
        try:
            print(f"  正在搜索B站视频: {keyword}")
            
            # 使用B站搜索API
            result = await search.search_by_type(
                keyword=keyword,
                search_type=search.SearchObjectType.VIDEO,
                page=1,
                page_size=5  # 获取前5个结果
            )
            
            # 检查是否有搜索结果
            if result.get('result') and len(result['result']) > 0:
                # 遍历搜索结果，找到最相关的视频
                for video in result['result']:
                    title = video.get('title', '').lower()
                    # 检查视频标题是否包含景点名称
                    if attraction_name in title or \
                       (attraction_name == "天津之眼" and "天津" in title and "摩天轮" in title) or \
                       (attraction_name == "五大道" and "天津" in title and "五大道" in title) or \
                       (attraction_name == "磁器口古镇" and "磁器口" in title) or \
                       (attraction_name == "洪崖洞" and "洪崖洞" in title):
                        
                        # 构造完整的B站视频链接
                        bvid = video.get('bvid')
                        if bvid:
                            video_url = f"https://www.bilibili.com/video/{bvid}"
                            print(f"  ✓ 找到相关视频: {video_url}")
                            return {
                                "video_url": video_url,
                                "title": video.get('title', ''),
                                "play": video.get('play', 0),
                                "duration": video.get('duration', '')
                            }
            
            # 添加延时，避免触发风控
            await asyncio.sleep(random.uniform(1, 2))
            
        except Exception as e:
            print(f"  搜索 {keyword} 时出错: {e}")
            # 如果遇到API错误，等待更长时间
            await asyncio.sleep(random.uniform(3, 5))
            continue
    
    # 如果没有找到相关视频，返回默认值
    print(f"  ✗ 未找到 {attraction_name} 的相关视频")
    return {
        "video_url": "",  # 空链接表示未找到相关视频
        "title": "",
        "play": 0,
        "duration": ""
    }

async def search_image_url(attraction_name, province_name):
    """
    搜索景点图片链接（这里简化处理，实际项目中可以接入图片搜索API）
    """
    # 这里我们使用维基百科等公共资源的图片链接格式
    # 实际项目中可以接入图片搜索API
    base_urls = [
        f"https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/{attraction_name.replace(' ', '_')}.jpg/800px-{attraction_name.replace(' ', '_')}.jpg",
        f"https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/{attraction_name.replace(' ', '_')}_view.jpg/800px-{attraction_name.replace(' ', '_')}_view.jpg",
        f"https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/{province_name}_{attraction_name.replace(' ', '_')}.jpg/800px-{province_name}_{attraction_name.replace(' ', '_')}.jpg"
    ]
    
    # 返回第一个链接作为示例
    return base_urls[0]

def get_attraction_description(attraction_name, province_name):
    """
    获取景点描述（这里使用预定义数据，实际项目中可以接入百科API）
    """
    descriptions = {
        "故宫博物院": f"{attraction_name}是明清两代的皇家宫殿，世界上现存规模最大、保存最完整的木质结构古建筑之一，是中华文明的瑰宝。",
        "天坛公园": f"{attraction_name}是明清两朝皇帝祭天的场所，中国现存最大的古代祭祀性建筑群，体现了中国古代建筑艺术的精华。",
        "颐和园": f"{attraction_name}是中国清朝时期皇家园林，以昆明湖、万寿山为基础，汲取江南园林的设计手法而建成，被誉为'皇家园林博物馆'。",
        "外滩": f"{attraction_name}是{province_name}的标志性景点，汇集了数十栋风格各异的历史建筑，对岸是现代化的陆家嘴金融区，展现了{province_name}的历史与现代的完美融合。",
        "东方明珠塔": f"{attraction_name}是{province_name}的标志性建筑之一，塔高468米，是亚洲第四、世界第六高塔，塔内有太空舱、旋转餐厅等设施。",
        "豫园": f"{attraction_name}是明代私人园林，典型的江南古典园林风格，周围是著名的城隍庙商业区，是体验老{province_name}风情的绝佳去处。",
    }
    
    # 如果有预定义描述，返回预定义的
    if attraction_name in descriptions:
        return descriptions[attraction_name]
    
    # 否则返回通用描述
    return f"{attraction_name}是{province_name}著名的旅游景点，拥有丰富的自然和文化价值。"

async def crawl_province_attractions():
    """
    爬取各省份景点数据
    """
    app = create_app()
    
    with app.app_context():
        print("开始爬取各省份景点数据...")
        print("=" * 50)
        
        # 存储所有爬取到的数据
        all_attractions_data = []
        
        # 遍历所有省份
        for province_name, attractions in PROVINCE_ATTRACTIONS.items():
            print(f"\n处理省份: {province_name}")
            print("-" * 30)
            
            # 获取或创建省份
            province = Province.objects(name=province_name).first()
            if not province:
                province = Province(name=province_name, description=f"{province_name}是中国的一个省份")
                province.save()
                print(f"创建新省份: {province_name}")
            else:
                print(f"省份已存在: {province_name}")
            
            # 为该省份的每个景点爬取数据
            for i, attraction_name in enumerate(attractions[:3]):  # 每个省份只处理前3个景点
                print(f"\n处理进度: {i+1}/3 - {attraction_name}")
                
                # 检查景点是否已存在
                existing_attraction = Attraction.objects(name=attraction_name, province=province).first()
                if existing_attraction:
                    print(f"  景点已存在，跳过: {attraction_name}")
                    continue
                
                # 获取景点描述
                description = get_attraction_description(attraction_name, province_name)
                
                # 获取图片链接
                image_url = await search_image_url(attraction_name, province_name)
                
                # 搜索B站视频
                video_data = await search_bilibili_video(attraction_name, province_name)
                video_url = video_data["video_url"]
                
                # 构造景点地址
                address = f"{province_name}{attraction_name}"
                
                # 创建景点数据
                attraction_data = {
                    "name": attraction_name,
                    "province": province_name,
                    "description": description,
                    "image_url": image_url,
                    "video_url": video_url,
                    "address": address
                }
                
                # 添加到总数据列表
                all_attractions_data.append(attraction_data)
                
                # 保存到数据库
                try:
                    attraction = Attraction(
                        name=attraction_name,
                        province=province,
                        description=description,
                        image_url=image_url,
                        video_url=video_url,
                        address=address
                    )
                    attraction.save()
                    print(f"  ✓ 成功保存景点: {attraction_name}")
                except Exception as e:
                    print(f"  ✗ 保存景点 {attraction_name} 时出错: {e}")
                
                # 添加随机延时，模拟人工操作
                await asyncio.sleep(random.uniform(1, 3))
        
        # 保存所有数据到JSON文件
        with open('province_attractions_data.json', 'w', encoding='utf-8') as f:
            json.dump(all_attractions_data, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 50)
        print("数据爬取完成!")
        print(f"共爬取 {len(all_attractions_data)} 个景点数据")
        print("数据已保存到 province_attractions_data.json 文件中")

async def main():
    """
    主函数
    """
    print("省份景点推荐与数据爬取工具")
    print("=" * 50)
    
    # 爬取各省份景点数据
    await crawl_province_attractions()

if __name__ == "__main__":
    # 运行异步主函数
    sync(main())