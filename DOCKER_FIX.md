# Docker Win32com 错误修复说明

## 问题描述

在使用 Docker 运行项目时遇到以下错误：
```
ModuleNotFoundError: No module named 'win32com'
```

## 原因分析

- `win32com` 是 Windows 特有的 COM 组件模块
- Docker 容器通常运行在 Linux 环境中
- Linux 环境不支持 Windows 特有的 COM 组件

## 解决方案

### 1. 代码修复 ✅

修改了 `utils/document_processor.py` 文件：

```python
# 条件导入 Windows 特有的模块
try:
    if os.name == 'nt':  # 只在 Windows 环境下导入
        import win32com.client as win32
        import pythoncom
        WINDOWS_COM_AVAILABLE = True
    else:
        WINDOWS_COM_AVAILABLE = False
except ImportError:
    WINDOWS_COM_AVAILABLE = False
```

### 2. Docker 优化 ✅

#### 创建专门的 Docker Requirements
- `requirements-docker.txt`: 不包含 Windows 特有依赖
- 移除了 `pywin32` 依赖

#### 优化 Dockerfile
- 添加了多种文档处理工具：`antiword`, `catdoc`, `pandoc`
- 改进了依赖安装流程
- 添加了健康检查

#### 改进 .dockerignore
- 排除不必要的文件，减小构建上下文

### 3. 功能兼容 ✅

- **Windows 环境**: 自动使用 win32com 进行高质量 DOC 转换
- **Linux/Docker 环境**: 使用替代工具：
  - LibreOffice
  - antiword
  - catdoc
  - Python 库解析

## 使用方法

### Docker 部署

```bash
# 构建镜像
docker build -t document-preview-editor .

# 运行容器
docker run -p 5000:5000 document-preview-editor

# 或使用 Docker Compose
docker-compose up -d
```

### 本地开发

```bash
# Windows 环境（支持完整功能）
python run.py

# Linux 环境（使用替代工具）
python run.py
```

## 文档处理能力对比

| 环境 | DOC 转换 | DOCX 处理 | TXT 转换 |
|------|----------|-----------|----------|
| Windows | ✅ 完整支持 | ✅ | ✅ |
| Linux/Docker | ✅ 基础支持 | ✅ | ✅ |

## 验证修复

运行以下命令验证修复是否成功：

```bash
# 测试导入
python -c "from utils.document_processor import EnhancedWordProcessor; print('✅ 修复成功')"

# 测试应用启动
python run.py
```

## 注意事项

1. **Docker 环境**：DOC 文件转换质量可能略低于 Windows 环境
2. **推荐格式**：建议优先使用 DOCX 格式以获得最佳体验
3. **功能完整性**：所有核心功能在 Docker 环境下都可正常使用

## 技术细节

### 条件导入机制
```python
# 检查操作系统和依赖可用性
if os.name == 'nt' and WINDOWS_COM_AVAILABLE:
    # 使用 Windows COM 组件
    result = self._convert_with_win32com(doc_path)
else:
    # 使用跨平台替代方案
    result = self._convert_with_alternative_tools(doc_path)
```

### 替代工具链
1. **LibreOffice**: 主要的跨平台文档转换工具
2. **antiword**: 专门处理 DOC 文件的轻量级工具
3. **catdoc**: 另一个 DOC 文件处理工具
4. **pandoc**: 通用文档转换工具

---

**修复完成** ✅  
现在可以在 Docker 环境中正常运行项目了！ 