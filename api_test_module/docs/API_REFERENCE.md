# API Reference / API参考

## Overview / 概述

This document provides detailed information about the Document Preview Editor API endpoints.
本文档提供文档预览编辑器API端点的详细信息。

## Base URL / 基础URL

```
http://localhost:5000
```

## Authentication / 认证

Currently, no authentication is required for API access.
目前，API访问不需要认证。

## Common Response Format / 通用响应格式

### Success Response / 成功响应
```json
{
    "success": true,
    "message": "Operation completed successfully",
    "data": { ... }
}
```

### Error Response / 错误响应
```json
{
    "success": false,
    "error": "Error description",
    "code": "ERROR_CODE"
}
```

## API Endpoints / API端点

### 1. Language Management / 语言管理

#### Get Current Language / 获取当前语言
```http
GET /api/get_language
```

**Response / 响应:**
```json
{
    "language": "zh",
    "available_languages": {
        "zh": "中文",
        "en": "English"
    }
}
```

#### Set Language / 设置语言
```http
POST /api/set_language
Content-Type: application/json

{
    "language": "zh"
}
```

**Parameters / 参数:**
- `language` (string): Language code ("zh" or "en") / 语言代码

**Response / 响应:**
```json
{
    "success": true,
    "language": "zh",
    "message": "Language set successfully"
}
```

### 2. Document Processing / 文档处理

#### Auto Load Documents / 自动加载文档
```http
POST /api/auto_load
Content-Type: application/json

{
    "document": "path/to/document.docx",
    "modifications": "path/to/modifications.csv",
    "auto_apply": false
}
```

**Parameters / 参数:**
- `document` (string): Path to the document file / 文档文件路径
- `modifications` (string): Path to the modifications CSV file / 修改条目CSV文件路径
- `auto_apply` (boolean): Whether to automatically apply modifications / 是否自动应用修改

**Response / 响应:**
```json
{
    "success": true,
    "document_id": "doc_12345",
    "document_info": {
        "filename": "document.docx",
        "size": 1024,
        "pages": 5
    },
    "modifications_count": 10,
    "message": "Document and modifications loaded successfully"
}
```

#### Upload Document / 上传文档
```http
POST /api/upload_document
Content-Type: multipart/form-data

file: [document file]
```

**Response / 响应:**
```json
{
    "success": true,
    "document_id": "doc_12345",
    "filename": "document.docx",
    "message": "Document uploaded successfully"
}
```

#### Process Document / 处理文档
```http
POST /api/process_document
Content-Type: application/json

{
    "document_id": "doc_12345",
    "modifications": [
        {
            "original": "原文本",
            "modified": "修改后文本",
            "reason": "修改原因"
        }
    ]
}
```

**Response / 响应:**
```json
{
    "success": true,
    "processed_document_id": "proc_12345",
    "changes_applied": 5,
    "message": "Document processed successfully"
}
```

#### Get Document Information / 获取文档信息
```http
GET /api/document_info/{document_id}
```

**Response / 响应:**
```json
{
    "success": true,
    "document_id": "doc_12345",
    "filename": "document.docx",
    "size": 1024,
    "pages": 5,
    "created_at": "2025-06-12T15:30:00Z",
    "status": "processed"
}
```

### 3. File Management / 文件管理

#### Download Processed Document / 下载处理后的文档
```http
GET /api/download/{document_id}
```

**Response / 响应:**
Binary file download / 二进制文件下载

#### Delete Document / 删除文档
```http
DELETE /api/document/{document_id}
```

**Response / 响应:**
```json
{
    "success": true,
    "message": "Document deleted successfully"
}
```

## CORS Support / CORS支持

The API supports Cross-Origin Resource Sharing (CORS) for the following origins:
API支持以下源的跨域资源共享(CORS)：

- `http://localhost:3000`
- `http://localhost:8080`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:8080`

### CORS Headers / CORS头
- `Access-Control-Allow-Origin`
- `Access-Control-Allow-Methods`
- `Access-Control-Allow-Headers`
- `Access-Control-Max-Age`

## Error Codes / 错误代码

| Code | Description / 描述 |
|------|-------------------|
| `INVALID_LANGUAGE` | Invalid language code / 无效的语言代码 |
| `FILE_NOT_FOUND` | File not found / 文件未找到 |
| `INVALID_FORMAT` | Invalid file format / 无效的文件格式 |
| `PROCESSING_ERROR` | Document processing error / 文档处理错误 |
| `UPLOAD_FAILED` | File upload failed / 文件上传失败 |

## Rate Limiting / 速率限制

Currently, no rate limiting is implemented.
目前未实施速率限制。

## Examples / 示例

### JavaScript Example / JavaScript示例
```javascript
// Get current language / 获取当前语言
fetch('/api/get_language')
  .then(response => response.json())
  .then(data => console.log(data));

// Set language / 设置语言
fetch('/api/set_language', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ language: 'en' })
})
.then(response => response.json())
.then(data => console.log(data));

// Auto load document / 自动加载文档
fetch('/api/auto_load', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    document: 'sample.docx',
    modifications: 'modifications.csv',
    auto_apply: false
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Python Example / Python示例
```python
import requests

# Get current language / 获取当前语言
response = requests.get('http://localhost:5000/api/get_language')
print(response.json())

# Set language / 设置语言
response = requests.post('http://localhost:5000/api/set_language', 
                        json={'language': 'en'})
print(response.json())

# Auto load document / 自动加载文档
response = requests.post('http://localhost:5000/api/auto_load', 
                        json={
                            'document': 'sample.docx',
                            'modifications': 'modifications.csv',
                            'auto_apply': False
                        })
print(response.json())
```

### cURL Example / cURL示例
```bash
# Get current language / 获取当前语言
curl -X GET http://localhost:5000/api/get_language

# Set language / 设置语言
curl -X POST http://localhost:5000/api/set_language \
  -H "Content-Type: application/json" \
  -d '{"language": "en"}'

# Auto load document / 自动加载文档
curl -X POST http://localhost:5000/api/auto_load \
  -H "Content-Type: application/json" \
  -d '{
    "document": "sample.docx",
    "modifications": "modifications.csv",
    "auto_apply": false
  }'
```

## Changelog / 更新日志

### Version 1.0.0 / 版本1.0.0
- Initial API release / 初始API发布
- Language management endpoints / 语言管理端点
- Document processing endpoints / 文档处理端点
- CORS support / CORS支持 