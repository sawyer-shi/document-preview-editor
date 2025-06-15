#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Auto Load Demo Script
增强版自动加载演示脚本

This script demonstrates the enhanced auto load functionality with various scenarios.
该脚本演示了各种场景下的增强版自动加载功能。

Author: sawyer-shi
License: Apache 2.0
"""

import requests
import json
import time
from typing import Dict, List

class EnhancedAutoLoadDemo:
    """增强版自动加载演示类"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def demo_scenario(self, name: str, description: str, document: str, 
                     modifications: str, auto_apply: bool, language: str) -> Dict:
        """演示单个场景"""
        print(f"\n🎯 场景: {name}")
        print(f"   描述: {description}")
        print(f"   语言: {language}")
        print(f"   文档: {document}")
        print(f"   修改: {modifications}")
        print(f"   自动应用: {auto_apply}")
        
        try:
            # 1. 设置语言
            print("   ⏳ 设置语言...")
            lang_response = self.session.post(
                f"{self.base_url}/api/set_language",
                json={"language": language},
                timeout=10
            )
            
            # 2. 测试自动加载
            print("   ⏳ 测试自动加载...")
            auto_load_response = self.session.post(
                f"{self.base_url}/api/auto_load",
                json={
                    "document": document,
                    "modifications": modifications,
                    "auto_apply": auto_apply
                },
                timeout=30
            )
            
            # 3. 评估结果
            lang_success = lang_response.status_code == 200
            auto_load_success = auto_load_response.status_code in [200, 400, 404]
            overall_success = lang_success and auto_load_success
            
            status = "✅ 成功" if overall_success else "❌ 失败"
            print(f"   {status} (语言: {lang_response.status_code}, 自动加载: {auto_load_response.status_code})")
            
            return {
                "scenario": name,
                "success": overall_success,
                "language_status": lang_response.status_code,
                "auto_load_status": auto_load_response.status_code,
                "description": description
            }
            
        except Exception as e:
            print(f"   ❌ 错误: {str(e)}")
            return {
                "scenario": name,
                "success": False,
                "error": str(e),
                "description": description
            }
    
    def run_demo(self):
        """运行完整演示"""
        print("=" * 80)
        print("🚀 增强版自动加载API功能演示")
        print("🚀 Enhanced Auto Load API Functionality Demo")
        print("=" * 80)
        
        # 测试服务器连接
        print("\n🔍 检查服务器状态...")
        try:
            response = self.session.get(f"{self.base_url}/api/get_language", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ 服务器正常运行 (当前语言: {data.get('language', 'unknown')})")
            else:
                print(f"   ❌ 服务器响应异常 (状态码: {response.status_code})")
                return
        except Exception as e:
            print(f"   ❌ 无法连接服务器: {str(e)}")
            return
        
        # 定义演示场景
        scenarios = [
            {
                "name": "本地文件基础测试",
                "description": "Local Files Basic Test",
                "document": "sample_document.docx",
                "modifications": "sample_modifications.csv",
                "auto_apply": False,
                "language": "zh"
            },
            {
                "name": "本地文件自动应用",
                "description": "Local Files with Auto Apply",
                "document": "sample_document.docx",
                "modifications": "sample_modifications.csv",
                "auto_apply": True,
                "language": "zh"
            },
            {
                "name": "英文环境测试",
                "description": "English Environment Test",
                "document": "sample_document.docx",
                "modifications": "sample_modifications.csv",
                "auto_apply": False,
                "language": "en"
            },
            {
                "name": "远程URL测试",
                "description": "Remote URL Test",
                "document": "https://example.com/sample.docx",
                "modifications": "https://example.com/sample.csv",
                "auto_apply": True,
                "language": "en"
            },
            {
                "name": "混合来源测试",
                "description": "Mixed Sources Test",
                "document": "sample_document.docx",
                "modifications": "https://example.com/sample.csv",
                "auto_apply": False,
                "language": "zh"
            }
        ]
        
        # 运行所有场景
        results = []
        for scenario in scenarios:
            result = self.demo_scenario(**scenario)
            results.append(result)
            time.sleep(1)  # 短暂延迟
        
        # 生成总结
        print("\n" + "=" * 80)
        print("📊 演示总结 / Demo Summary")
        print("=" * 80)
        
        total_scenarios = len(results)
        successful_scenarios = sum(1 for r in results if r["success"])
        success_rate = (successful_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0
        
        print(f"总场景数 / Total Scenarios: {total_scenarios}")
        print(f"成功场景 / Successful Scenarios: {successful_scenarios}")
        print(f"成功率 / Success Rate: {success_rate:.1f}%")
        
        print("\n详细结果 / Detailed Results:")
        for result in results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['scenario']}: {result['description']}")
            if not result["success"] and "error" in result:
                print(f"   错误: {result['error']}")
        
        # 结论
        if success_rate == 100:
            print("\n🎉 所有场景演示成功！增强版自动加载功能正常工作。")
            print("🎉 All scenarios demonstrated successfully! Enhanced auto load functionality is working properly.")
        elif success_rate >= 80:
            print("\n✅ 大部分场景演示成功，增强版自动加载功能基本正常。")
            print("✅ Most scenarios demonstrated successfully, enhanced auto load functionality is mostly working.")
        else:
            print("\n⚠️ 部分场景演示失败，请检查服务器配置。")
            print("⚠️ Some scenarios failed, please check server configuration.")
        
        return results

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Auto Load Demo / 增强版自动加载演示")
    parser.add_argument("--host", default="127.0.0.1", help="Server host / 服务器主机")
    parser.add_argument("--port", type=int, default=5000, help="Server port / 服务器端口")
    
    args = parser.parse_args()
    
    base_url = f"http://{args.host}:{args.port}"
    demo = EnhancedAutoLoadDemo(base_url=base_url)
    
    results = demo.run_demo()
    
    # 可选：保存结果
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"enhanced_auto_load_demo_results_{timestamp}.json"
    
    try:
        import os
        results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
        os.makedirs(results_dir, exist_ok=True)
        
        filepath = os.path.join(results_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": timestamp,
                "base_url": base_url,
                "results": results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 演示结果已保存到: {filepath}")
        print(f"📄 Demo results saved to: {filepath}")
    except Exception as e:
        print(f"\n⚠️ 无法保存结果: {str(e)}")

if __name__ == "__main__":
    main() 