import json
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from app.config import get_settings

logger = structlog.get_logger()
settings = get_settings()


class AIEngine:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _call_openai(self, prompt: str) -> str:
        response = await self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert code reviewer. Analyze code for quality, security, performance, and architecture."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=4096,
        )
        return response.choices[0].message.content

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _call_anthropic(self, prompt: str) -> str:
        response = await self.anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            system="You are an expert code reviewer. Analyze code for quality, security, performance, and architecture.",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    async def analyze_code(self, code: str, language: str) -> dict:
        prompt = self._build_analysis_prompt(code, language)

        if settings.AI_PROVIDER == "anthropic" and self.anthropic_client:
            response_text = await self._call_anthropic(prompt)
        elif self.openai_client:
            response_text = await self._call_openai(prompt)
        else:
            return self._mock_analysis(code, language)

        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            logger.error("Failed to parse AI response", response=response_text)
            return self._mock_analysis(code, language)

        return self._normalize_result(result)

    def _build_analysis_prompt(self, code: str, language: str) -> str:
        return f"""Analyze the following {language} code and provide a JSON response with:

1. overall_score (0-100)
2. grade (A+, A, B+, B, C+, C, D, F)
3. scores object with:
   - test_coverage (0-100)
   - dependency_health (0-100)
   - code_cleanliness (0-100)
   - architecture (0-100)
   - security (0-100)
4. summary (string)
5. issues array with:
   - category (string: security, performance, quality, architecture)
   - severity (string: critical, high, medium, low)
   - line_number (number or null)
   - message (string)
   - suggestion (string)
   - rule_id (string)
6. recommendations object with improvement suggestions

Code to analyze:
```{language}
{code}
```

Respond ONLY with valid JSON."""

    def _normalize_result(self, result: dict) -> dict:
        return {
            "overall_score": min(max(result.get("overall_score", 0), 0), 100),
            "grade": result.get("grade", "F"),
            "scores": {
                "test_coverage": min(max(result.get("scores", {}).get("test_coverage", 0), 0), 100),
                "dependency_health": min(max(result.get("scores", {}).get("dependency_health", 0), 0), 100),
                "code_cleanliness": min(max(result.get("scores", {}).get("code_cleanliness", 0), 0), 100),
                "architecture": min(max(result.get("scores", {}).get("architecture", 0), 0), 100),
                "security": min(max(result.get("scores", {}).get("security", 0), 0), 100),
            },
            "summary": result.get("summary", "Analysis completed"),
            "issues": result.get("issues", []),
            "recommendations": result.get("recommendations", {}),
            "detailed_scores": result.get("detailed_scores", {}),
        }

    def _mock_analysis(self, code: str, language: str) -> dict:
        lines = code.split("\n")
        line_count = len(lines)

        issues = []
        if "eval(" in code:
            issues.append({
                "category": "security",
                "severity": "critical",
                "line_number": next((i + 1 for i, l in enumerate(lines) if "eval(" in l), None),
                "message": "Use of eval() is dangerous and can lead to code injection attacks",
                "suggestion": "Avoid using eval(). Use safer alternatives like ast.literal_eval() for Python",
                "rule_id": "SEC001",
            })

        if "password" in code.lower() and "=" in code:
            issues.append({
                "category": "security",
                "severity": "high",
                "line_number": None,
                "message": "Potential hardcoded password detected",
                "suggestion": "Use environment variables or a secrets manager",
                "rule_id": "SEC002",
            })

        if "SELECT" in code.upper() and "+" in code:
            issues.append({
                "category": "security",
                "severity": "critical",
                "line_number": None,
                "message": "Potential SQL injection vulnerability",
                "suggestion": "Use parameterized queries or an ORM",
                "rule_id": "SEC003",
            })

        score = max(20, 100 - (len(issues) * 15))
        if line_count < 10:
            score = min(score + 10, 100)

        return {
            "overall_score": score,
            "grade": self._calculate_grade(score),
            "scores": {
                "test_coverage": max(0, score - 20),
                "dependency_health": min(100, score + 10),
                "code_cleanliness": score,
                "architecture": max(0, score - 5),
                "security": max(0, score - (len(issues) * 10)),
            },
            "summary": f"Analyzed {language} code ({line_count} lines). Found {len(issues)} issues.",
            "issues": issues,
            "recommendations": {
                "add_tests": "Consider adding unit tests",
                "improve_docs": "Add documentation and comments",
                "security_review": "Review security practices" if issues else "Good security practices",
            },
            "detailed_scores": {},
        }

    def _calculate_grade(self, score: int) -> str:
        if score >= 97:
            return "A+"
        elif score >= 93:
            return "A"
        elif score >= 90:
            return "A-"
        elif score >= 87:
            return "B+"
        elif score >= 83:
            return "B"
        elif score >= 80:
            return "B-"
        elif score >= 77:
            return "C+"
        elif score >= 73:
            return "C"
        elif score >= 70:
            return "C-"
        elif score >= 67:
            return "D+"
        elif score >= 60:
            return "D"
        else:
            return "F"
