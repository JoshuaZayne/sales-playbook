"""
Enterprise SaaS Sales Playbook - CLI Interface
===============================================

Command-line interface for the sales playbook tools.
"""

import click
import json
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from discovery.question_framework import QuestionFramework
from discovery.qualification import QualificationEngine
from objections.handler import ObjectionHandler
from roi.calculator import ROICalculator
from export.report_generator import ReportGenerator


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Enterprise SaaS Sales Playbook - Tools for complex fintech deals."""
    pass


@cli.command()
@click.option('--stage', '-s', type=click.Choice(['initial', 'technical', 'business', 'decision']),
              required=True, help='Discovery stage')
@click.option('--vertical', '-v', type=str, default=None, help='Industry vertical filter')
def discovery(stage: str, vertical: str):
    """Get discovery questions for a sales stage."""
    framework = QuestionFramework()
    questions = framework.get_questions_by_stage(stage)

    click.echo(f"\n{'='*60}")
    click.echo(f"DISCOVERY QUESTIONS - {stage.upper()} STAGE")
    click.echo(f"{'='*60}\n")

    for i, q in enumerate(questions, 1):
        click.echo(f"{i}. {q['question']}")
        click.echo(f"   Purpose: {q['purpose']}")
        click.echo(f"   Follow-up: {q['follow_up']}")
        click.echo()

    click.echo(f"Total questions: {len(questions)}")


@cli.command()
@click.option('--company', '-c', type=str, required=True, help='Company name')
@click.option('--budget', '-b', type=int, default=0, help='Budget amount in dollars')
@click.option('--authority', '-a', type=click.Choice(['cfo', 'cto', 'vp', 'director', 'manager', 'unknown']),
              default='unknown', help='Decision maker level')
@click.option('--need', '-n', type=click.Choice(['critical', 'high', 'medium', 'low']),
              default='medium', help='Business need level')
@click.option('--timeline', '-t', type=click.Choice(['q1', 'q2', 'q3', 'q4', 'next_year', 'unknown']),
              default='unknown', help='Implementation timeline')
def qualify(company: str, budget: int, authority: str, need: str, timeline: str):
    """Qualify a prospect using BANT framework."""
    engine = QualificationEngine()

    result = engine.score_bant(
        budget=budget,
        authority=authority,
        need=need,
        timeline=timeline
    )

    click.echo(f"\n{'='*60}")
    click.echo(f"QUALIFICATION SCORECARD - {company}")
    click.echo(f"{'='*60}\n")

    click.echo("BANT Breakdown:")
    click.echo(f"  Budget:    {result['breakdown']['budget']:>3}/25  ({budget:,} allocated)")
    click.echo(f"  Authority: {result['breakdown']['authority']:>3}/25  ({authority})")
    click.echo(f"  Need:      {result['breakdown']['need']:>3}/25  ({need})")
    click.echo(f"  Timeline:  {result['breakdown']['timeline']:>3}/25  ({timeline})")
    click.echo(f"  {'-'*30}")
    click.echo(f"  TOTAL:     {result['score']:>3}/100")
    click.echo()
    click.echo(f"Grade: {result['grade']}")
    click.echo(f"Recommendation: {result['recommendation']}")


@cli.command()
@click.option('--category', '-c', type=click.Choice(['price', 'competitor', 'timing', 'integration',
                                                      'security', 'authority', 'need', 'internal', 'risk']),
              required=True, help='Objection category')
@click.option('--list-all', '-l', is_flag=True, help='List all objections in category')
def objection(category: str, list_all: bool):
    """Get responses for common sales objections."""
    handler = ObjectionHandler()
    responses = handler.get_responses_by_category(category)

    click.echo(f"\n{'='*60}")
    click.echo(f"OBJECTION RESPONSES - {category.upper()}")
    click.echo(f"{'='*60}\n")

    for i, obj in enumerate(responses, 1):
        click.echo(f"Objection {i}:")
        click.echo(f"  \"{obj['objection']}\"")
        click.echo()
        click.echo(f"Response:")
        click.echo(f"  {obj['response']}")
        click.echo()
        click.echo(f"Proof Points:")
        for point in obj['proof_points']:
            click.echo(f"  - {point}")
        click.echo(f"\n{'-'*60}\n")


@cli.command()
@click.option('--current-cost', '-c', type=float, required=True, help='Current annual cost in dollars')
@click.option('--savings', '-s', type=float, required=True, help='Expected efficiency gain (0.0-1.0)')
@click.option('--implementation', '-i', type=float, default=0, help='Implementation cost in dollars')
@click.option('--annual-license', '-l', type=float, default=0, help='Annual license cost in dollars')
@click.option('--years', '-y', type=int, default=3, help='Analysis period in years')
@click.option('--scenario', type=click.Choice(['conservative', 'moderate', 'aggressive']),
              default='moderate', help='ROI scenario')
def roi(current_cost: float, savings: float, implementation: float, annual_license: float,
        years: int, scenario: str):
    """Calculate ROI for a prospect."""
    calculator = ROICalculator()

    result = calculator.calculate(
        current_annual_cost=current_cost,
        efficiency_gain=savings,
        implementation_cost=implementation,
        annual_license=annual_license,
        years=years,
        scenario=scenario
    )

    click.echo(f"\n{'='*60}")
    click.echo(f"ROI ANALYSIS - {scenario.upper()} SCENARIO")
    click.echo(f"{'='*60}\n")

    click.echo("INPUTS:")
    click.echo(f"  Current Annual Cost:    ${current_cost:>12,.2f}")
    click.echo(f"  Efficiency Gain:        {savings*100:>12.1f}%")
    click.echo(f"  Implementation Cost:    ${implementation:>12,.2f}")
    click.echo(f"  Annual License:         ${annual_license:>12,.2f}")
    click.echo(f"  Analysis Period:        {years:>12} years")
    click.echo()

    click.echo("RESULTS:")
    click.echo(f"  Annual Savings:         ${result['annual_savings']:>12,.2f}")
    click.echo(f"  Net Annual Benefit:     ${result['net_annual_benefit']:>12,.2f}")
    click.echo(f"  Total Investment:       ${result['total_investment']:>12,.2f}")
    click.echo(f"  {years}-Year Net Benefit:     ${result['total_net_benefit']:>12,.2f}")
    click.echo(f"  {'-'*40}")
    click.echo(f"  ROI:                    {result['roi_percent']:>12.1f}%")
    click.echo(f"  Payback Period:         {result['payback_months']:>12.1f} months")
    click.echo()

    click.echo("TALKING POINTS:")
    for point in result['talking_points']:
        click.echo(f"  - {point}")


@cli.command()
@click.option('--type', '-t', 'report_type', type=click.Choice(['discovery', 'qualification', 'roi', 'full']),
              required=True, help='Report type')
@click.option('--output', '-o', type=str, default='report.xlsx', help='Output file path')
@click.option('--prospect', '-p', type=str, default='Prospect', help='Prospect company name')
def export(report_type: str, output: str, prospect: str):
    """Export a report to Excel."""
    generator = ReportGenerator()

    # Ensure output directory exists
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    if not output.startswith('/') and not output.startswith('\\') and ':' not in output:
        output = str(output_dir / output)

    if report_type == 'discovery':
        path = generator.generate_discovery_report(
            prospect_name=prospect,
            output_path=output
        )
    elif report_type == 'qualification':
        path = generator.generate_qualification_report(
            prospect_name=prospect,
            output_path=output
        )
    elif report_type == 'roi':
        path = generator.generate_roi_report(
            prospect_name=prospect,
            output_path=output
        )
    else:
        path = generator.generate_full_report(
            prospect_name=prospect,
            output_path=output
        )

    click.echo(f"\nReport generated: {path}")


@cli.command()
def list_objections():
    """List all objection categories."""
    handler = ObjectionHandler()
    categories = handler.get_categories()

    click.echo("\nAvailable objection categories:")
    for cat in categories:
        count = len(handler.get_responses_by_category(cat))
        click.echo(f"  - {cat} ({count} objections)")


if __name__ == '__main__':
    cli()
