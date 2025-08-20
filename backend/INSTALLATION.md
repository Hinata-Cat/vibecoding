# 安装说明

## 网络配置

如果遇到网络连接问题，请先配置好网络代理或使用国内镜像源：

```bash
# 使用国内镜像源安装
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 或者配置全局pip镜像
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
```

## MongoDB安装

1. 下载并安装MongoDB Community Server:
   - 访问 https://www.mongodb.com/try/download/community
   - 下载适用于Windows的安装包
   - 按照安装向导完成安装

2. 启动MongoDB服务:
   - 在Windows上，MongoDB通常会作为服务自动启动
   - 或者手动启动: `net start MongoDB`

3. 验证MongoDB是否正常运行:
   ```bash
   mongo
   ```
   如果能成功连接，则MongoDB运行正常。

## 项目依赖安装

```bash
# 在项目根目录下执行
pip install -r requirements.txt
```

## 初始化数据

```bash
# 添加示例数据到数据库
python init_data.py
```

## 运行开发服务器

```bash
# 方法1: 使用Flask内置服务器
python app.py

# 方法2: 使用uvicorn部署（推荐）
uvicorn startup:app --host 0.0.0.0 --port 5000
```

## 测试API

启动服务器后，可以访问以下URL测试API:

- `http://localhost:5000/api/provinces` - 获取省份列表
- `http://localhost:5000/api/attractions` - 获取景点列表
- `http://localhost:5000/api/attractions?province_id=<id>` - 获取特定省份的景点列表

## 生产环境部署

在生产环境中，建议使用以下方式部署：

```bash
# 使用uvicorn部署
uvicorn startup:app --host 0.0.0.0 --port 8000 --workers 4
```