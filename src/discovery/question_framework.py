"""
Discovery Question Framework
============================

Stage-based discovery questions for financial services sales.
"""

from typing import List, Dict, Optional


class QuestionFramework:
    """
    Provides structured discovery questions organized by sales stage.

    Stages:
        - initial: First meeting, understand current state
        - technical: Deep dive on technology and integration
        - business: Business case and ROI discussion
        - decision: Decision process and timeline
    """

    def __init__(self):
        self.questions = self._build_question_database()

    def _build_question_database(self) -> Dict[str, List[Dict]]:
        """Build the complete question database."""
        return {
            "initial": [
                {
                    "question": "Can you walk me through your current member/customer data strategy?",
                    "purpose": "Understand current state and pain points",
                    "follow_up": "What's working well? What challenges are you facing?",
                    "pain_mapping": ["data_quality", "integration"]
                },
                {
                    "question": "How do you currently provide financial wellness tools to your members?",
                    "purpose": "Identify product gaps and competitive positioning",
                    "follow_up": "How are members responding to these tools?",
                    "pain_mapping": ["member_engagement", "competitive"]
                },
                {
                    "question": "What does your current tech stack look like for data aggregation and insights?",
                    "purpose": "Map technical landscape and identify integration points",
                    "follow_up": "Who are your core and digital banking providers?",
                    "pain_mapping": ["integration", "technical"]
                },
                {
                    "question": "What strategic initiatives are top priority for your organization this year?",
                    "purpose": "Align solution to strategic priorities",
                    "follow_up": "How does digital transformation fit into these priorities?",
                    "pain_mapping": ["strategic_alignment"]
                },
                {
                    "question": "How are you currently competing with digital-first banks and fintechs?",
                    "purpose": "Understand competitive pressure and urgency",
                    "follow_up": "What are members asking for that you can't currently provide?",
                    "pain_mapping": ["competitive", "member_engagement"]
                },
                {
                    "question": "What visibility do you have into member spending behavior today?",
                    "purpose": "Identify analytics gaps",
                    "follow_up": "Can you identify members at risk of attrition?",
                    "pain_mapping": ["analytics", "retention"]
                },
                {
                    "question": "Who else should be involved in evaluating a solution like this?",
                    "purpose": "Map the buying committee",
                    "follow_up": "What are their primary concerns likely to be?",
                    "pain_mapping": ["decision_process"]
                }
            ],
            "technical": [
                {
                    "question": "What's your current data architecture for member transaction data?",
                    "purpose": "Understand technical requirements and constraints",
                    "follow_up": "Where does data currently reside? Cloud or on-premise?",
                    "pain_mapping": ["technical", "integration"]
                },
                {
                    "question": "How do you handle data security and compliance requirements?",
                    "purpose": "Identify security concerns early",
                    "follow_up": "What certifications do you require from vendors?",
                    "pain_mapping": ["security", "compliance"]
                },
                {
                    "question": "What APIs or integration methods does your core banking platform support?",
                    "purpose": "Assess integration complexity",
                    "follow_up": "Do you have API documentation we could review?",
                    "pain_mapping": ["integration", "technical"]
                },
                {
                    "question": "What's your IT team's bandwidth for supporting a new implementation?",
                    "purpose": "Gauge implementation feasibility",
                    "follow_up": "What other projects are competing for IT resources?",
                    "pain_mapping": ["resources", "timeline"]
                },
                {
                    "question": "How do you currently handle data quality and cleansing?",
                    "purpose": "Identify data quality pain points",
                    "follow_up": "What percentage of transactions can you accurately categorize today?",
                    "pain_mapping": ["data_quality"]
                },
                {
                    "question": "What's your deployment preference - cloud, hybrid, or on-premise?",
                    "purpose": "Understand deployment constraints",
                    "follow_up": "Are there regulatory requirements driving that preference?",
                    "pain_mapping": ["technical", "compliance"]
                }
            ],
            "business": [
                {
                    "question": "How would you quantify the business impact of better member insights?",
                    "purpose": "Build ROI framework",
                    "follow_up": "What metrics would you use to measure success?",
                    "pain_mapping": ["roi", "metrics"]
                },
                {
                    "question": "What's your current cost for data management and analytics?",
                    "purpose": "Establish baseline for ROI calculation",
                    "follow_up": "Include internal headcount, tools, and third-party services",
                    "pain_mapping": ["roi", "cost"]
                },
                {
                    "question": "What's your member attrition rate, and what's a member worth over their lifetime?",
                    "purpose": "Quantify retention opportunity",
                    "follow_up": "What would a 1% improvement in retention be worth?",
                    "pain_mapping": ["retention", "roi"]
                },
                {
                    "question": "How does this initiative fit into your budget planning cycle?",
                    "purpose": "Understand budget availability and timing",
                    "follow_up": "Is there budget allocated, or would this need to be requested?",
                    "pain_mapping": ["budget", "timeline"]
                },
                {
                    "question": "What would success look like 12 months after implementation?",
                    "purpose": "Define success criteria",
                    "follow_up": "What KPIs would you track?",
                    "pain_mapping": ["metrics", "success"]
                },
                {
                    "question": "Who would own this initiative internally?",
                    "purpose": "Identify champion and accountability",
                    "follow_up": "What resources would they have to support it?",
                    "pain_mapping": ["champion", "resources"]
                }
            ],
            "decision": [
                {
                    "question": "What does your typical vendor evaluation process look like?",
                    "purpose": "Map decision process",
                    "follow_up": "How long does it typically take?",
                    "pain_mapping": ["decision_process", "timeline"]
                },
                {
                    "question": "Who needs to sign off on a decision of this size?",
                    "purpose": "Identify economic buyer and approvers",
                    "follow_up": "What are their primary concerns likely to be?",
                    "pain_mapping": ["decision_process", "stakeholders"]
                },
                {
                    "question": "What criteria will you use to make the final decision?",
                    "purpose": "Understand decision criteria",
                    "follow_up": "How would you weight those criteria?",
                    "pain_mapping": ["decision_criteria"]
                },
                {
                    "question": "Are you evaluating other solutions? If so, which ones?",
                    "purpose": "Understand competitive landscape",
                    "follow_up": "What do you see as their strengths and weaknesses?",
                    "pain_mapping": ["competitive"]
                },
                {
                    "question": "What would cause this initiative to stall or be deprioritized?",
                    "purpose": "Identify risks to deal progression",
                    "follow_up": "How can we help mitigate those risks?",
                    "pain_mapping": ["risks", "blockers"]
                },
                {
                    "question": "What's your target timeline for making a decision?",
                    "purpose": "Establish timeline and urgency",
                    "follow_up": "What's driving that timeline?",
                    "pain_mapping": ["timeline", "urgency"]
                },
                {
                    "question": "What would you need to see to feel confident moving forward?",
                    "purpose": "Identify next steps to close",
                    "follow_up": "Would a pilot or proof of concept be valuable?",
                    "pain_mapping": ["next_steps", "closing"]
                }
            ]
        }

    def get_questions_by_stage(self, stage: str) -> List[Dict]:
        """
        Get all questions for a specific stage.

        Args:
            stage: One of 'initial', 'technical', 'business', 'decision'

        Returns:
            List of question dictionaries
        """
        return self.questions.get(stage, [])

    def get_questions_by_pain(self, pain_point: str) -> List[Dict]:
        """
        Get questions that map to a specific pain point.

        Args:
            pain_point: Pain point identifier (e.g., 'data_quality', 'integration')

        Returns:
            List of question dictionaries
        """
        results = []
        for stage_questions in self.questions.values():
            for q in stage_questions:
                if pain_point in q.get('pain_mapping', []):
                    results.append(q)
        return results

    def get_all_stages(self) -> List[str]:
        """Return list of all available stages."""
        return list(self.questions.keys())

    def get_question_count(self) -> Dict[str, int]:
        """Return count of questions per stage."""
        return {stage: len(questions) for stage, questions in self.questions.items()}

    def search_questions(self, keyword: str) -> List[Dict]:
        """
        Search questions by keyword.

        Args:
            keyword: Search term

        Returns:
            List of matching question dictionaries
        """
        keyword = keyword.lower()
        results = []
        for stage_questions in self.questions.values():
            for q in stage_questions:
                if (keyword in q['question'].lower() or
                    keyword in q['purpose'].lower() or
                    keyword in q['follow_up'].lower()):
                    results.append(q)
        return results
