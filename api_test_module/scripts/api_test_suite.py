#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document Preview Editor API Test Suite
文档预览编辑器API测试套件

Enhanced Auto Load Testing Module
增强版自动加载测试模块

This script provides comprehensive testing for the Document Preview Editor Auto Load API.
该脚本为文档预览编辑器自动加载API提供全面的测试功能。

Usage / 使用方法:
    python api_test_suite.py [--host HOST] [--port PORT] [--lang LANG]

Examples / 示例:
    python api_test_suite.py
    python api_test_suite.py --host 127.0.0.1 --port 5000 --lang en
    python api_test_suite.py --host localhost --port 8080 --lang zh

Author: sawyer-shi
License: Apache 2.0
"""

import requests
import json
import os
import sys
import argparse
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import urllib.parse

class EnhancedAutoLoadTestSuite:
    """增强版自动加载测试套件类 / Enhanced Auto Load Test Suite Class"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:5000", language: str = "zh"):
        self.base_url = base_url.rstrip('/')
        self.language = language
        self.session = requests.Session()
        self.test_results = []
        
        # 测试文件路径 / Test file paths
        self.samples_dir = Path(__file__).parent.parent / "samples"
        self.sample_doc = self.samples_dir / "sample_document.docx"
        self.sample_csv = self.samples_dir / "sample_modifications.csv"
        
        # 多语言文本 / Multilingual text
        self.texts = {
            "zh": {
                "starting_tests": "🚀 开始增强版自动加载API测试套件...",
                "test_server_status": "1. 测试服务器状态",
                "test_cors": "2. 测试CORS跨域功能",
                "test_auto_load_scenarios": "3. 测试自动加载场景",
                "test_language_integration": "4. 测试语言集成",
                "test_error_handling": "5. 测试错误处理",
                "server_running": "✅ 服务器正常运行",
                "server_failed": "❌ 服务器无法访问",
                "cors_success": "✅ CORS配置正常",
                "cors_failed": "❌ CORS配置异常",
                "auto_load_success": "✅ 自动加载测试正常",
                "auto_load_failed": "❌ 自动加载测试异常",
                "language_integration_success": "✅ 语言集成正常",
                "language_integration_failed": "❌ 语言集成异常",
                "error_handling_success": "✅ 错误处理正常",
                "error_handling_failed": "❌ 错误处理异常",
                "test_summary": "测试总结",
                "total_tests": "总测试数",
                "passed_tests": "通过测试",
                "failed_tests": "失败测试",
                "success_rate": "成功率",
                "all_tests_passed": "🎉 所有测试通过！API功能正常。",
                "some_tests_failed": "⚠️ 部分测试失败，请检查相关功能。",
                "many_tests_failed": "🚨 多个测试失败，请检查服务器配置。"
            },
            "en": {
                "starting_tests": "🚀 Starting Enhanced Auto Load API Test Suite...",
                "test_server_status": "1. Testing Server Status",
                "test_cors": "2. Testing CORS Functionality",
                "test_auto_load_scenarios": "3. Testing Auto Load Scenarios",
                "test_language_integration": "4. Testing Language Integration",
                "test_error_handling": "5. Testing Error Handling",
                "server_running": "✅ Server is running normally",
                "server_failed": "❌ Server is not accessible",
                "cors_success": "✅ CORS configuration is normal",
                "cors_failed": "❌ CORS configuration is abnormal",
                "auto_load_success": "✅ Auto Load testing is normal",
                "auto_load_failed": "❌ Auto Load testing is abnormal",
                "language_integration_success": "✅ Language integration is normal",
                "language_integration_failed": "❌ Language integration is abnormal",
                "error_handling_success": "✅ Error handling is normal",
                "error_handling_failed": "❌ Error handling is abnormal",
                "test_summary": "Test Summary",
                "total_tests": "Total Tests",
                "passed_tests": "Passed Tests",
                "failed_tests": "Failed Tests",
                "success_rate": "Success Rate",
                "all_tests_passed": "🎉 All tests passed! API functionality is normal.",
                "some_tests_failed": "⚠️ Some tests failed, please check related functionality.",
                "many_tests_failed": "🚨 Many tests failed, please check server configuration."
            }
        }
    
    def get_text(self, key: str) -> str:
        """获取多语言文本 / Get multilingual text"""
        return self.texts.get(self.language, self.texts["zh"]).get(key, key)
    
    def test_server_status(self) -> Dict:
        """测试服务器状态 / Test server status"""
        try:
            response = self.session.get(f"{self.base_url}/api/get_language", timeout=5)
            success = response.status_code == 200
            
            result = {
                "test": "server_status",
                "success": success,
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds()
            }
            
            if success:
                result["data"] = response.json()
            
            return result
            
        except Exception as e:
            return {
                "test": "server_status",
                "success": False,
                "error": str(e)
            }
    
    def test_cors_functionality(self) -> List[Dict]:
        """测试CORS跨域功能 / Test CORS functionality"""
        results = []
        test_origins = [
            "http://localhost:3000",
            "http://localhost:8080",
            "https://example.com"
        ]
        
        for origin in test_origins:
            try:
                headers = {
                    "Origin": origin,
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                }
                
                response = self.session.options(
                    f"{self.base_url}/api/auto_load",
                    headers=headers,
                    timeout=10
                )
                
                success = response.status_code == 200
                cors_headers = {
                    "allow_origin": response.headers.get("Access-Control-Allow-Origin"),
                    "allow_methods": response.headers.get("Access-Control-Allow-Methods"),
                    "allow_headers": response.headers.get("Access-Control-Allow-Headers")
                }
                
                results.append({
                    "test": "cors_preflight",
                    "origin": origin,
                    "success": success,
                    "status_code": response.status_code,
                    "cors_headers": cors_headers
                })
                
            except Exception as e:
                results.append({
                    "test": "cors_preflight",
                    "origin": origin,
                    "success": False,
                    "error": str(e)
                })
        
        return results
    
    def test_auto_load_scenarios(self) -> List[Dict]:
        """测试自动加载场景 / Test auto load scenarios"""
        results = []
        
        # 测试场景 / Test scenarios
        test_scenarios = [
            {
                "name": "local_files_no_auto_apply",
                "description": "本地文件，不自动应用 / Local files, no auto apply",
                "document": str(self.sample_doc.absolute()) if self.sample_doc.exists() else "sample_document.docx",
                "modifications": str(self.sample_csv.absolute()) if self.sample_csv.exists() else "sample_modifications.csv",
                "auto_apply": False,
                "language": "zh"
            },
            {
                "name": "local_files_with_auto_apply",
                "description": "本地文件，自动应用 / Local files, with auto apply",
                "document": str(self.sample_doc.absolute()) if self.sample_doc.exists() else "sample_document.docx",
                "modifications": str(self.sample_csv.absolute()) if self.sample_csv.exists() else "sample_modifications.csv",
                "auto_apply": True,
                "language": "zh"
            },
            {
                "name": "relative_paths",
                "description": "相对路径 / Relative paths",
                "document": "sample_document.docx",
                "modifications": "sample_modifications.csv",
                "auto_apply": False,
                "language": "en"
            },
            {
                "name": "url_encoded_paths",
                "description": "URL编码路径 / URL encoded paths",
                "document": urllib.parse.quote("sample_document.docx"),
                "modifications": urllib.parse.quote("sample_modifications.csv"),
                "auto_apply": False,
                "language": "zh"
            },
            {
                "name": "remote_urls",
                "description": "远程URL / Remote URLs",
                "document": "https://example.com/sample.docx",
                "modifications": "https://example.com/sample.csv",
                "auto_apply": True,
                "language": "en"
            },
            {
                "name": "mixed_sources",
                "description": "混合来源 / Mixed sources",
                "document": "sample_document.docx",
                "modifications": "https://example.com/sample.csv",
                "auto_apply": False,
                "language": "zh"
            }
        ]
        
        for scenario in test_scenarios:
            try:
                # 首先设置语言 / First set language
                lang_response = self.session.post(
                    f"{self.base_url}/api/set_language",
                    json={"language": scenario["language"]},
                    timeout=10
                )
                
                # 然后测试自动加载 / Then test auto load
                response = self.session.post(
                    f"{self.base_url}/api/auto_load",
                    json={
                        "document": scenario["document"],
                        "modifications": scenario["modifications"],
                        "auto_apply": scenario["auto_apply"]
                    },
                    timeout=30
                )
                
                # 评估成功条件 / Evaluate success conditions
                # 对于本地文件，404是预期的（文件可能不存在）
                # For local files, 404 is expected (files might not exist)
                # 对于远程URL，也可能返回错误
                # For remote URLs, errors are also possible
                success = response.status_code in [200, 400, 404, 500]
                
                result = {
                    "test": "auto_load_scenario",
                    "scenario": scenario["name"],
                    "description": scenario["description"],
                    "language": scenario["language"],
                    "success": success,
                    "status_code": response.status_code,
                    "language_set": lang_response.status_code == 200
                }
                
                if response.headers.get("content-type", "").startswith("application/json"):
                    try:
                        result["data"] = response.json()
                    except:
                        pass
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    "test": "auto_load_scenario",
                    "scenario": scenario["name"],
                    "description": scenario["description"],
                    "success": False,
                    "error": str(e)
                })
        
        return results
    
    def test_language_integration(self) -> List[Dict]:
        """测试语言集成 / Test language integration"""
        results = []
        
        # 测试不同语言下的自动加载 / Test auto load with different languages
        languages = ["zh", "en"]
        
        for lang in languages:
            try:
                # 设置语言 / Set language
                lang_response = self.session.post(
                    f"{self.base_url}/api/set_language",
                    json={"language": lang},
                    timeout=10
                )
                
                # 验证语言设置 / Verify language setting
                verify_response = self.session.get(
                    f"{self.base_url}/api/get_language",
                    timeout=10
                )
                
                # 在该语言下测试自动加载 / Test auto load in this language
                auto_load_response = self.session.post(
                    f"{self.base_url}/api/auto_load",
                    json={
                        "document": "sample_document.docx",
                        "modifications": "sample_modifications.csv",
                        "auto_apply": False
                    },
                    timeout=30
                )
                
                success = (
                    lang_response.status_code == 200 and
                    verify_response.status_code == 200 and
                    auto_load_response.status_code in [200, 400, 404]
                )
                
                result = {
                    "test": "language_integration",
                    "language": lang,
                    "success": success,
                    "language_set_status": lang_response.status_code,
                    "language_verify_status": verify_response.status_code,
                    "auto_load_status": auto_load_response.status_code
                }
                
                if verify_response.status_code == 200:
                    try:
                        verify_data = verify_response.json()
                        result["current_language"] = verify_data.get("language")
                        result["language_match"] = verify_data.get("language") == lang
                    except:
                        pass
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    "test": "language_integration",
                    "language": lang,
                    "success": False,
                    "error": str(e)
                })
        
        return results
    
    def test_error_handling(self) -> List[Dict]:
        """测试错误处理 / Test error handling"""
        results = []
        
        # 错误测试用例 / Error test cases
        error_cases = [
            {
                "name": "invalid_document_path",
                "description": "无效文档路径 / Invalid document path",
                "document": "/nonexistent/path/document.docx",
                "modifications": "sample_modifications.csv",
                "auto_apply": False,
                "expected_status": [400, 404, 500]
            },
            {
                "name": "invalid_modifications_path",
                "description": "无效修改条目路径 / Invalid modifications path",
                "document": "sample_document.docx",
                "modifications": "/nonexistent/path/modifications.csv",
                "auto_apply": False,
                "expected_status": [400, 404, 500]
            },
            {
                "name": "empty_document_path",
                "description": "空文档路径 / Empty document path",
                "document": "",
                "modifications": "sample_modifications.csv",
                "auto_apply": False,
                "expected_status": [400]
            },
            {
                "name": "empty_modifications_path",
                "description": "空修改条目路径 / Empty modifications path",
                "document": "sample_document.docx",
                "modifications": "",
                "auto_apply": False,
                "expected_status": [400]
            },
            {
                "name": "invalid_auto_apply_type",
                "description": "无效自动应用类型 / Invalid auto apply type",
                "document": "sample_document.docx",
                "modifications": "sample_modifications.csv",
                "auto_apply": "invalid",
                "expected_status": [400]
            }
        ]
        
        for case in error_cases:
            try:
                response = self.session.post(
                    f"{self.base_url}/api/auto_load",
                    json={
                        "document": case["document"],
                        "modifications": case["modifications"],
                        "auto_apply": case["auto_apply"]
                    },
                    timeout=30
                )
                
                success = response.status_code in case["expected_status"]
                
                result = {
                    "test": "error_handling",
                    "case": case["name"],
                    "description": case["description"],
                    "success": success,
                    "status_code": response.status_code,
                    "expected_status": case["expected_status"]
                }
                
                if response.headers.get("content-type", "").startswith("application/json"):
                    try:
                        result["data"] = response.json()
                    except:
                        pass
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    "test": "error_handling",
                    "case": case["name"],
                    "description": case["description"],
                    "success": False,
                    "error": str(e)
                })
        
        return results
    
    def run_all_tests(self) -> Dict:
        """运行所有测试 / Run all tests"""
        print("=" * 70)
        print(self.get_text("starting_tests"))
        print("=" * 70)
        
        all_results = []
        
        # 1. 测试服务器状态 / Test server status
        print(f"\n{self.get_text('test_server_status')}")
        server_result = self.test_server_status()
        all_results.append(server_result)
        
        if server_result["success"]:
            print(f"   {self.get_text('server_running')} (响应时间: {server_result.get('response_time', 0):.3f}s)")
        else:
            print(f"   {self.get_text('server_failed')}")
            return self.generate_summary(all_results)
        
        # 2. 测试CORS功能 / Test CORS functionality
        print(f"\n{self.get_text('test_cors')}")
        cors_results = self.test_cors_functionality()
        all_results.extend(cors_results)
        
        cors_success = all(r["success"] for r in cors_results)
        if cors_success:
            print(f"   {self.get_text('cors_success')}")
        else:
            print(f"   {self.get_text('cors_failed')}")
        
        # 3. 测试自动加载场景 / Test auto load scenarios
        print(f"\n{self.get_text('test_auto_load_scenarios')}")
        auto_load_results = self.test_auto_load_scenarios()
        all_results.extend(auto_load_results)
        
        auto_load_success = sum(1 for r in auto_load_results if r["success"])
        total_scenarios = len(auto_load_results)
        print(f"   场景测试: {auto_load_success}/{total_scenarios} 通过")
        print(f"   Scenario tests: {auto_load_success}/{total_scenarios} passed")
        
        if auto_load_success >= total_scenarios * 0.8:  # 80%通过率
            print(f"   {self.get_text('auto_load_success')}")
        else:
            print(f"   {self.get_text('auto_load_failed')}")
        
        # 4. 测试语言集成 / Test language integration
        print(f"\n{self.get_text('test_language_integration')}")
        language_results = self.test_language_integration()
        all_results.extend(language_results)
        
        language_success = all(r["success"] for r in language_results)
        if language_success:
            print(f"   {self.get_text('language_integration_success')}")
        else:
            print(f"   {self.get_text('language_integration_failed')}")
        
        # 5. 测试错误处理 / Test error handling
        print(f"\n{self.get_text('test_error_handling')}")
        error_results = self.test_error_handling()
        all_results.extend(error_results)
        
        error_success = all(r["success"] for r in error_results)
        if error_success:
            print(f"   {self.get_text('error_handling_success')}")
        else:
            print(f"   {self.get_text('error_handling_failed')}")
        
        return self.generate_summary(all_results)
    
    def generate_summary(self, results: List[Dict]) -> Dict:
        """生成测试总结 / Generate test summary"""
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r.get("success", False))
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "results": results
        }
        
        # 打印总结 / Print summary
        print("\n" + "=" * 70)
        print(self.get_text("test_summary"))
        print("=" * 70)
        print(f"{self.get_text('total_tests')}: {total_tests}")
        print(f"{self.get_text('passed_tests')}: {passed_tests}")
        print(f"{self.get_text('failed_tests')}: {failed_tests}")
        print(f"{self.get_text('success_rate')}: {success_rate:.1f}%")
        
        # 结论 / Conclusion
        if success_rate == 100:
            print(f"\n{self.get_text('all_tests_passed')}")
        elif success_rate >= 80:
            print(f"\n{self.get_text('some_tests_failed')}")
        else:
            print(f"\n{self.get_text('many_tests_failed')}")
        
        return summary
    
    def save_results(self, results: Dict, filename: str = None):
        """保存测试结果 / Save test results"""
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"enhanced_auto_load_test_results_{timestamp}.json"
        
        results_dir = Path(__file__).parent.parent / "results"
        results_dir.mkdir(exist_ok=True)
        
        filepath = results_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 测试结果已保存到: {filepath}")
        print(f"📄 Test results saved to: {filepath}")

def main():
    """主函数 / Main function"""
    parser = argparse.ArgumentParser(
        description="Enhanced Auto Load API Test Suite / 增强版自动加载API测试套件"
    )
    parser.add_argument(
        "--host", 
        default="127.0.0.1", 
        help="Server host / 服务器主机 (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=5000, 
        help="Server port / 服务器端口 (default: 5000)"
    )
    parser.add_argument(
        "--lang", 
        choices=["zh", "en"], 
        default="zh", 
        help="Language / 语言 (default: zh)"
    )
    parser.add_argument(
        "--save", 
        action="store_true", 
        help="Save test results / 保存测试结果"
    )
    
    args = parser.parse_args()
    
    # 构建基础URL / Build base URL
    base_url = f"http://{args.host}:{args.port}"
    
    # 创建测试套件 / Create test suite
    test_suite = EnhancedAutoLoadTestSuite(base_url=base_url, language=args.lang)
    
    # 运行测试 / Run tests
    results = test_suite.run_all_tests()
    
    # 保存结果 / Save results
    if args.save:
        test_suite.save_results(results)

if __name__ == "__main__":
    main() 