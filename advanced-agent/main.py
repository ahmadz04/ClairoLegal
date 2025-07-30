from dotenv import load_dotenv
from src.workflow import ContractAnalysisWorkflow
import json
import sys
import os

load_dotenv()


def print_clause_analysis(analysis, clause_number):
    """Print a formatted clause analysis"""
    print(f"\n📋 Clause {clause_number}")
    print("=" * 60)
    print(f"📄 Original: {analysis.clause[:200]}{'...' if len(analysis.clause) > 200 else ''}")
    print(f"📝 Summary: {analysis.summary}")
    
    if analysis.is_risky:
        print(f"⚠️  RISKY: {analysis.risk_reason}")
    else:
        print(f"✅ Safe: {analysis.risk_reason}")
    
    if analysis.suggestion != "None":
        print(f"💡 Suggestion: {analysis.suggestion}")
    else:
        print("💡 Suggestion: No specific suggestions")


def print_summary_report(report):
    """Print the summary report"""
    print("\n" + "=" * 80)
    print("📊 CONTRACT ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"📋 Total Clauses: {report.total_clauses}")
    print(f"⚠️  Risky Clauses: {report.risky_clauses_count}")
    print(f"💡 Suggestions Provided: {report.suggestions_count}")
    
    if report.risky_clauses_count > 0:
        risk_percentage = (report.risky_clauses_count / report.total_clauses) * 100
        print(f"🚨 Risk Level: {risk_percentage:.1f}% of clauses flagged as risky")
    else:
        print("✅ Risk Level: No risky clauses detected")


def save_report_to_json(report, output_file):
    """Save the complete report to a JSON file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report.model_dump(), f, indent=2, ensure_ascii=False)
        print(f"\n💾 Report saved to: {output_file}")
    except Exception as e:
        print(f"❌ Error saving report: {str(e)}")


def main():
    workflow = ContractAnalysisWorkflow()
    print("🤖 Contract Analyzer & Negotiation Advisor")
    print("=" * 60)

    while True:
        # Get file path from user
        file_path = input("\n📁 Enter contract file path (PDF or text): ").strip()
        
        if file_path.lower() in {"quit", "exit", "q"}:
            print("👋 Goodbye!")
            break

        if not file_path:
            print("❌ Please provide a file path")
            continue

        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue

        try:
            print(f"\n🔍 Analyzing contract: {file_path}")
            print("=" * 60)
            
            # Run the analysis
            report = workflow.run(file_path)
            
            # Print detailed analysis
            print("\n📋 DETAILED CLAUSE ANALYSIS")
            print("=" * 60)
            
            for i, clause_analysis in enumerate(report.clauses, 1):
                print_clause_analysis(clause_analysis, i)
            
            # Print summary report
            print_summary_report(report)
            
            # Ask if user wants to save the report
            save_choice = input("\n💾 Save detailed report to JSON? (y/n): ").strip().lower()
            if save_choice in {"y", "yes"}:
                default_filename = f"contract_analysis_{os.path.splitext(os.path.basename(file_path))[0]}.json"
                output_file = input(f"📁 Output filename (default: {default_filename}): ").strip()
                if not output_file:
                    output_file = default_filename
                save_report_to_json(report, output_file)
            
            # Ask if user wants to analyze another contract
            another = input("\n🔄 Analyze another contract? (y/n): ").strip().lower()
            if another not in {"y", "yes"}:
                print("👋 Goodbye!")
                break
                
        except Exception as e:
            print(f"❌ Error analyzing contract: {str(e)}")
            print("Please check that the file is a valid PDF or text file.")


if __name__ == "__main__":
    main()