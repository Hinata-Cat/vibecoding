# 云旅游网站API文档

## 概述

本文档描述了云旅游网站后端提供的RESTful API接口。通过这些接口，前端可以获取中国各省份及其景点的信息，实现云旅游功能。

## 基本信息

- 服务器地址: `http://localhost:5000`
- API根路径: `/api`
- 数据格式: JSON
- 字符编码: UTF-8

## 状态码说明

| 状态码 | 说明 |
|-------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 404 | 资源未找到 |
| 500 | 服务器内部错误 |

## API列表

### 1. 获取省份列表

#### 接口地址
```
GET /api/provinces
```

#### 请求参数
无

#### 返回数据
成功返回省份列表，每个省份包含以下字段：
- `id` (string): 省份唯一标识符
- `name` (string): 省份名称
- `description` (string): 省份描述
- `created_at` (string): 创建时间（ISO 8601格式）
- `updated_at` (string): 更新时间（ISO 8601格式）

#### 返回示例
```json
[
  {
    "id": "60a8a1c1b1a8d92b6c123456",
    "name": "北京市",
    "description": "中国的首都，政治、文化中心",
    "created_at": "2023-05-22T10:30:25.123000",
    "updated_at": "2023-05-22T10:30:25.123000"
  },
  {
    "id": "60a8a1c1b1a8d92b6c123457",
    "name": "上海市",
    "description": "中国最大的城市，经济金融中心",
    "created_at": "2023-05-22T10:30:25.124000",
    "updated_at": "2023-05-22T10:30:25.124000"
  }
]
```

#### 错误返回
```json
{
  "error": "Failed to fetch provinces",
  "message": "具体的错误信息"
}
```

### 2. 获取特定省份信息

#### 接口地址
```
GET /api/provinces/{province_id}
```

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| province_id | string | 是 | 省份ID |

#### 返回数据
成功返回省份详细信息：
- `id` (string): 省份唯一标识符
- `name` (string): 省份名称
- `description` (string): 省份描述
- `created_at` (string): 创建时间（ISO 8601格式）
- `updated_at` (string): 更新时间（ISO 8601格式）

#### 返回示例
```json
{
  "id": "60a8a1c1b1a8d92b6c123456",
  "name": "北京市",
  "description": "中国的首都，政治、文化中心",
  "created_at": "2023-05-22T10:30:25.123000",
  "updated_at": "2023-05-22T10:30:25.123000"
}
```

#### 错误返回
```json
{
  "error": "Province not found"
}
```

或

```json
{
  "error": "Failed to fetch province",
  "message": "具体的错误信息"
}
```

### 3. 获取景点列表

#### 接口地址
```
GET /api/attractions
```

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| province_id | string | 否 | 省份ID，用于筛选特定省份的景点 |

#### 返回数据
成功返回景点列表，每个景点包含以下字段：
- `id` (string): 景点唯一标识符
- `name` (string): 景点名称
- `province` (object): 关联的省份信息
- `description` (string): 景点描述
- `image_url` (string): 景点图片链接
- `video_url` (string): 景点视频链接（如B站链接）
- `address` (string): 景点地址
- `created_at` (string): 创建时间（ISO 8601格式）
- `updated_at` (string): 更新时间（ISO 8601格式）

#### 返回示例
```json
[
  {
    "id": "60a8a1c1b1a8d92b6c234567",
    "name": "故宫博物院",
    "province": {
      "id": "60a8a1c1b1a8d92b6c123456",
      "name": "北京市",
      "description": "中国的首都，政治、文化中心",
      "created_at": "2023-05-22T10:30:25.123000",
      "updated_at": "2023-05-22T10:30:25.123000"
    },
    "description": "明清两代的皇家宫殿，世界上现存规模最大、保存最完整的木质结构古建筑之一",
    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Forbidden_City_Beijing_July_2008_01.jpg/800px-Forbidden_City_Beijing_July_2008_01.jpg",
    "video_url": "https://www.bilibili.com/video/BV1Vs411W7PT",
    "address": "北京市东城区景山前街4号",
    "created_at": "2023-05-22T10:30:25.234000",
    "updated_at": "2023-05-22T10:30:25.234000"
  }
]
```

#### 错误返回
```json
{
  "error": "Failed to fetch attractions",
  "message": "具体的错误信息"
}
```

或

```json
{
  "error": "Invalid province ID",
  "message": "具体的错误信息"
}
```

### 4. 获取特定景点信息

#### 接口地址
```
GET /api/attractions/{attraction_id}
```

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| attraction_id | string | 是 | 景点ID |

#### 返回数据
成功返回景点详细信息：
- `id` (string): 景点唯一标识符
- `name` (string): 景点名称
- `province` (object): 关联的省份信息
- `description` (string): 景点描述
- `image_url` (string): 景点图片链接
- `video_url` (string): 景点视频链接（如B站链接）
- `address` (string): 景点地址
- `created_at` (string): 创建时间（ISO 8601格式）
- `updated_at` (string): 更新时间（ISO 8601格式）

#### 返回示例
```json
{
  "id": "60a8a1c1b1a8d92b6c234567",
  "name": "故宫博物院",
  "province": {
    "id": "60a8a1c1b1a8d92b6c123456",
    "name": "北京市",
    "description": "中国的首都，政治、文化中心",
    "created_at": "2023-05-22T10:30:25.123000",
    "updated_at": "2023-05-22T10:30:25.123000"
  },
  "description": "明清两代的皇家宫殿，世界上现存规模最大、保存最完整的木质结构古建筑之一",
  "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Forbidden_City_Beijing_July_2008_01.jpg/800px-Forbidden_City_Beijing_July_2008_01.jpg",
  "video_url": "https://www.bilibili.com/video/BV1Vs411W7PT",
  "address": "北京市东城区景山前街4号",
  "created_at": "2023-05-22T10:30:25.234000",
  "updated_at": "2023-05-22T10:30:25.234000"
}
```

#### 错误返回
```json
{
  "error": "Attraction not found"
}
```

或

```json
{
  "error": "Failed to fetch attraction",
  "message": "具体的错误信息"
}
```

## 使用示例

### 获取所有省份
```bash
curl http://localhost:5000/api/provinces
```

### 获取特定省份的景点
```bash
curl http://localhost:5000/api/attractions?province_id=60a8a1c1b1a8d92b6c123456
```

### 获取特定景点
```bash
curl http://localhost:5000/api/attractions/60a8a1c1b1a8d92b6c234567
```

## 前端集成建议

1. 首先调用 `/api/provinces` 获取所有省份列表，在地图上显示
2. 当用户点击某个省份时，调用 `/api/attractions?province_id={id}` 获取该省份的景点列表
3. 在列表中显示景点名称和简要描述
4. 当用户点击某个景点时，使用返回数据中的 `image_url` 显示图片，或使用 `video_url` 跳转到视频页面

## 错误处理

所有API接口都包含适当的错误处理机制。当发生错误时，API会返回相应的HTTP状态码和包含错误信息的JSON对象。前端应根据返回的状态码和错误信息进行相应的处理。

# API接口文档

## 基础信息
- Host: `http://localhost:5000`
- Version: v1

## 接口列表

### 省份相关接口

#### 获取所有省份列表
- **URL**: `/api/provinces`
- **Method**: `GET`
- **Description**: 获取所有省份的列表信息
- **Response**:
  ```json
  [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
  ```

#### 获取特定省份信息
- **URL**: `/api/provinces/{province_id}`
- **Method**: `GET`
- **Description**: 根据省份ID获取特定省份的详细信息
- **Parameters**:
  - `province_id` (path): 省份ID
- **Response**:
  ```json
  {
    "id": "string",
    "name": "string",
    "description": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```

#### 根据省份名称获取省份信息
- **URL**: `/api/provinces/name/{province_name}`
- **Method**: `GET`
- **Description**: 根据省份名称获取特定省份的详细信息
- **Parameters**:
  - `province_name` (path): 省份名称（需要URL编码）
- **Response**:
  ```json
  {
    "id": "string",
    "name": "string",
    "description": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```

### 景点相关接口

#### 获取景点列表
- **URL**: `/api/attractions`
- **Method**: `GET`
- **Description**: 获取所有景点列表，支持按省份筛选
- **Parameters**:
  - `province_id` (query, optional): 省份ID，用于筛选特定省份的景点
  - `province_name` (query, optional): 省份名称（需要URL编码），用于筛选特定省份的景点
- **Response**:
  ```json
  [
    {
      "id": "string",
      "name": "string",
      "province": {
        "id": "string",
        "name": "string",
        "description": "string",
        "created_at": "datetime",
        "updated_at": "datetime"
      },
      "description": "string",
      "image_url": "string",
      "video_url": "string",
      "address": "string",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
  ```

#### 获取特定景点信息
- **URL**: `/api/attractions/{attraction_id}`
- **Method**: `GET`
- **Description**: 根据景点ID获取特定景点的详细信息
- **Parameters**:
  - `attraction_id` (path): 景点ID
- **Response**:
  ```json
  {
    "id": "string",
    "name": "string",
    "province": {
      "id": "string",
      "name": "string",
      "description": "string",
      "created_at": "datetime",
      "updated_at": "datetime"
    },
    "description": "string",
    "image_url": "string",
    "video_url": "string",
    "address": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```

## 使用示例

### 获取北京市的景点
```bash
curl "http://localhost:5000/api/attractions?province_name=北京市"
```

### 获取江西省的景点
```bash
curl "http://localhost:5000/api/attractions?province_name=江西省"
```

### 根据省份名称获取省份信息
```bash
curl "http://localhost:5000/api/provinces/name/北京市"
```
