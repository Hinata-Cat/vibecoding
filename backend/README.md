# 云旅游网站后端

基于Python Flask的RESTful API后端，使用MongoDB数据库，支持本地文件存储，可通过uvicorn部署。

## 功能特点

- RESTful API设计
- MongoDB数据库存储省份和景点信息
- 支持省份和景点的增删改查操作
- 可通过uvicorn部署
- 支持文件本地存储

## 技术栈

- **后端框架**: Python + Flask + Flask-RESTful
- **数据库**: MongoDB (通过mongoengine ORM)
- **API风格**: RESTful API
- **部署方式**: 支持uvicorn部署
- **文件存储**: 本地存储方案

## 项目结构

```
backend/
├── app.py              # Flask主应用文件
├── startup.py          # uvicorn部署入口
├── config.py           # 配置文件
├── database.py         # 数据库初始化
├── models.py           # 数据模型定义
├── routes.py           # API路由定义
├── init_data.py        # 示例数据初始化脚本
├── import_jiangxi_data.py # 江西省数据导入脚本
├── import_scenic_spots.py # 风景名胜数据导入脚本
├── import_all_data.py  # 综合数据导入脚本（整合所有数据导入功能）
├── bilibili_crawler.py # B站视频爬虫脚本
├── import_bilibili_data.py # B站视频数据导入脚本
├── verify_video_links.py # 视频链接验证脚本
├── province_attractions_crawler.py # 省份景点推荐和数据爬取脚本
├── verify_new_attractions.py # 新景点数据验证脚本
├── show_data_locations.py # 数据存储位置查询脚本
├── find_attraction_images.py # 景点图片搜索脚本（Wikimedia）
├── baidu_baike_image_crawler.py # 百度百科图片爬虫脚本
├── bing_image_crawler.py # Bing图片搜索爬虫脚本
├── add_province_descriptions.py # 省份详细描述添加脚本
├── add_jiangxi_images.py # 江西省景点图片添加脚本
├── check_jiangxi_images.py # 江西省景点图片检查脚本
├── export_data.py      # 数据库导出脚本
├── import_exported_data.py # 导出数据导入脚本
├── requirements.txt    # 项目依赖
├── testdata.json       # 测试数据文件
├── scenic_spots.json   # 风景名胜数据文件
├── bilibili_video_results.json # B站视频爬取结果文件
├── province_attractions_data.json # 省份景点数据文件
├── exported_data.json  # 导出的数据文件
├── README.md           # 项目说明文档
├── INSTALLATION.md     # 安装说明文档
├── MONGODB_INSTALLATION.md # MongoDB安装说明
├── API_DOCUMENTATION.md # API详细文档
└── apidoc.md           # API接口文档
```

## 数据模型

### Province (省份)
- name: 省份名称
- description: 省份描述
- created_at/updated_at: 时间戳

### Attraction (景点)
- name: 景点名称
- province: 关联的省份
- description: 景点描述
- image_url: 图片链接
- video_url: 视频链接 (如B站链接)
- address: 景点地址
- created_at/updated_at: 时间戳

## 数据存储

### 主要存储位置

1. **MongoDB数据库** (主要数据源)
   - 省份数据保存在 `provinces` 集合中
   - 景点数据保存在 `attractions` 集合中
   - 景点通过 `province` 字段关联到对应的省份

2. **JSON文件** (备份和查看)
   - [province_attractions_data.json](file:///C:/Users/lan/Documents/%E6%88%91%E7%9A%84codes/AI%E7%BC%96%E7%A8%8B/backend/province_attractions_data.json) - 省份景点爬取数据
   - [bilibili_video_results.json](file://c:\Users\lan\Documents\我的codes\AI编程\backend\bilibili_video_results.json) - B站视频爬取结果
   - [scenic_spots.json](file:///C:/Users/lan/Documents/%E6%88%91%E7%9A%84codes/AI%E7%BC%96%E7%A8%8B/backend/scenic_spots.json) - 风景名胜数据
   - [testdata.json](file:///C:/Users/lan/Documents/%E6%88%91%E7%9A%84codes/AI%E7%BC%96%E7%A8%8B/backend/testdata.json) - 测试数据
   - [exported_data.json](file://c:\Users\lan\Documents\我的codes\AI编程\backend\exported_data.json) - 导出的数据库数据

### 数据同步

- 爬虫爬取的数据会同时保存到数据库和JSON文件中
- 数据库是主要的数据源，用于API接口提供数据
- JSON文件作为备份，便于查看和调试

## API接口

### 省份相关接口

- `GET /api/provinces` - 获取所有省份列表
- `GET /api/provinces/<province_id>` - 获取特定省份信息
- `GET /api/provinces/name/<province_name>` - 根据省份名称获取省份信息

### 景点相关接口

- `GET /api/attractions` - 获取所有景点列表（可选参数: province_id, province_name）
- `GET /api/attractions/<attraction_id>` - 获取特定景点信息

## 安装和运行

### 环境要求
- Python 3.7+
- MongoDB 3.6+

### 安装步骤

1. 克隆项目代码：
   ```
   git clone <项目地址>
   cd backend
   ```

2. 创建虚拟环境（推荐）：
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

4. 安装并启动MongoDB：
   - 下载并安装MongoDB Community Server
   - 启动MongoDB服务：
     ```
     net start MongoDB  # Windows
     sudo systemctl start mongod  # Linux
     ```

### 数据初始化

运行综合数据导入脚本一次性导入所有示例数据：
```
python import_all_data.py
```

该脚本整合了以下三个独立的数据导入功能：
1. 基础示例数据导入
2. 江西省景点数据导入
3. 全国风景名胜数据导入

### 数据导出和导入

#### 导出数据
将数据库中的所有数据导出到JSON文件：
```
python export_data.py
```
导出的数据将保存在 [exported_data.json](file://c:\Users\lan\Documents\我的codes\AI编程\backend\exported_data.json) 文件中。

#### 导入数据
从导出的JSON文件导入数据到数据库：
```
python import_exported_data.py
```
注意：此操作将清空数据库中的现有数据！

### B站视频数据更新

为了提供更准确的景点相关视频，我们开发了专门的B站爬虫来获取与景点高度相关的视频链接：

1. 运行B站视频爬虫（可选）：
   ```
   python bilibili_crawler.py
   ```
   该脚本会爬取与景点相关的B站视频链接，并自动更新JSON数据文件和数据库。

2. 导入B站视频数据：
   ```
   python import_bilibili_data.py
   ```
   该脚本将爬取到的B站视频链接导入到数据库中，替换原有的视频链接。

3. 验证视频链接更新结果：
   ```
   python verify_video_links.py
   ```

### 省份景点推荐和数据爬取

为每个省份推荐热门景点并爬取相关数据：

1. 运行省份景点推荐和数据爬取脚本：
   ```
   python province_attractions_crawler.py
   ```
   该脚本会为每个省份推荐热门景点，并爬取相关数据（描述、图片、B站视频等），然后保存到数据库中。

2. 验证新爬取的景点数据：
   ```
   python verify_new_attractions.py
   ```

### 景点图片搜索

为景点搜索高质量图片：

1. 运行景点图片搜索脚本（使用Wikimedia Commons）：
   ```
   python find_attraction_images.py
   ```
   该脚本会使用Wikimedia Commons API为景点搜索相关图片，并选择最佳图片。

2. 运行百度百科图片爬虫：
   ```
   python baidu_baike_image_crawler.py
   ```
   该脚本会从百度百科为景点搜索相关图片，并将最佳图片链接更新到数据库中。

3. 运行Bing图片搜索爬虫（推荐）：
   ```
   python bing_image_crawler.py
   ```
   该脚本会使用Bing图片搜索为景点获取最相关的高质量图片，并更新到数据库中。

### 省份详细描述更新

为所有省份添加详细的介绍信息：

1. 运行省份详细描述更新脚本：
   ```
   python add_province_descriptions.py
   ```
   该脚本会为数据库中的所有省份添加详细的介绍信息，替换原来简单的描述。

### 查询数据存储位置

查看数据具体保存在哪里：
```
python show_data_locations.py
```

### 启动服务

1. 使用Flask内置服务器运行：
   ```
   python app.py
   ```

2. 或使用uvicorn部署（推荐）：
   ```
   uvicorn startup:app --host 0.0.0.0 --port 5000
   ```

3. 或使用gunicorn部署（生产环境）：
   ```
   gunicorn -w 4 -b 0.0.0.0:5000 startup:app
   ```

## API测试

启动服务后，可以使用以下URL测试API:

- `http://localhost:5000/` - 根路径，显示欢迎信息
- `http://localhost:5000/api/provinces` - 获取省份列表
- `http://localhost:5000/api/provinces/name/北京市` - 获取北京市信息
- `http://localhost:5000/api/attractions` - 获取景点列表
- `http://localhost:5000/api/attractions?province_id=<id>` - 获取特定省份的景点列表
- `http://localhost:5000/api/attractions?province_name=北京市` - 获取北京市的景点列表

## 配置

可以通过环境变量配置以下参数：
- [SECRET_KEY](file://c:/Users/lan/Documents/%E6%88%91%E7%9A%84codes/AI%E7%BC%96%E7%A8%8B/backend/config.py#L3-L3) - Flask密钥
- `MONGO_DB` - MongoDB数据库名（默认: virtual_tourism）
- `MONGO_HOST` - MongoDB主机地址（默认: localhost）
- `MONGO_PORT` - MongoDB端口（默认: 27017）
- `MONGO_USER` - MongoDB用户名（可选）
- `MONGO_PASSWORD` - MongoDB密码（可选）
- [UPLOAD_FOLDER](file://c:/Users/lan/Documents/%E6%88%91%E7%9A%84codes/AI%E7%BC%96%E7%A8%8B/backend/config.py#L11-L11) - 文件上传目录（默认: uploads）

## 文档

- [API详细文档](API_DOCUMENTATION.md)
- [API接口规范](apidoc.md)

## 许可证

本项目仅供学习和参考使用。