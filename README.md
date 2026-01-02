# 1688订单支付API服务

基于 FastAPI 的1688订单支付接口服务，提供支付链接获取和支付状态查询功能。

## API 接口

### 1. 获取支付链接

**POST** `/api/pay-url`

请求体:
```json
{
  "order_ids": ["订单ID1", "订单ID2"]
}
```

响应:
```json
{
  "success": true,
  "pay_url": "https://...",
  "success_order_ids": ["订单ID1", "订单ID2"],
  "failed_order_ids": [],
  "success_count": 2,
  "failed_count": 0,
  "total_count": 2,
  "error_msg": null
}
```

### 2. 获取支付状态

**GET** `/api/pay-status/{order_id}`

响应:
```json
{
  "success": true,
  "order_id": "订单ID",
  "pay_status": "已付款",
  "error_msg": null
}
```

## 部署方式

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
# 开发模式
python app.py

# 或使用 uvicorn（推荐生产环境）
uvicorn app:app --host 0.0.0.0 --port 8000

# 后台运行
nohup uvicorn app:app --host 0.0.0.0 --port 8000 > api.log 2>&1 &
```

### 3. 访问 API 文档

启动服务后访问: `http://your-server:8000/docs`

## 文件说明

| 文件 | 说明 |
|------|------|
| `app.py` | FastAPI 主应用 |
| `1688.py` | 原始本地测试脚本 |
| `requirements.txt` | Python 依赖 |

## 调用示例

### curl

```bash
# 获取支付链接
curl -X POST "http://localhost:8000/api/pay-url" \
  -H "Content-Type: application/json" \
  -d '{"order_ids": ["123456789", "987654321"]}'

# 获取支付状态
curl "http://localhost:8000/api/pay-status/123456789"
```

### Python

```python
import requests

# 获取支付链接
response = requests.post(
    "http://localhost:8000/api/pay-url",
    json={"order_ids": ["123456789"]}
)
print(response.json())

# 获取支付状态
response = requests.get("http://localhost:8000/api/pay-status/123456789")
print(response.json())
```
