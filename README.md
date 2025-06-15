# Document Preview Editor / 文档预览编辑器

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-red.svg)](https://flask.palletsprojects.com/)

A powerful web-based document editing system that supports intelligent document processing with multi-language support. Features document comparison before and after modifications, and supports downloading modified documents while maintaining original formatting.

一个强大的基于Web的文档编辑系统，支持智能文档处理和多语言支持。支持修改前后的文档对比，支持对修改后的文件下载并且格式保持不变。

## ✨ Features / 功能特性

- 🌐 **Multi-language Support** / **多语言支持**: Chinese and English interface
- 📄 **Document Processing** / **文档处理**: Support for Word documents (.docx) and text files (.txt)
- 🔄 **Batch Modifications** / **批量修改**: Apply multiple text modifications at once
- 📊 **Real-time Preview** / **实时预览**: Live document preview with modifications
- 📊 **Document Comparison** / **修改前后文档对比**: Compare documents before and after modifications
- 📥 **Format-Preserving Download** / **下载修改后文档**: Download modified documents while maintaining original formatting
- 🌍 **Remote API Access** / **远程API访问**: RESTful API for programmatic access
- 📱 **Responsive Design** / **响应式设计**: Works on desktop and mobile devices
- 🔒 **Secure File Handling** / **安全文件处理**: Secure upload and processing
- 🚀 **Auto-load Support** / **自动加载支持**: Load documents and modifications from URLs

## 🚀 Quick Start / 快速开始

### Prerequisites / 前置要求

- Python 3.8 or higher / Python 3.8 或更高版本
- pip package manager / pip 包管理器

### Installation / 安装

1. **Clone the repository / 克隆仓库**
   ```bash
   git clone https://github.com/sawyer-shi/document-preview-editor.git
   cd document-preview-editor
   ```

2. **Install dependencies / 安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application / 运行应用**
   ```bash
   python run.py
   ```

4. **Access the application / 访问应用**
   
   Open your browser and navigate to: http://127.0.0.1:5000
   
   在浏览器中打开：http://127.0.0.1:5000

## 📖 Usage Guide / 使用指南

### Method 1: Manual Upload and Edit / 方式一：手动上传和编辑

This is the most straightforward way to use the Document Preview Editor.

这是使用文档预览编辑器最直接的方式。

#### Step 1: Access the Homepage / 步骤1：访问首页

1. Open your web browser / 打开网页浏览器
2. Navigate to `http://127.0.0.1:5000` / 导航到 `http://127.0.0.1:5000`
3. Choose your preferred language (Chinese/English) / 选择您的首选语言（中文/英文）

#### Step 2: Upload Document / 步骤2：上传文档

1. Click the **"Upload Document"** button / 点击**"上传文档"**按钮
2. Select a Word document (.docx file) from your computer / 从计算机中选择Word文档（.docx文件）
3. Wait for the upload and processing to complete / 等待上传和处理完成
4. The document content will be displayed in the preview area / 文档内容将显示在预览区域

#### Step 3: Add Modifications / 步骤3：添加修改条目

You can add modifications in several ways: / 您可以通过多种方式添加修改条目：

**Option A: Manual Entry / 选项A：手动输入**
1. Click **"Add Modification"** button / 点击**"添加修改条目"**按钮
2. Fill in the modification form: / 填写修改表单：
   - **Original Text** / **原始文本**: Text to be replaced
   - **New Text** / **新文本**: Replacement text
   - **Reason** / **原因**: Reason for the modification
3. Click **"Add"** to save the modification / 点击**"添加"**保存修改条目

**Option B: CSV File Upload / 选项B：CSV文件上传**
1. Prepare a CSV file with columns: `original_text`, `new_text`, `reason`
2. Click **"Upload CSV"** button / 点击**"上传CSV"**按钮
3. Select your CSV file / 选择您的CSV文件
4. All modifications will be imported automatically / 所有修改条目将自动导入

#### Step 4: Apply and Download / 步骤4：应用和下载

1. Review your modifications in the list / 在列表中查看您的修改条目
2. Click **"Apply Modifications"** to process the document / 点击**"应用修改"**处理文档
3. Preview the modified document / 预览修改后的文档
4. Click **"Download Modified Document"** to save the result / 点击**"下载修改后的文档"**保存结果

### Method 2: Remote API Access / 方式二：远程API接口调用

For programmatic access and integration with other systems.

用于程序化访问和与其他系统集成。

#### API Endpoints / API端点

**Base URL**: `http://127.0.0.1:5000/api`

#### Auto-load and Process / 自动加载和处理

**Endpoint**: `POST /api/auto_load`

This powerful endpoint allows you to load documents and modifications from various sources and optionally apply them automatically.

这个强大的端点允许您从各种来源加载文档和修改条目，并可选择自动应用它们。

**Request Examples / 请求示例:**

**Example 1: Load from URLs with Auto-apply / 示例1：从URL加载并自动应用**
```bash
curl -X POST http://127.0.0.1:5000/api/auto_load \
  -H "Content-Type: application/json" \
  -d '{
    "document": "https://example.com/document.docx",
    "modifications": "https://example.com/modifications.csv",
    "language": "en",
    "auto_apply": true
  }'
```

**Example 2: Load from Local Files / 示例2：从本地文件加载**
```bash
curl -X POST http://127.0.0.1:5000/api/auto_load \
  -F "document_file=@/path/to/document.docx" \
  -F "modifications_file=@/path/to/modifications.csv" \
  -F "language=zh" \
  -F "auto_apply=true"
```

**Example 3: JSON Modifications / 示例3：JSON格式修改条目**
```bash
curl -X POST http://127.0.0.1:5000/api/auto_load \
  -H "Content-Type: application/json" \
  -d '{
    "document": "https://example.com/document.docx",
    "modifications": [
      {
        "original_text": "old text",
        "new_text": "new text",
        "reason": "improvement"
      }
    ],
    "language": "en",
    "auto_apply": true
  }'
```

**Response Format / 响应格式:**
```json
{
  "success": true,
  "message": "Document and modifications loaded and applied successfully",
  "doc_id": "uuid-string",
  "filename": "document.docx",
  "modification_count": 5,
  "paragraph_changes": 3,
  "table_changes": 0,
  "download_url": "/api/download_document/uuid-string",
  "redirect_url": "/?doc_id=uuid-string&from_test=true"
}
```

#### Direct Document Download / 直接文档下载

**Endpoint**: `GET /api/download_document/{doc_id}`

Download the processed document directly without using the web interface.

直接下载处理后的文档，无需使用Web界面。

```bash
curl -O http://127.0.0.1:5000/api/download_document/{doc_id}
```

#### Step-by-step API Usage / 分步API使用

**Step 1: Upload Document / 步骤1：上传文档**
```bash
curl -X POST http://127.0.0.1:5000/api/upload_document \
  -F "document=@/path/to/document.docx"
```

**Step 2: Add Modifications / 步骤2：添加修改条目**
```bash
curl -X POST http://127.0.0.1:5000/api/add_modifications \
  -H "Content-Type: application/json" \
  -d '{
    "doc_id": "your-doc-id",
    "modifications": [
      {
        "original_text": "text to replace",
        "new_text": "replacement text",
        "reason": "reason for change"
      }
    ]
  }'
```

**Step 3: Download Result / 步骤3：下载结果**
```bash
curl -O http://127.0.0.1:5000/api/download_document/your-doc-id
```

## 🔧 Configuration / 配置

### Environment Variables / 环境变量

Create a `.env` file in the project root: / 在项目根目录创建 `.env` 文件：

```env
# Server Configuration / 服务器配置
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# File Upload Configuration / 文件上传配置
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads

# CORS Configuration / CORS配置
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
CORS_STRICT_MODE=false

# Language Configuration / 语言配置
DEFAULT_LANGUAGE=zh
SUPPORTED_LANGUAGES=zh,en
```

### Docker Deployment / Docker部署

**Build and run with Docker: / 使用Docker构建和运行：**

```bash
# Build the image / 构建镜像
docker build -t document-preview-editor .

# Run the container / 运行容器
docker run -p 5000:5000 document-preview-editor
```

**Using Docker Compose: / 使用Docker Compose：**

```bash
docker-compose up -d
```

## 📁 Project Structure / 项目结构

```
document-preview-editor/
├── app.py                      # Main application entry / 主应用入口
├── run.py                      # Application runner / 应用运行器
├── requirements.txt            # Python dependencies / Python依赖
├── config/                     # Configuration modules / 配置模块
│   ├── __init__.py
│   ├── config.py              # Main configuration / 主配置
│   └── cors_config.py         # CORS configuration / CORS配置
├── routes/                     # Route modules / 路由模块
│   ├── __init__.py
│   ├── api.py                 # Main API routes / 主API路由
│   ├── main.py                # Web interface routes / Web界面路由
│   ├── document_routes.py     # Document handling / 文档处理
│   ├── modification_routes.py # Modification handling / 修改处理
│   ├── utility_routes.py      # Utility functions / 工具功能
│   └── auto_load_routes.py    # Auto-load functionality / 自动加载功能
├── utils/                      # Utility modules / 工具模块
│   ├── __init__.py
│   ├── document_processor.py  # Document processing / 文档处理
│   ├── i18n.py               # Internationalization / 国际化
│   └── logger.py             # Multi-language logging / 多语言日志
├── templates/                  # HTML templates / HTML模板
│   ├── index.html            # Main interface / 主界面
│   └── api_test.html         # API testing interface / API测试界面
├── static/                     # Static files / 静态文件
│   ├── css/
│   ├── js/
│   └── images/
├── api_test_module/           # API testing samples / API测试样例
│   └── samples/
├── uploads/                   # Upload directory / 上传目录
├── temp/                      # Temporary files / 临时文件
└── logs/                      # Application logs / 应用日志
```

## 🔍 API Testing / API测试

The application includes a built-in API testing interface:

应用程序包含内置的API测试界面：

1. Navigate to `http://127.0.0.1:5000/test` / 导航到 `http://127.0.0.1:5000/test`
2. Download sample files for testing / 下载测试样例文件
3. Test different API scenarios: / 测试不同的API场景：
   - File upload testing / 文件上传测试
   - URL-based loading / 基于URL的加载
   - JSON modification testing / JSON修改条目测试
   - Auto-apply functionality / 自动应用功能

## 🛠️ Development / 开发

### Setting up Development Environment / 设置开发环境

1. **Clone and setup / 克隆和设置**
   ```bash
   git clone https://github.com/sawyer-shi/document-preview-editor.git
   cd document-preview-editor
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run in development mode / 以开发模式运行**
   ```bash
   export FLASK_ENV=development
   export FLASK_DEBUG=True
   python run.py
   ```

### Adding New Features / 添加新功能

The modular structure makes it easy to extend:

模块化结构使扩展变得容易：

- **New API endpoints**: Add to appropriate route modules / **新API端点**：添加到适当的路由模块
- **Document processors**: Extend `utils/document_processor.py` / **文档处理器**：扩展 `utils/document_processor.py`
- **Languages**: Update `utils/i18n.py` / **语言**：更新 `utils/i18n.py`
- **Logging**: Use `utils/logger.py` for multi-language logs / **日志**：使用 `utils/logger.py` 进行多语言日志

## 📝 License / 许可证

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

本项目采用Apache License 2.0许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 🤝 Contributing / 贡献

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献！请随时提交Pull Request。

## 📞 Support / 支持

If you encounter any issues or have questions:

如果您遇到任何问题或有疑问：

- Create an issue on GitHub / 在GitHub上创建issue
- Check the API testing interface for examples / 查看API测试界面获取示例
- Review the logs in the `logs/` directory / 查看 `logs/` 目录中的日志

## 🔄 Version History / 版本历史

- **v1.0.0** - Initial release with full functionality / 初始版本，具备完整功能
  - Multi-language support / 多语言支持
  - Document processing / 文档处理
  - RESTful API / RESTful API
  - Auto-load functionality / 自动加载功能
  - Modular architecture / 模块化架构

---

**Made with ❤️ by sawyer-shi** / **由 sawyer-shi 用 ❤️ 制作** 