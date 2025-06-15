#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-language logging system / 多语言日志系统
Provides logging functionality with language-specific messages
提供支持特定语言消息的日志功能
"""

import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
from flask import session, request

class MultiLanguageLogger:
    """
    Multi-language logger class / 多语言日志记录器类
    Supports logging in different languages based on user preference
    支持根据用户偏好使用不同语言记录日志
    """
    
    def __init__(self, name: str = __name__):
        """
        Initialize the multi-language logger / 初始化多语言日志记录器
        
        Args:
            name: Logger name / 日志记录器名称
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist / 如果日志目录不存在则创建
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Set up file handler / 设置文件处理器
        log_file = f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Set up console handler / 设置控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter / 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger / 将处理器添加到日志记录器
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def get_current_language(self) -> str:
        """
        Get current user language / 获取当前用户语言
        
        Returns:
            Language code ('zh' or 'en') / 语言代码（'zh'或'en'）
        """
        try:
            # Try to get language from session / 尝试从会话中获取语言
            if 'language' in session:
                return session['language']
            
            # Try to get language from request headers / 尝试从请求头获取语言
            if request and hasattr(request, 'headers'):
                accept_language = request.headers.get('Accept-Language', '')
                if 'zh' in accept_language.lower():
                    return 'zh'
            
            # Default to English / 默认为英语
            return 'en'
        except:
            return 'en'
    
    def get_message(self, key: str, **kwargs) -> str:
        """
        Get localized message / 获取本地化消息
        
        Args:
            key: Message key / 消息键
            **kwargs: Format parameters / 格式化参数
            
        Returns:
            Localized message / 本地化消息
        """
        language = self.get_current_language()
        
        # Message templates / 消息模板
        messages = {
            'document_uploaded': {
                'zh': '文档上传成功: {filename}',
                'en': 'Document uploaded successfully: {filename}'
            },
            'document_processed': {
                'zh': '文档处理完成: {doc_id}',
                'en': 'Document processed successfully: {doc_id}'
            },
            'modifications_applied': {
                'zh': '修改应用完成 - 段落: {paragraphs}, 表格: {tables}',
                'en': 'Modifications applied - Paragraphs: {paragraphs}, Tables: {tables}'
            },
            'api_request_received': {
                'zh': '接收到API请求: {endpoint} - {method}',
                'en': 'API request received: {endpoint} - {method}'
            },
            'file_download_started': {
                'zh': '开始下载文件: {filename}',
                'en': 'File download started: {filename}'
            },
            'language_changed': {
                'zh': '语言已切换为: {language}',
                'en': 'Language changed to: {language}'
            },
            'error_occurred': {
                'zh': '发生错误: {error}',
                'en': 'Error occurred: {error}'
            },
            'csv_encoding_detected': {
                'zh': '成功使用编码 {encoding} 解码文件: {filename}',
                'en': 'Successfully decoded file using {encoding} encoding: {filename}'
            },
            'document_modification_started': {
                'zh': '开始应用修改到文档...',
                'en': 'Starting to apply modifications to document...'
            },
            'document_copy_created': {
                'zh': '已创建文档副本，开始应用文本修改...',
                'en': 'Document copy created, starting text modifications...'
            },
            'text_replacement': {
                'zh': '段落: \'{original}\' -> \'{new}\'',
                'en': 'Paragraph: \'{original}\' -> \'{new}\''
            },
            'modification_complete': {
                'zh': '修改应用完成',
                'en': 'Modification application complete'
            }
        }
        
        # Get message template / 获取消息模板
        message_dict = messages.get(key, {})
        message_template = message_dict.get(language, message_dict.get('en', key))
        
        # Format message with parameters / 使用参数格式化消息
        try:
            return message_template.format(**kwargs)
        except:
            return message_template
    
    def info(self, key: str, **kwargs):
        """Log info message / 记录信息消息"""
        message = self.get_message(key, **kwargs)
        self.logger.info(message)
    
    def warning(self, key: str, **kwargs):
        """Log warning message / 记录警告消息"""
        message = self.get_message(key, **kwargs)
        self.logger.warning(message)
    
    def error(self, key: str, **kwargs):
        """Log error message / 记录错误消息"""
        message = self.get_message(key, **kwargs)
        self.logger.error(message)
    
    def debug(self, key: str, **kwargs):
        """Log debug message / 记录调试消息"""
        message = self.get_message(key, **kwargs)
        self.logger.debug(message)

# Global logger instance / 全局日志记录器实例
app_logger = MultiLanguageLogger('document_preview_editor')

def log_info(key: str, **kwargs):
    """Convenience function for info logging / 信息日志记录便利函数"""
    app_logger.info(key, **kwargs)

def log_warning(key: str, **kwargs):
    """Convenience function for warning logging / 警告日志记录便利函数"""
    app_logger.warning(key, **kwargs)

def log_error(key: str, **kwargs):
    """Convenience function for error logging / 错误日志记录便利函数"""
    app_logger.error(key, **kwargs)

def log_debug(key: str, **kwargs):
    """Convenience function for debug logging / 调试日志记录便利函数"""
    app_logger.debug(key, **kwargs) 