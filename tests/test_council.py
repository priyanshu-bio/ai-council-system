from __future__ import annotations

import json

from src.council import AICouncil


if __name__ == "__main__":
    council = AICouncil(model="gpt-4o-mini")
    decision = council.decide(
        topic="Should our startup launch a premium AI assistant feature?",
        context=(
            "We have a strong customer signal, small engineering team, and moderate product-market fit. "
            "The launch could increase engagement but may also distract the team and increase support risk."
        ),
        constraints=[
            "Launch within 90 days",
            "Budget under $150k",
            "Keep the launch isolated to a pilot cohort",
        ],
        decision_type="strategic",
    )

    print(json.dumps({
        "topic": decision["topic"],
        "final_recommendation": decision["final_recommendation"],
        "confidence_score": decision["confidence_score"],
        "leader": decision["leader"],
        "lower_division_count": len(decision["lower_division"]),
        "upper_division_count": len(decision["upper_division"]),
    }, indent=2))
