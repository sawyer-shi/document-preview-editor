#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document Preview Editor
Copyright (c) 2025 sawyer-shi
Licensed under the Apache License, Version 2.0
https://github.com/sawyer-shi/document-preview-editor

文档预览编辑器启动脚本
Document Preview Editor Startup Script

Copyright 2025 sawyer-shi
Licensed under the Apache License, Version 2.0
https://github.com/sawyer-shi
"""

import os
import sys
import subprocess
import platform
from app import create_app
from config import Config

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)

def install_requirements():
    """安装依赖包"""
    print("检查并安装依赖包...")
    print("Checking and installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖包安装完成")
        print("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"依赖包安装失败: {e}")
        print(f"Failed to install dependencies: {e}")
        sys.exit(1)

def create_directories():
    """创建必要的目录"""
    directories = ['templates', 'static', 'static/css', 'static/js']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def start_application():
    """启动应用"""
    print("\n" + "="*50)
    print("启动Document Preview Editor...")
    print("Starting Document Preview Editor...")
    print("="*50)
    
    # 设置环境变量
    os.environ['FLASK_APP'] = 'app.py'
    os.environ['FLASK_ENV'] = 'development'
    
    try:
        # 启动Flask应用
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n应用已停止")
        print("Application stopped")
    except Exception as e:
        print(f"启动失败: {e}")
        print(f"Failed to start: {e}")

def main():
    """主函数"""
    print("Document Preview Editor / Document Preview Editor")
    print("Version 1.0.0")
    print("-" * 50)
    
    # 检查Python版本
    check_python_version()
    
    # 检查必要文件是否存在
    required_files = ['app.py', 'requirements.txt']
    for file in required_files:
        if not os.path.exists(file):
            print(f"错误: 缺少必要文件 {file}")
            print(f"Error: Missing required file {file}")
            sys.exit(1)
    
    # 创建必要目录
    create_directories()
    
    # 安装依赖
    if '--skip-install' not in sys.argv:
        install_requirements()
    
    # 启动应用
    start_application()

if __name__ == "__main__":
    main() 