# Sample Files / 示例文件

## Overview / 概述

This directory contains sample files for API testing.
此目录包含用于API测试的示例文件。

## Files / 文件

### sample_modifications.csv
Sample modifications file with Chinese text examples.
包含中文文本示例的修改条目文件。

**Format / 格式:**
```csv
OriginalText,ModifiedText,ModificationReason
人工智能技术,AI技术,使用更简洁的表达
机器学习算法,深度学习算法,更准确的技术描述
```

### sample_document.docx
Sample Word document for testing document processing.
用于测试文档处理的示例Word文档。

**Note / 注意:**
If this file doesn't exist, you can create any Word document for testing purposes.
如果此文件不存在，您可以创建任何Word文档用于测试。

## Usage / 使用方法

These files are used by the API test scripts to verify document processing functionality.
这些文件被API测试脚本用来验证文档处理功能。

### In Web Interface / 在Web界面中
1. Navigate to http://localhost:5000/test
2. Use "sample_document.docx" and "sample_modifications.csv" as file paths
3. Run the auto load test

### In Command Line / 在命令行中
```bash
cd api_test_module/scripts
python api_test_suite.py
```

## Creating Your Own Test Files / 创建您自己的测试文件

### Word Document / Word文档
Create a Word document with some text content that matches the original text in your CSV file.
创建一个Word文档，其中包含与CSV文件中原始文本匹配的一些文本内容。

### CSV File / CSV文件
Follow the format:
遵循格式：
```csv
OriginalText,ModifiedText,ModificationReason
原始文本,修改后文本,修改原因
```

Make sure the OriginalText exists in your Word document for successful testing.
确保原始文本存在于您的Word文档中以便成功测试。
