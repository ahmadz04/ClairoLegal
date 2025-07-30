
class ContractAnalysisPrompts:
    """Collection of prompts for analyzing contract clauses"""

    # Summary prompt
    SUMMARY_SYSTEM = """You are a legal expert who explains complex contract language in plain English. 
    Your goal is to make legal terms accessible to non-lawyers while maintaining accuracy."""

    @staticmethod
    def summary_user(clause: str) -> str:
        return f"""Please explain the following contract clause in plain English:

Clause: {clause}

Provide a clear, concise summary that:
- Explains what this clause means in simple terms
- Identifies the key obligations or rights
- Uses everyday language that a business person would understand
- Is 2-3 sentences maximum

Summary:"""

    # Risk detection prompt
    RISK_SYSTEM = """You are a legal risk analyst specializing in contract review. 
    You identify potentially problematic, vague, or one-sided clauses that could pose risks to the party reviewing the contract."""

    @staticmethod
    def risk_user(clause: str) -> str:
        return f"""Analyze the following contract clause for potential risks:

Clause: {clause}

Determine if this clause is risky and explain why. Consider:
- Vague or ambiguous language
- Overly broad terms
- One-sided obligations
- Unreasonable restrictions
- Missing important protections

Return your analysis in this exact JSON format:
{{
    "is_risky": true/false,
    "risk_reason": "Detailed explanation of why this clause is risky, or 'None' if not risky"
}}

Analysis:"""

    # Negotiation suggestion prompt
    SUGGESTION_SYSTEM = """You are a contract negotiation expert who provides practical advice on improving contract terms. 
    You offer specific, actionable suggestions for negotiating better terms."""

    @staticmethod
    def suggestion_user(clause: str, is_risky: bool, risk_reason: str) -> str:
        return f"""Based on this contract clause analysis, provide negotiation advice:

Clause: {clause}
Is Risky: {is_risky}
Risk Reason: {risk_reason}

Provide a practical negotiation suggestion that:
- Is specific and actionable
- Suggests concrete language changes or additions
- Focuses on protecting the party's interests
- Is reasonable and likely to be accepted by the other party

If the clause is not risky, suggest any improvements that would make it more favorable.

Suggestion:"""