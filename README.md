# Enterprise SaaS Sales Playbook

A comprehensive Python-based sales methodology and discovery framework for complex fintech deals.

## Features

- **Discovery Framework**: Stage-based discovery questions for financial services sales
- **Qualification Module**: BANT and MEDDIC scoring frameworks
- **Objection Handler**: 20+ common objections with response templates
- **ROI Calculator**: Calculate ROI, TCO, and payback period
- **Report Generator**: Export findings to Excel

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Get discovery questions for a sales stage
python src/main.py discovery --stage initial

# Qualify a prospect
python src/main.py qualify --company "Acme Bank" --budget 500000 --authority cfo --need high --timeline q2

# Handle an objection
python src/main.py objection --category price

# Calculate ROI
python src/main.py roi --current-cost 500000 --savings 0.25 --implementation 50000 --annual-license 100000

# Export discovery report
python src/main.py export --type discovery --output report.xlsx
```

## Project Structure

```
sales-playbook/
├── README.md
├── requirements.txt
├── config/
│   ├── config.json
│   └── objection_responses.json
├── src/
│   ├── main.py
│   ├── agent.py                   # Reusable agent configuration
│   ├── discovery/
│   │   ├── question_framework.py
│   │   └── qualification.py
│   ├── objections/
│   │   └── handler.py
│   ├── roi/
│   │   └── calculator.py
│   └── export/
│       └── report_generator.py
├── docs/
│   ├── METHODOLOGY.md
│   └── agent.md
└── output/
```

## Qualification Frameworks

### BANT Scoring
- **Budget**: Does the prospect have budget allocated?
- **Authority**: Are we talking to the decision maker?
- **Need**: How urgent is the business need?
- **Timeline**: When do they need to implement?

### MEDDIC Scoring
- **Metrics**: What metrics will measure success?
- **Economic Buyer**: Who controls the budget?
- **Decision Criteria**: What are their evaluation criteria?
- **Decision Process**: What is the approval process?
- **Identify Pain**: What problems are they solving?
- **Champion**: Who is advocating internally?

## Requirements

- Python 3.8+
- click
- openpyxl
- pandas

## License

MIT License
