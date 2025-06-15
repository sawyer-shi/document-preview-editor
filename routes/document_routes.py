#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document routes module / 文档路由模块
Handles document upload, download, and processing operations
处理文档上传、下载和处理操作
"""

import os
import tempfile
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename

from utils.document_processor import EnhancedWordProcessor
from utils.i18n import get_text
from utils.logger import log_info, log_error
from config import Config

# Create document blueprint / 创建文档蓝图
document_bp = Blueprint('document', __name__)

# Global variables for storing documents / 存储文档的全局变量
uploaded_documents = {}

def allowed_file(filename: str) -> bool:
    """
    Check if file type is allowed / 检查文件类型是否允许
    
    Args:
        filename: File name to check / 要检查的文件名
        
    Returns:
        True if file type is allowed / 如果文件类型允许则返回True
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@document_bp.route('/upload_document', methods=['POST'])
def upload_document():
    """
    Upload original Word document API / 上传原始Word文档API
    Handles document file upload and stores it for processing
    处理文档文件上传并存储以供处理
    """
    try:
        # Check if file is provided / 检查是否提供了文件
        if 'document' not in request.files:
            return jsonify({
                'success': False,
                'message': get_text('no_file_provided')
            })
        
        file = request.files['document']
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': get_text('no_file_selected')
            })
        
        # Validate file type / 验证文件类型
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'message': get_text('invalid_file_format')
            })
        
        # Generate unique ID / 生成唯一ID
        doc_id = str(uuid.uuid4())
        
        # Save original filename (for display) and safe filename (for filesystem)
        # 保存原始文件名（用于显示）和安全文件名（用于文件系统）
        original_filename = file.filename
        safe_filename = secure_filename(file.filename)
        
        # If secure_filename removed all characters, use default name
        # 如果secure_filename删除了所有字符，使用默认名称
        if not safe_filename:
            safe_filename = f"document_{doc_id}.docx"
        
        # Create uploads directory if it doesn't exist / 如果上传目录不存在则创建
        upload_dir = Config.UPLOAD_FOLDER
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # Save file / 保存文件
        file_path = os.path.join(upload_dir, f"{doc_id}_{safe_filename}")
        file.save(file_path)
        
        # Process document to extract content / 处理文档以提取内容
        from utils.document_processor import EnhancedWordProcessor
        processor = EnhancedWordProcessor()
        
        # Load and process the document / 加载并处理文档
        success, message = processor.load_document(file_path)
        if not success:
            # If processing fails, clean up and return error / 如果处理失败，清理并返回错误
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({
                'success': False,
                'message': f"{get_text('document_processing_failed')}: {message}"
            })
        
        # Extract document content with formatting / 提取带格式的文档内容
        content = processor.extract_content_with_formatting(processor.original_doc)
        
        # Store document info / 存储文档信息
        uploaded_documents[doc_id] = {
            'id': doc_id,
            'original_filename': original_filename,
            'safe_filename': safe_filename,
            'file_path': file_path,
            'upload_time': datetime.now().isoformat(),
            'processed': False,
            'modifications_applied': False,
            'content': content,  # Store extracted content / 存储提取的内容
            'processor': processor  # Store processor instance / 存储处理器实例
        }
        
        # Log successful upload / 记录成功上传
        log_info('document_uploaded', filename=original_filename)
        
        return jsonify({
            'success': True,
            'message': get_text('document_uploaded'),
            'doc_id': doc_id,
            'filename': original_filename,
            'content': content  # Return content to frontend / 返回内容给前端
        })
        
    except Exception as e:
        # Log error / 记录错误
        log_error('error_occurred', error=str(e))
        return jsonify({
            'success': False,
            'message': f"{get_text('server_error')}: {str(e)}"
        }), 500

@document_bp.route('/download_document/<doc_id>')
def download_document(doc_id: str):
    """
    Download processed document / 下载处理后的文档
    Returns the processed document file for download
    返回处理后的文档文件供下载
    """
    try:
        # Check if document exists / 检查文档是否存在
        if doc_id not in uploaded_documents:
            return jsonify({
                'success': False,
                'message': get_text('document_not_found')
            }), 404
        
        doc_info = uploaded_documents[doc_id]
        
        # Check if document has been processed / 检查文档是否已处理
        if not doc_info.get('processed', False):
            return jsonify({
                'success': False,
                'message': get_text('document_not_processed')
            }), 400
        
        # Get processed file path / 获取处理后的文件路径
        processed_file_path = doc_info.get('processed_file_path')
        if not processed_file_path or not os.path.exists(processed_file_path):
            return jsonify({
                'success': False,
                'message': get_text('processed_file_not_found')
            }), 404
        
        # Generate download filename / 生成下载文件名
        original_name = doc_info['original_filename']
        name_without_ext = os.path.splitext(original_name)[0]
        download_filename = f"{name_without_ext}_modified.docx"
        
        # Log download start / 记录下载开始
        log_info('file_download_started', filename=download_filename)
        
        # Send file / 发送文件
        return send_file(
            processed_file_path,
            as_attachment=True,
            download_name=download_filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        # Log error / 记录错误
        log_error('error_occurred', error=str(e))
        return jsonify({
            'success': False,
            'message': f"{get_text('server_error')}: {str(e)}"
        }), 500

@document_bp.route('/document_info/<doc_id>', methods=['GET'])
def get_document_info(doc_id: str):
    """
    Get document information / 获取文档信息
    Returns detailed information about a specific document
    返回特定文档的详细信息
    """
    try:
        # Check if document exists / 检查文档是否存在
        if doc_id not in uploaded_documents:
            return jsonify({
                'success': False,
                'message': get_text('document_not_found')
            }), 404
        
        doc_info = uploaded_documents[doc_id].copy()
        
        # Remove sensitive file path information / 移除敏感的文件路径信息
        if 'file_path' in doc_info:
            del doc_info['file_path']
        if 'processed_file_path' in doc_info:
            del doc_info['processed_file_path']
        
        # Return document info directly in the expected format for frontend
        # 直接返回前端期望格式的文档信息
        response_data = {
            'success': True,
            'content': doc_info.get('content'),
            'filename': doc_info.get('original_filename'),
            'doc_info': doc_info.get('processor').get_document_info() if doc_info.get('processor') else None,
            'modifications': doc_info.get('modifications', []),
            'modified_content': doc_info.get('modified_content'),
            'modifications_applied': doc_info.get('modifications_applied', False)
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        # Log error / 记录错误
        log_error('error_occurred', error=str(e))
        return jsonify({
            'success': False,
            'message': f"{get_text('server_error')}: {str(e)}"
        }), 500

@document_bp.route('/cleanup/<doc_id>', methods=['DELETE'])
def cleanup_document(doc_id: str):
    """
    Clean up document files / 清理文档文件
    Removes document files and clears memory
    删除文档文件并清理内存
    """
    try:
        # Check if document exists / 检查文档是否存在
        if doc_id not in uploaded_documents:
            return jsonify({
                'success': False,
                'message': get_text('document_not_found')
            }), 404
        
        doc_info = uploaded_documents[doc_id]
        
        # Remove original file / 删除原始文件
        if 'file_path' in doc_info and os.path.exists(doc_info['file_path']):
            os.remove(doc_info['file_path'])
        
        # Remove processed file / 删除处理后的文件
        if 'processed_file_path' in doc_info and os.path.exists(doc_info['processed_file_path']):
            os.remove(doc_info['processed_file_path'])
        
        # Remove from memory / 从内存中删除
        del uploaded_documents[doc_id]
        
        return jsonify({
            'success': True,
            'message': get_text('document_cleaned')
        })
        
    except Exception as e:
        # Log error / 记录错误
        log_error('error_occurred', error=str(e))
        return jsonify({
            'success': False,
            'message': f"{get_text('server_error')}: {str(e)}"
        }), 500

@document_bp.route('/cleanup_all', methods=['DELETE'])
def cleanup_all_documents():
    """
    Clean up all document files / 清理所有文档文件
    Removes all document files and clears memory
    删除所有文档文件并清理内存
    """
    try:
        cleanup_count = 0
        
        # Clean up all documents / 清理所有文档
        for doc_id in list(uploaded_documents.keys()):
            doc_info = uploaded_documents[doc_id]
            
            # Remove original file / 删除原始文件
            if 'file_path' in doc_info and os.path.exists(doc_info['file_path']):
                os.remove(doc_info['file_path'])
            
            # Remove processed file / 删除处理后的文件
            if 'processed_file_path' in doc_info and os.path.exists(doc_info['processed_file_path']):
                os.remove(doc_info['processed_file_path'])
            
            cleanup_count += 1
        
        # Clear memory / 清理内存
        uploaded_documents.clear()
        
        return jsonify({
            'success': True,
            'message': get_text('all_documents_cleaned'),
            'cleaned_count': cleanup_count
        })
        
    except Exception as e:
        # Log error / 记录错误
        log_error('error_occurred', error=str(e))
        return jsonify({
            'success': False,
            'message': f"{get_text('server_error')}: {str(e)}"
        }), 500 