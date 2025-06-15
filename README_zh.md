# 文档预览编辑器

一个强大的多格式文档预览和编辑工具，支持批量文本修改和一键处理。支持修改前后的文档对比，支持对修改后的文件下载并且格式保持不变。

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.7+-green.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-red.svg)](https://flask.palletsprojects.com/)

## ✨ 特性

### 🌍 多语言支持
- 🇨🇳 完整的中文界面支持
- 🇺🇸 全英文界面支持
- 🔄 动态语言切换

### 📄 文档格式支持
- 📝 **DOCX** - Microsoft Word 2007+ 文档
- 📄 **TXT** - 纯文本文件 (UTF-8, GBK, GB2312)
- 🔄 统一输出为DOCX格式

### 🚀 核心功能
- 📤 **文档上传预览** - 支持拖拽上传
- ✏️ **批量文本修改** - 智能文本替换
- 🔍 **智能文本匹配** - 精确定位修改内容
- 📊 **实时预览** - 实时显示文档修改效果
- 📊 **修改前后文档对比** - 支持修改前后的文档对比
- 📥 **一键下载处理后文档** - 即时生成结果
- 📥 **下载修改后文档** - 支持下载修改后的文档，并且文本格式和原文档保持不变
- 🌐 **RESTful API支持** - 完整API接口
- 🐳 **Docker容器化部署** - 一键部署

### 🎨 用户体验
- 📱 响应式设计，支持移动端
- 🎯 直观的拖拽上传界面
- ⚡ 实时处理进度显示
- 🔗 支持API直接跳转访问

## 🚀 四种安装方式

### 方式一：源码安装运行

```bash
# 克隆项目
git clone https://github.com/sawyer-shi/document-preview-editor.git
cd document-preview-editor

# 安装依赖
pip install -r requirements.txt

# 运行项目
python run.py
```

### 方式二：Python虚拟环境安装运行

```bash
# 克隆项目
git clone https://github.com/sawyer-shi/document-preview-editor.git
cd document-preview-editor

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行项目
python run.py
```

### 方式三：Conda环境安装运行

```bash
# 克隆项目
git clone https://github.com/sawyer-shi/document-preview-editor.git
cd document-preview-editor

# 创建conda环境
conda create -n document-editor python=3.9
conda activate document-editor

# 安装依赖
pip install -r requirements.txt

# 运行项目
python run.py
```

### 方式四：Docker容器安装运行

```bash
# 克隆项目
git clone https://github.com/sawyer-shi/document-preview-editor.git
cd document-preview-editor

# 使用Docker Compose运行
docker-compose up -d

# 或者自定义端口运行
HOST_PORT=8080 docker-compose up -d

# 查看运行状态
docker-compose ps

# 停止服务
docker-compose down
```

## 🌐 两种访问方式

### 方式一：直接URL访问

启动成功后，通过以下URL访问系统：

- **本地访问**: http://127.0.0.1:5000
- **网络访问**: http://YOUR_IP:5000

### 方式二：API接口跳转访问

⭐ **重点功能：组装接口连接跳转访问**

这种方式允许用户直接通过URL传递原文和修改内容，实现一键批量处理：

#### 一键处理API

```http
POST /api/process_document
Content-Type: multipart/form-data

# 表单数据包含：
- document: [文件]
- modifications: [JSON字符串]
```

#### JavaScript调用示例

```javascript
// 准备修改数据
const modifications = [
    {
        original_text: "原始文本",
        new_text: "修改后文本",
        reason: "修改原因"
    }
];

// 创建表单数据  
const formData = new FormData();
formData.append('document', fileInput.files[0]);
formData.append('modifications', JSON.stringify(modifications));

// 发送请求
fetch('/api/process_document', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // 直接跳转下载
        window.location.href = `/api/download_document/${data.doc_id}`;
    }
});
```

#### Python调用示例

```python
import requests
import json

# 准备数据
modifications = [
    {
        "original_text": "AI技术基础架构",
        "new_text": "AI技术基础架构2.0",
        "reason": "版本升级"
    }
]

# 发送请求
with open('document.docx', 'rb') as f:
    files = {'document': f}
    data = {'modifications': json.dumps(modifications)}
    
    response = requests.post(
        'http://127.0.0.1:5000/api/process_document',
        files=files,
        data=data
    )
    
    if response.json()['success']:
        doc_id = response.json()['doc_id']
        download_url = f'http://127.0.0.1:5000/api/download_document/{doc_id}'
        print(f"下载链接：{download_url}")
```

## 📚 完整API文档

### 1. 文档上传
```http
POST /api/upload_document
Content-Type: multipart/form-data
Body: document=[文件]
```

### 2. 添加修改条目
```http
POST /api/add_modifications
Content-Type: application/json
Body: {
    "doc_id": "文档ID",
    "modifications": [
        {
            "original_text": "原始文本",
            "new_text": "修改后文本", 
            "reason": "修改原因"
        }
    ]
}
```

### 3. 一键批量处理 (⭐核心API)
```http  
POST /api/process_document
Content-Type: multipart/form-data
Body: 
    - document=[文件]
    - modifications=[JSON修改数据]
```

### 4. 下载处理后文档
```http
GET /api/download_document/{doc_id}
```

### 5. 获取文档信息
```http
GET /api/document_info/{doc_id}
```

## ⚙️ 环境配置

创建 `.env` 文件进行自定义配置：

```bash
# 应用配置
HOST=0.0.0.0
PORT=5000
DEBUG=true
SECRET_KEY=your-secret-key-here

# Flask环境
FLASK_ENV=development
FLASK_APP=app.py

# 安全配置
MAX_CONTENT_LENGTH=52428800  # 50MB
```

## 🐳 Docker部署

### 基础部署
```bash
docker-compose up -d
```

### 自定义端口部署
```bash
HOST_PORT=8080 docker-compose up -d
```

### 生产环境部署
```bash
# 设置环境变量
export SECRET_KEY=your-production-secret-key
export DEBUG=false
export FLASK_ENV=production

# 启动服务
docker-compose -f docker-compose.prod.yml up -d
```

## 📋 系统要求

- **Python**: 3.7+ 
- **内存**: 512MB+
- **存储**: 100MB+
- **支持的操作系统**: Windows, Linux, macOS

## 🔧 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --no-cache-dir
   ```

2. **端口占用**
   ```bash
   # 修改端口
   export PORT=8080
   python run.py
   ```

3. **文件上传失败**
   - 检查文件大小是否超过50MB限制
   - 确认文件格式为DOCX/DOC/TXT

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支  
5. 创建Pull Request

## 📄 许可证

本项目基于 [Apache 2.0 许可证](LICENSE) 开源。

## 👨‍💻 作者

**sawyer-shi**
- GitHub: [@sawyer-shi](https://github.com/sawyer-shi)
- 项目地址: [document-preview-editor](https://github.com/sawyer-shi/document-preview-editor)

## 🙏 致谢

感谢所有为此项目做出贡献的开发者和用户！

---

## 🌟 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/sawyer-shi/document-preview-editor.git

# 2. 进入目录  
cd document-preview-editor

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动应用
python run.py

# 5. 访问应用
# 打开浏览器访问: http://127.0.0.1:5000
```

**立即开始使用文档预览编辑器，体验强大的文档批量编辑功能！** 🚀 