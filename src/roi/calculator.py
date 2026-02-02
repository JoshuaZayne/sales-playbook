"""
ROI Calculator
==============

Calculate ROI, TCO, and payback period for sales opportunities.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ROIResult:
    """Container for ROI calculation results."""
    annual_savings: float
    net_annual_benefit: float
    total_investment: float
    total_net_benefit: float
    roi_percent: float
    payback_months: float
    talking_points: List[str]


class ROICalculator:
    """
    Calculate ROI metrics for sales proposals.

    Supports conservative, moderate, and aggressive scenarios.
    """

    def __init__(self):
        self.scenario_multipliers = {
            "conservative": 0.7,
            "moderate": 1.0,
            "aggressive": 1.3
        }

    def calculate(
        self,
        current_annual_cost: float,
        efficiency_gain: float,
        implementation_cost: float = 0,
        annual_license: float = 0,
        years: int = 3,
        scenario: str = "moderate"
    ) -> Dict[str, Any]:
        """
        Calculate ROI for a prospect.

        Args:
            current_annual_cost: Current annual cost being replaced/reduced
            efficiency_gain: Expected efficiency improvement (0.0-1.0)
            implementation_cost: One-time implementation cost
            annual_license: Annual license/subscription cost
            years: Analysis period in years
            scenario: 'conservative', 'moderate', or 'aggressive'

        Returns:
            Dictionary with ROI metrics and talking points
        """
        # Apply scenario multiplier to efficiency gain
        multiplier = self.scenario_multipliers.get(scenario, 1.0)
        adjusted_efficiency = efficiency_gain * multiplier

        # Calculate annual savings
        annual_savings = current_annual_cost * adjusted_efficiency

        # Calculate net annual benefit (savings minus new costs)
        net_annual_benefit = annual_savings - annual_license

        # Total investment (implementation + first year license)
        total_investment = implementation_cost + annual_license

        # Multi-year calculations
        total_savings = annual_savings * years
        total_license_cost = annual_license * years
        total_net_benefit = total_savings - total_license_cost - implementation_cost

        # ROI percentage
        if total_investment > 0:
            roi_percent = (total_net_benefit / total_investment) * 100
        else:
            roi_percent = float('inf') if total_net_benefit > 0 else 0

        # Payback period in months
        if net_annual_benefit > 0:
            payback_months = (implementation_cost / net_annual_benefit) * 12
        else:
            payback_months = float('inf')

        # Generate talking points
        talking_points = self._generate_talking_points(
            annual_savings=annual_savings,
            roi_percent=roi_percent,
            payback_months=payback_months,
            total_net_benefit=total_net_benefit,
            years=years
        )

        return {
            "annual_savings": round(annual_savings, 2),
            "net_annual_benefit": round(net_annual_benefit, 2),
            "total_investment": round(total_investment, 2),
            "total_net_benefit": round(total_net_benefit, 2),
            "roi_percent": round(roi_percent, 1),
            "payback_months": round(payback_months, 1),
            "scenario": scenario,
            "years": years,
            "talking_points": talking_points,
            "year_by_year": self._calculate_year_by_year(
                implementation_cost, annual_license, annual_savings, years
            )
        }

    def _generate_talking_points(
        self,
        annual_savings: float,
        roi_percent: float,
        payback_months: float,
        total_net_benefit: float,
        years: int
    ) -> List[str]:
        """Generate executive talking points from ROI results."""
        points = []

        if annual_savings > 0:
            points.append(f"Projected annual savings of ${annual_savings:,.0f}")

        if roi_percent > 0 and roi_percent != float('inf'):
            points.append(f"{years}-year ROI of {roi_percent:.0f}%")

        if payback_months < 12 and payback_months > 0:
            points.append(f"Investment recovered in {payback_months:.0f} months")
        elif payback_months < 24:
            points.append(f"Payback period under 2 years ({payback_months:.0f} months)")

        if total_net_benefit > 100000:
            points.append(f"Total {years}-year value of ${total_net_benefit:,.0f}")

        if roi_percent > 300:
            points.append("Exceeds typical enterprise software ROI benchmarks")

        return points

    def _calculate_year_by_year(
        self,
        implementation_cost: float,
        annual_license: float,
        annual_savings: float,
        years: int
    ) -> List[Dict[str, float]]:
        """Calculate year-by-year cash flows."""
        results = []
        cumulative = -implementation_cost

        for year in range(1, years + 1):
            year_cost = annual_license
            year_savings = annual_savings
            year_net = year_savings - year_cost
            cumulative += year_net

            results.append({
                "year": year,
                "cost": round(year_cost, 2),
                "savings": round(year_savings, 2),
                "net": round(year_net, 2),
                "cumulative": round(cumulative, 2)
            })

        return results

    def calculate_tco(
        self,
        solution_costs: Dict[str, float],
        current_state_costs: Dict[str, float],
        years: int = 5
    ) -> Dict[str, Any]:
        """
        Calculate Total Cost of Ownership comparison.

        Args:
            solution_costs: Dict with 'implementation', 'annual_license', 'annual_support'
            current_state_costs: Dict with 'annual_operations', 'annual_maintenance', 'hidden_costs'
            years: Analysis period

        Returns:
            TCO comparison dictionary
        """
        # Current state TCO
        current_annual = sum([
            current_state_costs.get('annual_operations', 0),
            current_state_costs.get('annual_maintenance', 0),
            current_state_costs.get('hidden_costs', 0)
        ])
        current_tco = current_annual * years

        # Solution TCO
        solution_annual = sum([
            solution_costs.get('annual_license', 0),
            solution_costs.get('annual_support', 0)
        ])
        solution_tco = solution_costs.get('implementation', 0) + (solution_annual * years)

        # Comparison
        tco_savings = current_tco - solution_tco
        tco_savings_percent = (tco_savings / current_tco * 100) if current_tco > 0 else 0

        return {
            "current_state_tco": round(current_tco, 2),
            "solution_tco": round(solution_tco, 2),
            "tco_savings": round(tco_savings, 2),
            "tco_savings_percent": round(tco_savings_percent, 1),
            "years": years,
            "current_annual": round(current_annual, 2),
            "solution_annual": round(solution_annual, 2)
        }

    def sensitivity_analysis(
        self,
        base_inputs: Dict[str, float],
        variable: str,
        range_percent: float = 0.2
    ) -> List[Dict[str, Any]]:
        """
        Perform sensitivity analysis on a variable.

        Args:
            base_inputs: Base case inputs for calculate()
            variable: Variable to analyze ('efficiency_gain', 'annual_license', etc.)
            range_percent: Variation range (default 20%)

        Returns:
            List of results at different levels
        """
        results = []
        base_value = base_inputs.get(variable, 0)

        for multiplier in [1 - range_percent, 1.0, 1 + range_percent]:
            test_inputs = base_inputs.copy()
            test_inputs[variable] = base_value * multiplier

            result = self.calculate(**test_inputs)
            result['scenario_label'] = f"{variable} at {multiplier*100:.0f}%"
            result['variable_value'] = test_inputs[variable]
            results.append(result)

        return results
