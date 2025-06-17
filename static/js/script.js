// 全局变量
let currentDocId = null;
let originalContent = null;
let modifiedContent = null;
let modifications = [];
let appliedModifications = []; // 新增：追踪已应用的修改
let selectedModificationIndex = -1;
let currentLanguage = 'zh'; // 默认语言
let i18nTexts = {}; // 存储翻译文本

// DOM元素
const documentInput = document.getElementById('documentInput');
const uploadBtn = document.getElementById('uploadBtn');
const fileName = document.getElementById('fileName');
const originalContentDiv = document.getElementById('originalContent');
const modificationsContentDiv = document.getElementById('modificationsContent');
const previewContentDiv = document.getElementById('previewContent');
const addModBtn = document.getElementById('addModBtn');
const applyModsBtn = document.getElementById('applyModsBtn');
const clearModsBtn = document.getElementById('clearModsBtn');
const downloadBtn = document.getElementById('downloadBtn');
const modificationModal = document.getElementById('modificationModal');
const loadingOverlay = document.getElementById('loadingOverlay');
const messageToast = document.getElementById('messageToast');

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeLanguage();
    initializeEventListeners();
    
    // 强制设置文件上传相关控件为英文
    forceFileUploadTextToEnglish();
    
    // 检查是否有自动加载参数
    checkAutoLoadParams();
});

// 获取翻译文本
function getText(key, fallback = key) {
    if (i18nTexts[currentLanguage] && i18nTexts[currentLanguage][key]) {
        return i18nTexts[currentLanguage][key];
    }
    return fallback;
}

// 加载翻译文本
async function loadTranslations() {
    const translations = {
        zh: {
            save: '保存',
            update: '更新',
            cancel: '取消',
            delete: '删除',
            edit: '编辑',
            upload_success: '文档上传成功',
            upload_failed: '上传失败',
            invalid_file_format: '请选择支持的文档格式文件 (.docx 或 .txt)',
            preview_prompt: '应用修改后可预览最终文档',
            unsaved_changes: '您有未保存的修改，确定要离开吗？',
            language_change_failed: '语言切换失败',
            language_change_confirm: '⚠️ 注意：当前数据将被清空！确认继续切换语言？',
            add_modification: '添加修改条目',
            edit_modification: '编辑修改条目',
            fill_all_fields: '请填写所有字段',
            modification_updated: '修改条目已更新',
            modification_added: '修改条目已添加',
            modification_deleted: '修改条目已删除',
            reapply_needed: '修改已更新，请重新应用修改以查看效果',
            no_modifications: '暂无修改条目',
            no_modifications_to_apply: '没有可应用的修改',
            modifications_applied: '修改应用成功',
            original_text: '原文内容',
            new_text: '修改为',
            modification_reason: '修改原因',
            total_modifications: '总计',
            applied: '已应用',
            pending: '待应用',
            csv_invalid_format: 'CSV文件格式不正确',
            csv_missing_fields: '缺少必需字段',
            csv_empty_data: '文件中没有有效数据',
            csv_import_success: '成功导入{count}条修改条目',
            csv_import_failed: 'CSV导入失败',
            total_records: '共{count}条记录',
            csv_validation_success: '文件验证通过',
                          csv_validation_failed: '文件验证失败',
              select_csv_file: 'Select CSV File',
              csv_template_downloaded: 'CSV模板文件已下载'
        },
        en: {
            save: 'Save',
            update: 'Update', 
            cancel: 'Cancel',
            delete: 'Delete',
            edit: 'Edit',
            upload_success: 'Document uploaded successfully',
            upload_failed: 'Upload failed',
            invalid_file_format: 'Please select supported document format (.docx or .txt)',
            preview_prompt: 'Preview will be available after applying modifications',
            unsaved_changes: 'You have unsaved changes. Are you sure you want to leave?',
            language_change_failed: 'Language change failed',
            language_change_confirm: '⚠️ Warning: Current data will be cleared! Confirm language switch?',
            add_modification: 'Add',
            edit_modification: 'Edit Modification',
            fill_all_fields: 'Please fill in all fields',
            modification_updated: 'Modification item updated',
            modification_added: 'Modification item added',
            modification_deleted: 'Modification item deleted',
            reapply_needed: 'Modifications updated, please reapply to see effects',
            no_modifications: 'No modifications',
            no_modifications_to_apply: 'No modifications to apply',
            modifications_applied: 'Modifications applied successfully',
            original_text: 'Original Text',
            new_text: 'Modified Text',
            modification_reason: 'Modification Reason',
            total_modifications: 'Total',
            applied: 'Applied',
            pending: 'Pending',
            csv_invalid_format: 'Invalid CSV file format',
            csv_missing_fields: 'Missing required fields',
            csv_empty_data: 'No valid data in file',
            csv_import_success: 'Successfully imported {count} modification items',
            csv_import_failed: 'CSV import failed',
            total_records: '{count} records in total',
            csv_validation_success: 'File validation passed',
                          csv_validation_failed: 'File validation failed',
              select_csv_file: 'Select CSV File',
              csv_template_downloaded: 'CSV template file downloaded'
        }
    };
    i18nTexts = translations;
}

// 强制设置文件上传相关控件为英文
function forceFileUploadTextToEnglish() {
    // 确保批量导入按钮文本为英文
    const selectCsvBtn = document.getElementById('selectCsvBtn');
    if (selectCsvBtn) {
        selectCsvBtn.textContent = 'Select CSV File';
    }
    
    // 确保文件名显示区域为空
    const csvFileName = document.getElementById('csvFileName');
    if (csvFileName && !csvFileName.textContent) {
        csvFileName.textContent = '';
    }
    
    // 设置所有文件输入框的样式，确保原生控件不显示
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.style.display = 'none';
        input.style.opacity = '0';
        input.style.position = 'absolute';
        input.style.left = '-9999px';
    });
}

// 初始化语言设置
async function initializeLanguage() {
    try {
        await loadTranslations();
        const response = await fetch('/api/get_language');
        const result = await response.json();
        if (result.success) {
            currentLanguage = result.language;
            document.documentElement.lang = currentLanguage;
        }
    } catch (error) {
        console.error('获取语言设置失败:', error);
    }
}

// 语言切换标志，用于禁用beforeunload提示
let isChangingLanguage = false;

// 更改语言
async function changeLanguage(language) {
    // 检查是否有数据需要清空
    const hasData = modifications.length > 0 || currentDocId !== null;
    
    if (hasData) {
        // 显示确认提示
        const confirmMessage = getText('language_change_confirm');
        if (!confirm(confirmMessage)) {
            // 用户取消，恢复原来的语言选择
            const currentLang = currentLanguage;
            setTimeout(() => {
                const radioButtons = document.querySelectorAll('input[name="language"]');
                radioButtons.forEach(radio => {
                    radio.checked = radio.value === currentLang;
                });
            }, 0);
            return;
        }
    }
    
    // 设置语言切换标志，禁用beforeunload提示
    isChangingLanguage = true;
    
    try {
        const response = await fetch('/api/set_language', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({language: language})
        });
        
        const result = await response.json();
        if (result.success) {
            // 重新加载页面以应用新语言
            window.location.reload();
        } else {
            showMessage(result.message, 'error');
            // 如果失败，重置标志
            isChangingLanguage = false;
        }
    } catch (error) {
        showMessage(getText('language_change_failed') + ': ' + error.message, 'error');
        // 如果失败，重置标志
        isChangingLanguage = false;
    }
}

function initializeEventListeners() {
    // 文件上传
    uploadBtn.addEventListener('click', () => documentInput.click());
    documentInput.addEventListener('change', handleFileUpload);
    
    // 修改条目操作
    addModBtn.addEventListener('click', showModificationModal);
    applyModsBtn.addEventListener('click', applyModifications);
    clearModsBtn.addEventListener('click', clearModifications);
    downloadBtn.addEventListener('click', downloadModifiedDocument);
    
    // 批量导入操作
    const batchImportBtn = document.getElementById('batchImportBtn');
    if (batchImportBtn) {
        batchImportBtn.addEventListener('click', showBatchImportModal);
        console.log('Batch import button event listener added');
    } else {
        console.error('Batch import button not found');
    }
    
    const downloadTemplateBtn = document.getElementById('downloadTemplateBtn');
    if (downloadTemplateBtn) {
        downloadTemplateBtn.addEventListener('click', downloadCsvTemplate);
        console.log('Download template button event listener added');
    }
    
    const selectCsvBtn = document.getElementById('selectCsvBtn');
    if (selectCsvBtn) {
        selectCsvBtn.addEventListener('click', () => {
            console.log('Select CSV button clicked');
            document.getElementById('csvFileInput').click();
        });
        console.log('Select CSV button event listener added');
    }
    
    const csvFileInput = document.getElementById('csvFileInput');
    if (csvFileInput) {
        csvFileInput.addEventListener('change', handleCsvUpload);
        console.log('CSV file input event listener added');
    }
    
    const importCsvBtn = document.getElementById('importCsvBtn');
    if (importCsvBtn) {
        importCsvBtn.addEventListener('click', importCsvData);
        console.log('Import CSV button event listener added');
    }
    
    // 模态框操作
    const modal = document.getElementById('modificationModal');
    const closeBtn = modal.querySelector('.close');
    const saveBtn = document.getElementById('saveModBtn');
    const cancelBtn = document.getElementById('cancelModBtn');
    
    closeBtn.addEventListener('click', hideModificationModal);
    cancelBtn.addEventListener('click', hideModificationModal);
    saveBtn.addEventListener('click', saveModification);
    
    // 点击模态框外部关闭
    window.addEventListener('click', (event) => {
        const modificationModal = document.getElementById('modificationModal');
        const batchImportModal = document.getElementById('batchImportModal');
        
        if (event.target === modificationModal) {
            hideModificationModal();
        } else if (event.target === batchImportModal) {
            hideBatchImportModal();
        }
    });
}

// 文件上传处理
async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    if (!file.name.endsWith('.docx') && !file.name.endsWith('.txt')) {
        showMessage(getText('invalid_file_format'), 'error');
        return;
    }
    
    showLoading();
    
    const formData = new FormData();
    formData.append('document', file);
    
    try {
        const response = await fetch('/api/upload_document', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentDocId = result.doc_id;
            originalContent = result.content;
            fileName.textContent = result.filename;
            
            // 清空之前的修改条目
            modifications = [];
            appliedModifications = [];
            modifiedContent = null;
            
            displayOriginalDocument(result.content);
            enableModificationControls();
            updateModificationsList();
            updateModificationStats(0, 0, 0);
            
            // 清空预览区域
            previewContentDiv.innerHTML = `
                <div class="placeholder">
                    <i class="icon-preview"></i>
                    <p>${getText('preview_prompt')}</p>
                </div>
            `;
            
            // 禁用下载按钮
            downloadBtn.disabled = true;
            
            showMessage(getText('upload_success'), 'success');
        } else {
            showMessage(result.message, 'error');
        }
    } catch (error) {
        showMessage(getText('upload_failed') + ': ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

// 显示原始文档内容
function displayOriginalDocument(content) {
    const html = generateDocumentHTML(content, 'original');
    originalContentDiv.innerHTML = `<div class="document-content">${html}</div>`;
}

// 显示修改后文档内容
function displayModifiedDocument(content) {
    const html = generateDocumentHTML(content, 'modified');
    previewContentDiv.innerHTML = `<div class="document-content">${html}</div>`;
}

// 生成文档HTML
function generateDocumentHTML(content, type) {
    let html = '';
    
    // Check if content is valid array / 检查content是否为有效数组
    if (!content || !Array.isArray(content)) {
        return '<div class="placeholder"><p>No content available</p></div>';
    }
    
    content.forEach((item, index) => {
        if (item.type === 'paragraph') {
            html += generateParagraphHTML(item, index, type);
        } else if (item.type === 'table') {
            html += generateTableHTML(item, index, type);
        }
    });
    
    return html;
}

function generateParagraphHTML(item, index, type) {
    const paragraphId = `${type}-para-${index}`;
    let paragraphHTML = '';
    let paragraphStyles = [];
    
    // 段落对齐
    if (item.alignment) {
        paragraphStyles.push(`text-align: ${item.alignment}`);
    }
    
    // 段落格式
    if (item.paragraph_format) {
        const pf = item.paragraph_format;
        if (pf.space_before > 0) paragraphStyles.push(`margin-top: ${pf.space_before}pt`);
        if (pf.space_after > 0) paragraphStyles.push(`margin-bottom: ${pf.space_after}pt`);
        if (pf.line_spacing && pf.line_spacing !== 1.0) paragraphStyles.push(`line-height: ${pf.line_spacing}`);
        if (pf.left_indent > 0) paragraphStyles.push(`margin-left: ${pf.left_indent}pt`);
        if (pf.right_indent > 0) paragraphStyles.push(`margin-right: ${pf.right_indent}pt`);
        if (pf.first_line_indent !== 0) paragraphStyles.push(`text-indent: ${pf.first_line_indent}pt`);
    }
    
    // 如果有runs（格式化文本）
    if (item.runs && item.runs.length > 0) {
        item.runs.forEach(run => {
            paragraphHTML += generateRunHTML(run);
        });
    } else {
        paragraphHTML = escapeHtml(item.text);
    }
    
    // 添加图片
    if (item.images && item.images.length > 0) {
        item.images.forEach(image => {
            paragraphHTML += `
                <div class="word-image-container">
                    <img src="data:${image.mime_type};base64,${image.data}" 
                         alt="${image.filename}" 
                         class="word-document-image" />
                    <div class="word-image-caption">${image.filename}</div>
                </div>
            `;
        });
    }
    
    let paragraphClasses = 'word-paragraph';
    if (type === 'modified') {
        // 检查是否为修改的段落
        const isModified = modifications.some(mod => 
            item.text.includes(mod.new_text) && !item.text.includes(mod.original_text)
        );
        if (isModified) {
            paragraphClasses += ' modified';
        }
    }
    
    const styleAttr = paragraphStyles.length > 0 ? ` style="${paragraphStyles.join('; ')}"` : '';
    
    return `<div class="${paragraphClasses}" id="${paragraphId}" data-text="${escapeHtml(item.text)}" data-style="${item.style || 'Normal'}"${styleAttr}>${paragraphHTML}</div>`;
}

function generateRunHTML(run) {
    let runHTML = escapeHtml(run.text);
    let runStyles = [];
    let runClasses = ['word-run'];
    
    // 字体样式
    if (run.bold) runStyles.push('font-weight: bold');
    if (run.italic) runStyles.push('font-style: italic');
    if (run.underline) runStyles.push('text-decoration: underline');
    
    // 字体属性
    if (run.font_name) runStyles.push(`font-family: "${run.font_name}", serif`);
    if (run.font_size) runStyles.push(`font-size: ${run.font_size}pt`);
    if (run.font_color) runStyles.push(`color: ${run.font_color}`);
    
    // 高亮颜色
    if (run.highlight_color) runStyles.push(`background-color: ${run.highlight_color}`);
    
    // 上标下标
    if (run.superscript) runStyles.push('vertical-align: super; font-size: smaller');
    if (run.subscript) runStyles.push('vertical-align: sub; font-size: smaller');
    
    const styleAttr = runStyles.length > 0 ? ` style="${runStyles.join('; ')}"` : '';
    
    return `<span class="${runClasses.join(' ')}"${styleAttr}>${runHTML}</span>`;
}

function generateTableHTML(item, index, type) {
    let tableStyles = [];
    let tableClasses = 'word-table';
    
    // 表格格式
    if (item.table_format) {
        const tf = item.table_format;
        if (tf.width) tableStyles.push(`width: ${tf.width}`);
        if (tf.border_style && tf.border_width && tf.border_color) {
            tableStyles.push(`border: ${tf.border_width} ${tf.border_style} ${tf.border_color}`);
            tableStyles.push('border-collapse: collapse');
        }
    }
    
    const styleAttr = tableStyles.length > 0 ? ` style="${tableStyles.join('; ')}"` : '';
    let html = `<table class="${tableClasses}" data-style="${item.style || 'Table Grid'}"${styleAttr}>`;
    
    item.rows.forEach((row, rowIndex) => {
        html += '<tr class="word-table-row">';
        row.forEach(cell => {
            const tag = rowIndex === 0 ? 'th' : 'td';
            let cellHTML = '';
            let cellStyles = [];
            
            // 单元格格式
            if (cell.cell_format) {
                const cf = cell.cell_format;
                if (cf.background_color) cellStyles.push(`background-color: ${cf.background_color}`);
                if (cf.vertical_alignment) cellStyles.push(`vertical-align: ${cf.vertical_alignment}`);
                if (cf.padding) cellStyles.push(`padding: ${cf.padding}`);
            }
            
            // 默认单元格样式
            cellStyles.push('border: 1px solid #000');
            
            // 处理单元格中的段落
            if (cell.paragraphs && cell.paragraphs.length > 0) {
                cell.paragraphs.forEach(para => {
                    let paraHTML = '';
                    let paraStyles = [];
                    
                    if (para.alignment) {
                        paraStyles.push(`text-align: ${para.alignment}`);
                    }
                    
                    if (para.runs && para.runs.length > 0) {
                        para.runs.forEach(run => {
                            paraHTML += generateRunHTML(run);
                        });
                    } else {
                        paraHTML = escapeHtml(para.text);
                    }
                    
                    const paraStyleAttr = paraStyles.length > 0 ? ` style="${paraStyles.join('; ')}"` : '';
                    cellHTML += `<div class="word-cell-paragraph"${paraStyleAttr}>${paraHTML}</div>`;
                });
            } else {
                cellHTML = escapeHtml(cell.text);
            }
            
            const cellStyleAttr = cellStyles.length > 0 ? ` style="${cellStyles.join('; ')}"` : '';
            html += `<${tag} class="word-table-cell"${cellStyleAttr}>${cellHTML}</${tag}>`;
        });
        html += '</tr>';
    });
    
    html += '</table>';
    return html;
}

// HTML转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 启用修改控件
function enableModificationControls() {
    addModBtn.disabled = false;
    clearModsBtn.disabled = false;
    document.getElementById('batchImportBtn').disabled = false;
}

// 显示修改条目模态框
function showModificationModal() {
    const modal = document.getElementById('modificationModal');
    
    // 确保是新增模式
    modal.removeAttribute('data-edit-index');
    const modalTitle = modal.querySelector('.modal-header h3');
    modalTitle.textContent = getText('add_modification', '添加修改条目');
    const saveBtn = document.getElementById('saveModBtn');
    saveBtn.textContent = getText('save');
    
    // 清空表单
    document.getElementById('originalText').value = '';
    document.getElementById('newText').value = '';
    document.getElementById('reason').value = '';
    
    modal.style.display = 'block';
}

// 隐藏修改条目模态框
function hideModificationModal() {
    const modal = document.getElementById('modificationModal');
    modal.style.display = 'none';
    
    // 清理编辑状态
    modal.removeAttribute('data-edit-index');
    const modalTitle = modal.querySelector('.modal-header h3');
    modalTitle.textContent = getText('add_modification', '添加修改条目');
    const saveBtn = document.getElementById('saveModBtn');
    saveBtn.textContent = getText('save');
    
    // 清空表单
    document.getElementById('originalText').value = '';
    document.getElementById('newText').value = '';
    document.getElementById('reason').value = '';
}

// 保存修改条目
function saveModification() {
    const originalText = document.getElementById('originalText').value.trim();
    const newText = document.getElementById('newText').value.trim();
    const reason = document.getElementById('reason').value.trim();
    
    if (!originalText || !newText || !reason) {
        showMessage(getText('fill_all_fields', '请填写所有字段'), 'error');
        return;
    }
    
    const modification = {
        original_text: originalText,
        new_text: newText,
        reason: reason
    };
    
    const modal = document.getElementById('modificationModal');
    const editIndex = modal.getAttribute('data-edit-index');
    
    if (editIndex !== null && editIndex !== '') {
        // 编辑模式
        const index = parseInt(editIndex);
        const oldMod = modifications[index];
        
        // 检查原修改是否已应用，如果是则从已应用列表中移除
        const oldModIndex = appliedModifications.findIndex(appliedMod => 
            appliedMod.original_text === oldMod.original_text && 
            appliedMod.new_text === oldMod.new_text && 
            appliedMod.reason === oldMod.reason
        );
        
        if (oldModIndex !== -1) {
            appliedModifications.splice(oldModIndex, 1);
        }
        
        modifications[index] = modification;
        showMessage(getText('modification_updated', `修改条目 #${index + 1} 已更新`), 'success');
        
        // 重置模态框状态
        modal.removeAttribute('data-edit-index');
        const modalTitle = modal.querySelector('.modal-header h3');
        modalTitle.textContent = getText('add_modification', '添加修改条目');
        const saveBtn = document.getElementById('saveModBtn');
        saveBtn.textContent = getText('save');
        
        // 如果之前有应用过修改，提示需要重新应用
        if (modifiedContent) {
            showMessage(getText('reapply_needed', '修改已更新，请重新应用修改以查看效果'), 'info');
        }
    } else {
        // 新增模式
        modifications.push(modification);
        showMessage(getText('modification_added', '修改条目已添加'), 'success');
    }
    
    updateModificationsList();
    hideModificationModal();
    
    // 启用应用修改按钮
    applyModsBtn.disabled = false;
}

// 更新修改条目列表
function updateModificationsList() {
    // 清除当前选中状态和视觉效果
    clearHighlights();
    clearConnectionLines();
    selectedModificationIndex = -1;
    
    const totalCount = modifications.length;
    const appliedCount = appliedModifications.length;
    const pendingCount = totalCount - appliedCount;
    
    // 更新统计信息
    updateModificationStats(totalCount, appliedCount, pendingCount);
    
    if (modifications.length === 0) {
        modificationsContentDiv.innerHTML = `
            <div class="placeholder">
                <i class="icon-edit"></i>
                <p>${getText('no_modifications', '暂无修改条目')}</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    modifications.forEach((mod, index) => {
        // 检查当前修改是否在已应用列表中
        const isApplied = appliedModifications.some(appliedMod => 
            appliedMod.original_text === mod.original_text && 
            appliedMod.new_text === mod.new_text && 
            appliedMod.reason === mod.reason
        );
        
        const itemClass = isApplied ? 'modification-item applied' : 'modification-item pending';
        const indexClass = isApplied ? 'modification-index applied' : 'modification-index pending';
        
        html += `
            <div class="${itemClass}" data-index="${index}">
                <div class="modification-header" onclick="selectModification(${index})">
                    <div class="modification-index-container">
                        <div class="${indexClass}">${index + 1}</div>
                        <button class="pointer-indicator" onclick="selectModification(${index}); event.stopPropagation();" title="${getText('point_to_this_item', '指向此条目')}">👈</button>
                    </div>
                    <div class="modification-actions">
                        <button class="btn btn-edit" onclick="editModification(${index}, event)" title="${getText('edit')}">
                            ${getText('edit')}
                        </button>
                        <button class="btn btn-danger" onclick="removeModification(${index}, event)" title="${getText('delete')}">
                            ${getText('delete')}
                        </button>
                    </div>
                </div>
                <div class="modification-content">
                    <div class="modification-field">
                        <label>${getText('original_text')}:</label>
                        <textarea class="field-content original-text editable-field" 
                                  data-index="${index}" 
                                  data-field="original_text"
                                  title="${escapeHtml(mod.original_text)}"
                                  onchange="updateModificationField(${index}, 'original_text', this.value)"
                                  onblur="updateModificationField(${index}, 'original_text', this.value)">${escapeHtml(mod.original_text)}</textarea>
                    </div>
                    <div class="modification-field">
                        <label>${getText('new_text')}:</label>
                        <textarea class="field-content new-text editable-field" 
                                  data-index="${index}" 
                                  data-field="new_text"
                                  title="${escapeHtml(mod.new_text)}"
                                  onchange="updateModificationField(${index}, 'new_text', this.value)"
                                  onblur="updateModificationField(${index}, 'new_text', this.value)">${escapeHtml(mod.new_text)}</textarea>
                    </div>
                    <div class="modification-field">
                        <label>${getText('modification_reason')}:</label>
                        <textarea class="field-content reason editable-field" 
                                  data-index="${index}" 
                                  data-field="reason"
                                  title="${escapeHtml(mod.reason)}"
                                  onchange="updateModificationField(${index}, 'reason', this.value)"
                                  onblur="updateModificationField(${index}, 'reason', this.value)">${escapeHtml(mod.reason)}</textarea>
                    </div>
                </div>
            </div>
        `;
    });
    
    modificationsContentDiv.innerHTML = html;
}

// 更新修改条目统计信息
function updateModificationStats(total, applied, pending) {
    // 查找或创建统计信息容器
    let statsContainer = document.getElementById('modificationStats');
    if (!statsContainer) {
        // 创建统计信息容器
        const panelHeader = document.querySelector('.middle-panel .panel-header');
        statsContainer = document.createElement('div');
        statsContainer.id = 'modificationStats';
        statsContainer.className = 'modification-stats';
        panelHeader.appendChild(statsContainer); // 添加到panel-header的末尾
    }
    
    // 更新统计信息
    statsContainer.innerHTML = `
        <div class="stats-item">
            <span class="stats-label">${getText('total_modifications', '总计')}:</span>
            <span class="stats-value total">${total}</span>
        </div>
        <div class="stats-item">
            <span class="stats-label">${getText('applied', '已应用')}:</span>
            <span class="stats-value applied">${applied}</span>
        </div>
        <div class="stats-item">
            <span class="stats-label">${getText('pending', '待应用')}:</span>
            <span class="stats-value pending">${pending}</span>
        </div>
    `;
}

// 编辑修改条目
function editModification(index, event) {
    event.stopPropagation();
    
    const modification = modifications[index];
    
    // 在模态框中预填充当前数据
    document.getElementById('originalText').value = modification.original_text;
    document.getElementById('newText').value = modification.new_text;
    document.getElementById('reason').value = modification.reason;
    
    // 设置编辑模式
    const modal = document.getElementById('modificationModal');
    modal.setAttribute('data-edit-index', index);
    
    // 更改模态框标题
    const modalTitle = modal.querySelector('.modal-header h3');
    modalTitle.textContent = getText('edit_modification', `编辑修改条目 #${index + 1}`);
    
    // 更改保存按钮文本
    const saveBtn = document.getElementById('saveModBtn');
    saveBtn.textContent = getText('update');
    
    modificationModal.style.display = 'block';
}

// 选中修改条目
function selectModification(index) {
    // 立即清除之前的选中状态和所有视觉效果
    document.querySelectorAll('.modification-item').forEach(item => {
        item.classList.remove('selected');
    });
    clearHighlights();
    clearConnectionLines();
    
    // 重置选中索引
    selectedModificationIndex = -1;
    
    // 选中当前条目
    const selectedItem = document.querySelector(`[data-index="${index}"]`);
    if (selectedItem) {
        selectedItem.classList.add('selected');
        selectedModificationIndex = index;
        
        // 延迟处理，确保DOM状态完全清除
        setTimeout(() => {
            // 重新高亮对应的文本
            highlightText(modifications[index]);
            
            // 再次延迟绘制连接线，确保高亮完成后重新计算位置
            setTimeout(() => {
                drawConnectionLines(modifications[index]);
            }, 150);
        }, 50);
    }
}

// 高亮文本
function highlightText(modification) {
    const originalText = modification.original_text;
    const newText = modification.new_text;
    
    console.log('开始高亮文本:', { originalText, newText });
    
    // 清除之前的高亮
    clearHighlights();
    
    // 在原始文档中高亮原始文本（黄色背景）
    highlightTextInContainer(originalContentDiv, originalText, 'highlight-original');
    
    // 在原始文档中添加字符级别的差异高亮（蓝色背景）
    highlightCharacterDifferencesInOriginal(originalText, newText);
    
    // 在修改后文档中高亮新文本（红色背景）
    if (modifiedContent) {
        highlightTextInContainer(previewContentDiv, newText, 'highlight-modified');
        
        // 在修改后文档中添加字符级别的差异高亮（蓝色背景）
        highlightCharacterDifferencesInModified(originalText, newText);
    } else {
        console.log('没有修改后的文档内容');
    }
}

// 新增：在原文档中应用字符级别差异高亮
function highlightCharacterDifferencesInOriginal(originalText, newText) {
    if (!originalText || !newText || originalText === newText) {
        return;
    }
    
    console.log('开始原文档字符级差异高亮:', { originalText, newText });
    
    // 找到所有已经高亮的原文档元素
    const originalHighlights = document.querySelectorAll('#originalContent .highlight-original, #originalContent .highlight-original-run');
    
    originalHighlights.forEach(element => {
        // 对每个高亮元素进行字符级差异标记（原文档视角）
        applyCharacterDifferencesInOriginal(element, originalText, newText);
    });
}

// 新增：在修改后文档中应用字符级别差异高亮
function highlightCharacterDifferencesInModified(originalText, newText) {
    if (!originalText || !newText || originalText === newText) {
        return;
    }
    
    console.log('开始修改后文档字符级差异高亮:', { originalText, newText });
    
    // 找到所有已经高亮的修改后文档元素
    const modifiedHighlights = document.querySelectorAll('#previewContent .highlight-modified, #previewContent .highlight-modified-run');
    
    modifiedHighlights.forEach(element => {
        // 对每个高亮元素进行字符级差异标记（修改后文档视角）
        applyCharacterDifferencesInModified(element, originalText, newText);
    });
}

// 新增：在原文档中应用字符级差异标记
function applyCharacterDifferencesInOriginal(element, originalText, newText) {
    try {
        const elementText = element.textContent;
        
        // 检查元素是否包含原文本
        if (!elementText.includes(originalText)) {
            return;
        }
        
        // 计算字符级差异（从原文档角度）
        const diffs = computeCharacterDifferencesForOriginal(originalText, newText);
        
        if (diffs.length === 0) {
            return;
        }
        
        // 在元素中应用字符级高亮（原文档）
        applyCharacterHighlightingInOriginal(element, originalText, diffs);
        
    } catch (error) {
        console.error('应用原文档字符级差异时出错:', error);
    }
}

// 新增：在修改后文档中应用字符级差异标记
function applyCharacterDifferencesInModified(element, originalText, newText) {
    try {
        const elementText = element.textContent;
        
        // 检查元素是否包含新文本
        if (!elementText.includes(newText)) {
            return;
        }
        
        // 计算字符级差异（从修改后文档角度）
        const diffs = computeCharacterDifferencesForModified(originalText, newText);
        
        if (diffs.length === 0) {
            return;
        }
        
        // 在元素中应用字符级高亮（修改后文档）
        applyCharacterHighlightingInModified(element, newText, diffs);
        
    } catch (error) {
        console.error('应用修改后文档字符级差异时出错:', error);
    }
}

// 新增：计算原文档的字符级差异（标记将要被修改的字符）
function computeCharacterDifferencesForOriginal(original, modified) {
    const differences = [];
    const maxLength = Math.max(original.length, modified.length);
    
    for (let i = 0; i < maxLength; i++) {
        const originalChar = i < original.length ? original[i] : null;
        const modifiedChar = i < modified.length ? modified[i] : null;
        
        if (originalChar !== null && modifiedChar === null) {
            // 将要被删除的字符
            differences.push({
                type: 'to_be_deleted',
                char: originalChar,
                position: i
            });
        } else if (originalChar !== null && originalChar !== modifiedChar) {
            // 将要被替换的字符
            differences.push({
                type: 'to_be_changed',
                char: originalChar,
                position: i
            });
        }
        // 相同字符和新增字符（原文档中不存在）无需处理
    }
    
    console.log('原文档字符差异计算结果:', differences);
    return differences;
}

// 新增：计算修改后文档的字符级差异（标记已经被修改的字符）
function computeCharacterDifferencesForModified(original, modified) {
    const differences = [];
    const maxLength = Math.max(original.length, modified.length);
    
    for (let i = 0; i < maxLength; i++) {
        const originalChar = i < original.length ? original[i] : null;
        const modifiedChar = i < modified.length ? modified[i] : null;
        
        if (originalChar === null && modifiedChar !== null) {
            // 新增的字符
            differences.push({
                type: 'added',
                char: modifiedChar,
                position: i
            });
        } else if (originalChar !== modifiedChar && modifiedChar !== null) {
            // 替换的字符
            differences.push({
                type: 'changed',
                char: modifiedChar,
                position: i
            });
        }
        // 删除的字符（在修改后文本中不显示）和相同字符无需处理
    }
    
    console.log('修改后文档字符差异计算结果:', differences);
    return differences;
}

// 新增：在原文档元素中应用字符级高亮
function applyCharacterHighlightingInOriginal(element, targetText, differences) {
    try {
        const elementText = element.textContent;
        
        // 找到目标文本在元素中的位置
        const textIndex = elementText.indexOf(targetText);
        if (textIndex === -1) {
            return;
        }
        
        // 处理原文档的字符高亮
        let highlightedText = '';
        for (let i = 0; i < targetText.length; i++) {
            const char = targetText[i];
            const shouldHighlight = differences.some(diff => 
                diff.position === i && 
                (diff.type === 'to_be_deleted' || diff.type === 'to_be_changed')
            );
            
            if (shouldHighlight) {
                highlightedText += `<span class="highlight-changed-char">${escapeHtml(char)}</span>`;
            } else {
                highlightedText += escapeHtml(char);
            }
        }
        
        // 替换元素中的目标文本
        const originalHTML = element.innerHTML;
        const escapedTargetText = escapeHtml(targetText);
        
        // 尝试直接替换文本内容
        if (originalHTML.includes(escapedTargetText)) {
            element.innerHTML = originalHTML.replace(escapedTargetText, highlightedText);
        } else {
            // 如果直接替换失败，尝试处理文本节点
            replaceTextInElement(element, targetText, highlightedText);
        }
        
        console.log('原文档字符级高亮应用完成:', { targetText, differences: differences.length });
        
    } catch (error) {
        console.error('应用原文档字符高亮时出错:', error);
    }
}

// 新增：在修改后文档元素中应用字符级高亮
function applyCharacterHighlightingInModified(element, targetText, differences) {
    try {
        const elementText = element.textContent;
        
        // 找到目标文本在元素中的位置
        const textIndex = elementText.indexOf(targetText);
        if (textIndex === -1) {
            return;
        }
        
        // 处理修改后文档的字符高亮
        let highlightedText = '';
        for (let i = 0; i < targetText.length; i++) {
            const char = targetText[i];
            const shouldHighlight = differences.some(diff => 
                diff.position === i && 
                (diff.type === 'added' || diff.type === 'changed')
            );
            
            if (shouldHighlight) {
                highlightedText += `<span class="highlight-changed-char">${escapeHtml(char)}</span>`;
            } else {
                highlightedText += escapeHtml(char);
            }
        }
        
        // 替换元素中的目标文本
        const originalHTML = element.innerHTML;
        const escapedTargetText = escapeHtml(targetText);
        
        // 尝试直接替换文本内容
        if (originalHTML.includes(escapedTargetText)) {
            element.innerHTML = originalHTML.replace(escapedTargetText, highlightedText);
        } else {
            // 如果直接替换失败，尝试处理文本节点
            replaceTextInElement(element, targetText, highlightedText);
        }
        
        console.log('修改后文档字符级高亮应用完成:', { targetText, differences: differences.length });
        
    } catch (error) {
        console.error('应用修改后文档字符高亮时出错:', error);
    }
}

// 新增：辅助函数 - 在元素中替换文本
function replaceTextInElement(element, targetText, highlightedText) {
    const walker = document.createTreeWalker(
        element,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    const textNodes = [];
    let node;
    while (node = walker.nextNode()) {
        textNodes.push(node);
    }
    
    for (const textNode of textNodes) {
        if (textNode.textContent.includes(targetText)) {
            const parent = textNode.parentNode;
            const wrapper = document.createElement('span');
            wrapper.innerHTML = textNode.textContent.replace(
                targetText, 
                highlightedText
            );
            parent.replaceChild(wrapper, textNode);
            break;
        }
    }
}

// 在指定容器中高亮文本
function highlightTextInContainer(container, text, highlightClass) {
    if (!container || !text || text.trim() === '') {
        console.log('高亮参数无效:', { container: !!container, text, highlightClass });
        return;
    }
    
    console.log(`在容器中高亮文本:`, { text, highlightClass, containerClass: container.className });
    
    // 获取所有段落和表格单元格
    const elements = container.querySelectorAll('.word-paragraph, .document-paragraph, .word-table-cell, .document-table td, .document-table th');
    
    let foundMatches = 0;
    elements.forEach(element => {
        if (element.textContent.includes(text)) {
            foundMatches++;
            
            // 高亮整个元素
            element.classList.add(highlightClass);
            
            // 如果元素包含runs，尝试高亮具体的run
            const runs = element.querySelectorAll('.word-run, .document-run');
            runs.forEach(run => {
                if (run.textContent.includes(text)) {
                    run.classList.add(highlightClass + '-run');
                }
            });
            
            // 滚动到高亮元素
            element.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center',
                inline: 'nearest'
            });
        }
    });
    
    console.log(`高亮完成，找到 ${foundMatches} 个匹配项`);
}

// 清除高亮
function clearHighlights() {
    // 清除旧的高亮样式
    document.querySelectorAll('.document-paragraph.highlighted, .word-paragraph.highlighted').forEach(para => {
        para.classList.remove('highlighted');
    });
    
    // 清除新的高亮样式
    document.querySelectorAll('.highlight-original, .highlight-modified').forEach(element => {
        element.classList.remove('highlight-original', 'highlight-modified');
    });
    
    // 清除run级别的高亮
    document.querySelectorAll('.highlight-original-run, .highlight-modified-run').forEach(run => {
        run.classList.remove('highlight-original-run', 'highlight-modified-run');
    });
    
    // 清除字符级别的蓝色高亮
    document.querySelectorAll('.highlight-changed-char').forEach(char => {
        // 将高亮的字符替换为普通文本
        const parent = char.parentNode;
        if (parent) {
            parent.replaceChild(document.createTextNode(char.textContent), char);
            // 合并相邻的文本节点
            parent.normalize();
        }
    });
    
    // 清除连接线
    clearConnectionLines();
    
    selectedModificationIndex = -1;
}

// 删除修改条目
async function removeModification(index, event) {
    event.stopPropagation();
    
    const removedMod = modifications[index];
    
    // 从修改列表中移除该条目
    modifications.splice(index, 1);
    
    // 如果还有剩余的修改条目，重新应用它们
    if (modifications.length > 0) {
        // 重新应用剩余的修改条目
        try {
            showLoading();
            const response = await fetch('/api/add_modifications', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    doc_id: currentDocId,
                    modifications: modifications
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                modifiedContent = result.modified_content;
                // 更新已应用修改列表
                appliedModifications = modifications.map(mod => ({
                    original_text: mod.original_text,
                    new_text: mod.new_text,
                    reason: mod.reason
                }));
                
                displayModifiedDocument(result.modified_content);
                downloadBtn.disabled = false;
            } else {
                showMessage(result.message, 'error');
            }
        } catch (error) {
            showMessage('重新应用修改失败: ' + error.message, 'error');
        } finally {
            hideLoading();
        }
    } else {
        // 如果没有剩余修改，清空预览和已应用修改列表
        appliedModifications = [];
        modifiedContent = null;
        previewContentDiv.innerHTML = `
            <div class="placeholder">
                <i class="icon-preview"></i>
                <p>${getText('preview_prompt')}</p>
            </div>
        `;
        downloadBtn.disabled = true;
        applyModsBtn.disabled = true;
    }
    
    updateModificationsList();
    clearHighlights();
    clearConnectionLines();
    
    showMessage(getText('modification_deleted', '修改条目已删除'), 'info');
}

// 应用所有修改
async function applyModifications() {
    if (!currentDocId || modifications.length === 0) {
        showMessage(getText('no_modifications_to_apply', '没有可应用的修改'), 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/add_modifications', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                doc_id: currentDocId,
                modifications: modifications
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            modifiedContent = result.modified_content;
            // 更新已应用修改列表 - 创建当前修改的深拷贝
            appliedModifications = modifications.map(mod => ({
                original_text: mod.original_text,
                new_text: mod.new_text,
                reason: mod.reason
            }));
            
            displayModifiedDocument(result.modified_content);
            downloadBtn.disabled = false;
            showMessage(getText('modifications_applied', '修改应用成功'), 'success');
            
            // 更新修改条目列表显示
            updateModificationsList();
            
            // 如果有选中的修改条目，重新高亮
            if (selectedModificationIndex >= 0) {
                highlightText(modifications[selectedModificationIndex]);
            }
        } else {
            showMessage(result.message, 'error');
        }
    } catch (error) {
        showMessage('应用修改失败: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

// 清空所有修改
function clearModifications() {
    if (modifications.length === 0) return;
    
    if (confirm('确定要清空所有修改条目吗？')) {
        modifications = [];
        appliedModifications = []; // 清空已应用修改列表
        updateModificationsList();
        clearHighlights();
        clearConnectionLines();
        
        previewContentDiv.innerHTML = `
            <div class="placeholder">
                <i class="icon-preview"></i>
                <p>应用修改后可预览最终文档</p>
            </div>
        `;
        
        applyModsBtn.disabled = true;
        downloadBtn.disabled = true;
        modifiedContent = null;
        
        showMessage('修改条目已清空', 'info');
    }
}

// 下载修改后的文档
function downloadModifiedDocument() {
    if (!currentDocId) {
        showMessage('没有可下载的文档', 'error');
        return;
    }
    
    const downloadUrl = `/api/download_document/${currentDocId}`;
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = '';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    showMessage('文档下载已开始', 'success');
}

// 显示加载动画
function showLoading() {
    loadingOverlay.style.display = 'flex';
}

// 隐藏加载动画
function hideLoading() {
    loadingOverlay.style.display = 'none';
}

// 显示消息提示
function showMessage(message, type = 'info') {
    messageToast.textContent = message;
    messageToast.className = `message-toast ${type} show`;
    
    setTimeout(() => {
        messageToast.classList.remove('show');
    }, 3000);
}

// 键盘快捷键
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + U: 上传文档
    if ((event.ctrlKey || event.metaKey) && event.key === 'u') {
        event.preventDefault();
        if (!currentDocId) {
            documentInput.click();
        }
    }
    
    // Ctrl/Cmd + M: 添加修改条目
    if ((event.ctrlKey || event.metaKey) && event.key === 'm') {
        event.preventDefault();
        if (currentDocId && !addModBtn.disabled) {
            showModificationModal();
        }
    }
    
    // Ctrl/Cmd + Enter: 应用修改
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        if (!applyModsBtn.disabled) {
            applyModifications();
        }
    }
    
    // Escape: 关闭模态框或清除选中
    if (event.key === 'Escape') {
        if (modificationModal.style.display === 'block') {
            hideModificationModal();
        } else if (selectedModificationIndex >= 0) {
            clearHighlights();
            document.querySelectorAll('.modification-item').forEach(item => {
                item.classList.remove('selected');
            });
        }
    }
});

// 拖拽上传功能
document.addEventListener('dragover', function(event) {
    event.preventDefault();
});

document.addEventListener('drop', function(event) {
    event.preventDefault();
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.name.endsWith('.docx') || file.name.endsWith('.doc') || file.name.endsWith('.txt')) {
            documentInput.files = files;
            handleFileUpload({ target: { files: [file] } });
        } else {
            showMessage('请拖拽Word文档格式文件', 'error');
        }
    }
});

// 自动保存功能（可选）
let autoSaveTimer;
function scheduleAutoSave() {
    clearTimeout(autoSaveTimer);
    autoSaveTimer = setTimeout(() => {
        // 这里可以实现自动保存到本地存储
        if (modifications.length > 0) {
            localStorage.setItem('word_editor_modifications', JSON.stringify({
                docId: currentDocId,
                modifications: modifications,
                timestamp: Date.now()
            }));
        }
    }, 5000);
}

// 页面加载时恢复数据
function restoreFromLocalStorage() {
    const saved = localStorage.getItem('word_editor_modifications');
    if (saved) {
        try {
            const data = JSON.parse(saved);
            // 检查是否是最近的数据（24小时内）
            if (Date.now() - data.timestamp < 24 * 60 * 60 * 1000) {
                // 这里可以询问用户是否恢复数据
                console.log('Found saved modifications:', data);
            }
        } catch (error) {
            console.error('Failed to restore from localStorage:', error);
        }
    }
}

// 页面卸载时清理
window.addEventListener('beforeunload', function(event) {
    // 如果正在切换语言，不显示确认提示
    if (isChangingLanguage) {
        return;
    }
    
    if (modifications.length > 0) {
        event.preventDefault();
        event.returnValue = getText('unsaved_changes');
    }
});

// 清除连接线
function clearConnectionLines() {
    // 清除所有连接线元素
    const existingLines = document.querySelectorAll('.connection-line');
    existingLines.forEach(line => line.remove());
    
    // 清除SVG容器
    const svgContainer = document.getElementById('connectionSvg');
    if (svgContainer) {
        svgContainer.remove();
    }
}

// 绘制连接线
function drawConnectionLines(modification) {
    try {
        // 先清除现有连接线，确保完全清空
        clearConnectionLines();
        
        // 检查当前是否有选中的修改条目
        if (selectedModificationIndex < 0) {
            console.log('没有选中的修改条目');
            return;
        }
        
        // 查找当前选中的修改条目
        const selectedModItem = document.querySelector('.modification-item.selected');
        if (!selectedModItem) {
            console.log('找不到选中的修改条目元素');
            return;
        }
        
        // 查找修改条目中的"原文内容"和"修改为"字段
        const originalTextField = selectedModItem.querySelector('.field-content.original-text');
        const newTextField = selectedModItem.querySelector('.field-content.new-text');
        
        console.log('找到的字段元素:', {
            originalTextField: !!originalTextField,
            newTextField: !!newTextField
        });
        
        // 重新查找高亮元素，每次都重新获取最新位置
        const originalHighlights = document.querySelectorAll('#originalContent .highlight-original, #originalContent .highlight-original-run');
        const modifiedHighlights = document.querySelectorAll('#previewContent .highlight-modified, #previewContent .highlight-modified-run');
        
        console.log('找到的高亮元素:', {
            originalHighlights: originalHighlights.length,
            modifiedHighlights: modifiedHighlights.length
        });
        
        // 延迟绘制，确保DOM和布局完全稳定
        setTimeout(() => {
            // 只有存在高亮元素时才绘制连接线
            if (originalTextField && originalHighlights.length > 0) {
                console.log('开始绘制红色连接线到原文档');
                // 绘制从"原文内容"到原文档的红色虚线
                originalHighlights.forEach((highlight, i) => {
                    drawConnectionLine(originalTextField, highlight, i, 'original');
                });
            }
            
            if (newTextField && modifiedHighlights.length > 0) {
                console.log('开始绘制绿色连接线到修改后文档');
                // 绘制从"修改为"到修改后文档的绿色虚线
                modifiedHighlights.forEach((highlight, i) => {
                    drawConnectionLine(newTextField, highlight, i + 100, 'modified');
                });
            }
            
            if (!originalTextField || originalHighlights.length === 0) {
                console.log('无法绘制红色连接线:', {
                    hasOriginalField: !!originalTextField,
                    highlightCount: originalHighlights.length
                });
            }
            
            if (!newTextField || modifiedHighlights.length === 0) {
                console.log('无法绘制绿色连接线:', {
                    hasNewField: !!newTextField,
                    highlightCount: modifiedHighlights.length
                });
            }
        }, 100);
    } catch (error) {
        console.error('绘制连接线时出错:', error);
    }
}

// 绘制单条连接线
function drawConnectionLine(startElement, endElement, index, type = 'original') {
    try {
        console.log(`开始绘制${type === 'original' ? '红色' : '绿色'}连接线`);
        
        // 创建SVG容器（如果不存在）
        let svgContainer = document.getElementById('connectionSvg');
        if (!svgContainer) {
            svgContainer = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
            svgContainer.id = 'connectionSvg';
            svgContainer.style.position = 'fixed';
            svgContainer.style.top = '0';
            svgContainer.style.left = '0';
            svgContainer.style.width = '100%';
            svgContainer.style.height = '100%';
            svgContainer.style.pointerEvents = 'none';
            svgContainer.style.zIndex = '9999';
            document.body.appendChild(svgContainer);
            console.log('创建了新的SVG容器');
        }
        
        // 获取元素位置
        const startRect = startElement.getBoundingClientRect();
        const endRect = endElement.getBoundingClientRect();
        
        // 根据连接类型计算连接点
        let startX, startY, endX, endY;
        
        if (type === 'original') {
            // 从修改条目的"原文内容"连接到左侧原文档
            startX = startRect.left;  // 从左边开始
            startY = startRect.top + startRect.height / 2;
            endX = endRect.right;    // 连接到右边
            endY = endRect.top + endRect.height / 2;
        } else {
            // 从修改条目的"修改为"连接到右侧修改后文档
            startX = startRect.right; // 从右边开始
            startY = startRect.top + startRect.height / 2;
            endX = endRect.left;     // 连接到左边
            endY = endRect.top + endRect.height / 2;
        }
        
        // 创建贝塞尔曲线路径
        const controlX1 = startX + (endX - startX) * 0.3;
        const controlY1 = startY;
        const controlX2 = startX + (endX - startX) * 0.7;
        const controlY2 = endY;
        
        const pathData = `M ${startX} ${startY} C ${controlX1} ${controlY1}, ${controlX2} ${controlY2}, ${endX} ${endY}`;
        
        // 创建路径元素
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', pathData);
        // 根据类型设置不同的颜色：红色用于原文，绿色用于修改后
        const strokeColor = type === 'original' ? '#dc3545' : '#28a745';
        path.setAttribute('stroke', strokeColor);
        path.setAttribute('stroke-width', '2');
        path.setAttribute('stroke-dasharray', '5,5');
        path.setAttribute('fill', 'none');
        path.classList.add('connection-line');
        path.setAttribute('data-type', type);
        
        // 添加动画效果
        path.style.opacity = '0';
        svgContainer.appendChild(path);
        
        // 淡入动画
        setTimeout(() => {
            path.style.transition = 'opacity 0.5s ease-in-out';
            path.style.opacity = '0.8';
        }, index * 50); // 延迟显示，创建动画效果
        
        // 添加箭头
        const arrowHead = createArrowHead(endX, endY, startX, startY, type);
        svgContainer.appendChild(arrowHead);
        
        console.log(`${type === 'original' ? '红色' : '绿色'}连接线已添加到SVG`);
        
    } catch (error) {
        console.error('绘制单条连接线时出错:', error);
    }
}

// 创建箭头头部
function createArrowHead(x, y, fromX, fromY, type = 'original') {
    // 计算箭头方向
    const angle = Math.atan2(y - fromY, x - fromX);
    const arrowLength = 8;
    const arrowAngle = Math.PI / 6; // 30度
    
    // 箭头的三个点
    const x1 = x - arrowLength * Math.cos(angle - arrowAngle);
    const y1 = y - arrowLength * Math.sin(angle - arrowAngle);
    const x2 = x - arrowLength * Math.cos(angle + arrowAngle);
    const y2 = y - arrowLength * Math.sin(angle + arrowAngle);
    
    const arrow = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
    arrow.setAttribute('points', `${x},${y} ${x1},${y1} ${x2},${y2}`);
    // 根据类型设置不同的颜色：红色用于原文，绿色用于修改后
    const fillColor = type === 'original' ? '#dc3545' : '#28a745';
    arrow.setAttribute('fill', fillColor);
    arrow.classList.add('connection-line');
    arrow.setAttribute('data-type', type);
    arrow.style.opacity = '0';
    
    // 淡入动画
    setTimeout(() => {
        arrow.style.transition = 'opacity 0.5s ease-in-out';
        arrow.style.opacity = '0.8';
    }, 200);
    
    return arrow;
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 重新绘制连接线的函数
function redrawConnectionLines() {
    if (selectedModificationIndex >= 0) {
        drawConnectionLines(modifications[selectedModificationIndex]);
    }
}

// 使用防抖的重新绘制函数
const debouncedRedraw = debounce(redrawConnectionLines, 150);

// 窗口大小改变时重新绘制连接线
window.addEventListener('resize', debouncedRedraw);

// 滚动时重新绘制连接线
document.addEventListener('scroll', debouncedRedraw, true);

// 面板内容滚动时也要重新绘制
document.addEventListener('DOMContentLoaded', () => {
    const panelContents = document.querySelectorAll('.panel-content');
    panelContents.forEach(panel => {
        panel.addEventListener('scroll', debouncedRedraw, true);
    });
    
    // 也监听document-content的滚动
    const documentContents = document.querySelectorAll('.document-content');
    documentContents.forEach(content => {
        content.addEventListener('scroll', debouncedRedraw, true);
    });
});

// 批量导入相关函数
let csvData = null;

// 显示批量导入模态框
function showBatchImportModal() {
    console.log('showBatchImportModal called');
    const modal = document.getElementById('batchImportModal');
    if (!modal) {
        console.error('Batch import modal not found');
        return;
    }
    
    // 检查所有相关元素是否存在
    const selectCsvBtn = document.getElementById('selectCsvBtn');
    const csvFileInput = document.getElementById('csvFileInput');
    const csvFileName = document.getElementById('csvFileName');
    
    console.log('Modal elements check:');
    console.log('selectCsvBtn:', selectCsvBtn);
    console.log('csvFileInput:', csvFileInput);
    console.log('csvFileName:', csvFileName);
    
    modal.style.display = 'block';
    resetBatchImportModal();
}

// 隐藏批量导入模态框
function hideBatchImportModal() {
    const modal = document.getElementById('batchImportModal');
    modal.style.display = 'none';
    resetBatchImportModal();
}

// 重置批量导入模态框
function resetBatchImportModal() {
    csvData = null;
    // 确保文件名显示区域为空，不显示任何文本
    document.getElementById('csvFileName').textContent = '';
    document.getElementById('csvPreview').style.display = 'none';
    document.getElementById('importCsvBtn').disabled = true;
    document.getElementById('csvFileInput').value = '';
}

// 下载CSV模板
function downloadCsvTemplate() {
    let csvContent;
    
    if (currentLanguage === 'en') {
        csvContent = `OriginalText,ModifiedText,ModificationReason
"Sample original text 1","Sample modified text 1","Sample modification reason 1"
"Sample original text 2","Sample modified text 2","Sample modification reason 2"
"Sample original text 3","Sample modified text 3","Sample modification reason 3"`;
    } else {
        csvContent = `OriginalText,ModifiedText,ModificationReason
"示例原文内容1","示例修改后内容1","示例修改原因1"
"示例原文内容2","示例修改后内容2","示例修改原因2"
"示例原文内容3","示例修改后内容3","示例修改原因3"`;
    }

    // 添加UTF-8 BOM以确保中文正确显示
    const BOM = '\uFEFF';
    const blob = new Blob([BOM + csvContent], { 
        type: 'text/csv;charset=utf-8;' 
    });
    
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', 'modification_template.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // 清理URL对象
    setTimeout(() => URL.revokeObjectURL(url), 100);
    
    showMessage(getText('csv_template_downloaded'), 'success');
}

// 处理CSV文件上传
function handleCsvUpload(event) {
    const file = event.target.files[0];
    if (!file) {
        // 当没有文件时，始终显示英文
        document.getElementById('csvFileName').textContent = '';
        return;
    }
    
    if (!file.name.toLowerCase().endsWith('.csv')) {
        showMessage('Please select a CSV file', 'error');
        return;
    }
    
    document.getElementById('csvFileName').textContent = file.name;
    
    // 首先尝试UTF-8编码读取
    const reader = new FileReader();
    reader.onload = function(e) {
        let csvContent = e.target.result;
        console.log('File content with UTF-8:', csvContent.substring(0, 200));
        
        // 检查是否包含乱码
        if (csvContent.includes('�') || detectGarbledText(csvContent)) {
            console.log('Detected garbled text, trying GBK encoding...');
            // 如果检测到乱码，尝试GBK编码
            readFileWithGBK(file);
        } else {
            try {
                parseCsvFile(csvContent);
            } catch (error) {
                showMessage(getText('csv_import_failed') + ': ' + error.message, 'error');
            }
        }
    };
    
    reader.onerror = function() {
        showMessage(getText('csv_import_failed'), 'error');
    };
    
    reader.readAsText(file, 'utf-8');
}

// 检测乱码文本
function detectGarbledText(text) {
    // 检查是否有常见的乱码模式
    const garbledPatterns = [
        /[\u00c0-\u00ff]{2,}/,  // 连续的高位字符，可能是编码问题
        /\u00e4\u00b8\u00ad/,  // "中" 的UTF-8乱码
        /\u00e6\u0096\u0087/,  // "文" 的UTF-8乱码
        /\u00c4\u00ea/,        // 常见乱码模式
        /\u00a6\u00d2/,        // 常见乱码模式
    ];
    
    // 检查是否包含中文但显示为乱码
    const hasChineseChars = /[\u4e00-\u9fff]/.test(text);
    const hasGarbledChars = garbledPatterns.some(pattern => pattern.test(text));
    
    // 如果没有中文字符但有乱码模式，或者同时有中文和乱码，则认为可能有编码问题
    return hasGarbledChars && !hasChineseChars;
}

// 使用多种编码尝试读取文件
function readFileWithGBK(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const arrayBuffer = e.target.result;
        
        // 按优先级尝试不同编码
        const encodings = ['gbk', 'gb2312', 'big5', 'utf-8'];
        let success = false;
        
        for (const encoding of encodings) {
            try {
                console.log(`Trying encoding: ${encoding}`);
                const decoder = new TextDecoder(encoding, { fatal: true });
                const csvContent = decoder.decode(arrayBuffer);
                
                // 检查解码结果是否包含正常的中文字符
                if (/[\u4e00-\u9fff]/.test(csvContent) && !detectGarbledText(csvContent)) {
                    console.log(`Successfully decoded with ${encoding}`);
                    console.log('File content:', csvContent.substring(0, 200));
                    parseCsvFile(csvContent);
                    success = true;
                    break;
                }
            } catch (error) {
                console.log(`${encoding} decoding failed:`, error.message);
                continue;
            }
        }
        
        if (!success) {
            console.log('All encodings failed, using UTF-8 with error tolerance...');
            // 最后尝试使用UTF-8但不抛出错误
            const decoder = new TextDecoder('utf-8', { fatal: false });
            const csvContent = decoder.decode(arrayBuffer);
            
            if (csvContent.includes('�')) {
                showMessage(getText('csv_encoding_warning') || '文件编码可能不正确，请确保CSV文件使用UTF-8编码保存', 'warning');
            }
            
            parseCsvFile(csvContent);
        }
    };
    
    reader.onerror = function() {
        showMessage(getText('csv_import_failed'), 'error');
    };
    
    reader.readAsArrayBuffer(file);
}

// 解析CSV文件
function parseCsvFile(csvText) {
    console.log('Raw CSV text:', csvText);
    
    try {
        // 改进的CSV解析 - 正确处理引号和逗号
        const lines = csvText.split('\n').filter(line => line.trim());
        if (lines.length < 2) {
            showMessage(getText('csv_invalid_format'), 'error');
            return;
        }
        
        // 解析CSV行的函数
        function parseCSVLine(line) {
            const result = [];
            let current = '';
            let inQuotes = false;
            let i = 0;
            
            while (i < line.length) {
                const char = line[i];
                
                if (char === '"') {
                    if (inQuotes && line[i + 1] === '"') {
                        // 转义的引号
                        current += '"';
                        i += 2;
                    } else {
                        // 开始或结束引号
                        inQuotes = !inQuotes;
                        i++;
                    }
                } else if (char === ',' && !inQuotes) {
                    // 字段分隔符
                    result.push(current.trim());
                    current = '';
                    i++;
                } else {
                    current += char;
                    i++;
                }
            }
            
            // 添加最后一个字段
            result.push(current.trim());
            return result;
        }
        
        // 解析标题行
        const headers = parseCSVLine(lines[0]);
        console.log('Headers:', headers);
        
        // 验证必需的字段
        const requiredFields = ['OriginalText', 'ModifiedText', 'ModificationReason'];
        const missingFields = requiredFields.filter(field => !headers.includes(field));
        
        if (missingFields.length > 0) {
            showMessage(getText('csv_missing_fields') + ': ' + missingFields.join(', '), 'error');
            return;
        }
        
        // 解析数据行
        const data = [];
        for (let i = 1; i < lines.length; i++) {
            if (!lines[i].trim()) continue; // 跳过空行
            
            const values = parseCSVLine(lines[i]);
            console.log(`Line ${i} values:`, values);
            
            if (values.length !== headers.length) {
                console.warn(`Line ${i + 1}: Expected ${headers.length} fields, got ${values.length}`);
                // 继续处理，但补齐缺失的字段
                while (values.length < headers.length) {
                    values.push('');
                }
            }
            
            const row = {};
            headers.forEach((header, index) => {
                row[header] = values[index] || '';
            });
            
            // 验证必需字段不为空
            if (!row.OriginalText || !row.ModifiedText || !row.ModificationReason) {
                console.warn(`Line ${i + 1}: Missing required fields`, row);
                continue; // 跳过不完整的行
            }
            
            data.push(row);
        }
        
        if (data.length === 0) {
            showMessage(getText('csv_empty_data'), 'error');
            return;
        }
        
        console.log('Parsed data:', data);
        csvData = data;
        displayCsvPreview(data);
        
    } catch (error) {
        console.error('CSV parsing error:', error);
        showMessage(getText('csv_invalid_format') + ': ' + error.message, 'error');
    }
}

// 显示CSV预览
function displayCsvPreview(data) {
    const previewDiv = document.getElementById('csvPreview');
    const contentDiv = document.getElementById('csvPreviewContent');
    const resultDiv = document.getElementById('csvValidationResult');
    
    // 构建预览表格 - 使用容器包装以支持滚动
    let tableHtml = `
        <div class="csv-preview-table-container">
            <table class="csv-preview-table">
                <thead>
                    <tr>
                        <th>${getText('original_text')}</th>
                        <th>${getText('new_text')}</th>
                        <th>${getText('modification_reason')}</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    // 显示所有数据，但通过CSS控制高度和滚动
    data.forEach((row, index) => {
        tableHtml += `
            <tr>
                <td>${escapeHtml(row.OriginalText)}</td>
                <td>${escapeHtml(row.ModifiedText)}</td>
                <td>${escapeHtml(row.ModificationReason)}</td>
            </tr>
        `;
    });
    
    tableHtml += `
                </tbody>
            </table>
        </div>
    `;
    
    // 添加总记录数信息
    if (data.length > 3) {
        tableHtml += `<p style="color: #666; font-size: 0.9rem; margin-top: 10px;">${getText('total_records').replace('{count}', data.length)} (${getText('scroll_to_view_more', '滚动查看更多')})</p>`;
    } else {
        tableHtml += `<p style="color: #666; font-size: 0.9rem; margin-top: 10px;">${getText('total_records').replace('{count}', data.length)}</p>`;
    }
    
    contentDiv.innerHTML = tableHtml;
    
    // 显示验证结果
    resultDiv.className = 'valid';
    resultDiv.textContent = `✓ ${getText('csv_validation_success')}, ${getText('total_records').replace('{count}', data.length)}`;
    
    previewDiv.style.display = 'block';
    document.getElementById('importCsvBtn').disabled = false;
}

// 导入CSV数据
function importCsvData() {
    if (!csvData || csvData.length === 0) {
        showMessage(getText('csv_empty_data'), 'error');
        return;
    }
    
    // 转换为修改条目格式
    const newModifications = csvData.map(row => ({
        original_text: row.OriginalText,
        new_text: row.ModifiedText,
        reason: row.ModificationReason
    }));
    
    // 添加到现有修改条目
    modifications.push(...newModifications);
    
    // 更新界面
    updateModificationsList();
    applyModsBtn.disabled = false;
    
    // 关闭模态框
    hideBatchImportModal();
    
    showMessage(getText('csv_import_success').replace('{count}', newModifications.length), 'success');
}

// 更新修改条目字段
function updateModificationField(index, field, value) {
    if (modifications[index]) {
        const oldValue = modifications[index][field];
        if (oldValue !== value) {
            modifications[index][field] = value;
            
            // 更新title属性以反映新值
            const textarea = document.querySelector(`textarea[data-index="${index}"][data-field="${field}"]`);
            if (textarea) {
                textarea.setAttribute('title', value);
            }
            
            showMessage(getText('modification_updated', `修改条目 #${index + 1} 已更新`), 'info');
            
            // 如果当前修改已经应用，需要重新应用所有修改
            const isApplied = appliedModifications.some(appliedMod => 
                appliedMod.original_text === oldValue && field === 'original_text' ||
                appliedMod.new_text === oldValue && field === 'new_text' ||
                appliedMod.reason === oldValue && field === 'reason'
            );
            
            if (isApplied && modifications.length > 0) {
                // 延迟重新应用修改，避免频繁操作
                setTimeout(() => {
                    reapplyModifications();
                }, 1000);
            }
        }
    }
}

// 重新应用修改
async function reapplyModifications() {
    if (!currentDocId || modifications.length === 0) {
        return;
    }
    
    try {
        showLoading();
        const response = await fetch('/api/add_modifications', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                doc_id: currentDocId,
                modifications: modifications
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            modifiedContent = result.modified_content;
            appliedModifications = modifications.map(mod => ({
                original_text: mod.original_text,
                new_text: mod.new_text,
                reason: mod.reason
            }));
            
            displayModifiedDocument(result.modified_content);
            downloadBtn.disabled = false;
            
            // 更新修改条目列表显示
            updateModificationsList();
        }
    } catch (error) {
        console.error('重新应用修改失败:', error);
    } finally {
        hideLoading();
    }
}

// 检查自动加载参数
async function checkAutoLoadParams() {
    // 从URL参数获取自动加载信息
    const urlParams = new URLSearchParams(window.location.search);
    console.log('URL search params:', window.location.search);
    // 对URL参数进行解码，处理中文字符
    const documentSource = urlParams.get('document') ? decodeURIComponent(urlParams.get('document')) : null;
    const modificationsSource = urlParams.get('modifications') ? decodeURIComponent(urlParams.get('modifications')) : null;
    const autoApply = urlParams.get('auto_apply') === 'true';
    const docId = urlParams.get('doc_id'); // 新增：支持直接加载已处理的文档
    
    console.log('Parsed URL params:', {
        documentSource,
        modificationsSource,
        autoApply,
        docId
    });
    
    // 如果有doc_id参数，直接加载已处理的文档
    if (docId) {
        console.log('Found doc_id, calling loadExistingDocument');
        await loadExistingDocument(docId);
        return;
    }
    
    if (documentSource) {
        showMessage('正在自动加载文档和修改条目...', 'info');
        showLoading();
        
        try {
            const response = await fetch('/api/auto_load', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    document: documentSource,
                    modifications: modificationsSource,
                    auto_apply: autoApply
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // 设置当前文档ID
                currentDocId = result.doc_id;
                
                // 显示原始文档
                originalContent = result.content;
                displayOriginalDocument(result.content);
                
                // 更新文件名显示
                fileName.textContent = result.filename;
                
                // 更新文档信息
                if (result.doc_info) {
                    document.getElementById('fileSizeInfo').textContent = result.doc_info.file_size || '-';
                    document.getElementById('paragraphCountInfo').textContent = result.doc_info.paragraph_count || '-';
                    document.getElementById('originalDocInfo').style.display = 'block';
                }
                
                // 加载修改条目
                if (result.modifications && result.modifications.length > 0) {
                    modifications = result.modifications;
                    updateModificationsList();
                    enableModificationControls();
                    
                    if (result.auto_applied) {
                        // 如果已自动应用，显示修改后的文档
                        modifiedContent = result.modified_content;
                        appliedModifications = [...modifications];
                        displayModifiedDocument(result.modified_content);
                        downloadBtn.disabled = false;
                        applyModsBtn.disabled = true; // 已应用，禁用应用按钮
                        
                        // 重新更新修改条目列表以显示正确的状态（绿色）
                        updateModificationsList();
                        
                        showMessage(`文档和 ${modifications.length} 个修改条目已自动加载并应用！`, 'success');
                    } else {
                        // 未自动应用，启用应用按钮
                        applyModsBtn.disabled = false;
                        showMessage(`文档和 ${modifications.length} 个修改条目已自动加载，请确认是否应用修改。`, 'success');
                    }
                } else {
                    showMessage('文档已自动加载！', 'success');
                }
                
                // 清除URL参数（可选）
                if (window.history && window.history.replaceState) {
                    window.history.replaceState({}, document.title, window.location.pathname);
                }
                
            } else {
                showMessage('自动加载失败: ' + result.message, 'error');
            }
            
        } catch (error) {
            showMessage('自动加载失败: ' + error.message, 'error');
        } finally {
            hideLoading();
        }
    }
}

// 加载已存在的文档
async function loadExistingDocument(docId) {
    console.log('loadExistingDocument called with docId:', docId);
    showMessage('正在加载文档...', 'info');
    showLoading();
    
    try {
        // 获取文档信息
        console.log('Fetching document info from:', `/api/document_info/${docId}`);
        const infoResponse = await fetch(`/api/document_info/${docId}`);
        console.log('Response status:', infoResponse.status);
        const infoResult = await infoResponse.json();
        console.log('Document info result:', infoResult);
        
        if (!infoResult.success) {
            console.error('Document info failed:', infoResult.message);
            showMessage('文档不存在或已过期: ' + infoResult.message, 'error');
            return;
        }
        
        // 设置当前文档ID
        currentDocId = docId;
        
        // 显示原始文档
        originalContent = infoResult.content;
        displayOriginalDocument(infoResult.content);
        
        // 更新文件名显示
        fileName.textContent = infoResult.filename;
        
        // 更新文档信息
        if (infoResult.doc_info) {
            document.getElementById('fileSizeInfo').textContent = infoResult.doc_info.file_size || '-';
            document.getElementById('paragraphCountInfo').textContent = infoResult.doc_info.paragraph_count || '-';
            document.getElementById('originalDocInfo').style.display = 'block';
        }
        
        // 加载修改条目（使用已获取的信息）
        if (infoResult.modifications && infoResult.modifications.length > 0) {
            // 加载修改条目
            modifications = infoResult.modifications;
            updateModificationsList();
            enableModificationControls();
            
            // 如果有修改后的内容，显示预览
            if (infoResult.modified_content) {
                modifiedContent = infoResult.modified_content;
                appliedModifications = [...modifications]; // 标记为已应用
                displayModifiedDocument(infoResult.modified_content);
                downloadBtn.disabled = false;
                applyModsBtn.disabled = true; // 已应用，禁用应用按钮
                
                // 重新更新修改条目列表以显示正确的状态（绿色）
                updateModificationsList();
                
                showMessage(`文档和 ${modifications.length} 个修改条目已加载并应用！`, 'success');
            } else {
                // 没有修改后的内容，启用应用按钮
                appliedModifications = []; // 标记为未应用
                applyModsBtn.disabled = false;
                showMessage(`文档和 ${modifications.length} 个修改条目已加载，请确认是否应用修改。`, 'success');
            }
        } else {
            showMessage('文档已加载！', 'success');
        }
        
        // 清除URL参数
        if (window.history && window.history.replaceState) {
            window.history.replaceState({}, document.title, window.location.pathname);
        }
        
    } catch (error) {
        showMessage('加载文档失败: ' + error.message, 'error');
    } finally {
        hideLoading();
          }
} 