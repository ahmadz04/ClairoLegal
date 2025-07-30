from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import json
from .models import ContractState, ClauseAnalysis, ContractReport
from .pdf_loader import PDFLoader
from .clause_splitter import ClauseSplitter
from .prompts import ContractAnalysisPrompts


class ContractAnalysisWorkflow:
    def __init__(self):
        self.pdf_loader = PDFLoader()
        self.clause_splitter = ClauseSplitter()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        self.prompts = ContractAnalysisPrompts()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(ContractState)
        graph.add_node("load_contract", self._load_contract_step)
        graph.add_node("split_clauses", self._split_clauses_step)
        graph.add_node("analyze_clauses", self._analyze_clauses_step)
        graph.add_node("generate_report", self._generate_report_step)
        
        graph.set_entry_point("load_contract")
        graph.add_edge("load_contract", "split_clauses")
        graph.add_edge("split_clauses", "analyze_clauses")
        graph.add_edge("analyze_clauses", "generate_report")
        graph.add_edge("generate_report", END)
        
        return graph.compile()

    def _load_contract_step(self, state: ContractState) -> Dict[str, Any]:
        """Load contract from file (PDF or text)"""
        print("📄 Loading contract file...")
        
        # This will be set by the caller
        if not hasattr(state, 'file_path'):
            raise ValueError("file_path must be provided in state")
        
        file_path = state.file_path
        
        # Determine file type and load accordingly
        if file_path.lower().endswith('.pdf'):
            contract_text = self.pdf_loader.load_pdf(file_path)
        else:
            contract_text = self.pdf_loader.load_text_file(file_path)
        
        if not contract_text:
            raise ValueError(f"Failed to load contract from {file_path}")
        
        print(f"✅ Loaded contract ({len(contract_text)} characters)")
        return {"contract_text": contract_text}

    def _split_clauses_step(self, state: ContractState) -> Dict[str, Any]:
        """Split contract text into individual clauses"""
        print("🔪 Splitting contract into clauses...")
        
        clauses = self.clause_splitter.split_clauses(state.contract_text)
        
        if not clauses:
            raise ValueError("No clauses found in contract text")
        
        print(f"✅ Split into {len(clauses)} clauses")
        return {"clauses": clauses}

    def _analyze_clauses_step(self, state: ContractState) -> Dict[str, Any]:
        """Analyze each clause for summary, risk, and suggestions"""
        print("🔍 Analyzing clauses...")
        
        clause_analyses = []
        
        for i, clause in enumerate(state.clauses, 1):
            print(f"  Analyzing clause {i}/{len(state.clauses)}...")
            
            try:
                analysis = self._analyze_single_clause(clause)
                clause_analyses.append(analysis)
            except Exception as e:
                print(f"    Error analyzing clause {i}: {str(e)}")
                # Create a fallback analysis
                clause_analyses.append(ClauseAnalysis(
                    clause=clause,
                    summary="Analysis failed",
                    is_risky=False,
                    risk_reason="None",
                    suggestion="None"
                ))
        
        print(f"✅ Completed analysis of {len(clause_analyses)} clauses")
        return {"clause_analyses": clause_analyses}

    def _analyze_single_clause(self, clause: str) -> ClauseAnalysis:
        """Analyze a single clause using LLM"""
        
        # Step 1: Generate summary
        summary_messages = [
            SystemMessage(content=self.prompts.SUMMARY_SYSTEM),
            HumanMessage(content=self.prompts.summary_user(clause))
        ]
        summary_response = self.llm.invoke(summary_messages)
        summary = summary_response.content.strip()
        
        # Step 2: Detect risks
        risk_messages = [
            SystemMessage(content=self.prompts.RISK_SYSTEM),
            HumanMessage(content=self.prompts.risk_user(clause))
        ]
        risk_response = self.llm.invoke(risk_messages)
        
        # Parse risk analysis
        try:
            risk_data = json.loads(risk_response.content)
            is_risky = risk_data.get("is_risky", False)
            risk_reason = risk_data.get("risk_reason", "None")
        except json.JSONDecodeError:
            # Fallback parsing
            content = risk_response.content.lower()
            is_risky = "true" in content and "false" not in content
            risk_reason = "Analysis failed - manual review recommended"
        
        # Step 3: Generate suggestion
        suggestion_messages = [
            SystemMessage(content=self.prompts.SUGGESTION_SYSTEM),
            HumanMessage(content=self.prompts.suggestion_user(clause, is_risky, risk_reason))
        ]
        suggestion_response = self.llm.invoke(suggestion_messages)
        suggestion = suggestion_response.content.strip()
        
        return ClauseAnalysis(
            clause=clause,
            summary=summary,
            is_risky=is_risky,
            risk_reason=risk_reason,
            suggestion=suggestion
        )

    def _generate_report_step(self, state: ContractState) -> Dict[str, Any]:
        """Generate final summary report"""
        print("📊 Generating final report...")
        
        total_clauses = len(state.clause_analyses)
        risky_clauses_count = sum(1 for analysis in state.clause_analyses if analysis.is_risky)
        suggestions_count = sum(1 for analysis in state.clause_analyses if analysis.suggestion != "None")
        
        report = ContractReport(
            total_clauses=total_clauses,
            risky_clauses_count=risky_clauses_count,
            suggestions_count=suggestions_count,
            clauses=state.clause_analyses
        )
        
        print(f"✅ Report generated: {total_clauses} clauses, {risky_clauses_count} risky, {suggestions_count} suggestions")
        return {"report": report}

    def run(self, file_path: str) -> ContractReport:
        """Run the complete contract analysis workflow"""
        initial_state = ContractState(file_path=file_path)
        final_state = self.workflow.invoke(initial_state)
        return final_state["report"]