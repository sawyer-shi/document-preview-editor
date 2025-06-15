#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility routes module / 工具路由模块
Handles language settings, sample file downloads, and other utility functions
处理语言设置、样例文件下载和其他工具功能
"""

import os
from flask import Blueprint, request, jsonify, send_file

from utils.i18n import get_text, set_language, get_current_language
from utils.logger import log_info, log_error
from config import Config

# Create utility blueprint / 创建工具蓝图
utility_bp = Blueprint('utility', __name__)

@utility_bp.route('/set_language', methods=['POST'])
def set_app_language():
    """
    Set application language / 设置应用语言
    Changes the current language setting for the application
    更改应用程序的当前语言设置
    """
    try:
        # Get request data / 获取请求数据
        data = request.get_json()
        language = data.get('language')
        
        # Validate language / 验证语言
        if language and language in Config.LANGUAGES:
            success = set_language(language)
            if success:
                # Log language change / 记录语言更改
                log_info('language_changed', language=language)
                
                return jsonify({
                    'success': True,
                    'message': get_text('language_changed'),
                    'language': language
                })
        
        return jsonify({
            'success': False,
            'message': get_text('invalid_language')
        })
        
    except Exception as e:
        # Log error / 记录错误
        log_error('error_occurred', error=str(e))
        return jsonify({
            'success': False,
            'message': f"{get_text('server_error')}: {str(e)}"
        })

@utility_bp.route('/get_language', methods=['GET'])
def get_app_language():
    """
    Get current language / 获取当前语言
    Returns the current language setting and available languages
    返回当前语言设置和可用语言
    """
    try:
        return jsonify({
            'success': True,
            'language': get_current_language(),
            'available_languages': Config.LANGUAGES
        })
        
    except Exception as e:
        # Log error / 记录错误
        log_error('error_occurred', error=str(e))
        return jsonify({
            'success': False,
            'message': f"{get_text('server_error')}: {str(e)}"
        })

@utility_bp.route('/download_sample/<file_type>/<language>')
def download_sample_file(file_type: str, language: str):
    """
    Download sample files / 下载样例文件
    Provides sample documents and modification files for testing
    提供用于测试的样例文档和修改文件
    
    Args:
        file_type: Type of file ('document' or 'modifications') / 文件类型（'document'或'modifications'）
        language: Language code ('zh' or 'en') / 语言代码（'zh'或'en'）
    """
    try:
        # Validate parameters / 验证参数
        if file_type not in ['document', 'modifications']:
            return jsonify({
                'success': False,
                'message': 'Invalid file type'
            }), 400
            
        if language not in ['zh', 'en']:
            return jsonify({
                'success': False,
                'message': 'Invalid language'
            }), 400
        
        # Build file path / 构建文件路径
        if file_type == 'document':
            if language == 'zh':
                file_path = os.path.join('api_test_module', 'samples', 'sample_document.docx')
                filename = 'sample_document_zh.docx'
            else:
                file_path = os.path.join('api_test_module', 'samples', 'sample_document_en.docx')
                filename = 'sample_document_en.docx'
        else:  # modifications
            if language == 'zh':
                file_path = os.path.join('api_test_module', 'samples', 'sample_modifications.csv')
                filename = 'sample_modifications_zh.csv'
            else:
                file_path = os.path.join('api_test_module', 'samples', 'sample_modifications_en.csv')
                filename = 'sample_modifications_en.csv'
        
        # Check if file exists / 检查文件是否存在
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'message': 'Sample file not found'
            }), 404
        
        # Log download start / 记录下载开始
        log_info('file_download_started', filename=filename)
        
        # Send file / 发送文件
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        # Log error / 记录错误
        log_error('error_occurred', error=str(e))
        return jsonify({
            'success': False,
            'message': f"Error downloading sample file: {str(e)}"
        }), 500

@utility_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint / 健康检查端点
    Returns the current status of the application
    返回应用程序的当前状态
    """
    try:
        return jsonify({
            'success': True,
            'status': 'healthy',
            'message': get_text('service_healthy'),
            'language': get_current_language()
        })
        
    except Exception as e:
        # Log error / 记录错误
        log_error('error_occurred', error=str(e))
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'message': f"{get_text('server_error')}: {str(e)}"
        }), 500

@utility_bp.route('/version', methods=['GET'])
def get_version():
    """
    Get application version / 获取应用版本
    Returns version information about the application
    返回应用程序的版本信息
    """
    try:
        return jsonify({
            'success': True,
            'name': 'Document Preview Editor',
            'version': '1.0.0',
            'description': get_text('app_description'),
            'language': get_current_language()
        })
        
    except Exception as e:
        # Log error / 记录错误
        log_error('error_occurred', error=str(e))
        return jsonify({
            'success': False,
            'message': f"{get_text('server_error')}: {str(e)}"
        }), 500 