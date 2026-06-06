"""
Code Review - AI代码审查工具
受 graphify (60k stars) 启发，支持多维度代码审查
"""

import json
import os
from typing import Dict, List, Any, Generator
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class CodeReviewer:
    """
    AI代码审查工具
    支持：代码质量、安全性、性能、最佳实践
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def review_code(self, code: str, language: str = "Python", focus: List[str] = None) -> Dict:
        """审查代码"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        focus = focus or ["质量", "安全", "性能", "最佳实践"]
        focus_text = "、".join(focus)

        prompt = f"""请审查以下{language}代码，重点关注{focus_text}方面：

```{language}
{code}
```

请按以下格式返回JSON：
{{
    "summary": "一句话总结",
    "score": 1-10,
    "issues": [
        {{"severity": "high/medium/low", "type": "类型", "line": 行号, "description": "描述", "suggestion": "建议"}}
    ],
    "strengths": ["优点1", "优点2"],
    "improvements": ["改进1", "改进2"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            return {"error": str(e), "raw": content}

        return {"summary": content}

    def review_file(self, file_path: str, focus: List[str] = None) -> Dict:
        """审查文件"""
        path = Path(file_path)
        if not path.exists():
            return {"error": f"文件不存在: {file_path}"}

        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()

        # 检测语言
        ext = path.suffix.lower()
        lang_map = {
            ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
            ".java": "Java", ".cpp": "C++", ".c": "C", ".go": "Go",
            ".rs": "Rust", ".rb": "Ruby", ".php": "PHP"
        }
        language = lang_map.get(ext, "Unknown")

        result = self.review_code(code, language, focus)
        result["file"] = str(path)
        result["language"] = language
        return result

    def review_directory(self, dir_path: str, extensions: List[str] = None) -> List[Dict]:
        """审查目录"""
        path = Path(dir_path)
        if not path.exists():
            return [{"error": f"目录不存在: {dir_path}"}]

        extensions = extensions or [".py", ".js", ".ts"]
        results = []

        for ext in extensions:
            for file_path in path.rglob(f"*{ext}"):
                if "node_modules" in str(file_path) or "__pycache__" in str(file_path):
                    continue
                try:
                    result = self.review_file(str(file_path))
                    results.append(result)
                except Exception as e:
                    results.append({"file": str(file_path), "error": str(e)})

        return results

    def suggest_refactor(self, code: str, language: str = "Python") -> str:
        """建议重构"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请为以下{language}代码提供重构建议，输出重构后的代码：

```{language}
{code}
```

要求：
1. 保持功能不变
2. 提高可读性
3. 遵循最佳实践
4. 添加必要注释"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def generate_tests(self, code: str, language: str = "Python") -> str:
        """生成测试代码"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请为以下{language}代码生成单元测试：

```{language}
{code}
```

要求：
1. 覆盖主要功能
2. 包含边界情况
3. 使用标准测试框架
4. 添加必要注释"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def explain_code(self, code: str, language: str = "Python", level: str = "intermediate") -> str:
        """解释代码"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请用{level}水平解释以下{language}代码：

```{language}
{code}
```

要求：
1. 整体功能说明
2. 关键逻辑解析
3. 重要细节说明
4. 使用场景"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content


def create_reviewer(**kwargs) -> CodeReviewer:
    """创建代码审查器"""
    return CodeReviewer(**kwargs)


if __name__ == "__main__":
    reviewer = create_reviewer()

    print("Code Review Tool")
    print()

    # 测试代码
    test_code = """
def calculate_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
"""

    print("Reviewing code...")
    result = reviewer.review_code(test_code, "Python")
    print(json.dumps(result, ensure_ascii=False, indent=2))
