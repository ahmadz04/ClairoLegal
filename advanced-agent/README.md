# Contract Analyzer & Negotiation Advisor

An AI-powered tool that analyzes legal contracts and provides plain-English explanations, risk assessments, and negotiation suggestions for each clause.

## 🎯 Features

- **PDF & Text Support**: Load contracts from PDF files or plain text
- **Intelligent Clause Splitting**: Automatically splits contracts into individual clauses using regex patterns
- **Plain English Summaries**: Converts complex legal language into understandable explanations
- **Risk Detection**: Identifies vague, overly broad, or one-sided clauses
- **Negotiation Advice**: Provides practical suggestions for improving contract terms
- **Structured Output**: Generates detailed JSON reports with analysis results
- **Summary Statistics**: Overview of total clauses, risky clauses, and suggestions provided

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd advanced-agent
```

2. Install dependencies:

```bash
pip install -e .
```

3. Set up your OpenAI API key:

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Usage

Run the contract analyzer:

```bash
python main.py
```

The tool will prompt you to:

1. Enter the path to your contract file (PDF or text)
2. View the detailed analysis of each clause
3. See the summary report
4. Optionally save the complete analysis to a JSON file

## 📋 Output Format

For each clause, the tool provides:

```json
{
  "clause": "Original contract text",
  "summary": "Plain English explanation",
  "is_risky": true/false,
  "risk_reason": "Why it's risky (or 'None')",
  "suggestion": "Negotiation tip (or 'None')"
}
```

The final report includes:

- Total number of clauses analyzed
- Number of risky clauses flagged
- Number of suggestions generated
- Complete analysis of each clause

## 🏗️ Architecture

The project uses a LangGraph workflow with the following steps:

1. **PDF Loader**: Extracts text from PDF files using PyMuPDF
2. **Clause Splitter**: Splits contract text into individual clauses using regex patterns
3. **Clause Analyzer**: Uses GPT-4o to analyze each clause for:
   - Plain English summary
   - Risk assessment
   - Negotiation suggestions
4. **Report Generator**: Aggregates results and creates final report

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### Model Configuration

The tool uses GPT-4o-mini by default. You can modify the model in `src/workflow.py`:

```python
self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
```

## 📁 Project Structure

```
advanced-agent/
├── main.py                 # Main application entry point
├── pyproject.toml         # Project dependencies and metadata
├── README.md              # This file
└── src/
    ├── __init__.py
    ├── models.py          # Pydantic models for data structures
    ├── pdf_loader.py      # PDF text extraction
    ├── clause_splitter.py # Contract clause splitting logic
    ├── prompts.py         # LLM prompt templates
    └── workflow.py        # LangGraph workflow implementation
```

## 🎯 Use Cases

- **Business Contracts**: Analyze vendor agreements, service contracts, and partnership agreements
- **Employment Contracts**: Review employment terms, non-compete clauses, and benefits
- **Real Estate**: Examine lease agreements and purchase contracts
- **Software Licensing**: Review software licenses and terms of service
- **Legal Review**: Assist lawyers in initial contract review and risk assessment

## 🚀 Deployment

### Quick Deployment Options

#### Docker (Recommended)

```bash
docker-compose up --build
```

#### Heroku

```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

#### Railway/Render

Connect your GitHub repository and set environment variables.

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## ⚠️ Disclaimer

This tool is designed to assist with contract analysis but should not replace professional legal advice. Always consult with qualified legal professionals for important contract decisions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🆘 Support

For issues and questions, please open an issue on the repository.
