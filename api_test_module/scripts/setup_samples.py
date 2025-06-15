#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sample Files Setup Script
示例文件设置脚本

This script helps set up sample files for API testing.
该脚本帮助设置用于API测试的示例文件。

Usage / 使用方法:
    python setup_samples.py

Author: sawyer-shi
License: Apache 2.0
"""

import os
import shutil
from pathlib import Path

def setup_sample_files():
    """设置示例文件 / Setup sample files"""
    print("🔧 Setting up sample files... / 设置示例文件...")
    print("=" * 50)
    
    # 获取路径 / Get paths
    script_dir = Path(__file__).parent
    samples_dir = script_dir.parent / "samples"
    project_root = script_dir.parent.parent
    
    # 确保samples目录存在 / Ensure samples directory exists
    samples_dir.mkdir(exist_ok=True)
    
    success_count = 0
    total_files = 0
    
    # 复制测试文件 / Copy test files
    test_files = [
        ("test_modifications.csv", "sample_modifications.csv"),
        ("test_document.docx", "sample_document.docx")
    ]
    
    for source_name, target_name in test_files:
        total_files += 1
        source_path = project_root / source_name
        target_path = samples_dir / target_name
        
        if source_path.exists():
            try:
                shutil.copy2(source_path, target_path)
                print(f"✅ Copied {source_name} → {target_name}")
                print(f"   复制 {source_name} → {target_name}")
                success_count += 1
            except Exception as e:
                print(f"❌ Failed to copy {source_name}: {e}")
                print(f"   复制失败 {source_name}: {e}")
        else:
            print(f"⚠️  Source file not found: {source_name}")
            print(f"   源文件未找到: {source_name}")
    
    # 创建示例CSV文件（如果不存在）/ Create sample CSV file (if not exists)
    sample_csv_path = samples_dir / "sample_modifications.csv"
    if not sample_csv_path.exists():
        try:
            with open(sample_csv_path, 'w', encoding='utf-8') as f:
                f.write("OriginalText,ModifiedText,ModificationReason\n")
                f.write("人工智能技术,AI技术,使用更简洁的表达\n")
                f.write("机器学习算法,深度学习算法,更准确的技术描述\n")
                f.write("数据处理,智能数据处理,强调智能化特性\n")
                f.write("传统方法,创新方法,体现技术进步\n")
                f.write("基础架构,技术基础架构,更具体的描述\n")
            
            print("✅ Created sample_modifications.csv")
            print("   创建了 sample_modifications.csv")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to create sample CSV: {e}")
            print(f"   创建示例CSV失败: {e}")
    
    # 创建示例Word文档说明 / Create sample Word document instructions
    doc_readme_path = samples_dir / "README.md"
    try:
        with open(doc_readme_path, 'w', encoding='utf-8') as f:
            f.write("""# Sample Files / 示例文件

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
""")
        
        print("✅ Created README.md")
        print("   创建了 README.md")
        
    except Exception as e:
        print(f"❌ Failed to create README: {e}")
        print(f"   创建README失败: {e}")
    
    # 总结 / Summary
    print("\n" + "=" * 50)
    print("📊 Setup Summary / 设置总结")
    print("=" * 50)
    print(f"Files processed / 处理的文件: {total_files}")
    print(f"Successfully set up / 成功设置: {success_count}")
    print(f"Sample files location / 示例文件位置: {samples_dir}")
    
    if success_count > 0:
        print("\n🎉 Sample files are ready for testing!")
        print("   示例文件已准备好进行测试！")
        print("\nNext steps / 下一步:")
        print("1. Run quick test: python quick_test.py")
        print("2. Run full test suite: python api_test_suite.py")
        print("3. Open web interface: http://localhost:5000/test")
    else:
        print("\n⚠️  No files were set up. Please check the source files.")
        print("   没有设置文件。请检查源文件。")

def main():
    """主函数 / Main function"""
    try:
        setup_sample_files()
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelled by user / 用户取消设置")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print(f"   设置失败: {e}")

if __name__ == "__main__":
    main() 