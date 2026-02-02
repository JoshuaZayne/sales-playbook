"""
Agent Configuration for Sales Playbook
=======================================

This module provides reusable agent configuration for automating
sales playbook operations. Can be used with Claude Code or other
AI-powered automation tools.

Usage:
    from agent import SalesPlaybookAgent
    agent = SalesPlaybookAgent()
    agent.run_discovery("Acme Bank", "initial")
"""

import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path


class SalesPlaybookAgent:
    """
    Reusable agent for sales playbook automation.

    This agent can be integrated with AI assistants to automate:
    - Discovery question generation
    - Prospect qualification
    - Objection handling
    - ROI calculations
    - Report generation
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the agent with configuration."""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "config.json"

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.context = {
            "current_prospect": None,
            "discovery_stage": None,
            "qualification_scores": {},
            "objections_handled": [],
            "roi_calculated": False
        }

    def set_prospect(self, company_name: str, metadata: Optional[Dict] = None) -> None:
        """Set the current prospect context."""
        self.context["current_prospect"] = {
            "name": company_name,
            "metadata": metadata or {}
        }

    def run_discovery(self, company_name: str, stage: str) -> Dict[str, Any]:
        """
        Run discovery for a prospect at a given stage.

        Args:
            company_name: Name of the prospect company
            stage: Discovery stage (initial, technical, business, decision)

        Returns:
            Dictionary containing questions and context
        """
        from discovery.question_framework import QuestionFramework

        self.set_prospect(company_name)
        self.context["discovery_stage"] = stage

        framework = QuestionFramework()
        questions = framework.get_questions_by_stage(stage)

        return {
            "prospect": company_name,
            "stage": stage,
            "questions": questions,
            "next_stage": self._get_next_stage(stage)
        }

    def qualify_prospect(self, scores: Dict[str, Any]) -> Dict[str, Any]:
        """
        Qualify a prospect using BANT and MEDDIC frameworks.

        Args:
            scores: Dictionary with qualification inputs

        Returns:
            Qualification results and recommendations
        """
        from discovery.qualification import QualificationEngine

        engine = QualificationEngine()

        bant_result = engine.score_bant(
            budget=scores.get("budget", 0),
            authority=scores.get("authority", "unknown"),
            need=scores.get("need", "low"),
            timeline=scores.get("timeline", "unknown")
        )

        self.context["qualification_scores"] = {
            "bant": bant_result
        }

        return {
            "bant_score": bant_result["score"],
            "bant_grade": bant_result["grade"],
            "recommendation": self._get_qualification_recommendation(bant_result["score"])
        }

    def handle_objection(self, category: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Get response for a sales objection.

        Args:
            category: Objection category (price, competitor, timing, etc.)
            context: Additional context about the objection

        Returns:
            Objection response with proof points
        """
        from objections.handler import ObjectionHandler

        handler = ObjectionHandler()
        responses = handler.get_responses_by_category(category)

        self.context["objections_handled"].append(category)

        return {
            "category": category,
            "responses": responses,
            "context_note": f"Consider prospect context: {context}" if context else None
        }

    def calculate_roi(self, inputs: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate ROI for the current prospect.

        Args:
            inputs: Dictionary with current_cost, savings_rate, implementation_cost, annual_license

        Returns:
            ROI calculations and talking points
        """
        from roi.calculator import ROICalculator

        calc = ROICalculator()
        result = calc.calculate(
            current_annual_cost=inputs.get("current_cost", 0),
            efficiency_gain=inputs.get("savings_rate", 0),
            implementation_cost=inputs.get("implementation_cost", 0),
            annual_license=inputs.get("annual_license", 0)
        )

        self.context["roi_calculated"] = True

        return result

    def generate_report(self, output_path: str) -> str:
        """
        Generate a comprehensive report for the current prospect.

        Args:
            output_path: Path for the output Excel file

        Returns:
            Path to the generated report
        """
        from export.report_generator import ReportGenerator

        generator = ReportGenerator()
        return generator.generate_discovery_report(
            prospect_name=self.context["current_prospect"]["name"] if self.context["current_prospect"] else "Unknown",
            qualification_scores=self.context["qualification_scores"],
            output_path=output_path
        )

    def _get_next_stage(self, current_stage: str) -> Optional[str]:
        """Get the next discovery stage."""
        stages = self.config.get("sales_stages", [])
        try:
            idx = stages.index(current_stage)
            if idx < len(stages) - 1:
                return stages[idx + 1]
        except ValueError:
            pass
        return None

    def _get_qualification_recommendation(self, score: int) -> str:
        """Get recommendation based on qualification score."""
        if score >= 80:
            return "HOT - Schedule executive meeting and proposal presentation"
        elif score >= 60:
            return "WARM - Continue discovery and build champion relationship"
        elif score >= 40:
            return "DEVELOPING - Nurture with content and check back quarterly"
        else:
            return "COLD - Deprioritize and add to long-term nurture campaign"

    def get_context(self) -> Dict[str, Any]:
        """Return the current agent context."""
        return self.context.copy()

    def reset_context(self) -> None:
        """Reset the agent context for a new prospect."""
        self.context = {
            "current_prospect": None,
            "discovery_stage": None,
            "qualification_scores": {},
            "objections_handled": [],
            "roi_calculated": False
        }


def create_agent(config_path: Optional[str] = None) -> SalesPlaybookAgent:
    """Factory function to create a configured agent."""
    return SalesPlaybookAgent(config_path)


# Agent metadata for discovery by automation tools
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
