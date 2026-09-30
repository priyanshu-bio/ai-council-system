from __future__ import annotations

import json
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None

ROOT_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT_DIR / "config" / "council_config.json"
PROMPT_DIR = ROOT_DIR / "config" / "prompts"
RULES_PATH = ROOT_DIR / "config" / "decision_rules.json"
OUTPUT_DIR = ROOT_DIR / "outputs" / "decisions"


class AICouncil:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.config = self._load_json(CONFIG_PATH)
        self.prompt_library = {
            "lower_division": self._load_json(PROMPT_DIR / "lower_division_prompts.json"),
            "upper_division": self._load_json(PROMPT_DIR / "upper_division_prompts.json"),
            "leader": self._load_json(PROMPT_DIR / "leader_prompts.json"),
        }
        self.rules = self._load_json(RULES_PATH)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        self.lower_division = [
            "risk_analyst",
            "product_strategist",
            "research_analyst",
            "technical_architect",
            "ethics_reviewer",
            "ux_analyst",
            "finance_analyst",
            "ops_analyst",
        ]
        self.upper_division = ["chief_reviewer", "strategy_lead"]

    @staticmethod
    def _load_json(path: Path) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _llm_response(self, system_prompt: str, user_prompt: str) -> str | None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or OpenAI is None:
            return None

        client = OpenAI(api_key=api_key)
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self.config["council"].get("temperature", 0.7),
                max_tokens=self.config["council"].get("max_tokens", 2000),
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return None

    def _fallback_role_response(self, member_name: str, topic: str, context: str, constraints: List[str], decision_type: str) -> Dict[str, Any]:
        profiles = {
            "risk_analyst": {
                "opinion": "Proceed only with a staged rollout and explicit risk controls.",
                "risks": [
                    "Unclear operational failure points",
                    "Insufficient rollback plan",
                    "Regulatory exposure if controls are weak",
                ],
                "recommendation": "Mitigate first, then iterate with a controlled pilot.",
                "confidence": 0.8,
            },
            "product_strategist": {
                "opinion": "The initiative has real value if the user problem is clearly framed and the UX is simple.",
                "risks": [
                    "Customer confusion",
                    "Poor differentiation",
                    "Weak adoption without a strong value proposition",
                ],
                "recommendation": "Create a demand-driven pilot with a clear value narrative.",
                "confidence": 0.82,
            },
            "research_analyst": {
                "opinion": "Evidence is promising but insufficient for a full commitment without more validation.",
                "risks": [
                    "Assumption-heavy decision-making",
                    "Unverified user demand",
                    "Misreading the signal from small sample sizes",
                ],
                "recommendation": "Test hypotheses with quick, measurable evidence gathering.",
                "confidence": 0.74,
            },
            "technical_architect": {
                "opinion": "Implementation is feasible but should be phased to avoid architecture debt.",
                "risks": [
                    "Integration complexity",
                    "Scalability bottlenecks",
                    "Long-term maintenance burden",
                ],
                "recommendation": "Use simple architecture first and expand only after validation.",
                "confidence": 0.84,
            },
            "ethics_reviewer": {
                "opinion": "The concept can be ethical if privacy, consent, and fairness are treated as core design constraints.",
                "risks": [
                    "User trust erosion",
                    "Consent ambiguity",
                    "Unintended harm to vulnerable populations",
                ],
                "recommendation": "Build trust through explicit consent and transparent design.",
                "confidence": 0.79,
            },
            "ux_analyst": {
                "opinion": "User adoption depends on clarity, simplicity, and trust.",
                "risks": [
                    "Cognitive overload",
                    "Accessibility gaps",
                    "High friction in core workflow",
                ],
                "recommendation": "Reduce the surface area and validate UX before scale.",
                "confidence": 0.8,
            },
            "finance_analyst": {
                "opinion": "The idea could create value if costs remain lean and ROI is measured early.",
                "risks": [
                    "Overbudget execution",
                    "Weak return in early phases",
                    "Cost drift from feature creep",
                ],
                "recommendation": "Set a limited pilot budget and define exit metrics early.",
                "confidence": 0.76,
            },
            "ops_analyst": {
                "opinion": "The plan can work if execution is disciplined and dependencies are managed carefully.",
                "risks": [
                    "Team overload",
                    "Timeline slippage",
                    "Operational bottlenecks",
                ],
                "recommendation": "Keep rollout narrow, measurable, and operationally realistic.",
                "confidence": 0.78,
            },
        }

        profile = profiles.get(member_name, {
            "opinion": "The proposal needs clearer validation before broad commitment.",
            "risks": ["Insufficient evidence"],
            "recommendation": "Collect more evidence before proceeding.",
            "confidence": 0.7,
        })

        return {
            "member": member_name,
            "role": member_name.replace("_", " ").title(),
            "topic": topic,
            "decision_type": decision_type,
            "context": context,
            "constraints": constraints,
            "opinion": profile["opinion"],
            "recommendation": profile["recommendation"],
            "risks": profile["risks"],
            "opportunities": [
                "Improved user trust if the model is carefully designed",
                "Clearer strategic positioning with early validation",
                "Better operational learning through a controlled pilot",
            ],
            "confidence": profile["confidence"],
            "evidence_summary": f"Decision is evaluated under {decision_type} conditions with context: {context[:180]}.",
        }

    def _call_lower_member(self, member_name: str, topic: str, context: str, constraints: List[str], decision_type: str) -> Dict[str, Any]:
        prompt = (
            f"Topic: {topic}\n\nContext: {context}\n\nConstraints: {constraints}\n\n"
            f"Decision Type: {decision_type}\n\n"
            "Provide: (1) opinion, (2) recommendation, (3) primary risks, (4) opportunities, (5) confidence score."
        )
        system_prompt = self.prompt_library["lower_division"].get(member_name, {}).get("system_prompt", "You are a strategic decision advisor.")
        llm_output = self._llm_response(system_prompt, prompt)

        if llm_output:
            return {
                "member": member_name,
                "role": self.prompt_library["lower_division"].get(member_name, {}).get("name", member_name.replace("_", " ").title()),
                "opinion": llm_output[:500],
                "recommendation": "Use AI output when available.",
                "risks": ["Review the LLM reasoning for unsupported assumptions."],
                "opportunities": ["Fast expert-style synthesis"],
                "confidence": 0.82,
                "evidence_summary": llm_output[:300],
            }

        return self._fallback_role_response(member_name, topic, context, constraints, decision_type)

    def _call_upper_member(self, member_name: str, lower_outputs: List[Dict[str, Any]], topic: str, context: str) -> Dict[str, Any]:
        combined = json.dumps(lower_outputs, indent=2)
        prompt = (
            f"Topic: {topic}\n\nContext: {context}\n\nLower Division Results:\n{combined}\n\n"
            "Audit the inputs for contradictions, missing assumptions, and most credible path forward."
        )
        system_prompt = self.prompt_library["upper_division"].get(member_name, {}).get("system_prompt", "You are a senior reviewer.")
        llm_output = self._llm_response(system_prompt, prompt)

        if llm_output:
            return {
                "member": member_name,
                "assessment": llm_output[:600],
                "quality_score": 0.84,
                "priority_ranking": ["Pilot first", "Validate assumptions", "Scale only after proof"],
            }

        average_confidence = sum(item.get("confidence", 0.7) for item in lower_outputs) / max(len(lower_outputs), 1)
        if member_name == "chief_reviewer":
            return {
                "member": member_name,
                "assessment": "The council varies in confidence, but the decision appears viable if responsibilities and guardrails are explicit.",
                "quality_score": round(min(0.96, max(0.65, average_confidence + 0.08)), 2),
                "priority_ranking": ["Evaluate risk controls", "Confirm user value", "Create a measured pilot"],
            }

        return {
            "member": member_name,
            "assessment": "The proposal should proceed with controlled analysis rather than broad commitment.",
            "quality_score": round(min(0.97, max(0.7, average_confidence + 0.06)), 2),
            "priority_ranking": ["Strongest value path", "Moderate risk path", "Avoid high-risk expansion"],
        }

    def _call_leader(self, topic: str, context: str, lower_outputs: List[Dict[str, Any]], upper_outputs: List[Dict[str, Any]], constraints: List[str]) -> Dict[str, Any]:
        prompt = (
            f"Topic: {topic}\n\nContext: {context}\n\nConstraints: {constraints}\n\n"
            f"Lower Division Outputs: {json.dumps(lower_outputs, indent=2)}\n\n"
            f"Upper Division Review: {json.dumps(upper_outputs, indent=2)}\n\n"
            "Deliver a final recommendation with rationale, conflict summary, key risks, and next steps."
        )
        system_prompt = self.prompt_library["leader"].get("council_leader", {}).get("system_prompt", "You are the final decision leader.")
        llm_output = self._llm_response(system_prompt, prompt)

        if llm_output:
            return {
                "member": "council_leader",
                "final_decision": llm_output[:500],
                "rationale": llm_output[500:1000] if len(llm_output) > 500 else "AI rationale generated for this decision.",
                "resolved_conflicts": ["Risk controls should be explicit before scale.", "Value must be proven through measurable outcomes."],
                "next_steps": ["Run a small pilot", "Measure outcomes", "Review with leadership"],
                "confidence": 0.86,
            }

        avg_lower = sum(item.get("confidence", 0.7) for item in lower_outputs) / max(len(lower_outputs), 1)
        avg_upper = sum(item.get("quality_score", 0.75) for item in upper_outputs) / max(len(upper_outputs), 1)

        final_confidence = max(0.5, min(0.94, (avg_lower * 0.6 + avg_upper * 0.4)))
        return {
            "member": "council_leader",
            "final_decision": "Proceed with a controlled pilot rather than a full launch. Validate value, de-risk operations, and commit only after strong evidence appears.",
            "rationale": "The lower division shows meaningful upside but also marked uncertainty. Upper review confirms that the initiative is viable when phased and constrained by explicit risk controls.",
            "resolved_conflicts": [
                "Balance ambition with realistic execution timing.",
                "Protect user trust and safety while validating business value.",
            ],
            "next_steps": [
                "Define success metrics and milestones.",
                "Run a narrow pilot with clear rollback criteria.",
                "Review risk, ethics, and operating readiness before expansion.",
            ],
            "confidence": round(final_confidence, 2),
        }

    def decide(self, topic: str, context: str, constraints: List[str] | None = None, decision_type: str = "strategic") -> Dict[str, Any]:
        constraints = constraints or ["No broad rollout without validation", "Align with stakeholder priorities"]

        with ThreadPoolExecutor(max_workers=len(self.lower_division)) as executor:
            futures = [
                executor.submit(self._call_lower_member, member_name, topic, context, constraints, decision_type)
                for member_name in self.lower_division
            ]
            lower_outputs = [future.result() for future in futures]

        upper_outputs = [
            self._call_upper_member(member_name, lower_outputs, topic, context)
            for member_name in self.upper_division
        ]

        leader_output = self._call_leader(topic, context, lower_outputs, upper_outputs, constraints)

        result = {
            "decision_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "topic": topic,
            "decision_type": decision_type,
            "constraints": constraints,
            "final_recommendation": leader_output["final_decision"],
            "confidence_score": leader_output.get("confidence", 0.8),
            "rationale": leader_output.get("rationale", "The council recommends a measured, evidence-driven decision."),
            "risks": sorted({risk for member in lower_outputs for risk in member.get("risks", [])})[:8],
            "opportunities": sorted({opp for member in lower_outputs for opp in member.get("opportunities", [])})[:8],
            "lower_division": {item["member"]: item for item in lower_outputs},
            "upper_division": {item["member"]: item for item in upper_outputs},
            "leader": leader_output,
            "metadata": {
                "lower_division_count": len(self.lower_division),
                "upper_division_count": len(self.upper_division),
                "decision_rule_threshold": self.rules.get("confidence_threshold", 0.7),
                "escalation_required": bool(leader_output.get("confidence", 0.0) < self.rules.get("confidence_threshold", 0.7)),
            },
        }

        self._save_result(result)
        return result

    def _save_result(self, result: Dict[str, Any]) -> None:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        file_path = OUTPUT_DIR / f"decision_{timestamp}.json"
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(result, file, indent=2)


def _demo() -> None:
    council = AICouncil()
    result = council.decide(
        topic="Should we launch a new feature in a six-week window?",
        context="We have product demand, modest engineering capacity, and a clear customer problem but limited budget and execution certainty.",
        constraints=["Budget under $200k", "Ship within 6 weeks", "Keep operational risk moderate"],
        decision_type="strategic",
    )
    print(json.dumps({
        "topic": result["topic"],
        "final_recommendation": result["final_recommendation"],
        "confidence_score": result["confidence_score"],
        "leader": result["leader"],
    }, indent=2))


if __name__ == "__main__":
    _demo()
