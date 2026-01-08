from pydantic import BaseModel
from typing import List, Optional, Literal

Severity = Literal["P0", "P1", "P2"]
Category = Literal["correctness", "security", "performance", "maintainability"]

class Finding(BaseModel):
    severity: Severity
    category: Category
    file: Optional[str] = None
    line_range: Optional[str] = None
    title: str
    description: str
    recommendation: str
    confidence: float  # 0.0 - 1.0

class AgentFindings(BaseModel):
    findings: List[Finding]


class TriageResult(BaseModel):
    summary: str
    risk: Literal["low", "medium", "high"]
    focus_files: List[str]
    questions_for_author: List[str] = []