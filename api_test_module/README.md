# Document Preview Editor API Test Module
# 文档预览编辑器API测试模块

## Enhanced Auto Load Testing Module
## 增强版自动加载测试模块

A comprehensive testing suite for the Document Preview Editor's Auto Load API functionality, featuring multilingual support and extensive scenario coverage.

文档预览编辑器自动加载API功能的综合测试套件，具有多语言支持和广泛的场景覆盖。

## 🚀 Key Features / 主要功能

### Enhanced Auto Load Testing / 增强版自动加载测试
- **Multiple Test Scenarios** / **多种测试场景**
  - Local files with/without auto-apply / 本地文件（带/不带自动应用）
  - Remote URL sources / 远程URL来源
  - Mixed source combinations / 混合来源组合
  - Error handling validation / 错误处理验证
  - URL encoding support / URL编码支持

- **Language Integration Testing** / **语言集成测试**
  - Automatic language switching / 自动语言切换
  - Language parameter integration / 语言参数集成
  - Bilingual result reporting / 双语结果报告

- **CORS Functionality Testing** / **CORS功能测试**
  - Cross-origin request validation / 跨域请求验证
  - Preflight request testing / 预检请求测试
  - Multiple origin support / 多源支持

### Web Interface / Web界面
- **Modern Responsive Design** / **现代响应式设计**
- **Scenario-based Testing** / **基于场景的测试**
- **Real-time Result Display** / **实时结果显示**
- **Bilingual Interface** / **双语界面**

### Command Line Tools / 命令行工具
- **Comprehensive Test Suite** / **综合测试套件**
- **Quick Testing Scripts** / **快速测试脚本**
- **Automated Setup Tools** / **自动化设置工具**

## 📁 Directory Structure / 目录结构

```
api_test_module/
├── README.md                           # Main documentation / 主要文档
├── docs/                              # Documentation / 文档目录
│   ├── API_REFERENCE.md               # API reference / API参考
│   ├── TESTING_GUIDE.md               # Testing guide / 测试指南
│   └── TROUBLESHOOTING.md             # Troubleshooting / 故障排除
├── scripts/                           # Test scripts / 测试脚本
│   ├── api_test_suite.py              # Enhanced auto load test suite / 增强版自动加载测试套件
│   ├── quick_test.py                  # Quick connectivity test / 快速连接测试
│   └── setup_samples.py               # Sample file setup / 示例文件设置
└── samples/                           # Sample files / 示例文件
    ├── README.md                      # Sample file documentation / 示例文件文档
    ├── sample_document.docx           # Sample document / 示例文档
    └── sample_modifications.csv       # Sample modifications / 示例修改条目
```

## 🎯 Enhanced Auto Load Test Scenarios / 增强版自动加载测试场景

### 1. Local Files - No Auto Apply / 本地文件 - 不自动应用
- **Document**: `sample_document.docx`
- **Modifications**: `sample_modifications.csv`
- **Auto Apply**: `false`
- **Language**: `zh` (Chinese)

### 2. Local Files - With Auto Apply / 本地文件 - 自动应用
- **Document**: `sample_document.docx`
- **Modifications**: `sample_modifications.csv`
- **Auto Apply**: `true`
- **Language**: `zh` (Chinese)

### 3. Remote URLs / 远程URL
- **Document**: `https://example.com/sample.docx`
- **Modifications**: `https://example.com/sample.csv`
- **Auto Apply**: `true`
- **Language**: `en` (English)

### 4. Mixed Sources / 混合来源
- **Document**: `sample_document.docx` (local)
- **Modifications**: `https://example.com/sample.csv` (remote)
- **Auto Apply**: `false`
- **Language**: `zh` (Chinese)

### 5. Error Handling / 错误处理
- **Document**: `/nonexistent/path/document.docx`
- **Modifications**: `sample_modifications.csv`
- **Auto Apply**: `false`
- **Language**: `en` (English)

### 6. URL Encoded Paths / URL编码路径
- **Document**: URL-encoded file paths
- **Modifications**: URL-encoded file paths
- **Auto Apply**: `false`
- **Language**: `zh` (Chinese)

## 🛠️ Quick Start / 快速开始

### 1. Setup Sample Files / 设置示例文件
```bash
cd api_test_module/scripts
python setup_samples.py
```

### 2. Run Quick Test / 运行快速测试
```bash
python quick_test.py
```

### 3. Run Enhanced Auto Load Test Suite / 运行增强版自动加载测试套件
```bash
# Default settings / 默认设置
python api_test_suite.py

# Custom host and port / 自定义主机和端口
python api_test_suite.py --host 127.0.0.1 --port 5000

# English interface / 英文界面
python api_test_suite.py --lang en

# Save results / 保存结果
python api_test_suite.py --save
```

### 4. Web Interface Testing / Web界面测试
1. Start the main application / 启动主应用程序
2. Navigate to `/test` endpoint / 访问 `/test` 端点
3. Select test scenarios / 选择测试场景
4. Configure parameters / 配置参数
5. Run tests and view results / 运行测试并查看结果

## 📊 Test Categories / 测试类别

### 1. Server Status Testing / 服务器状态测试
- Connectivity verification / 连接验证
- Response time measurement / 响应时间测量
- Basic functionality check / 基本功能检查

### 2. CORS Functionality Testing / CORS功能测试
- Preflight request validation / 预检请求验证
- Multiple origin testing / 多源测试
- Header configuration verification / 头配置验证

### 3. Auto Load Scenario Testing / 自动加载场景测试
- Local file processing / 本地文件处理
- Remote URL handling / 远程URL处理
- Mixed source combinations / 混合来源组合
- Auto-apply functionality / 自动应用功能

### 4. Language Integration Testing / 语言集成测试
- Language switching / 语言切换
- Parameter integration / 参数集成
- Bilingual response handling / 双语响应处理

### 5. Error Handling Testing / 错误处理测试
- Invalid path handling / 无效路径处理
- Missing file scenarios / 文件缺失场景
- Parameter validation / 参数验证

## 🔧 Configuration Options / 配置选项

### Command Line Arguments / 命令行参数
- `--host`: Server host (default: 127.0.0.1) / 服务器主机
- `--port`: Server port (default: 5000) / 服务器端口
- `--lang`: Interface language (zh/en, default: zh) / 界面语言
- `--save`: Save test results to file / 保存测试结果到文件

### Environment Variables / 环境变量
- `API_TEST_HOST`: Override default host / 覆盖默认主机
- `API_TEST_PORT`: Override default port / 覆盖默认端口
- `API_TEST_LANG`: Override default language / 覆盖默认语言

## 📈 Test Results and Reporting / 测试结果和报告

### Success Criteria / 成功标准
- **Server Status**: HTTP 200 response / HTTP 200响应
- **CORS Tests**: Proper headers present / 正确的头信息存在
- **Auto Load Tests**: Expected status codes (200, 400, 404) / 预期状态码
- **Language Integration**: Successful language switching / 成功的语言切换
- **Error Handling**: Appropriate error responses / 适当的错误响应

### Result Formats / 结果格式
- **Console Output**: Real-time progress and summary / 实时进度和摘要
- **JSON Files**: Detailed test results (with --save) / 详细测试结果
- **Web Interface**: Interactive result display / 交互式结果显示

## 🌐 API Endpoints Tested / 测试的API端点

### Primary Endpoints / 主要端点
- `GET /api/get_language` - Language retrieval / 语言获取
- `POST /api/set_language` - Language setting / 语言设置
- `POST /api/auto_load` - Auto load functionality / 自动加载功能
- `OPTIONS /api/auto_load` - CORS preflight / CORS预检

### Test Parameters / 测试参数
- **Document paths**: Local files, URLs, encoded paths / 文档路径
- **Modification paths**: CSV files, remote sources / 修改条目路径
- **Auto apply**: Boolean flag / 布尔标志
- **Language**: zh/en language codes / 语言代码

## 🔍 Integration Examples / 集成示例

### JavaScript/Node.js
```javascript
// Test auto load with language integration
const testAutoLoad = async () => {
    // Set language first
    await fetch('/api/set_language', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: 'zh' })
    });
    
    // Then test auto load
    const response = await fetch('/api/auto_load', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            document: 'sample_document.docx',
            modifications: 'sample_modifications.csv',
            auto_apply: false
        })
    });
    
    return response.json();
};
```

### Python
```python
import requests

def test_enhanced_auto_load():
    base_url = "http://127.0.0.1:5000"
    
    // Set language
    lang_response = requests.post(
        f"{base_url}/api/set_language",
        json={"language": "zh"}
    )
    
    // Test auto load
    auto_load_response = requests.post(
        f"{base_url}/api/auto_load",
        json={
            "document": "sample_document.docx",
            "modifications": "sample_modifications.csv",
            "auto_apply": False
        }
    )
    
    return auto_load_response.json()
```

### cURL
```bash
# Set language first
curl -X POST http://127.0.0.1:5000/api/set_language \
  -H "Content-Type: application/json" \
  -d '{"language": "zh"}'

# Test auto load
curl -X POST http://127.0.0.1:5000/api/auto_load \
  -H "Content-Type: application/json" \
  -d '{
    "document": "sample_document.docx",
    "modifications": "sample_modifications.csv",
    "auto_apply": false
  }'
```

## 🚨 Troubleshooting / 故障排除

### Common Issues / 常见问题

1. **Connection Refused / 连接被拒绝**
   - Ensure the main application is running / 确保主应用程序正在运行
   - Check host and port configuration / 检查主机和端口配置

2. **File Not Found Errors / 文件未找到错误**
   - Run `setup_samples.py` to create sample files / 运行设置脚本创建示例文件
   - Verify file paths are correct / 验证文件路径正确

3. **CORS Errors / CORS错误**
   - Check server CORS configuration / 检查服务器CORS配置
   - Verify origin headers / 验证源头信息

4. **Language Integration Issues / 语言集成问题**
   - Ensure language API is working / 确保语言API正常工作
   - Check language parameter format / 检查语言参数格式

For detailed troubleshooting, see [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

详细故障排除请参见 [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

## 📚 Documentation / 文档

- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation / 完整API文档
- **[Testing Guide](docs/TESTING_GUIDE.md)** - Detailed testing instructions / 详细测试说明
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Problem resolution guide / 问题解决指南

## 🤝 Contributing / 贡献

1. Fork the repository / 分叉仓库
2. Create a feature branch / 创建功能分支
3. Add tests for new scenarios / 为新场景添加测试
4. Update documentation / 更新文档
5. Submit a pull request / 提交拉取请求

## 📄 License / 许可证

This project is licensed under the Apache 2.0 License.

本项目采用Apache 2.0许可证。

## 🔗 Related Links / 相关链接

- **Main Application Repository** / 主应用程序仓库
- **API Documentation** / API文档
- **Issue Tracker** / 问题跟踪器

---

**Version**: 2.0.0  
**Last Updated**: 2025-01-12  
**Author**: sawyer-shi 