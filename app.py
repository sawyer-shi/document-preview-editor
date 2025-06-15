#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document Preview Editor
Copyright (c) 2025 sawyer-shi
Licensed under the Apache License, Version 2.0
https://github.com/sawyer-shi/document-preview-editor

文档预览编辑器主应用模块
Document Preview Editor Main Application Module
"""

import os
from flask import Flask, request, jsonify

from config import config
from config.cors_config import get_cors_headers
from utils.i18n import i18n
from routes.main import main_bp
from routes.api import api_bp

def create_app(config_name=None):
    """应用工厂函数"""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 全局CORS配置 - 处理来自其他应用服务的跨域请求
    @app.before_request
    def handle_preflight():
        """处理预检请求"""
        if request.method == "OPTIONS":
            response = jsonify({'status': 'ok'})
            
            # 使用CORS配置模块获取响应头
            origin = request.headers.get('Origin')
            debug_mode = app.config.get('DEBUG', False)
            cors_headers = get_cors_headers(origin, debug_mode)
            
            # 添加CORS头到响应
            for header, value in cors_headers.items():
                response.headers.add(header, value)
            
            return response

    @app.after_request
    def after_request(response):
        """为所有响应添加CORS头"""
        # 获取请求来源和调试模式
        origin = request.headers.get('Origin')
        debug_mode = app.config.get('DEBUG', False)
        
        # 使用CORS配置模块获取响应头
        cors_headers = get_cors_headers(origin, debug_mode)
        
        # 添加CORS头到响应
        for header, value in cors_headers.items():
            response.headers.add(header, value)
        
        return response
    
    # 初始化国际化支持
    i18n.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 创建必要的目录
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
    os.makedirs(app.config.get('TEMP_FOLDER', 'temp'), exist_ok=True)
    
    return app

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    # 获取配置
    config_obj = app.config
    
    # 启动应用
    app.run(
        debug=config_obj.get('DEBUG', True),
        host=config_obj.get('HOST', '0.0.0.0'),
        port=config_obj.get('PORT', 5000)
    ) 