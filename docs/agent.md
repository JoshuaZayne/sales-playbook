# Sales Playbook Agent Documentation

## Overview

The Sales Playbook Agent (`src/agent.py`) provides a reusable interface for automating sales playbook operations. It can be integrated with AI assistants, automation tools, or custom applications.

## Agent Capabilities

| Capability | Description |
|------------|-------------|
| `discovery_questions` | Generate stage-appropriate discovery questions |
| `prospect_qualification` | Score prospects using BANT/MEDDIC frameworks |
| `objection_handling` | Retrieve responses for common objections |
| `roi_calculation` | Calculate ROI, TCO, and payback metrics |
| `report_generation` | Export findings to Excel reports |

## Quick Start

```python
from agent import SalesPlaybookAgent, create_agent

# Create an agent instance
agent = create_agent()

# Set the current prospect
agent.set_prospect("Acme Bank", {"industry": "banking", "size": "regional"})

# Run discovery
discovery = agent.run_discovery("Acme Bank", "initial")
print(discovery["questions"])

# Qualify the prospect
qualification = agent.qualify_prospect({
    "budget": 250000,
    "authority": "vp",
    "need": "high",
    "timeline": "q2"
})
print(f"Score: {qualification['bant_score']}, Grade: {qualification['bant_grade']}")

# Handle an objection
response = agent.handle_objection("price", "They said we're 20% more expensive")
print(response["responses"])

# Calculate ROI
roi = agent.calculate_roi({
    "current_cost": 500000,
    "savings_rate": 0.30,
    "implementation_cost": 50000,
    "annual_license": 100000
})
print(f"ROI: {roi['roi_percent']}%")

# Generate report
report_path = agent.generate_report("output/acme_report.xlsx")
```

## Agent Context

The agent maintains context throughout a sales engagement:

```python
context = agent.get_context()
# Returns:
# {
#     "current_prospect": {"name": "Acme Bank", "metadata": {...}},
#     "discovery_stage": "initial",
#     "qualification_scores": {"bant": {...}},
#     "objections_handled": ["price"],
#     "roi_calculated": True
# }

# Reset for new prospect
agent.reset_context()
```

## Integration with Claude Code

The agent can be used with Claude Code or other AI assistants:

```python
# In a Claude Code hook or automation script
from agent import AGENT_METADATA, create_agent

# Check agent capabilities
print(AGENT_METADATA["capabilities"])

# Create and use the agent
agent = create_agent()
result = agent.run_discovery("Prospect Corp", "technical")
```

## Agent Metadata

The `AGENT_METADATA` constant provides information for automation tool discovery:

```python
AGENT_METADATA = {
    "name": "sales-playbook-agent",
    "version": "1.0.0",
    "description": "Automates sales methodology and discovery for fintech deals",
    "capabilities": [
        "discovery_questions",
        "prospect_qualification",
        "objection_handling",
        "roi_calculation",
        "report_generation"
    ],
    "config_schema": {
        "type": "object",
        "properties": {
            "config_path": {"type": "string", "description": "Path to config.json"}
        }
    }
}
```

## Custom Configuration

The agent can be initialized with a custom configuration path:

```python
agent = SalesPlaybookAgent(config_path="/path/to/custom/config.json")
```

## Error Handling

```python
try:
    result = agent.run_discovery("Prospect", "invalid_stage")
except ValueError as e:
    print(f"Invalid stage: {e}")
```

## Extending the Agent

To add new capabilities:

1. Add method to `SalesPlaybookAgent` class
2. Update `AGENT_METADATA["capabilities"]`
3. Document in this file

Example:

```python
def custom_analysis(self, data: Dict) -> Dict:
    """Custom analysis method."""
    # Implementation
    return {"result": "..."}
```
