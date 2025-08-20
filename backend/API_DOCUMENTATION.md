# 云旅游网站后端API文档

## 基础URL
```
http://localhost:5000
```

## 状态码
| 状态码 | 说明 |
|-------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 资源未找到 |
| 500 | 服务器内部错误 |

## 接口列表

### 1. 获取省份列表
#### 请求URL
```
GET /api/provinces
```

#### 请求参数
无

#### 响应示例
```json
[
  {
    "id": "5f8d0d5f8b8d5f0017f3d5b1",
    "name": "北京市",
    "description": "北京市，简称\"京\"，是中华人民共和国的首都...",
    "created_at": "2023-01-01T00:00:00.000Z",
    "updated_at": "2023-01-01T00:00:00.000Z"
  },
  {
    "id": "5f8d0d5f8b8d5f0017f3d5b2",
    "name": "上海市",
    "description": "上海市，简称\"沪\"，是中国最大的城市...",
    "created_at": "2023-01-01T00:00:00.000Z",
    "updated_at": "2023-01-01T00:00:00.000Z"
  }
]
```

### 2. 获取特定省份信息
#### 请求URL
```
GET /api/provinces/{province_id}
```

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| province_id | string | 是 | 省份ID |

#### 响应示例
```json
{
  "id": "5f8d0d5f8b8d5f0017f3d5b1",
  "name": "北京市",
  "description": "北京市，简称\"京\"，是中华人民共和国的首都...",
  "created_at": "2023-01-01T00:00:00.000Z",
  "updated_at": "2023-01-01T00:00:00.000Z"
}
```

### 3. 根据省份名称获取省份信息
#### 请求URL
```
GET /api/provinces/name/{province_name}
```

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| province_name | string | 是 | 省份名称（URL编码） |

#### 响应示例
```json
{
  "id": "5f8d0d5f8b8d5f0017f3d5b1",
  "name": "北京市",
  "description": "北京市，简称\"京\"，是中华人民共和国的首都...",
  "created_at": "2023-01-01T00:00:00.000Z",
  "updated_at": "2023-01-01T00:00:00.000Z"
}
```

### 4. 获取景点列表
#### 请求URL
```
GET /api/attractions
```

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| province_id | string | 否 | 省份ID，用于筛选特定省份的景点 |
| province_name | string | 否 | 省份名称（URL编码），用于筛选特定省份的景点 |

#### 响应示例
```json
[
  {
    "id": "5f8d0d5f8b8d5f0017f3d5c1",
    "name": "故宫博物院",
    "province": {
      "id": "5f8d0d5f8b8d5f0017f3d5b1",
      "name": "北京市",
      "description": "北京市，简称\"京\"，是中华人民共和国的首都...",
      "created_at": "2023-01-01T00:00:00.000Z",
      "updated_at": "2023-01-01T00:00:00.000Z"
    },
    "description": "明清两代的皇家宫殿，世界上现存规模最大、保存最完整的木质结构古建筑之一",
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Forbidden_City_Beijing_July_2008_01.jpg/800px-Forbidden_City_Beijing_July_2008_01.jpg",
    "video_url": "https://www.bilibili.com/video/BV1Vs411W7PT",
    "address": "北京市东城区景山前街4号",
    "created_at": "2023-01-01T00:00:00.000Z",
    "updated_at": "2023-01-01T00:00:00.000Z"
  }
]
```

### 5. 获取特定景点信息
#### 请求URL
```
GET /api/attractions/{attraction_id}
```

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| attraction_id | string | 是 | 景点ID |

#### 响应示例
```json
{
  "id": "5f8d0d5f8b8d5f0017f3d5c1",
  "name": "故宫博物院",
  "province": {
    "id": "5f8d0d5f8b8d5f0017f3d5b1",
    "name": "北京市",
    "description": "北京市，简称\"京\"，是中华人民共和国的首都...",
    "created_at": "2023-01-01T00:00:00.000Z",
    "updated_at": "2023-01-01T00:00:00.000Z"
  },
  "description": "明清两代的皇家宫殿，世界上现存规模最大、保存最完整的木质结构古建筑之一",
  "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Forbidden_City_Beijing_July_2008_01.jpg/800px-Forbidden_City_Beijing_July_2008_01.jpg",
  "video_url": "https://www.bilibili.com/video/BV1Vs411W7PT",
  "address": "北京市东城区景山前街4号",
  "created_at": "2023-01-01T00:00:00.000Z",
  "updated_at": "2023-01-01T00:00:00.000Z"
}
```

## 使用示例

### 获取北京市的景点
```
GET /api/attractions?province_name=北京市
```

### 获取江西省的景点
```
GET /api/attractions?province_name=江西省
```