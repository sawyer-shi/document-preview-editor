#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick API Test Script
快速API测试脚本

A simple script to quickly test if the Document Preview Editor API is working.
用于快速测试文档预览编辑器API是否正常工作的简单脚本。

Usage / 使用方法:
    python quick_test.py

Author: sawyer-shi
License: Apache 2.0
"""

import requests
import sys

def quick_test(base_url="http://127.0.0.1:5000"):
    """快速测试API / Quick test API"""
    print("🔍 Quick API Test / 快速API测试")
    print("=" * 40)
    
    try:
        # 测试服务器连接 / Test server connection
        print("Testing server connection... / 测试服务器连接...")
        response = requests.get(f"{base_url}/api/get_language", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server is running / 服务器正在运行")
            print(f"   Language: {data.get('language', 'unknown')}")
            print(f"   Response time: {response.elapsed.total_seconds():.3f}s")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server / 无法连接到服务器")
        print("   Please make sure the server is running on http://127.0.0.1:5000")
        print("   请确保服务器在 http://127.0.0.1:5000 上运行")
        return False
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1) 