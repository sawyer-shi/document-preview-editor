# Document Preview Editor

<div align="center">

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-red.svg)](https://flask.palletsprojects.com/)

**Language / 语言:** 
[🇺🇸 English](#english) | [🇨🇳 中文](#中文)

</div>

---

## English

<div id="english">

### 🌟 Overview

A powerful web-based document editing system that supports intelligent document processing with multi-language support. Features document comparison before and after modifications, and supports downloading modified documents while maintaining original formatting.

![image](https://github.com/user-attachments/assets/a7257b1f-a7e3-4709-893a-f8aaf5319be9)
![image](https://github.com/user-attachments/assets/2705459e-f692-4e5c-b6da-d5b7c6bada04)



### ✨ Features

- 🌐 **Multi-language Support**: Chinese and English interface with dynamic switching
- 📄 **Document Processing**: Support for Word documents (.docx) and text files (.txt)
- 🔄 **Batch Modifications**: Apply multiple text modifications at once
- 📊 **Real-time Preview**: Live document preview with modifications
- 📊 **Document Comparison**: Compare documents before and after modifications
- 📥 **Format-Preserving Download**: Download modified documents while maintaining original formatting
- 🌍 **Remote API Access**: RESTful API for programmatic access
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🔒 **Secure File Handling**: Secure upload and processing
- 🚀 **Auto-load Support**: Load documents and modifications from URLs
- 🐳 **Docker Support**: Containerized deployment ready

### 🚀 Quick Start

#### Prerequisites

- Python 3.8 or higher
- pip package manager

#### Installation Methods

**Method 1: Direct Installation**
```bash
# Clone the repository
git clone https://github.com/sawyer-shi/document-preview-editor.git
cd document-preview-editor

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

**Method 2: Virtual Environment**
```bash
# Clone the repository
git clone https://github.com/sawyer-shi/document-preview-editor.git
cd document-preview-editor

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

**Method 3: Conda Environment**
```bash
# Clone the repository
git clone https://github.com/sawyer-shi/document-preview-editor.git
cd document-preview-editor

# Create conda environment
conda create -n document-editor python=3.9
conda activate document-editor

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

**Method 4: Docker Deployment**
```bash
# Clone the repository
git clone https://github.com/sawyer-shi/document-preview-editor.git
cd document-preview-editor

# Run with Docker Compose
docker-compose up -d

# Custom port deployment
HOST_PORT=8080 docker-compose up -d

# Check status
docker-compose ps

# Stop services
docker-compose down
```

#### Access the Application

After successful startup, access the system via:

- **Local Access**: http://127.0.0.1:5000
- **Network Access**: http://YOUR_IP:5000

### 📖 Usage Guide

#### Method 1: Manual Upload and Edit

**Step 1: Access Homepage**
1. Open your web browser
2. Navigate to `http://127.0.0.1:5000`
3. Choose your preferred language (Chinese/English)

**Step 2: Upload Document**
1. Click the **"Upload Document"** button
2. Select a Word document (.docx file) from your computer
3. Wait for the upload and processing to complete
4. The document content will be displayed in the preview area

**Step 3: Add Modifications**

**Option A: Manual Entry**
1. Click **"Add Modification"** button
2. Fill in the modification form:
   - **Original Text**: Text to be replaced
   - **New Text**: Replacement text
   - **Reason**: Reason for the modification
3. Click **"Add"** to save the modification

**Option B: CSV File Upload**
1. Prepare a CSV file with columns: `original_text`, `new_text`, `reason`
2. Click **"Upload CSV"** button
3. Select your CSV file
4. All modifications will be imported automatically

**Step 4: Apply and Download**
1. Review your modifications in the list
2. Click **"Apply Modifications"** to process the document
3. Preview the modified document
4. Click **"Download Modified Document"** to save the result

#### Method 2: Remote API Access

**Base URL**: `http://127.0.0.1:5000/api`

**Auto-load and Process Endpoint**: `POST /api/auto_load`

**Example 1: Load from URLs with Auto-apply**
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

**Example 2: Load from Local Files**
```bash
curl -X POST http://127.0.0.1:5000/api/auto_load \
  -F "document_file=@/path/to/document.docx" \
  -F "modifications_file=@/path/to/modifications.csv" \
  -F "language=en" \
  -F "auto_apply=true"
```

**Example 3: JSON Modifications**
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

### 🔧 Configuration

#### Environment Variables

Create a `.env` file in the project root:

```env
# Server Configuration
HOST=0.0.0.0
PORT=5000
DEBUG=True

# Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads
TEMP_FOLDER=temp

# Security
SECRET_KEY=your-secret-key-here

# Language Settings
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,zh
```

### 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

### 👤 Author

**Sawyer Shi**
- GitHub: [@sawyer-shi](https://github.com/sawyer-shi)
- Project Link: [https://github.com/sawyer-shi/document-preview-editor](https://github.com/sawyer-shi/document-preview-editor)

### 🙏 Acknowledgments

- Flask Web Framework
- Python-docx Library
- All contributors and users

</div>

---

## 中文

<div id="中文">

### 🌟 项目概述

一个强大的基于Web的文档编辑系统，支持智能文档处理和多语言支持。支持修改前后的文档对比，支持对修改后的文件下载并且格式保持不变。

![image](https://github.com/user-attachments/assets/a7257b1f-a7e3-4709-893a-f8aaf5319be9)
![image](https://github.com/user-attachments/assets/2705459e-f692-4e5c-b6da-d5b7c6bada04)

### ✨ 功能特性

- 🌐 **多语言支持**: 中文和英文界面，支持动态切换
- 📄 **文档处理**: 支持Word文档(.docx)和文本文件(.txt)
- 🔄 **批量修改**: 一次性应用多个文本修改
- 📊 **实时预览**: 实时显示文档修改效果
- 📊 **文档对比**: 支持修改前后的文档对比
- 📥 **格式保持下载**: 下载修改后文档，保持原有格式
- 🌍 **远程API访问**: 提供RESTful API接口
- 📱 **响应式设计**: 支持桌面端和移动端
- 🔒 **安全文件处理**: 安全的文件上传和处理
- 🚀 **自动加载支持**: 从URL加载文档和修改内容
- 🐳 **Docker支持**: 支持容器化部署

### 🚀 快速开始

#### 环境要求

- Python 3.8 或更高版本
- pip 包管理器

#### 安装方式

**方式一：源码直接安装**
```bash
# 克隆项目
git clone https://github.com/sawyer-shi/document-preview-editor.git
cd document-preview-editor

# 安装依赖
pip install -r requirements.txt

# 运行项目
python run.py
```

**方式二：虚拟环境安装**
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

**方式三：Conda环境安装**
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

**方式四：Docker容器部署**
```bash
# 克隆项目
git clone https://github.com/sawyer-shi/document-preview-editor.git
cd document-preview-editor

# 使用Docker Compose运行
docker-compose up -d

# 自定义端口运行
HOST_PORT=8080 docker-compose up -d

# 查看运行状态
docker-compose ps

# 停止服务
docker-compose down
```

#### 访问应用

启动成功后，通过以下URL访问系统：

- **本地访问**: http://127.0.0.1:5000
- **网络访问**: http://YOUR_IP:5000

### 📖 使用指南

#### 方式一：手动上传和编辑

**步骤1：访问首页**
1. 打开网页浏览器
2. 导航到 `http://127.0.0.1:5000`
3. 选择您的首选语言（中文/英文）

**步骤2：上传文档**
1. 点击**"上传文档"**按钮
2. 从计算机中选择Word文档（.docx文件）
3. 等待上传和处理完成
4. 文档内容将显示在预览区域

**步骤3：添加修改条目**

**选项A：手动输入**
1. 点击**"添加修改条目"**按钮
2. 填写修改表单：
   - **原始文本**: 要替换的文本
   - **新文本**: 替换后的文本
   - **原因**: 修改原因
3. 点击**"添加"**保存修改条目

**选项B：CSV文件上传**
1. 准备包含 `original_text`, `new_text`, `reason` 列的CSV文件
2. 点击**"上传CSV"**按钮
3. 选择您的CSV文件
4. 所有修改条目将自动导入

**步骤4：应用和下载**
1. 在列表中查看您的修改条目
2. 点击**"应用修改"**处理文档
3. 预览修改后的文档
4. 点击**"下载修改后的文档"**保存结果

#### 方式二：远程API访问

**基础URL**: `http://127.0.0.1:5000/api`

**自动加载和处理端点**: `POST /api/auto_load`

**示例1：从URL加载并自动应用**
```bash
curl -X POST http://127.0.0.1:5000/api/auto_load \
  -H "Content-Type: application/json" \
  -d '{
    "document": "https://example.com/document.docx",
    "modifications": "https://example.com/modifications.csv",
    "language": "zh",
    "auto_apply": true
  }'
```

**示例2：从本地文件加载**
```bash
curl -X POST http://127.0.0.1:5000/api/auto_load \
  -F "document_file=@/path/to/document.docx" \
  -F "modifications_file=@/path/to/modifications.csv" \
  -F "language=zh" \
  -F "auto_apply=true"
```

**示例3：JSON格式修改条目**
```bash
curl -X POST http://127.0.0.1:5000/api/auto_load \
  -H "Content-Type: application/json" \
  -d '{
    "document": "https://example.com/document.docx",
    "modifications": [
      {
        "original_text": "旧文本",
        "new_text": "新文本",
        "reason": "改进"
      }
    ],
    "language": "zh",
    "auto_apply": true
  }'
```

### 🔧 配置说明

#### 环境变量

在项目根目录创建 `.env` 文件：

```env
# 服务器配置
HOST=0.0.0.0
PORT=5000
DEBUG=True

# 上传配置
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=uploads
TEMP_FOLDER=temp

# 安全配置
SECRET_KEY=你的密钥

# 语言设置
DEFAULT_LANGUAGE=zh
SUPPORTED_LANGUAGES=en,zh
```

### 🤝 贡献指南

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

### 📝 许可证

本项目基于Apache License 2.0许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

### 👤 作者

**Sawyer Shi**
- GitHub: [@sawyer-shi](https://github.com/sawyer-shi)
- 项目链接: [https://github.com/sawyer-shi/document-preview-editor](https://github.com/sawyer-shi/document-preview-editor)

### 🙏 致谢

- Flask Web框架
- Python-docx库
- 所有贡献者和用户

</div>
