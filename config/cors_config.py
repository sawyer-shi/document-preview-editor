#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document Preview Editor
Copyright (c) 2025 sawyer-shi
Licensed under the Apache License, Version 2.0

CORS跨域配置模块 / CORS Configuration Module
Handles Cross-Origin Resource Sharing configuration for the application
处理应用程序的跨域资源共享配置
"""

import os
from typing import List, Optional
from flask import Blueprint, request, jsonify

class CORSConfig:
    """
    CORS跨域配置类 / CORS Configuration Class
    Manages CORS settings and policies for the application
    管理应用程序的CORS设置和策略
    """
    
    # 默认允许的域名列表 / Default allowed origins list
    DEFAULT_ALLOWED_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:8080',
        'http://localhost:5000',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:8080', 
        'http://127.0.0.1:5000',
        'https://localhost:3000',
        'https://localhost:8080',
        'https://localhost:5000',
        'https://127.0.0.1:3000',
        'https://127.0.0.1:8080',
        'https://127.0.0.1:5000',
    ]
    
    # 允许的请求头 / Allowed request headers
    ALLOWED_HEADERS = [
        'Content-Type',
        'Authorization',
        'X-Requested-With',
        'Accept',
        'Origin',
        'X-Custom-Header',
        'Cache-Control',
        'Pragma',
        'X-API-Key',
        'X-Client-Version'
    ]
    
    # 允许的HTTP方法 / Allowed HTTP methods
    ALLOWED_METHODS = [
        'GET',
        'POST',
        'PUT',
        'DELETE',
        'OPTIONS',
        'HEAD',
        'PATCH'
    ]
    
    # 暴露的响应头 / Exposed response headers
    EXPOSED_HEADERS = [
        'Content-Disposition',
        'Content-Length',
        'Content-Type',
        'X-Total-Count',
        'X-Page-Count'
    ]
    
    @classmethod
    def get_allowed_origins(cls) -> List[str]:
        """
        获取允许的域名列表 / Get allowed origins list
        Returns a list of allowed origins from default and environment variables
        从默认设置和环境变量返回允许的域名列表
        """
        # 从环境变量读取额外的允许域名 / Read additional allowed origins from environment variables
        env_origins = os.environ.get('CORS_ALLOWED_ORIGINS', '')
        additional_origins = [origin.strip() for origin in env_origins.split(',') if origin.strip()]
        
        # 合并默认域名和环境变量中的域名 / Merge default origins with environment origins
        all_origins = cls.DEFAULT_ALLOWED_ORIGINS + additional_origins
        
        # 去重并返回 / Remove duplicates and return
        return list(set(all_origins))
    
    @classmethod
    def is_origin_allowed(cls, origin: Optional[str], debug_mode: bool = False) -> bool:
        """
        检查域名是否被允许 / Check if origin is allowed
        Validates if the given origin is permitted to access the API
        验证给定的域名是否被允许访问API
        """
        if not origin:
            return True
        
        # 开发模式下允许所有域名 / Allow all origins in debug mode
        if debug_mode:
            return True
        
        # 检查是否在允许列表中 / Check if origin is in allowed list
        allowed_origins = cls.get_allowed_origins()
        return origin in allowed_origins
    
    @classmethod
    def get_cors_headers(cls, origin: Optional[str] = None, debug_mode: bool = False) -> dict:
        """
        获取CORS响应头 / Get CORS response headers
        Returns appropriate CORS headers based on origin and debug mode
        根据域名和调试模式返回适当的CORS头
        """
        headers = {}
        
        # 设置允许的域名 / Set allowed origin
        if cls.is_origin_allowed(origin, debug_mode):
            headers['Access-Control-Allow-Origin'] = origin or '*'
        else:
            # 根据安全策略决定是否允许未知域名 / Decide whether to allow unknown origins based on security policy
            strict_mode = os.environ.get('CORS_STRICT_MODE', 'false').lower() == 'true'
            if not strict_mode:
                headers['Access-Control-Allow-Origin'] = '*'
        
        # 设置其他CORS头 / Set other CORS headers
        headers.update({
            'Access-Control-Allow-Headers': ', '.join(cls.ALLOWED_HEADERS),
            'Access-Control-Allow-Methods': ', '.join(cls.ALLOWED_METHODS),
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '86400',
            'Access-Control-Expose-Headers': ', '.join(cls.EXPOSED_HEADERS)
        })
        
        return headers

def setup_cors(blueprint: Blueprint, debug_mode: bool = False):
    """
    设置蓝图的CORS配置 / Setup CORS configuration for blueprint
    Configures CORS handling for the given Flask blueprint
    为给定的Flask蓝图配置CORS处理
    
    Args:
        blueprint: Flask blueprint to configure / 要配置的Flask蓝图
        debug_mode: Whether to enable debug mode / 是否启用调试模式
    """
    
    @blueprint.after_request
    def after_request(response):
        """
        添加CORS头到所有响应 / Add CORS headers to all responses
        Automatically adds appropriate CORS headers to every response
        自动为每个响应添加适当的CORS头
        """
        origin = request.headers.get('Origin')
        cors_headers = CORSConfig.get_cors_headers(origin, debug_mode)
        
        for header, value in cors_headers.items():
            response.headers[header] = value
        
        return response
    
    @blueprint.route('/<path:path>', methods=['OPTIONS'])
    def handle_options(path):
        """
        处理所有路径的OPTIONS预检请求 / Handle OPTIONS preflight requests for all paths
        Responds to CORS preflight requests with appropriate headers
        使用适当的头响应CORS预检请求
        """
        origin = request.headers.get('Origin')
        cors_headers = CORSConfig.get_cors_headers(origin, debug_mode)
        
        response = jsonify({'status': 'ok'})
        for header, value in cors_headers.items():
            response.headers[header] = value
        
        return response

# 便捷函数 / Convenience functions
def get_cors_headers(origin: Optional[str] = None, debug_mode: bool = False) -> dict:
    """
    获取CORS响应头的便捷函数 / Convenience function to get CORS response headers
    Wrapper function for easy access to CORS headers
    用于轻松访问CORS头的包装函数
    """
    return CORSConfig.get_cors_headers(origin, debug_mode)

def is_origin_allowed(origin: Optional[str], debug_mode: bool = False) -> bool:
    """
    检查域名是否被允许的便捷函数 / Convenience function to check if origin is allowed
    Wrapper function for easy origin validation
    用于轻松验证域名的包装函数
    """
    return CORSConfig.is_origin_allowed(origin, debug_mode) 