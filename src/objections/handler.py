"""
Objection Handler
=================

Database of common sales objections with response templates and proof points.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional


class ObjectionHandler:
    """
    Handles sales objections with prepared responses and proof points.

    Categories:
        - price: Cost and budget objections
        - competitor: Competitive comparisons
        - timing: Timeline and priority objections
        - integration: Technical integration concerns
        - security: Security and compliance concerns
        - authority: Decision-making authority issues
        - need: Questioning the need for the solution
        - internal: Internal build vs. buy objections
        - risk: Risk and uncertainty concerns
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the objection handler.

        Args:
            config_path: Path to objection_responses.json (optional)
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "objection_responses.json"

        self.config_path = Path(config_path)
        self.objections = self._load_objections()

    def _load_objections(self) -> List[Dict]:
        """Load objections from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                return data.get('objections', [])
        except FileNotFoundError:
            return self._get_default_objections()

    def _get_default_objections(self) -> List[Dict]:
        """Return default objections if config file not found."""
        return [
            {
                "id": 1,
                "category": "price",
                "objection": "Your solution is too expensive.",
                "response": "I understand cost is important. Let's look at the total value and ROI.",
                "proof_points": ["Average 35% cost reduction", "6-month payback period"]
            }
        ]

    def get_responses_by_category(self, category: str) -> List[Dict]:
        """
        Get all objection responses for a category.

        Args:
            category: Objection category

        Returns:
            List of objection dictionaries
        """
        return [obj for obj in self.objections if obj.get('category', '').lower() == category.lower()]

    def get_categories(self) -> List[str]:
        """Get list of all unique categories."""
        categories = set()
        for obj in self.objections:
            if 'category' in obj:
                categories.add(obj['category'])
        return sorted(list(categories))

    def search_objections(self, keyword: str) -> List[Dict]:
        """
        Search objections by keyword.

        Args:
            keyword: Search term

        Returns:
            List of matching objection dictionaries
        """
        keyword = keyword.lower()
        results = []
        for obj in self.objections:
            if (keyword in obj.get('objection', '').lower() or
                keyword in obj.get('response', '').lower() or
                keyword in obj.get('category', '').lower()):
                results.append(obj)
        return results

    def get_objection_by_id(self, objection_id: int) -> Optional[Dict]:
        """
        Get a specific objection by ID.

        Args:
            objection_id: Objection ID

        Returns:
            Objection dictionary or None
        """
        for obj in self.objections:
            if obj.get('id') == objection_id:
                return obj
        return None

    def get_proof_points(self, category: str) -> List[str]:
        """
        Get all proof points for a category.

        Args:
            category: Objection category

        Returns:
            List of unique proof points
        """
        proof_points = set()
        for obj in self.get_responses_by_category(category):
            for point in obj.get('proof_points', []):
                proof_points.add(point)
        return list(proof_points)

    def get_random_response(self, category: str) -> Optional[Dict]:
        """
        Get a random objection response from a category.

        Args:
            category: Objection category

        Returns:
            Random objection dictionary or None
        """
        import random
        responses = self.get_responses_by_category(category)
        return random.choice(responses) if responses else None

    def get_statistics(self) -> Dict:
        """Get statistics about the objection database."""
        categories = self.get_categories()
        return {
            "total_objections": len(self.objections),
            "categories": len(categories),
            "by_category": {cat: len(self.get_responses_by_category(cat)) for cat in categories}
        }
