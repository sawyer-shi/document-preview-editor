#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document Preview Editor
Copyright (c) 2025 sawyer-shi
Licensed under the Apache License, Version 2.0
https://github.com/sawyer-shi/document-preview-editor

国际化支持模块
Internationalization Support Module
"""

from flask import session, request
from config import Config

# 语言翻译字典
TRANSLATIONS = {
    'zh': {
        # 页面标题和主要内容
        'page_title': '文档预览编辑器',
        'page_subtitle': 'Document Preview Editor',
        'original_document': '原始文档',
        'modifications': '修改条目',
        'preview_document': '预览文档',
        'language': '语言',
        'chinese': '中文',
        'english': 'English',
        
        # 按钮和操作
        'select_document': '导入文档',
        'import_document': '导入文档',
        'add_modification': '添加修改条目',
        'apply_modifications': '应用所有修改',
        'clear_modifications': '清空修改',
        'download_document': '下载修改后文档',
        'save': '保存',
        'cancel': '取消',
        'delete': '删除',
        'edit': '编辑',
        'close': '关闭',
        
        # 表单字段
        'original_text': '原文内容',
        'new_text': '修改为',
        'modification_reason': '修改原因',
        'original_text_placeholder': '请输入要修改的原文内容',
        'new_text_placeholder': '请输入修改后的内容',
        'reason_placeholder': '请描述修改的原因',
        
        # 统计信息
        'total_modifications': '总计',
        'applied': '已应用',
        'pending': '待处理',
        
        # 提示信息
        'upload_prompt': '请上传Word文档以开始编辑',
        'upload_support': '支持 .docx 和 .txt 格式',
        'upload_support_txt': '支持 .docx 和 .txt 格式',
        'no_modifications': '上传文档后可添加修改条目',
        'preview_prompt': '应用修改后可预览最终文档',
        'processing': '处理中，请稍候...',
        
        # 消息提示
        'upload_success': '文档上传成功',
        'upload_failed': '文档上传失败',
        'modification_added': '修改条目已添加',
        'modification_deleted': '修改条目已删除',
        'modifications_applied': '修改应用成功',
        'modifications_cleared': '修改条目已清空',
        'download_started': '文档下载已开始',
        'fill_all_fields': '请填写所有字段',
        'invalid_file_format': '请选择支持的文档格式文件 (.docx 或 .txt)',
        'no_document': '没有可下载的文档',
        'no_modifications_to_apply': '没有可应用的修改',
        'confirm_clear': '确定要清空所有修改条目吗？',
        'unsaved_changes': '您有未保存的修改，确定要离开吗？',
        'language_change_confirm': '系统将重新载入，当前数据将清空！确认切换语言吗？',
        
        # 服务器日志消息
        'starting_app': '启动Document Preview Editor...',
        'app_stopped': '应用已停止',
        'document_applying_modifications': '开始应用修改到文档...',
        'document_copy_created': '已创建文档副本，开始应用文本修改...',
        'text_replacement': '跨runs替换文本',
        'paragraph_replacement': '在段落中替换文本',
        'text_modification_complete': '文本修改完成',
        'modification_applied_complete': '修改应用完成',
        'doc_extraction_trying': '尝试DOC文档内容提取',
        'doc_extraction_failed': 'DOC提取失败',
        'docx_conversion_success': 'DOCX转换成功',
        'table_replacement': '表格',
        'paragraph_replacement': '段落',
        
        # 错误信息
        'server_error': '服务器错误',
        'network_error': '网络错误',
        'file_not_found': '文件不存在',
        'resource_not_found': '资源不存在',
        'processing_failed': '处理失败',
        'service_healthy': '服务正常',
        'app_description': '文档预览编辑器 - 高级文档编辑解决方案',
        'api_description': '文档预览编辑器API - 提供文档处理和修改功能',
        
        # 快捷键提示
        'shortcuts_title': '快捷键',
        'shortcut_upload': '上传文档',
        'shortcut_add': '添加修改条目',
        'shortcut_apply': '应用修改',
        'shortcut_close': '关闭模态框或取消选中',
        
        # API相关
        'api_title': 'API接口',
        'api_test': '接口测试',
        'api_upload': '上传文档接口',
        'api_modify': '修改文档接口',
        'api_download': '下载文档接口',
        
        # 状态信息
        'document_loaded': '文档已加载',
        'modifications_count': '修改条目数',
        'file_size': '文件大小',
        'last_modified': '最后修改时间',
        
        # 额外的API消息
        'no_file_provided': '未提供文档文件',
        'no_file_selected': '未选择文件',
        'no_document_provided': '未提供文档',
        'document_not_found': '文档不存在',
        'document_processing_error': '文档处理错误',
        'no_modifications_provided': '未提供修改条目',
        'modifications_processing_error': '修改条目处理错误',
        'no_valid_modifications': '没有有效的修改条目',
        'invalid_modification_format': '修改条目格式不正确',
        'no_modifications_applied': '未应用任何修改',
        'document_processed_successfully': '文档处理成功',
        'invalid_json_format': '修改条目JSON格式错误',
        'cleanup_completed': '清理完成',
        'file_too_large': '文件过大',
        'bad_request': '错误请求',
        'language_changed': '语言已切换',
        'invalid_language': '无效的语言设置',
        'language_change_failed': '语言切换失败',
        'document_processing_failed': '文档处理失败',
        'auto_load_and_process_complete': '自动加载和处理完成',
        'auto_load_complete': '自动加载完成',
        'scroll_to_view_more': '滚动查看更多',
        'doc_format_warning': 'DOC格式文件可能出现格式问题，建议转换为DOCX格式后使用',
        'doc_conversion_notice': '正在尝试转换DOC文件，可能需要一些时间...',
        'doc_conversion_limited': 'DOC文件转换成功，但可能存在格式限制',
        
        # 批量导入相关
        'batch_import': '批量导入',
        'batch_import_modifications': '批量导入修改条目',
        'step1_download_template': '步骤1：下载CSV模板',
        'step2_upload_csv': '步骤2：上传填写好的CSV文件',
        'download_csv_template': '下载CSV模板',
        'download_csv_template_desc': '请先下载CSV模板文件，并按照模板格式填写修改条目：',
        'csv_file_requirements': 'CSV文件必须包含以下三个字段：',
        'csv_field_original': 'OriginalText - 原文内容',
        'csv_field_modified': 'ModifiedText - 修改为',
        'csv_field_reason': 'ModificationReason - 修改原因',
        'select_csv_file': '选择CSV文件',
        'preview_import_data': '预览导入数据：',
        'import_data': '导入数据',
        'csv_validation_success': '文件验证通过',
        'csv_validation_failed': '文件验证失败',
        'csv_invalid_format': 'CSV文件格式不正确',
        'csv_missing_fields': '缺少必需字段',
        'csv_empty_data': '文件中没有有效数据',
        'csv_import_success': '成功导入{count}条修改条目',
        'csv_import_failed': 'CSV导入失败',
        'csv_encoding_warning': '文件编码可能不正确，请确保CSV文件使用UTF-8编码保存。如果显示乱码，请重新保存为UTF-8编码。',
        'total_records': '共{count}条记录',
        'sample': '样本',
        'point_to_this_item': '指向此条目',
    },
    
    'en': {
        # 页面标题和主要内容
        'page_title': 'Document Preview Editor',
        'page_subtitle': 'Advanced Document Editing Solution',
        'original_document': 'Original Document',
        'modifications': 'Modifications',
        'preview_document': 'Preview Document',
        'language': 'Language',
        'chinese': '中文',
        'english': 'English',
        
        # 按钮和操作
        'select_document': 'Import Document',
        'import_document': 'Import Document',
        'add_modification': 'Add',
        'apply_modifications': 'Apply All Modifications',
        'clear_modifications': 'Clear Modifications',
        'download_document': 'Download Result',
        'save': 'Save',
        'cancel': 'Cancel',
        'delete': 'Delete',
        'edit': 'Edit',
        'close': 'Close',
        
        # 表单字段
        'original_text': 'Original Text',
        'new_text': 'Modified Text',
        'modification_reason': 'Modification Reason',
        'original_text_placeholder': 'Enter the original text to be modified',
        'new_text_placeholder': 'Enter the modified text',
        'reason_placeholder': 'Describe the reason for modification',
        
        # 统计信息
        'total_modifications': 'Total',
        'applied': 'Applied',
        'pending': 'Pending',
        
        # 提示信息
        'upload_prompt': 'Please upload a Word document to start editing',
        'upload_support': 'Supports .docx and .txt formats',
        'upload_support_txt': 'Supports .docx and .txt formats',
        'no_modifications': 'Upload document to add modifications',
        'preview_prompt': 'Preview will be available after applying modifications',
        'processing': 'Processing, please wait...',
        
        # 消息提示
        'upload_success': 'Document uploaded successfully',
        'upload_failed': 'Failed to upload document',
        'modification_added': 'Modification item added',
        'modification_deleted': 'Modification item deleted',
        'modifications_applied': 'Modifications applied successfully',
        'modifications_cleared': 'Modifications cleared',
        'download_started': 'Document download started',
        'fill_all_fields': 'Please fill in all fields',
        'invalid_file_format': 'Please select supported document format (.docx or .txt)',
        'no_document': 'No document available for download',
        'no_modifications_to_apply': 'No modifications to apply',
        'confirm_clear': 'Are you sure you want to clear all modifications?',
        'unsaved_changes': 'You have unsaved changes. Are you sure you want to leave?',
        'language_change_confirm': 'System will reload and current data will be cleared! Confirm language switch?',
        
        # 服务器日志消息
        'starting_app': 'Starting Document Preview Editor...',
        'app_stopped': 'Application stopped',
        'document_applying_modifications': 'Starting to apply modifications to document...',
        'document_copy_created': 'Document copy created, starting text modifications...',
        'text_replacement': 'Cross-runs text replacement',
        'paragraph_replacement': 'Text replacement in paragraph',
        'text_modification_complete': 'Text modification complete',
        'modification_applied_complete': 'Modification application complete',
        'doc_extraction_trying': 'Attempting DOC document content extraction',
        'doc_extraction_failed': 'DOC extraction failed',
        'docx_conversion_success': 'DOCX conversion successful',
        'table_replacement': 'Table',
        'paragraph_replacement': 'Paragraph',
        
        # 错误信息
        'server_error': 'Server Error',
        'network_error': 'Network Error',
        'file_not_found': 'File Not Found',
        'resource_not_found': 'Resource Not Found',
        'processing_failed': 'Processing Failed',
        'service_healthy': 'Service is healthy',
        'app_description': 'Document Preview Editor - Advanced Document Editing Solution',
        'api_description': 'Document Preview Editor API - Provides document processing and modification capabilities',
        
        # 快捷键提示
        'shortcuts_title': 'Shortcuts',
        'shortcut_upload': 'Upload document',
        'shortcut_add': 'Add modification',
        'shortcut_apply': 'Apply modifications',
        'shortcut_close': 'Close modal or cancel selection',
        
        # API相关
        'api_title': 'API Interface',
        'api_test': 'API Test',
        'api_upload': 'Upload Document API',
        'api_modify': 'Modify Document API',
        'api_download': 'Download Document API',
        
        # 状态信息
        'document_loaded': 'Document Loaded',
        'modifications_count': 'Modification Count',
        'file_size': 'File Size',
        'last_modified': 'Last Modified',
        
        # 额外的API消息
        'no_file_provided': 'No file provided',
        'no_file_selected': 'No file selected',
        'no_document_provided': 'No document provided',
        'document_not_found': 'Document not found',
        'document_processing_error': 'Document processing error',
        'no_modifications_provided': 'No modifications provided',
        'modifications_processing_error': 'Modifications processing error',
        'no_valid_modifications': 'No valid modifications',
        'invalid_modification_format': 'Invalid modification format',
        'no_modifications_applied': 'No modifications applied',
        'document_processed_successfully': 'Document processed successfully',
        'invalid_json_format': 'Invalid JSON format for modifications',
        'cleanup_completed': 'Cleanup completed',
        'file_too_large': 'File too large',
        'bad_request': 'Bad request',
        'language_changed': 'Language changed',
        'invalid_language': 'Invalid language setting',
        'language_change_failed': 'Language change failed',
        'document_processing_failed': 'Document processing failed',
        'auto_load_and_process_complete': 'Auto load and processing complete',
        'auto_load_complete': 'Auto load complete',
        'scroll_to_view_more': 'Scroll to view more',
        'doc_format_warning': 'DOC format files may have formatting issues, recommend converting to DOCX format',
        'doc_conversion_notice': 'Converting DOC file, this may take some time...',
        'doc_conversion_limited': 'DOC file converted successfully, but may have format limitations',
        
        # 批量导入相关
        'batch_import': 'Batch Import',
        'batch_import_modifications': 'Batch Import Modifications',
        'step1_download_template': 'Step 1: Download CSV Template',
        'step2_upload_csv': 'Step 2: Upload Filled CSV File',
        'download_csv_template': 'Download CSV Template',
        'download_csv_template_desc': 'Please download the CSV template file first and fill in modification items according to the template format:',
        'csv_file_requirements': 'CSV file must contain the following three fields:',
        'csv_field_original': 'OriginalText - Original content',
        'csv_field_modified': 'ModifiedText - Modified content',
        'csv_field_reason': 'ModificationReason - Modification reason',
        'select_csv_file': 'Select CSV File',
        'preview_import_data': 'Preview Import Data:',
        'import_data': 'Import Data',
        'csv_validation_success': 'File validation passed',
        'csv_validation_failed': 'File validation failed',
        'csv_invalid_format': 'Invalid CSV file format',
        'csv_missing_fields': 'Missing required fields',
        'csv_empty_data': 'No valid data in file',
        'csv_import_success': 'Successfully imported {count} modification items',
        'csv_import_failed': 'CSV import failed',
        'csv_encoding_warning': 'File encoding may be incorrect. Please ensure CSV file is saved with UTF-8 encoding. If you see garbled text, please re-save as UTF-8.',
        'total_records': '{count} records in total',
        'sample': 'Sample',
        'point_to_this_item': 'Point to this item',
    }
}

class I18n:
    """国际化支持类"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """初始化Flask应用的国际化支持"""
        self.app = app
        
        # 注册模板全局函数
        app.jinja_env.globals['get_text'] = self.get_text
        app.jinja_env.globals['get_current_language'] = self.get_current_language
        app.jinja_env.globals['get_available_languages'] = self.get_available_languages
        
        # 添加语言选择的上下文处理器
        @app.context_processor
        def inject_language():
            return {
                'current_language': self.get_current_language(),
                'available_languages': Config.LANGUAGES
            }
    
    def get_current_language(self):
        """获取当前语言"""
        # 优先从session获取
        language = session.get('language')
        if language and language in Config.LANGUAGES:
            return language
        
        # 从请求头获取
        language = request.headers.get('Accept-Language', '').split(',')[0].split('-')[0]
        if language in Config.LANGUAGES:
            return language
        
        # 使用默认语言
        return Config.DEFAULT_LANGUAGE
    
    def set_language(self, language):
        """设置当前语言"""
        if language in Config.LANGUAGES:
            session['language'] = language
            return True
        return False
    
    def get_text(self, key, language=None):
        """获取翻译文本"""
        if language is None:
            language = self.get_current_language()
        
        # 获取翻译文本
        translations = TRANSLATIONS.get(language, TRANSLATIONS[Config.DEFAULT_LANGUAGE])
        return translations.get(key, f"[{key}]")  # 如果找不到翻译，返回key
    
    def get_available_languages(self):
        """获取可用语言列表"""
        return Config.LANGUAGES

# 创建全局i18n实例
i18n = I18n()

def get_text(key, language=None):
    """全局翻译函数"""
    return i18n.get_text(key, language)

def set_language(language):
    """全局设置语言函数"""
    return i18n.set_language(language)

def get_current_language():
    """全局获取当前语言函数"""
    return i18n.get_current_language() 