#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main API routes module / 主API路由模块
Integrates all API route modules and provides CORS handling
整合所有API路由模块并提供CORS处理

Document Preview Editor
Copyright (c) 2025 sawyer-shi
Licensed under the Apache License, Version 2.0
https://github.com/sawyer-shi/document-preview-editor
"""

from flask import Blueprint, jsonify

from utils.i18n import get_text
from utils.logger import log_error
from config.cors_config import setup_cors

# Import all route modules / 导入所有路由模块
from .document_routes import document_bp
from .modification_routes import modification_bp
from .utility_routes import utility_bp
from .auto_load_routes import auto_load_bp

# Create main API blueprint / 创建主API蓝图
api_bp = Blueprint('api', __name__)

# Register all sub-blueprints / 注册所有子蓝图
api_bp.register_blueprint(document_bp)
api_bp.register_blueprint(modification_bp)
api_bp.register_blueprint(utility_bp)
api_bp.register_blueprint(auto_load_bp)

# Apply CORS configuration / 应用CORS配置
setup_cors(api_bp)

# Global error handlers / 全局错误处理器
@api_bp.errorhandler(413)
def too_large(e):
    """
    Handle file too large error / 处理文件过大错误
    Returns error response when uploaded file exceeds size limit
    当上传文件超过大小限制时返回错误响应
    """
    log_error('error_occurred', error='File too large')
    return jsonify({
        'success': False,
        'message': get_text('file_too_large')
    }), 413

@api_bp.errorhandler(400)
def bad_request(e):
    """
    Handle bad request error / 处理错误请求错误
    Returns error response for malformed requests
    为格式错误的请求返回错误响应
    """
    log_error('error_occurred', error='Bad request')
    return jsonify({
        'success': False,
        'message': get_text('bad_request')
    }), 400

@api_bp.errorhandler(404)
def not_found(e):
    """
    Handle not found error / 处理未找到错误
    Returns error response when resource is not found
    当资源未找到时返回错误响应
    """
    log_error('error_occurred', error='Resource not found')
    return jsonify({
        'success': False,
        'message': get_text('resource_not_found')
    }), 404

@api_bp.errorhandler(500)
def internal_error(e):
    """
    Handle internal server error / 处理内部服务器错误
    Returns error response for unexpected server errors
    为意外的服务器错误返回错误响应
    """
    log_error('error_occurred', error='Internal server error')
    return jsonify({
        'success': False,
        'message': get_text('server_error')
    }), 500

# Health check endpoint / 健康检查端点
@api_bp.route('/', methods=['GET'])
def api_root():
    """
    API root endpoint / API根端点
    Returns basic API information and status
    返回基本API信息和状态
    """
    return jsonify({
        'success': True,
        'name': 'Document Preview Editor API',
        'version': '1.0.0',
        'description': get_text('api_description'),
        'endpoints': {
            'documents': {
                'upload': '/api/upload_document',
                'download': '/api/download_document/<doc_id>',
                'info': '/api/document_info/<doc_id>',
                'cleanup': '/api/cleanup/<doc_id>'
            },
            'modifications': {
                'add': '/api/add_modifications',
                'process': '/api/process_document'
            },
            'auto_load': {
                'load': '/api/auto_load'
            },
            'utilities': {
                'language': '/api/set_language',
                'samples': '/api/download_sample/<file_type>/<language>',
                'health': '/api/health',
                'version': '/api/version'
            }
        }
    }) 