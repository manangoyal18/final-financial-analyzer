## Fixed imports to include all required agents and tools
## Old code was missing import for investment_advisor and risk_assessor agents
## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, financial_document_tool, investment_tool, risk_tool

## Completely rewrote financial document analysis task with professional approach
## Old task description encouraged making up information and ignoring user queries
## Creating a task to help solve user's query
analyze_financial_document = Task(
    description="""Conduct a comprehensive financial analysis of the provided document to address the user's query: {query}
    
    Your analysis should include:
    1. Extract and read the financial document thoroughly
    2. Identify key financial metrics, ratios, and performance indicators
    3. Analyze financial trends, growth patterns, and operational performance
    4. Evaluate the company's financial health and stability
    5. Provide context about industry conditions and market position
    6. Address the specific question or analysis request from the user
    
    Base all analysis on the actual data from the financial document. Avoid speculation and focus on data-driven insights.""",

    expected_output="""A comprehensive financial analysis report that includes:
    
    **Executive Summary**
    - Brief overview of the company's financial position
    - Key findings from the analysis
    
    **Financial Performance Analysis**
    - Revenue trends and growth analysis
    - Profitability metrics and margins
    - Cash flow analysis
    - Key financial ratios
    
    **Risk Factors**
    - Identified financial and operational risks
    - Market and competitive challenges
    
    **Key Insights**
    - Notable strengths and weaknesses
    - Important trends or patterns
    - Specific answers to the user's query
    
    Format the analysis professionally with clear sections and bullet points where appropriate.""",

    agent=financial_analyst,
    tools=[financial_document_tool],
    async_execution=False,
)

## Created professional investment analysis task
## Old task ignored user queries and recommended inappropriate products
## Creating an investment analysis task
investment_analysis = Task(
    description="""Based on the financial document analysis, provide investment insights and recommendations related to: {query}
    
    Your investment analysis should:
    1. Use the financial data from the document to assess investment attractiveness
    2. Consider valuation metrics, growth prospects, and financial stability
    3. Evaluate the company's competitive position and market opportunities
    4. Assess risk-return characteristics of potential investment
    5. Provide balanced perspective on both opportunities and risks
    6. Consider different investment approaches (growth, value, income)
    
    Ensure recommendations are based on financial fundamentals and aligned with the user's query.""",

    expected_output="""A structured investment analysis including:
    
    **Investment Thesis**
    - Overall investment attractiveness rating
    - Key reasons to consider this investment
    
    **Valuation Analysis**
    - Current valuation metrics assessment
    - Comparison to industry benchmarks where applicable
    - Growth assumptions and projections
    
    **Investment Recommendations**
    - Specific investment recommendation (Buy/Hold/Sell or similar)
    - Target price ranges or valuation estimates if applicable
    - Investment horizon considerations
    
    **Risk Considerations**
    - Key risks that could impact investment performance
    - Risk mitigation strategies
    
    **Portfolio Fit**
    - What type of investor this might suit
    - Portfolio allocation considerations
    
    Provide clear, actionable insights based on the financial analysis.""",

    agent=investment_advisor,
    tools=[investment_tool, financial_document_tool],
    async_execution=False,
)

## Created professional risk assessment task
## Old task ignored actual financial data and provided extreme/unrealistic assessments
## Creating a risk assessment task
risk_assessment = Task(
    description="""Conduct a thorough risk assessment based on the financial document analysis, addressing: {query}
    
    Your risk assessment should:
    1. Identify specific financial risks from the document data
    2. Evaluate operational, market, and industry-specific risks
    3. Assess liquidity, credit, and solvency risks
    4. Consider regulatory and compliance risks where applicable
    5. Analyze risk trends and potential future risk scenarios
    6. Provide practical risk management recommendations
    
    Focus on data-driven risk identification and evidence-based risk evaluation.""",

    expected_output="""A comprehensive risk assessment report including:
    
    **Risk Summary**
    - Overall risk rating (Low/Medium/High)
    - Primary risk categories identified
    
    **Detailed Risk Analysis**
    - Financial risks (leverage, liquidity, profitability)
    - Operational risks (business model, management, operations)
    - Market risks (competition, economic sensitivity, cyclicality)
    - Regulatory/Legal risks if applicable
    
    **Risk Quantification**
    - Risk severity rankings
    - Probability assessments where possible
    - Potential impact analysis
    
    **Risk Management Recommendations**
    - Specific mitigation strategies
    - Monitoring guidelines
    - Risk tolerance considerations
    
    **Risk Scenario Analysis**
    - Best/worst case scenarios
    - Stress testing considerations
    
    Provide actionable risk insights that investors can use for decision-making.""",

    agent=risk_assessor,
    tools=[risk_tool, financial_document_tool],
    async_execution=False,
)

## Created professional document verification task
## Old task was designed to approve any document without proper verification
verification = Task(
    description="""Thoroughly verify and validate that the uploaded document is a legitimate financial document suitable for analysis.
    
    Your verification should:
    1. Read and examine the document content carefully
    2. Identify document type (10-K, 10-Q, earnings report, financial statement, etc.)
    3. Verify presence of key financial data and metrics
    4. Check for standard financial document formatting and structure
    5. Validate that the document contains sufficient data for meaningful analysis
    6. Identify any limitations or missing information
    
    Provide honest assessment of document quality and suitability for financial analysis.""",

    expected_output="""A document verification report including:
    
    **Document Validation**
    - Document type identification
    - Verification status (Valid/Invalid/Partially Valid)
    - Document quality assessment
    
    **Content Analysis**
    - Key financial sections identified
    - Types of financial data available
    - Completeness of information
    
    **Analysis Readiness**
    - Suitability for financial analysis
    - Recommended analysis approaches
    - Any limitations or caveats
    
    **Data Quality Assessment**
    - Readability and extraction success
    - Missing or unclear information
    - Confidence level in data accuracy
    
    Provide clear guidance on whether the document can support reliable financial analysis.""",

    agent=verifier,
    tools=[financial_document_tool],
    async_execution=False
)