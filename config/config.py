#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document Preview Editor
Copyright (c) 2025 sawyer-shi
Licensed under the Apache License, Version 2.0
https://github.com/sawyer-shi/document-preview-editor

配置文件模块
Configuration Module

项目配置文件
Project Configuration

Copyright 2025 sawyer-shi
Licensed under the Apache License, Version 2.0
https://github.com/sawyer-shi
"""

import os
from datetime import timedelta

class Config:
    """基础配置类"""
    
    # 应用基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'document-preview-editor-secret-key-2024'
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'docx', 'doc', 'txt'}
    
    # 临时文件配置
    TEMP_FOLDER = 'temp'
    TEMP_FILE_LIFETIME = timedelta(hours=24)  # 临时文件保存24小时
    
    # 国际化配置
    LANGUAGES = {
        'zh': '中文',
        'en': 'English'
    }
    DEFAULT_LANGUAGE = 'zh'
    
    # API配置
    API_PREFIX = '/api'
    
    # 调试配置
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    
    def __init__(self):
        super().__init__()
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("生产环境必须设置SECRET_KEY环境变量")

class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = True
    TESTING = True

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 