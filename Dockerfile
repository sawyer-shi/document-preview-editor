# 使用Python 3.12官方镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# 安装系统依赖和文档处理工具
RUN apt-get update && apt-get install -y \
    # LibreOffice for document conversion
    libreoffice \
    # Document processing tools
    antiword \
    catdoc \
    pandoc \
    # System utilities
    file \
    libmagic1 \
    # Build dependencies for Python packages
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 复制Docker专用的requirements文件
COPY requirements-docker.txt requirements.txt

# 安装Python依赖
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 如果Docker专用requirements不存在，则使用标准requirements
COPY requirements.txt requirements-fallback.txt
RUN if [ ! -f requirements-docker.txt ]; then \
        pip install --no-cache-dir -r requirements-fallback.txt; \
    fi

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p uploads temp static/css static/js templates logs

# 设置权限
RUN chmod +x run.py app.py

# 设置默认环境变量（可以被docker-compose或运行时覆盖）
ENV HOST=0.0.0.0
ENV PORT=5000
ENV DEBUG=False
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# 启动命令
CMD ["python", "run.py"] 