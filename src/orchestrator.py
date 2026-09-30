from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class CouncilMemberResult:
    member: str
    role: str
    opinion: str
    recommendation: str
    risks: List[str]
    opportunities: List[str]
    confidence: float
    evidence_summary: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CouncilDecision:
    decision_id: str
    timestamp: str
    topic: str
    decision_type: str
    constraints: List[str]
    final_recommendation: str
    confidence_score: float
    rationale: str
    risks: List[str]
    opportunities: List[str]
    lower_division: Dict[str, Dict[str, Any]]
    upper_division: Dict[str, Dict[str, Any]]
    leader: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
