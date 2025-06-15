#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document Preview Editor
Copyright (c) 2025 sawyer-shi
Licensed under the Apache License, Version 2.0
https://github.com/sawyer-shi/document-preview-editor

主路由模块
Main Routes Module
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from utils.i18n import get_text, set_language, get_current_language
from config import Config

# 创建主蓝图
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@main_bp.route('/auto_load')
def auto_load_page():
    """自动加载页面 - 支持URL参数自动加载文档和修改条目"""
    # 获取URL参数
    document_source = request.args.get('document')
    modifications_source = request.args.get('modifications')
    auto_apply = request.args.get('auto_apply', 'false').lower() == 'true'
    
    # 将参数传递给模板
    return render_template('index.html', 
                         auto_load_params={
                             'document': document_source,
                             'modifications': modifications_source,
                             'auto_apply': auto_apply
                         })

@main_bp.route('/set_language/<language>')
def set_page_language(language):
    """通过URL设置语言"""
    if language in Config.LANGUAGES:
        set_language(language)
    
    # 重定向回原页面或主页
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')

@main_bp.route('/help')
def help_page():
    """帮助页面"""
    return render_template('help.html')

@main_bp.route('/debug')
def debug_batch_import():
    """调试批量导入页面"""
    return render_template('debug_batch_import.html')

@main_bp.route('/test')
def test_page():
    """API测试页面"""
    # 检查是否有语言参数
    lang = request.args.get('lang')
    if lang and lang in Config.LANGUAGES:
        set_language(lang)
    
    # 确保模板获取到最新的语言设置
    return render_template('api_test.html', 
                         current_language=get_current_language(),
                         available_languages=Config.LANGUAGES,
                         get_text=get_text)

# 模板上下文处理器
@main_bp.context_processor
def inject_template_vars():
    """注入模板变量"""
    return {
        'current_language': get_current_language(),
        'available_languages': Config.LANGUAGES,
        'get_text': get_text
    } 