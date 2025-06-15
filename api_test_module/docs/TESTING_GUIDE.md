# Testing Guide / 测试指南

## Overview / 概述

This guide provides comprehensive instructions for testing the Document Preview Editor API using the provided test tools.
本指南提供使用提供的测试工具对文档预览编辑器API进行全面测试的详细说明。

## Prerequisites / 前置条件

### System Requirements / 系统要求
- Python 3.7 or higher / Python 3.7或更高版本
- Document Preview Editor server running / 文档预览编辑器服务器正在运行
- Network access to the server / 对服务器的网络访问

### Required Packages / 必需的包
```bash
pip install requests
```

## Quick Start / 快速开始

### 1. Start the Server / 启动服务器
```bash
# Navigate to the main project directory / 导航到主项目目录
cd /path/to/document-preview-editor

# Start the server / 启动服务器
python run.py
```

### 2. Run Quick Test / 运行快速测试
```bash
# Navigate to the test scripts directory / 导航到测试脚本目录
cd api_test_module/scripts

# Run quick test / 运行快速测试
python quick_test.py
```

Expected output / 预期输出:
```
🔍 Quick API Test / 快速API测试
========================================
Testing server connection... / 测试服务器连接...
✅ Server is running / 服务器正在运行
   Language: zh
   Response time: 0.045s
```

### 3. Run Full Test Suite / 运行完整测试套件
```bash
# Run full test suite / 运行完整测试套件
python api_test_suite.py
```

## Test Categories / 测试类别

### 1. Server Status Test / 服务器状态测试

**Purpose / 目的:** Verify that the server is running and accessible
**目的:** 验证服务器正在运行且可访问

**Test Steps / 测试步骤:**
1. Send GET request to `/api/get_language`
2. Check response status code (should be 200)
3. Verify response contains language information

**Expected Results / 预期结果:**
- Status code: 200
- Response contains current language and available languages

### 2. CORS Functionality Test / CORS功能测试

**Purpose / 目的:** Verify Cross-Origin Resource Sharing configuration
**目的:** 验证跨域资源共享配置

**Test Steps / 测试步骤:**
1. Send OPTIONS request with different origins
2. Check CORS headers in response
3. Verify allowed methods and headers

**Expected Results / 预期结果:**
- Proper CORS headers in response
- Support for common development origins

### 3. Language API Test / 语言API测试

**Purpose / 目的:** Test language management functionality
**目的:** 测试语言管理功能

**Test Steps / 测试步骤:**
1. Get current language setting
2. Set language to different values
3. Verify language changes are applied

**Expected Results / 预期结果:**
- Language retrieval works correctly
- Language setting updates successfully
- Invalid language codes are rejected

### 4. Auto Load API Test / 自动加载API测试

**Purpose / 目的:** Test document and modifications loading
**目的:** 测试文档和修改条目加载

**Test Steps / 测试步骤:**
1. Send auto load request with sample files
2. Test with different parameter combinations
3. Verify error handling for invalid files

**Expected Results / 预期结果:**
- Valid requests return appropriate responses
- Invalid file paths return error messages
- Parameters are processed correctly

## Using the Web Interface / 使用Web界面

### 1. Access the Test Page / 访问测试页面
1. Open your browser / 打开浏览器
2. Navigate to `http://localhost:5000/test`
3. The API test interface will load / API测试界面将加载

### 2. Quick Test / 快速测试
1. Click "快速测试 / Quick Test" button
2. Results will appear in both test panels
3. Green background indicates success / 绿色背景表示成功
4. Red background indicates failure / 红色背景表示失败

### 3. Custom API Test / 自定义API测试
1. Select HTTP method (GET, POST, OPTIONS)
2. Enter API endpoint (e.g., `/api/get_language`)
3. Add request headers if needed (JSON format)
4. Add request body if needed (JSON format)
5. Click "发送请求 / Send" button
6. View results in the result area

### 4. Auto Load Test / 自动加载测试
1. Enter document path (e.g., `sample_document.docx`)
2. Enter modifications path (e.g., `sample_modifications.csv`)
3. Select auto apply option (Yes/No)
4. Click "测试自动加载 / Test Auto Load" button
5. View results in the result area

## Command Line Testing / 命令行测试

### Basic Usage / 基本使用
```bash
# Test with default settings / 使用默认设置测试
python api_test_suite.py

# Test with custom host and port / 使用自定义主机和端口测试
python api_test_suite.py --host localhost --port 8080

# Test with English interface / 使用英文界面测试
python api_test_suite.py --lang en

# Save test results / 保存测试结果
python api_test_suite.py --save
```

### Advanced Options / 高级选项
```bash
# Set environment variables / 设置环境变量
export API_TEST_HOST=192.168.1.100
export API_TEST_PORT=5000
export API_TEST_LANG=zh

# Run tests with environment variables / 使用环境变量运行测试
python api_test_suite.py
```

## Test Data / 测试数据

### Sample Files / 示例文件
The test module includes sample files for testing:
测试模块包含用于测试的示例文件：

1. **sample_document.docx** - Sample Word document
2. **sample_modifications.csv** - Sample modifications file

### CSV Format / CSV格式
```csv
OriginalText,ModifiedText,ModificationReason
人工智能技术,AI技术,使用更简洁的表达
机器学习算法,深度学习算法,更准确的技术描述
数据处理,智能数据处理,强调智能化特性
```

## Interpreting Results / 解释结果

### Success Indicators / 成功指标
- ✅ Green checkmark / 绿色对勾
- Status code 200 for successful requests
- Proper JSON response format
- Expected data in response

### Error Indicators / 错误指标
- ❌ Red X mark / 红色X标记
- Non-200 status codes for failed requests
- Error messages in response
- Connection timeouts or network errors

### Common Status Codes / 常见状态码
| Code | Meaning / 含义 | Description / 描述 |
|------|---------------|-------------------|
| 200 | OK | Request successful / 请求成功 |
| 400 | Bad Request | Invalid request format / 无效的请求格式 |
| 404 | Not Found | Endpoint or file not found / 端点或文件未找到 |
| 500 | Internal Server Error | Server error / 服务器错误 |

## Troubleshooting / 故障排除

### Common Issues / 常见问题

#### 1. Connection Refused / 连接被拒绝
**Symptoms / 症状:**
- "Cannot connect to server" error
- Connection timeout

**Solutions / 解决方案:**
1. Verify server is running / 验证服务器正在运行
2. Check host and port settings / 检查主机和端口设置
3. Verify firewall settings / 验证防火墙设置
4. Test with `curl` or browser / 使用curl或浏览器测试

#### 2. CORS Errors / CORS错误
**Symptoms / 症状:**
- "CORS policy" error in browser
- Missing CORS headers

**Solutions / 解决方案:**
1. Check server CORS configuration / 检查服务器CORS配置
2. Verify allowed origins / 验证允许的源
3. Test with different origins / 使用不同源进行测试

#### 3. File Not Found / 文件未找到
**Symptoms / 症状:**
- 404 status code
- "File not found" error message

**Solutions / 解决方案:**
1. Verify file paths are correct / 验证文件路径正确
2. Check file permissions / 检查文件权限
3. Use absolute paths if needed / 如需要使用绝对路径

#### 4. JSON Parse Errors / JSON解析错误
**Symptoms / 症状:**
- "Invalid JSON" error
- Malformed request body

**Solutions / 解决方案:**
1. Validate JSON format / 验证JSON格式
2. Check for trailing commas / 检查尾随逗号
3. Use JSON validator tools / 使用JSON验证工具

### Debug Mode / 调试模式
```bash
# Enable debug output / 启用调试输出
python api_test_suite.py --debug

# Verbose logging / 详细日志
python api_test_suite.py --verbose
```

## Performance Testing / 性能测试

### Response Time Measurement / 响应时间测量
The test suite automatically measures response times for all requests.
测试套件自动测量所有请求的响应时间。

**Acceptable Response Times / 可接受的响应时间:**
- Language API: < 100ms
- Auto Load API: < 5000ms (depending on file size)
- CORS preflight: < 50ms

### Load Testing / 负载测试
For load testing, consider using tools like:
对于负载测试，考虑使用以下工具：

- Apache Bench (ab)
- wrk
- JMeter

Example with Apache Bench:
```bash
# Test 100 requests with 10 concurrent connections
ab -n 100 -c 10 http://localhost:5000/api/get_language
```

## Continuous Integration / 持续集成

### GitHub Actions Example / GitHub Actions示例
```yaml
name: API Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install requests
    - name: Start server
      run: python run.py &
    - name: Wait for server
      run: sleep 10
    - name: Run API tests
      run: python api_test_module/scripts/api_test_suite.py
```

## Best Practices / 最佳实践

### 1. Test Environment / 测试环境
- Use dedicated test server / 使用专用测试服务器
- Isolate test data / 隔离测试数据
- Clean up after tests / 测试后清理

### 2. Test Data Management / 测试数据管理
- Use consistent sample files / 使用一致的示例文件
- Version control test data / 版本控制测试数据
- Document test scenarios / 记录测试场景

### 3. Error Handling / 错误处理
- Test both success and failure cases / 测试成功和失败情况
- Verify error messages are helpful / 验证错误消息有用
- Check edge cases / 检查边缘情况

### 4. Documentation / 文档
- Keep test documentation updated / 保持测试文档更新
- Document known issues / 记录已知问题
- Provide clear examples / 提供清晰示例

## Reporting Issues / 报告问题

When reporting issues, please include:
报告问题时，请包含：

1. Test environment details / 测试环境详情
2. Steps to reproduce / 重现步骤
3. Expected vs actual results / 预期与实际结果
4. Error messages and logs / 错误消息和日志
5. Test configuration / 测试配置

## Contributing / 贡献

To contribute to the test suite:
为测试套件做贡献：

1. Fork the repository / 分叉仓库
2. Create a feature branch / 创建功能分支
3. Add new tests or improve existing ones / 添加新测试或改进现有测试
4. Update documentation / 更新文档
5. Submit a pull request / 提交拉取请求

---

**Happy Testing! / 测试愉快！** 🧪 