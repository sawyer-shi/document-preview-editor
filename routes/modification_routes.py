#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modification routes module / 修改条目路由模块
Handles modification items management and document processing
处理修改条目管理和文档处理
"""

import os
import tempfile
import json
import csv
import io
from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from utils.document_processor import EnhancedWordProcessor
from utils.i18n import get_text
from utils.logger import log_info, log_error
from config import Config
from .document_routes import uploaded_documents

# Create modification blueprint / 创建修改条目蓝图
modification_bp = Blueprint('modification', __name__)

# Global variables for storing modification items / 存储修改条目的全局变量
modification_items = {}

def decode_file_content(file_data: bytes, filename: str) -> str:
    """
    Decode file content with automatic encoding detection / 自动检测编码并解码文件内容
    
    Args:
        file_data: File data in bytes / 字节格式的文件数据
        filename: Original filename / 原始文件名
        
    Returns:
        Decoded file content / 解码后的文件内容
    """
    # Common encodings to try / 要尝试的常见编码
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin-1']
    
    for encoding in encodings:
        try:
            content = file_data.decode(encoding)
            # Log successful encoding detection / 记录成功的编码检测
            log_info('csv_encoding_detected', encoding=encoding, filename=filename)
            return content
        except UnicodeDecodeError:
            continue
    
    # If all encodings fail, use utf-8 with error handling
    # 如果所有编码都失败，使用utf-8并处理错误
    return file_data.decode('utf-8', errors='replace')

def parse_csv_modifications(csv_content: str) -> list:
    """
    Parse CSV content into modification list / 将CSV内容解析为修改列表
    
    Args:
        csv_content: CSV file content / CSV文件内容
        
    Returns:
        List of modification dictionaries / 修改字典列表
    """
    modifications = []
    
    try:
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        # Debug: log CSV headers
        fieldnames = csv_reader.fieldnames
        print(f"CSV字段名: {fieldnames}")
        
        row_count = 0
        for row in csv_reader:
            row_count += 1
            print(f"处理第{row_count}行: {dict(row)}")
            
            # Handle different CSV column names / 处理不同的CSV列名
            original_text = (row.get('original_text') or row.get('OriginalText') or 
                            row.get('original') or row.get('原文') or row.get('原始文本'))
            new_text = (row.get('new_text') or row.get('ModifiedText') or 
                       row.get('modified') or row.get('新文本') or row.get('修改后文本'))
            reason = (row.get('reason') or row.get('ModificationReason') or 
                     row.get('原因') or row.get('修改原因') or '')
            
            print(f"  原文: '{original_text}'")
            print(f"  新文: '{new_text}'")
            print(f"  原因: '{reason}'")
            
            if original_text and new_text:
                modifications.append({
                    'original_text': original_text.strip(),
                    'new_text': new_text.strip(),
                    'reason': reason.strip()
                })
                print(f"  ✅ 添加修改条目")
            else:
                print(f"  ❌ 跳过（缺少必要字段）")
        
        print(f"CSV解析完成，共{row_count}行，有效修改条目{len(modifications)}个")
        
    except Exception as e:
        print(f"CSV解析错误: {e}")
        import traceback
        traceback.print_exc()
    
    return modifications

@modification_bp.route('/add_modifications', methods=['POST'])
def add_modifications():
    """
    Add modification items API / 添加修改条目API
    Accepts modification items and applies them to documents
    接受修改条目并将其应用到文档
    """
    try:
        # Get document ID / 获取文档ID
        doc_id = request.form.get('doc_id') or request.json.get('doc_id') if request.is_json else None
        
        if not doc_id:
            return jsonify({
                'success': False,
                'message': get_text('no_document_id')
            })
        
        # Check if document exists / 检查文档是否存在
        if doc_id not in uploaded_documents:
            return jsonify({
                'success': False,
                'message': get_text('document_not_found')
            })
        
        modifications = []
        
        # Handle different input types / 处理不同的输入类型
        if request.is_json:
            # JSON input / JSON输入
            data = request.get_json()
            modifications = data.get('modifications', [])
        else:
            # Form input with file or text / 表单输入（文件或文本）
            if 'modifications_file' in request.files:
                # File upload / 文件上传
                file = request.files['modifications_file']
                if file.filename != '':
                    file_content = file.read()
                    csv_content = decode_file_content(file_content, file.filename)
                    modifications = parse_csv_modifications(csv_content)
            elif 'modifications' in request.form:
                # Text input / 文本输入
                modifications_text = request.form['modifications']
                try:
                    modifications = json.loads(modifications_text)
                except json.JSONDecodeError:
                    # Try to parse as CSV / 尝试解析为CSV
                    modifications = parse_csv_modifications(modifications_text)
        
        if not modifications:
            return jsonify({
                'success': False,
                'message': get_text('no_modifications_provided')
            })
        
        # Validate modifications format / 验证修改条目格式
        for i, mod in enumerate(modifications):
            if not isinstance(mod, dict) or 'original_text' not in mod or 'new_text' not in mod:
                return jsonify({
                    'success': False,
                    'message': f"{get_text('invalid_modification_format')}: {i+1}"
                })
        
        # Store modifications / 存储修改条目
        modification_items[doc_id] = {
            'doc_id': doc_id,
            'modifications': modifications,
            'created_time': datetime.now().isoformat()
        }
        
        # Process document with modifications / 使用修改条目处理文档
        doc_info = uploaded_documents[doc_id]
        
        # Log modification start / 记录修改开始
        log_info('document_modification_started')
        
        # Initialize document processor / 初始化文档处理器
        processor = EnhancedWordProcessor()
        
        # Load original document / 加载原始文档
        processor.load_document(doc_info['file_path'])
        
        # Log document copy creation / 记录文档副本创建
        log_info('document_copy_created')
        
        # Apply modifications / 应用修改
        success, message = processor.apply_modifications(modifications)
        
        if not success:
            return jsonify({
                'success': False,
                'message': message
            })
        
        # Save processed document / 保存处理后的文档
        processed_filename = f"processed_{doc_info['safe_filename']}"
        processed_file_path = os.path.join(Config.UPLOAD_FOLDER, f"{doc_id}_{processed_filename}")
        success, save_message = processor.save_modified_document(processed_file_path)
        
        if not success:
            return jsonify({
                'success': False,
                'message': save_message
            })
        
        # Extract modified document content for preview / 提取修改后的文档内容用于预览
        modified_content = processor.extract_content_with_formatting(processor.modified_doc)
        
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
            'process_time': datetime.now().isoformat()
        })
        
        # Log completion / 记录完成
        log_info('modifications_applied', paragraphs=paragraph_count, tables=table_count)
        log_info('modification_complete')
        
        return jsonify({
            'success': True,
            'message': get_text('modifications_applied'),
            'doc_id': doc_id,
            'modification_count': len(modifications),
            'paragraph_changes': paragraph_count,
            'table_changes': table_count,
            'download_url': f'/api/download_document/{doc_id}',
            'modified_content': modified_content
        })
        
    except Exception as e:
        # Log error / 记录错误
        log_error('error_occurred', error=str(e))
        return jsonify({
            'success': False,
            'message': f"{get_text('server_error')}: {str(e)}"
        }), 500

@modification_bp.route('/process_document', methods=['POST'])
def process_document():
    """
    Process document with stored modifications / 使用存储的修改条目处理文档
    Applies previously stored modifications to a document
    将之前存储的修改条目应用到文档
    """
    try:
        # Get request data / 获取请求数据
        data = request.get_json()
        doc_id = data.get('doc_id')
        
        if not doc_id:
            return jsonify({
                'success': False,
                'message': get_text('no_document_id')
            })
        
        # Check if document exists / 检查文档是否存在
        if doc_id not in uploaded_documents:
            return jsonify({
                'success': False,
                'message': get_text('document_not_found')
            })
        
        # Check if modifications exist / 检查修改条目是否存在
        if doc_id not in modification_items:
            return jsonify({
                'success': False,
                'message': get_text('no_modifications_found')
            })
        
        doc_info = uploaded_documents[doc_id]
        mod_info = modification_items[doc_id]
        
        # Log processing start / 记录处理开始
        log_info('document_processed', doc_id=doc_id)
        
        # Initialize document processor / 初始化文档处理器
        processor = EnhancedWordProcessor()
        
        # Load original document / 加载原始文档
        processor.load_document(doc_info['file_path'])
        
        # Apply modifications / 应用修改
        success, message = processor.apply_modifications(mod_info['modifications'])
        
        if not success:
            return jsonify({
                'success': False,
                'message': message
            })
        
        # Save processed document / 保存处理后的文档
        processed_filename = f"processed_{doc_info['safe_filename']}"
        processed_file_path = os.path.join(Config.UPLOAD_FOLDER, f"{doc_id}_{processed_filename}")
        success, save_message = processor.save_modified_document(processed_file_path)
        
        if not success:
            return jsonify({
                'success': False,
                'message': save_message
            })
        
        # Extract modified document content for preview / 提取修改后的文档内容用于预览
        modified_content = processor.extract_content_with_formatting(processor.modified_doc)
        
        # Count modifications for reporting / 统计修改数量用于报告
        paragraph_count = len(mod_info['modifications'])
        table_count = 0
        
        # Update document info / 更新文档信息
        uploaded_documents[doc_id].update({
            'processed': True,
            'modifications_applied': True,
            'processed_file_path': processed_file_path,
            'processed_filename': processed_filename,
            'modification_count': len(mod_info['modifications']),
            'paragraph_changes': paragraph_count,
            'table_changes': table_count,
            'process_time': datetime.now().isoformat()
        })
        
        # Log completion / 记录完成
        log_info('modifications_applied', paragraphs=paragraph_count, tables=table_count)
        
        return jsonify({
            'success': True,
            'message': get_text('document_processed'),
            'doc_id': doc_id,
            'modification_count': len(mod_info['modifications']),
            'paragraph_changes': paragraph_count,
            'table_changes': table_count,
            'download_url': f'/api/download_document/{doc_id}',
            'modified_content': modified_content
        })
        
    except Exception as e:
        # Log error / 记录错误
        log_error('error_occurred', error=str(e))
        return jsonify({
            'success': False,
            'message': f"{get_text('server_error')}: {str(e)}"
        }), 500 