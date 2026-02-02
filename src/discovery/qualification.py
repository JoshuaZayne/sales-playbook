"""
Qualification Engine
====================

BANT and MEDDIC qualification frameworks for sales opportunities.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class QualificationResult:
    """Result of a qualification assessment."""
    score: int
    grade: str
    breakdown: Dict[str, int]
    recommendation: str
    next_steps: list


class QualificationEngine:
    """
    Qualification scoring engine supporting BANT and MEDDIC frameworks.

    BANT: Budget, Authority, Need, Timeline
    MEDDIC: Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion
    """

    def __init__(self):
        self.thresholds = {
            "hot": 80,
            "warm": 60,
            "cold": 40
        }

    def score_bant(self, budget: int, authority: str, need: str, timeline: str) -> Dict[str, Any]:
        """
        Score a prospect using BANT framework.

        Args:
            budget: Budget amount in dollars (0 if unknown)
            authority: Decision maker level ('cfo', 'cto', 'vp', 'director', 'manager', 'unknown')
            need: Business need level ('critical', 'high', 'medium', 'low')
            timeline: Implementation timeline ('q1', 'q2', 'q3', 'q4', 'next_year', 'unknown')

        Returns:
            Dictionary with score, grade, breakdown, and recommendation
        """
        breakdown = {}

        # Budget scoring (0-25 points)
        if budget >= 500000:
            breakdown['budget'] = 25
        elif budget >= 250000:
            breakdown['budget'] = 20
        elif budget >= 100000:
            breakdown['budget'] = 15
        elif budget >= 50000:
            breakdown['budget'] = 10
        elif budget > 0:
            breakdown['budget'] = 5
        else:
            breakdown['budget'] = 0

        # Authority scoring (0-25 points)
        authority_scores = {
            'cfo': 25, 'cto': 25, 'ceo': 25,
            'vp': 20,
            'director': 15,
            'manager': 10,
            'unknown': 5
        }
        breakdown['authority'] = authority_scores.get(authority.lower(), 5)

        # Need scoring (0-25 points)
        need_scores = {
            'critical': 25,
            'high': 20,
            'medium': 12,
            'low': 5
        }
        breakdown['need'] = need_scores.get(need.lower(), 5)

        # Timeline scoring (0-25 points)
        timeline_scores = {
            'q1': 25, 'q2': 20, 'q3': 15, 'q4': 10,
            'next_year': 5, 'unknown': 3
        }
        breakdown['timeline'] = timeline_scores.get(timeline.lower(), 3)

        # Calculate total
        total_score = sum(breakdown.values())

        # Determine grade
        if total_score >= self.thresholds['hot']:
            grade = "HOT"
            recommendation = "Schedule executive meeting and prepare proposal"
            next_steps = [
                "Arrange meeting with economic buyer",
                "Prepare custom ROI analysis",
                "Draft proposal and pricing",
                "Identify reference customers in same vertical"
            ]
        elif total_score >= self.thresholds['warm']:
            grade = "WARM"
            recommendation = "Continue discovery and build champion relationship"
            next_steps = [
                "Schedule technical deep-dive",
                "Provide case studies and references",
                "Build relationship with internal champion",
                "Clarify budget and timeline"
            ]
        elif total_score >= self.thresholds['cold']:
            grade = "DEVELOPING"
            recommendation = "Nurture with content and check back quarterly"
            next_steps = [
                "Add to nurture campaign",
                "Send relevant content and thought leadership",
                "Schedule quarterly check-in",
                "Monitor for trigger events"
            ]
        else:
            grade = "COLD"
            recommendation = "Deprioritize - not a fit at this time"
            next_steps = [
                "Add to long-term nurture list",
                "Set reminder to revisit in 6 months",
                "Track company news for changes"
            ]

        return {
            "score": total_score,
            "grade": grade,
            "breakdown": breakdown,
            "recommendation": recommendation,
            "next_steps": next_steps
        }

    def score_meddic(self, metrics: str, economic_buyer: str, decision_criteria: str,
                     decision_process: str, pain: str, champion: str) -> Dict[str, Any]:
        """
        Score a prospect using MEDDIC framework.

        Args:
            metrics: Clarity of success metrics ('defined', 'partial', 'unclear')
            economic_buyer: Access to economic buyer ('direct', 'indirect', 'none')
            decision_criteria: Understanding of criteria ('clear', 'partial', 'unknown')
            decision_process: Understanding of process ('mapped', 'partial', 'unknown')
            pain: Pain identification ('compelling', 'identified', 'unclear')
            champion: Champion status ('active', 'potential', 'none')

        Returns:
            Dictionary with score, grade, breakdown, and recommendation
        """
        breakdown = {}

        # Metrics (0-17 points)
        metrics_scores = {'defined': 17, 'partial': 10, 'unclear': 3}
        breakdown['metrics'] = metrics_scores.get(metrics.lower(), 3)

        # Economic Buyer (0-17 points)
        eb_scores = {'direct': 17, 'indirect': 10, 'none': 3}
        breakdown['economic_buyer'] = eb_scores.get(economic_buyer.lower(), 3)

        # Decision Criteria (0-17 points)
        dc_scores = {'clear': 17, 'partial': 10, 'unknown': 3}
        breakdown['decision_criteria'] = dc_scores.get(decision_criteria.lower(), 3)

        # Decision Process (0-17 points)
        dp_scores = {'mapped': 17, 'partial': 10, 'unknown': 3}
        breakdown['decision_process'] = dp_scores.get(decision_process.lower(), 3)

        # Identify Pain (0-16 points)
        pain_scores = {'compelling': 16, 'identified': 10, 'unclear': 3}
        breakdown['pain'] = pain_scores.get(pain.lower(), 3)

        # Champion (0-16 points)
        champion_scores = {'active': 16, 'potential': 10, 'none': 3}
        breakdown['champion'] = champion_scores.get(champion.lower(), 3)

        # Calculate total
        total_score = sum(breakdown.values())

        # Determine grade and recommendations
        if total_score >= 85:
            grade = "A - COMMIT"
            recommendation = "High confidence deal - commit resources"
        elif total_score >= 65:
            grade = "B - PROBABLE"
            recommendation = "Good opportunity - continue qualification"
        elif total_score >= 45:
            grade = "C - POSSIBLE"
            recommendation = "Needs work - address gaps before advancing"
        else:
            grade = "D - UNLIKELY"
            recommendation = "Significant gaps - reassess opportunity"

        # Identify weakest areas
        gaps = [k for k, v in breakdown.items() if v <= 5]

        return {
            "score": total_score,
            "grade": grade,
            "breakdown": breakdown,
            "recommendation": recommendation,
            "gaps": gaps
        }

    def combine_scores(self, bant_result: Dict, meddic_result: Dict) -> Dict[str, Any]:
        """
        Combine BANT and MEDDIC scores for overall qualification.

        Args:
            bant_result: Result from score_bant()
            meddic_result: Result from score_meddic()

        Returns:
            Combined qualification assessment
        """
        # Weighted average (BANT 40%, MEDDIC 60%)
        combined_score = int(bant_result['score'] * 0.4 + meddic_result['score'] * 0.6)

        if combined_score >= 80:
            overall_grade = "COMMIT"
        elif combined_score >= 60:
            overall_grade = "PROBABLE"
        elif combined_score >= 40:
            overall_grade = "DEVELOPING"
        else:
            overall_grade = "UNLIKELY"

        return {
            "combined_score": combined_score,
            "overall_grade": overall_grade,
            "bant_score": bant_result['score'],
            "meddic_score": meddic_result['score'],
            "bant_grade": bant_result['grade'],
            "meddic_grade": meddic_result['grade'],
            "priority_gaps": meddic_result.get('gaps', [])
        }
