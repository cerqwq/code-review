# 🔍 Code Review

AI代码审查工具，受graphify (60k stars)启发，支持多维度代码审查。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/OpenAI-API-green?logo=openai" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

## ✨ 特性

- 🔍 多维度代码审查（质量、安全、性能）
- 📁 文件和目录批量审查
- 🔄 重构建议
- 🧪 测试代码生成
- 📖 代码解释

## 🚀 快速开始

```bash
pip install openai

python reviewer.py
```

## 📖 使用

```python
from reviewer import create_reviewer

reviewer = create_reviewer()

# 审查代码
result = reviewer.review_code("""
def add(a, b):
    return a + b
""", language="Python", focus=["质量", "安全"])

# 审查文件
result = reviewer.review_file("path/to/file.py")

# 审查目录
results = reviewer.review_directory("src/", extensions=[".py", ".js"])

# 重构建议
refactored = reviewer.suggest_refactor(code, "Python")

# 生成测试
tests = reviewer.generate_tests(code, "Python")

# 解释代码
explanation = reviewer.explain_code(code, "Python", level="beginner")
```

## 📁 项目结构

```
code-review/
├── reviewer.py    # 代码审查核心
└── README.md
```

## 📄 许可证

MIT License
