#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document Preview Editor
Copyright (c) 2025 sawyer-shi
Licensed under the Apache License, Version 2.0

配置包初始化文件
Configuration Package Initialization
"""

# 导入配置类
from .config import Config, DevelopmentConfig, ProductionConfig, TestingConfig

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# 导出配置
__all__ = ['Config', 'DevelopmentConfig', 'ProductionConfig', 'TestingConfig', 'config'] 