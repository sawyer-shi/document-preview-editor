#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-load routes module / 自动加载路由模块
Handles automatic loading of documents and modifications from various sources
处理从各种来源自动加载文档和修改条目
"""

import os
import tempfile
import uuid
import json
import requests
import csv
import io
from datetime import datetime
from flask import Blueprint, request, jsonify
from urllib.parse import urlparse, unquote

from utils.document_processor import EnhancedWordProcessor
from utils.i18n import get_text, set_language
from utils.logger import log_info, log_error
from config import Config
from .document_routes import uploaded_documents
from .modification_routes import modification_items, decode_file_content, parse_csv_modifications

# Create auto-load blueprint / 创建自动加载蓝图
auto_load_bp = Blueprint('auto_load', __name__)

def process_document_source(document_source):
    """
    Process document from various sources / 处理来自各种来源的文档
    
    Args:
        document_source: Document source (file path, URL, or file object) / 文档来源（文件路径、URL或文件对象）
        
    Returns:
        Tuple of (success, file_path, filename, error_message) / 返回(成功状态, 文件路径, 文件名, 错误信息)元组
    """
    try:
        temp_file_path = None
        filename = None
        
        if isinstance(document_source, str):
            # Handle file path or URL / 处理文件路径或URL
            if document_source.startswith(('http://', 'https://')):
                # Download from URL / 从URL下载
                response = requests.get(document_source, timeout=30)
                response.raise_for_status()
                
                # Get filename from URL / 从URL获取文件名
                parsed_url = urlparse(document_source)
                filename = os.path.basename(unquote(parsed_url.path))
                if not filename or '.' not in filename:
                    filename = 'document.docx'
                
                # Save to temporary file / 保存到临时文件
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
                temp_file.write(response.content)
                temp_file_path = temp_file.name
                temp_file.close()
                
            else:
                # Local file path / 本地文件路径
                if os.path.exists(document_source):
                    temp_file_path = document_source
                    filename = os.path.basename(document_source)
                else:
                    return False, None, None, f"File not found: {document_source}"
        else:
            # Handle file object / 处理文件对象
            filename = getattr(document_source, 'filename', 'document.docx')
            
            # Ensure proper file extension / 确保正确的文件扩展名
            if not filename.lower().endswith(('.docx', '.txt')):
                filename += '.docx'
            
            # Create temporary file with proper extension / 创建带有正确扩展名的临时文件
            file_ext = os.path.splitext(filename)[1] or '.docx'
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_ext)
            temp_file.close()  # Close the file handle first
            
            # Save the uploaded file / 保存上传的文件
            document_source.save(temp_file.name)
            temp_file_path = temp_file.name
        
        return True, temp_file_path, filename, None
        
    except Exception as e:
        return False, None, None, str(e)

def process_modifications_source(modifications_source):
    """
    Process modifications from various sources / 处理来自各种来源的修改条目
    
    Args:
        modifications_source: Modifications source (file path, URL, JSON string, list, or file object)
                             修改条目来源（文件路径、URL、JSON字符串、列表或文件对象）
        
    Returns:
        Tuple of (success, modifications_list, error_message) / 返回(成功状态, 修改条目列表, 错误信息)元组
    """
    try:
        modifications = []
        
        if isinstance(modifications_source, list):
            # Already a list (from JSON request) / 已经是列表（来自JSON请求）
            modifications = modifications_source
            
        elif isinstance(modifications_source, str):
            # Handle string input / 处理字符串输入
            if modifications_source.startswith(('http://', 'https://')):
                # Download from URL / 从URL下载
                response = requests.get(modifications_source, timeout=30)
                response.raise_for_status()
                content = response.text
                
                # Try to parse as JSON first, then CSV / 先尝试解析为JSON，然后是CSV
                try:
                    modifications = json.loads(content)
                except json.JSONDecodeError:
                    modifications = parse_csv_modifications(content)
                    
            elif modifications_source.startswith('[') or modifications_source.startswith('{'):
                # JSON string / JSON字符串
                modifications = json.loads(modifications_source)
                
            elif os.path.exists(modifications_source):
                # Local file path / 本地文件路径
                with open(modifications_source, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Try to parse as JSON first, then CSV / 先尝试解析为JSON，然后是CSV
                try:
                    modifications = json.loads(content)
                except json.JSONDecodeError:
                    modifications = parse_csv_modifications(content)
            else:
                # Treat as CSV content / 作为CSV内容处理
                modifications = parse_csv_modifications(modifications_source)
                
        elif hasattr(modifications_source, 'read'):
            # Handle file object / 处理文件对象
            file_content = modifications_source.read()
            if isinstance(file_content, bytes):
                file_content = decode_file_content(file_content, getattr(modifications_source, 'filename', 'modifications.csv'))
            
            # Debug: log file content
            log_info('file_content_decoded', filename=getattr(modifications_source, 'filename', 'unknown'), length=len(file_content))
            
            # Try to parse as JSON first, then CSV / 先尝试解析为JSON，然后是CSV
            try:
                modifications = json.loads(file_content)
                log_info('parsed_as_json', count=len(modifications))
            except json.JSONDecodeError:
                modifications = parse_csv_modifications(file_content)
                log_info('parsed_as_csv', count=len(modifications))
        else:
            # Unknown type, try to convert to string and parse / 未知类型，尝试转换为字符串并解析
            modifications_str = str(modifications_source)
            if modifications_str.startswith('[') or modifications_str.startswith('{'):
                modifications = json.loads(modifications_str)
            else:
                modifications = parse_csv_modifications(modifications_str)
        
        return True, modifications, None
        
    except Exception as e:
        return False, [], str(e)

@auto_load_bp.route('/auto_load', methods=['GET', 'POST'])
def auto_load_document_and_modifications():
    """
    Auto-load document and modifications API / 自动加载文档和修改条目API
    Supports loading from files, URLs, and direct content
    支持从文件、URL和直接内容加载
    """
    try:
        # Log API request / 记录API请求
        log_info('api_request_received', endpoint='/auto_load', method=request.method)
        
        # Handle different request types / 处理不同的请求类型
        if request.method == 'GET':
            # GET request with query parameters / 带查询参数的GET请求
            document_source = request.args.get('document')
            modifications_source = request.args.get('modifications')
            language = request.args.get('language', 'zh')
            auto_apply = request.args.get('auto_apply', 'false').lower() == 'true'
        else:
            # POST request / POST请求
            if request.is_json:
                # JSON request / JSON请求
                data = request.get_json()
                document_source = data.get('document')
                modifications_source = data.get('modifications')
                language = data.get('language', 'zh')
                auto_apply = data.get('auto_apply', False)
            else:
                # Form request / 表单请求
                document_source = request.files.get('document_file') or request.files.get('document') or request.form.get('document')
                modifications_source = request.files.get('modifications_file') or request.files.get('modifications') or request.form.get('modifications')
                language = request.form.get('language', 'zh')
                auto_apply = request.form.get('auto_apply', 'false').lower() == 'true'
        
        # Set language first / 首先设置语言
        if language in Config.LANGUAGES:
            set_language(language)
        
        # Validate required parameters / 验证必需参数
        if not document_source:
            return jsonify({
                'success': False,
                'message': get_text('no_document_provided')
            }), 400
        
        if not modifications_source:
            return jsonify({
                'success': False,
                'message': get_text('no_modifications_provided')
            }), 400
        
        # Process document source / 处理文档来源
        doc_success, doc_file_path, doc_filename, doc_error = process_document_source(document_source)
        if not doc_success:
            return jsonify({
                'success': False,
                'message': f"{get_text('document_processing_error')}: {doc_error}"
            }), 400
        
        # Process modifications source / 处理修改条目来源
        mod_success, modifications, mod_error = process_modifications_source(modifications_source)
        if not mod_success:
            return jsonify({
                'success': False,
                'message': f"{get_text('modifications_processing_error')}: {mod_error}"
            }), 400
        
        # Debug: log modifications processing result
        log_info('modifications_processed', count=len(modifications) if modifications else 0)
        
        if not modifications:
            return jsonify({
                'success': False,
                'message': get_text('no_valid_modifications')
            }), 400
        
        # Generate unique document ID / 生成唯一文档ID
        doc_id = str(uuid.uuid4())
        
        # Create permanent file path / 创建永久文件路径
        upload_dir = Config.UPLOAD_FOLDER
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        permanent_file_path = os.path.join(upload_dir, f"{doc_id}_{doc_filename}")
        
        # Copy to permanent location if it's a temporary file / 如果是临时文件则复制到永久位置
        if doc_file_path != permanent_file_path:
            import shutil
            shutil.copy2(doc_file_path, permanent_file_path)
            # Clean up temporary file / 清理临时文件
            if doc_file_path.startswith(tempfile.gettempdir()):
                os.unlink(doc_file_path)
        
        # Initialize document processor to get content / 初始化文档处理器获取内容
        processor = EnhancedWordProcessor()
        success, message = processor.load_document(permanent_file_path)
        if not success:
            return jsonify({
                'success': False,
                'message': f"{get_text('document_processing_error')}: {message}"
            }), 400
        
        # Extract document content with formatting / 提取带格式的文档内容
        original_content = processor.extract_content_with_formatting(processor.original_doc)
        
        # Store document info / 存储文档信息
        uploaded_documents[doc_id] = {
            'id': doc_id,
            'original_filename': doc_filename,
            'safe_filename': doc_filename,
            'file_path': permanent_file_path,
            'upload_time': datetime.now().isoformat(),
            'processed': False,
            'modifications_applied': False,
            'auto_loaded': True,
            'content': original_content,  # Store original content / 存储原始内容
            'processor': processor,  # Store processor instance / 存储处理器实例
            'modifications': modifications  # Store modifications / 存储修改条目
        }
        
        # Store modifications / 存储修改条目
        modification_items[doc_id] = {
            'doc_id': doc_id,
            'modifications': modifications,
            'created_time': datetime.now().isoformat(),
            'auto_loaded': True
        }
        
        # Log successful upload / 记录成功上传
        log_info('document_uploaded', filename=doc_filename)
        
        # Apply modifications if auto_apply is True / 如果auto_apply为True则应用修改
        if auto_apply:
            # Log modification start / 记录修改开始
            log_info('document_modification_started')
            
            # Use the existing processor instance / 使用现有的处理器实例
            # Log document copy creation / 记录文档副本创建
            log_info('document_copy_created')
            
            # Apply modifications / 应用修改
            success, message = processor.apply_modifications(modifications)
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': message
                }), 500
            
            # Get modified content / 获取修改后的内容
            modified_content = processor.extract_content_with_formatting(processor.modified_doc)
            
            # Save processed document / 保存处理后的文档
            processed_filename = f"processed_{doc_filename}"
            processed_file_path = os.path.join(upload_dir, f"{doc_id}_{processed_filename}")
            success, save_message = processor.save_modified_document(processed_file_path)
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': save_message
                }), 500
            
            # Count modifications for reporting / 统计修改数量用于报告
            paragraph_count = len(modifications)
            table_count = 0
            
            # Update document info / 更新文档信息
            uploaded_documents[doc_id].update({
                'processed': True,
                'modifications_applied': True,
                'processed_file_path': processed_file_path,
                'processed_filename': processed_filename,
                'modification_count': len(modifications),
                'paragraph_changes': paragraph_count,
                'table_changes': table_count,
                'process_time': datetime.now().isoformat(),
                'modified_content': modified_content  # Store modified content / 存储修改后的内容
            })
            
            # Log completion / 记录完成
            log_info('modifications_applied', paragraphs=paragraph_count, tables=table_count)
            log_info('modification_complete')
            
            return jsonify({
                'success': True,
                'message': get_text('auto_load_and_process_complete'),
                'doc_id': doc_id,
                'filename': doc_filename,
                'modification_count': len(modifications),
                'paragraph_changes': paragraph_count,
                'table_changes': table_count,
                'download_url': f'/api/download_document/{doc_id}',
                'redirect_url': f'/?doc_id={doc_id}&from_test=true'
            })
        else:
            return jsonify({
                'success': True,
                'message': get_text('auto_load_complete'),
                'doc_id': doc_id,
                'filename': doc_filename,
                'modification_count': len(modifications),
                'redirect_url': f'/?doc_id={doc_id}&from_test=true'
            })
        
    except Exception as e:
        # Log error / 记录错误
        log_error('error_occurred', error=str(e))
        return jsonify({
            'success': False,
            'message': f"{get_text('server_error')}: {str(e)}"
        }), 500 