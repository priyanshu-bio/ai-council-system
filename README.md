# AI Council System - Hierarchical Multi-Agent Decision Framework

A sophisticated 11-member hierarchical AI council system designed for complex decision-making, strategic planning, and comprehensive analysis.

## Architecture Overview

```
                          ┌─────────────────┐
                          │     LEADER      │
                          │ (Final Decision)│
                          └────────┬────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
            ┌───────▼────────┐           ┌───────▼────────┐
            │  UPPER DIV: 1  │           │  UPPER DIV: 2  │
            │  Chief Decision│           │  Strategic     │
            │  Reviewer      │           │  Integration   │
            └───────┬────────┘           └───────┬────────┘
                    │                             │
        ┌───────────┴──────────────────────────────┴───────────┐
        │                                                      │
   ┌────▼──┐  ┌────▼──┐  ┌────▼──┐  ┌────▼──┐  ┌────▼──┐  ┌────▼──┐  ┌────▼──┐  ┌────▼──┐
   │LD: 1  │  │LD: 2  │  │LD: 3  │  │LD: 4  │  │LD: 5  │  │LD: 6  │  │LD: 7  │  │LD: 8  │
   │ Risk  │  │Product│  │Research│ │Tech   │  │Ethics │  │ UX/CX │  │Finance│  │Ops    │
   │Analyst│  │Strat  │  │Analyst │  │Arch   │  │Review │  │Analyst│  │Analyst│  │Analyst│
   └───────┘  └───────┘  └───────┘  └───────┘  └───────┘  └───────┘  └───────┘  └───────┘

        LOWER DIVISION (8 Specialized Members)
```

## System Features

✅ **3-Tier Hierarchy**: Lower division → Upper division → Leader  
✅ **8 Specialized Lower-Division Members**: Different expertise verticals  
✅ **2 Senior Reviewers**: Cross-domain analysis and conflict resolution  
✅ **1 Final Decision Leader**: Strategic synthesis and final recommendation  
✅ **Parallel Processing**: All agents work independently for diversity  
✅ **Conflict Detection**: Identifies disagreements and flags concerns  
✅ **Confidence Scoring**: Weighted recommendations based on expertise  
✅ **Escalation Rules**: Automatic escalation for high-risk decisions  
✅ **Audit Trail**: Full decision history and rationale tracking  

## Lower Division Members

| Member | Role | Focus Area |
|--------|------|-----------|
| **LD-1** | Risk Analyst | Security, failure modes, risk mitigation |
| **LD-2** | Product Strategist | Market fit, user needs, competitive advantage |
| **LD-3** | Research Analyst | Data validation, research gaps, evidence |
| **LD-4** | Technical Architect | Feasibility, scalability, technical debt |
| **LD-5** | Ethics & Compliance | Legal, ethical, regulatory, fairness |
| **LD-6** | UX/Customer Experience | User impact, usability, adoption |
| **LD-7** | Finance & ROI Analyst | Cost-benefit, ROI, financial sustainability |
| **LD-8** | Operations & Execution | Implementation, timelines, resource needs |

## Upper Division Members

| Member | Role | Focus Area |
|--------|------|-----------|
| **UD-1** | Chief Decision Reviewer | Quality assurance, logical consistency, completeness |
| **UD-2** | Strategic Integration Lead | Cross-domain synthesis, priority ranking, strategic fit |

## Leader

| Member | Role | Focus Area |
|--------|------|-----------|
| **L** | Council Leader | Final decision, conflict resolution, strategic direction |

## How It Works

### Phase 1: Lower Division Analysis (Parallel)
Each of the 8 members analyzes the input independently from their expertise perspective.

### Phase 2: Upper Division Review (Sequential)
Both upper-division members review all lower-division outputs and:
- Identify conflicts and contradictions
- Flag gaps in analysis
- Rank recommendations by quality and strategic fit
- Prepare synthesis for leader

### Phase 3: Leadership Decision (Final)
The leader:
- Reviews all outputs
- Resolves conflicts using strategic judgment
- Makes final decision
- Provides unified rationale and next steps

## Project Structure

```
ai-council-system/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── config/
│   ├── council_config.json           # Council structure and settings
│   ├── prompts/
│   │   ├── lower_division_prompts.json    # 8 member prompts
│   │   ├── upper_division_prompts.json    # 2 member prompts
│   │   └── leader_prompts.json            # Leader prompt
│   └── decision_rules.json            # Escalation and decision rules
├── src/
│   ├── __init__.py
│   ├── council.py                     # Main Council orchestrator
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py              # Base agent class
│   │   ├── lower_division/
│   │   │   ├── __init__.py
│   │   │   ├── risk_analyst.py
│   │   │   ├── product_strategist.py
│   │   │   ├── research_analyst.py
│   │   │   ├── technical_architect.py
│   │   │   ├── ethics_reviewer.py
│   │   │   ├── ux_analyst.py
│   │   │   ├── finance_analyst.py
│   │   │   └── ops_analyst.py
│   │   ├── upper_division/
│   │   │   ├── __init__.py
│   │   │   ├── chief_reviewer.py
│   │   │   └── strategy_lead.py
│   │   └── leader/
│   │       ├── __init__.py
│   │       └── council_leader.py
│   ├── orchestrator.py                # Workflow orchestration
│   ├── synthesizer.py                 # Output synthesis
│   └── utils/
│       ├── __init__.py
│       ├── logger.py                  # Logging and audit
│       ├── validator.py               # Output validation
│       └── metrics.py                 # Confidence and scoring
├── examples/
│   ├── basic_council.py               # Simple usage example
│   ├── complex_decision.py            # Complex scenario
│   └── api_server.py                  # REST API server
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_orchestrator.py
│   └── test_council.py
└── outputs/
    └── decisions/                     # Decision logs and audit trail
```

## Quick Start

### 1. Installation

```bash
git clone https://github.com/priyanshu-bio/ai-council-system.git
cd ai-council-system
pip install -r requirements.txt
```

### 2. Set up API Keys

```bash
export OPENAI_API_KEY="your-api-key"
export ANTHROPIC_API_KEY="your-api-key"  # Optional
```

### 3. Run a Simple Example

```bash
python examples/basic_council.py
```

### 4. Use the Council

```python
from src.council import AICouncil

# Initialize council
council = AICouncil(model="gpt-4o-mini")

# Present a decision
result = council.decide(
    topic="Should we launch a new feature?",
    context="We have market opportunity but limited engineering resources.",
    constraints=["6-month timeline", "$500k budget", "2-person team"],
    decision_type="strategic"
)

# View results
print(result.final_recommendation)
print(result.risks)
print(result.next_steps)
print(result.confidence_score)
```

## Output Format

The system generates structured JSON output:

```json
{
  "decision_id": "uuid",
  "timestamp": "2026-09-30T14:30:00Z",
  "topic": "Feature Launch Decision",
  "final_recommendation": "Proceed with limited beta...",
  "confidence_score": 0.82,
  "lower_division": {
    "risk_analyst": { "opinion": "...", "confidence": 0.75, "risks": [...] },
    "product_strategist": { "opinion": "...", "confidence": 0.88, "opportunities": [...] },
    ...
  },
  "upper_division": {
    "chief_reviewer": { "assessment": "...", "quality_score": 0.85 },
    "strategy_lead": { "synthesis": "...", "priority_ranking": [...] }
  },
  "leader": {
    "final_decision": "...",
    "rationale": "...",
    "resolved_conflicts": [...],
    "next_steps": [...]
  },
  "audit_trail": {
    "phases": ["lower_division", "upper_division", "leadership"],
    "duration_seconds": 45,
    "tokens_used": 12500
  }
}
```

## Configuration

Edit `config/council_config.json` to customize:

```json
{
  "council": {
    "name": "Strategic Decision Council",
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 2000
  },
  "decision_rules": {
    "confidence_threshold": 0.70,
    "conflict_threshold": 0.40,
    "escalation_on_conflict": true,
    "require_unanimity": false
  },
  "phases": {
    "lower_division_parallel": true,
    "upper_division_sequential": true,
    "leader_final": true
  },
  "timeout_seconds": 120
}
```

## API Usage

Start the REST API server:

```bash
python examples/api_server.py
```

Then POST to the council:

```bash
curl -X POST http://localhost:8000/decide \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Launch new product?",
    "context": "Market analysis shows demand...",
    "constraints": ["6-month timeline"],
    "decision_type": "strategic"
  }'
```

## Advanced Features

### 1. Custom Agent Roles

Add a new lower-division member by creating a new agent class:

```python
# src/agents/lower_division/custom_analyst.py
from src.agents.base_agent import BaseAgent

class CustomAnalyst(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Custom Analyst",
            role="Your custom role",
            expertise="Your expertise areas"
        )
    
    def analyze(self, topic, context):
        # Your custom analysis logic
        pass
```

### 2. Weighted Voting

Configure weighted voting in `config/decision_rules.json`:

```json
{
  "voting_weights": {
    "lower_division": 0.4,
    "upper_division": 0.35,
    "leader": 0.25
  },
  "member_weights": {
    "risk_analyst": 1.2,
    "product_strategist": 1.0,
    ...
  }
}
```

### 3. Escalation Rules

Automatically escalate high-risk or high-conflict decisions:

```python
council.escalate_to_human_review(
    reason="Confidence below threshold",
    decision_id="uuid",
    recommended_stakeholders=["CEO", "Legal"]
)
```

## Monitoring & Metrics

View decision metrics and council performance:

```python
metrics = council.get_metrics()
print(f"Avg confidence: {metrics['avg_confidence']}")
print(f"Total decisions: {metrics['total_decisions']}")
print(f"Escalations: {metrics['escalations']}")
print(f"Avg processing time: {metrics['avg_time']}s")
```

## Decision Types Supported

- **Strategic**: Long-term direction and major initiatives
- **Operational**: Day-to-day execution and process decisions
- **Risk**: High-stakes, high-uncertainty scenarios
- **Innovation**: New product or service launches
- **Resource Allocation**: Budget, team, or priority decisions
- **Ethical**: Compliance, fairness, and policy decisions
- **Technical**: Architecture and technology choices
- **Custom**: Any decision you define

## Use Cases

✅ Product launch decisions  
✅ Strategic partnerships  
✅ Budget allocation  
✅ Risk assessments  
✅ Feature prioritization  
✅ Vendor selection  
✅ Team restructuring  
✅ Technology stack choices  
✅ Ethical dilemmas  
✅ Crisis management  

## Performance & Optimization

- **Parallel Processing**: Lower division runs in parallel for speed
- **Token Optimization**: Intelligent prompt compression
- **Caching**: Responses cached to reduce API calls
- **Async Execution**: Non-blocking workflow
- **Batch Processing**: Handle multiple decisions efficiently

Typical council decision time: **30-60 seconds**  
Typical token usage per decision: **8,000-15,000 tokens**

## Testing

Run the full test suite:

```bash
pytest tests/ -v
```

Individual test categories:

```bash
pytest tests/test_agents.py -v              # Test individual agents
pytest tests/test_orchestrator.py -v        # Test workflow
pytest tests/test_council.py -v             # Integration tests
```

## Contributing

Contributions welcome! Areas for enhancement:

- [ ] Additional agent types
- [ ] Alternative LLM providers
- [ ] Advanced conflict resolution algorithms
- [ ] Real-time decision monitoring UI
- [ ] Integration with business intelligence tools
- [ ] Custom decision templates

## License

MIT License - See LICENSE file

## Support

For issues, questions, or suggestions:
- Open a GitHub issue
- Check existing documentation
- Review example implementations

## Roadmap

- [ ] Web dashboard for decision tracking
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Custom prompt templates
- [ ] Integration with Slack/Teams
- [ ] Mobile app support
- [ ] Enterprise deployment guide

---

**Built with ❤️ for complex decision-making**
