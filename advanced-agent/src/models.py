from typing import List, Optional
from pydantic import BaseModel, Field


class ClauseAnalysis(BaseModel):
    """Structured output for individual clause analysis"""
    clause: str
    summary: str
    is_risky: bool
    risk_reason: str
    suggestion: str


class ContractReport(BaseModel):
    """Summary report for the entire contract"""
    total_clauses: int
    risky_clauses_count: int
    suggestions_count: int
    clauses: List[ClauseAnalysis]


class ContractState(BaseModel):
    """State management for contract analysis workflow"""
    file_path: str = ""
    contract_text: str = ""
    clauses: List[str] = []
    clause_analyses: List[ClauseAnalysis] = []
    report: Optional[ContractReport] = None