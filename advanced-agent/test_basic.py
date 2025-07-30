#!/usr/bin/env python3
"""
Basic test script to verify the Contract Analyzer modules can be imported
and basic functionality works without requiring an OpenAI API key.
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        from src.models import ClauseAnalysis, ContractReport, ContractState
        print("✅ Models imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import models: {e}")
        return False
    
    try:
        from src.pdf_loader import PDFLoader
        print("✅ PDF Loader imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import PDF Loader: {e}")
        return False
    
    try:
        from src.clause_splitter import ClauseSplitter
        print("✅ Clause Splitter imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Clause Splitter: {e}")
        return False
    
    try:
        from src.prompts import ContractAnalysisPrompts
        print("✅ Prompts imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Prompts: {e}")
        return False
    
    return True

def test_clause_splitter():
    """Test the clause splitter with sample text"""
    print("\n🔍 Testing clause splitter...")
    
    try:
        from src.clause_splitter import ClauseSplitter
        
        sample_text = """
        1. FIRST CLAUSE. This is the first clause of the contract.
        
        2. SECOND CLAUSE. This is the second clause with some legal language.
        
        3. THIRD CLAUSE. This clause contains more complex terms and conditions.
        """
        
        splitter = ClauseSplitter()
        clauses = splitter.split_clauses(sample_text)
        
        print(f"✅ Split into {len(clauses)} clauses")
        for i, clause in enumerate(clauses, 1):
            print(f"   Clause {i}: {clause[:50]}...")
        
        return len(clauses) > 0
        
    except Exception as e:
        print(f"❌ Clause splitter test failed: {e}")
        return False

def test_models():
    """Test Pydantic model creation"""
    print("\n🔍 Testing Pydantic models...")
    
    try:
        from src.models import ClauseAnalysis, ContractReport, ContractState
        
        # Test ClauseAnalysis
        clause = ClauseAnalysis(
            clause="Sample clause text",
            summary="This is a summary",
            is_risky=True,
            risk_reason="Vague language",
            suggestion="Add specific terms"
        )
        print("✅ ClauseAnalysis model created successfully")
        
        # Test ContractState
        state = ContractState(
            contract_text="Sample contract",
            clauses=["Clause 1", "Clause 2"],
            clause_analyses=[clause]
        )
        print("✅ ContractState model created successfully")
        
        # Test ContractReport
        report = ContractReport(
            total_clauses=2,
            risky_clauses_count=1,
            suggestions_count=1,
            clauses=[clause]
        )
        print("✅ ContractReport model created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Contract Analyzer - Basic Functionality Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_clause_splitter,
        test_models
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Contract Analyzer is ready to use.")
        print("\nNext steps:")
        print("1. Set up your OpenAI API key in a .env file")
        print("2. Run: python main.py")
        print("3. Try analyzing the sample_contract.txt file")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 