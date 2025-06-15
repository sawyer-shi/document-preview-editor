# Troubleshooting Guide / 故障排除指南

## Overview / 概述

This guide helps you resolve common issues when using the Document Preview Editor API Test Module.
本指南帮助您解决使用文档预览编辑器API测试模块时的常见问题。

## Common Issues / 常见问题

### 1. Server Connection Issues / 服务器连接问题

#### Problem / 问题
```
❌ Cannot connect to server / 无法连接到服务器
ConnectionError: [Errno 61] Connection refused
```

#### Possible Causes / 可能原因
- Server is not running / 服务器未运行
- Wrong host or port / 错误的主机或端口
- Firewall blocking connection / 防火墙阻止连接
- Server crashed or stopped / 服务器崩溃或停止

#### Solutions / 解决方案

**1. Check if server is running / 检查服务器是否运行**
```bash
# Check if process is running / 检查进程是否运行
ps aux | grep python
netstat -an | grep 5000

# On Windows / 在Windows上
tasklist | findstr python
netstat -an | findstr 5000
```

**2. Start the server / 启动服务器**
```bash
cd /path/to/document-preview-editor
python run.py
```

**3. Check server logs / 检查服务器日志**
Look for error messages in the server console output.
查看服务器控制台输出中的错误消息。

**4. Test with curl / 使用curl测试**
```bash
curl -X GET http://localhost:5000/api/get_language
```

**5. Check firewall settings / 检查防火墙设置**
- Ensure port 5000 is not blocked
- 确保端口5000未被阻止

### 2. CORS Errors / CORS错误

#### Problem / 问题
```
Access to fetch at 'http://localhost:5000/api/get_language' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

#### Possible Causes / 可能原因
- CORS not properly configured / CORS配置不正确
- Origin not in allowed list / 源不在允许列表中
- Missing CORS headers / 缺少CORS头

#### Solutions / 解决方案

**1. Check CORS configuration / 检查CORS配置**
```python
# In config/cors_config.py
ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8080',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8080'
]
```

**2. Test CORS with curl / 使用curl测试CORS**
```bash
curl -X OPTIONS \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  http://localhost:5000/api/auto_load
```

**3. Check browser developer tools / 检查浏览器开发者工具**
- Open Network tab / 打开网络选项卡
- Look for preflight OPTIONS requests / 查找预检OPTIONS请求
- Check response headers / 检查响应头

### 3. File Not Found Errors / 文件未找到错误

#### Problem / 问题
```
❌ File not found: sample_document.docx
404 Not Found
```

#### Possible Causes / 可能原因
- Sample files not created / 示例文件未创建
- Wrong file path / 错误的文件路径
- File permissions issue / 文件权限问题

#### Solutions / 解决方案

**1. Run setup script / 运行设置脚本**
```bash
cd api_test_module/scripts
python setup_samples.py
```

**2. Check file existence / 检查文件是否存在**
```bash
ls -la api_test_module/samples/
# On Windows / 在Windows上
dir api_test_module\samples\
```

**3. Use absolute paths / 使用绝对路径**
```python
# Instead of / 而不是
document = "sample_document.docx"

# Use / 使用
document = "/full/path/to/api_test_module/samples/sample_document.docx"
```

**4. Check file permissions / 检查文件权限**
```bash
chmod 644 api_test_module/samples/*
```

### 4. JSON Parse Errors / JSON解析错误

#### Problem / 问题
```
❌ Invalid JSON format
JSONDecodeError: Expecting ',' delimiter
```

#### Possible Causes / 可能原因
- Malformed JSON in request / 请求中的JSON格式错误
- Trailing commas / 尾随逗号
- Missing quotes / 缺少引号
- Invalid escape characters / 无效的转义字符

#### Solutions / 解决方案

**1. Validate JSON format / 验证JSON格式**
```json
// Correct / 正确
{
    "language": "zh",
    "auto_apply": false
}

// Incorrect / 错误
{
    "language": "zh",
    "auto_apply": false,  // Trailing comma / 尾随逗号
}
```

**2. Use JSON validator / 使用JSON验证器**
- Online tools: jsonlint.com
- Command line: `python -m json.tool`

**3. Check for special characters / 检查特殊字符**
```json
// Escape special characters / 转义特殊字符
{
    "text": "This is a \"quoted\" string"
}
```

### 5. Import Errors / 导入错误

#### Problem / 问题
```
ModuleNotFoundError: No module named 'requests'
ImportError: cannot import name 'get_cors_headers'
```

#### Possible Causes / 可能原因
- Missing dependencies / 缺少依赖
- Python path issues / Python路径问题
- Module structure changes / 模块结构变化

#### Solutions / 解决方案

**1. Install missing packages / 安装缺少的包**
```bash
pip install requests
pip install -r requirements.txt
```

**2. Check Python path / 检查Python路径**
```python
import sys
print(sys.path)
```

**3. Run from correct directory / 从正确目录运行**
```bash
# Make sure you're in the project root / 确保在项目根目录
cd /path/to/document-preview-editor
python api_test_module/scripts/api_test_suite.py
```

### 6. Permission Errors / 权限错误

#### Problem / 问题
```
PermissionError: [Errno 13] Permission denied
```

#### Possible Causes / 可能原因
- Insufficient file permissions / 文件权限不足
- Directory access restrictions / 目录访问限制
- File in use by another process / 文件被其他进程使用

#### Solutions / 解决方案

**1. Check file permissions / 检查文件权限**
```bash
ls -la api_test_module/
chmod 755 api_test_module/scripts/
chmod 644 api_test_module/samples/*
```

**2. Run with appropriate privileges / 使用适当权限运行**
```bash
# On Unix/Linux/Mac
sudo python api_test_suite.py

# On Windows (run as administrator)
# 在Windows上（以管理员身份运行）
```

**3. Close files in other applications / 关闭其他应用程序中的文件**
Make sure Word documents are not open in Microsoft Word.
确保Word文档未在Microsoft Word中打开。

### 7. Encoding Issues / 编码问题

#### Problem / 问题
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
UnicodeEncodeError: 'ascii' codec can't encode character
```

#### Possible Causes / 可能原因
- File encoding mismatch / 文件编码不匹配
- System locale issues / 系统区域设置问题
- Special characters in file names / 文件名中的特殊字符

#### Solutions / 解决方案

**1. Set environment variables / 设置环境变量**
```bash
export PYTHONIOENCODING=utf-8
export LC_ALL=en_US.UTF-8

# On Windows / 在Windows上
set PYTHONIOENCODING=utf-8
```

**2. Use explicit encoding / 使用显式编码**
```python
with open('file.csv', 'r', encoding='utf-8') as f:
    content = f.read()
```

**3. Check file encoding / 检查文件编码**
```bash
file -i filename.csv
chardet filename.csv
```

### 8. Performance Issues / 性能问题

#### Problem / 问题
- Slow response times / 响应时间慢
- Timeouts / 超时
- High memory usage / 内存使用率高

#### Possible Causes / 可能原因
- Large file sizes / 文件大小过大
- Network latency / 网络延迟
- Server overload / 服务器过载

#### Solutions / 解决方案

**1. Increase timeout values / 增加超时值**
```python
response = requests.get(url, timeout=30)  # 30 seconds
```

**2. Use smaller test files / 使用较小的测试文件**
Create smaller sample documents for testing.
创建较小的示例文档进行测试。

**3. Monitor system resources / 监控系统资源**
```bash
top
htop
# On Windows / 在Windows上
taskmgr
```

## Debugging Tips / 调试技巧

### 1. Enable Debug Mode / 启用调试模式
```bash
# Set debug environment variable / 设置调试环境变量
export FLASK_DEBUG=1
export FLASK_ENV=development

# Run with verbose output / 使用详细输出运行
python api_test_suite.py --verbose
```

### 2. Use Browser Developer Tools / 使用浏览器开发者工具
1. Open browser developer tools (F12)
2. Go to Network tab / 转到网络选项卡
3. Monitor API requests and responses / 监控API请求和响应
4. Check console for JavaScript errors / 检查控制台中的JavaScript错误

### 3. Check Server Logs / 检查服务器日志
Monitor the server console output for error messages and stack traces.
监控服务器控制台输出中的错误消息和堆栈跟踪。

### 4. Test Individual Components / 测试单个组件
```bash
# Test only server connection / 仅测试服务器连接
python quick_test.py

# Test specific endpoint / 测试特定端点
curl -X GET http://localhost:5000/api/get_language
```

### 5. Use Python Debugger / 使用Python调试器
```python
import pdb
pdb.set_trace()  # Add breakpoint / 添加断点
```

## Getting Help / 获取帮助

### 1. Check Documentation / 查看文档
- [API Reference](API_REFERENCE.md)
- [Testing Guide](TESTING_GUIDE.md)
- [README](../README.md)

### 2. Search Issues / 搜索问题
Check the GitHub issues page for similar problems:
在GitHub问题页面搜索类似问题：
https://github.com/sawyer-shi/document-preview-editor/issues

### 3. Create New Issue / 创建新问题
If you can't find a solution, create a new issue with:
如果找不到解决方案，请创建新问题并包含：

- **Environment details / 环境详情**
  - Operating system / 操作系统
  - Python version / Python版本
  - Package versions / 包版本

- **Steps to reproduce / 重现步骤**
  - Exact commands run / 运行的确切命令
  - Input data used / 使用的输入数据
  - Expected behavior / 预期行为

- **Error messages / 错误消息**
  - Full error output / 完整错误输出
  - Stack traces / 堆栈跟踪
  - Log files / 日志文件

- **Screenshots / 截图**
  - Browser console errors / 浏览器控制台错误
  - Test results / 测试结果

### 4. Community Support / 社区支持
- GitHub Discussions
- Stack Overflow (tag: document-preview-editor)

## Prevention Tips / 预防技巧

### 1. Regular Testing / 定期测试
Run the test suite regularly to catch issues early.
定期运行测试套件以尽早发现问题。

### 2. Keep Dependencies Updated / 保持依赖更新
```bash
pip list --outdated
pip install --upgrade package_name
```

### 3. Use Version Control / 使用版本控制
Keep track of changes that might affect the API.
跟踪可能影响API的更改。

### 4. Monitor Server Health / 监控服务器健康
- Check disk space / 检查磁盘空间
- Monitor memory usage / 监控内存使用
- Watch for error patterns / 观察错误模式

### 5. Backup Test Data / 备份测试数据
Keep copies of working test files and configurations.
保留工作测试文件和配置的副本。

---

**Need more help? / 需要更多帮助？**
Contact the development team or create an issue on GitHub.
联系开发团队或在GitHub上创建问题。 