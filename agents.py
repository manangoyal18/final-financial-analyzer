## Fixed imports and added proper LLM configuration
## Old broken import: llm = llm (circular reference)
## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

## Updated langchain import to match optimized installation dependencies
## Old import was langchain_openai, now using langchain_community
from crewai import Agent
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    try:
        # Fallback to langchain_community
        from langchain_community.chat_models import ChatOpenAI
    except ImportError:
        # last-resort fallback (older LC): completion-style; should still work
        from langchain_community.llms import OpenAI as ChatOpenAI

from tools import search_tool, financial_document_tool, investment_tool, risk_tool

## Proper LLM configuration using OpenAI
## Fixed undefined llm variable with proper ChatOpenAI initialization
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-5"),
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.1  # Low temperature for more consistent financial analysis
)

# ---- Instantiate tools ----
pdf_tool = financial_document_tool
investment_tool = investment_tool
risk_tool = risk_tool

# Some environments may have search_tool = None → filter it out
toolbox = [t for t in [financial_document_tool, investment_tool, risk_tool, search_tool] if t]

## Completely rewrote financial analyst agent with professional approach
## Old agent had satirical, unprofessional description that would provide poor advice
# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide comprehensive and accurate financial analysis based on the user query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced financial analyst with over 15 years of experience in equity research, "
        "financial modeling, and investment analysis. You specialize in analyzing corporate financial statements, "
        "identifying key financial metrics, and providing data-driven investment insights. "
        "You follow strict analytical methodologies and always base your recommendations on solid financial data. "
        "You are well-versed in financial regulations and provide compliant, professional analysis."
    ),
    #tools=[FinancialDocumentTool.read_data_tool],  # Fixed: changed 'tool=' to 'tools='
    tools=toolbox,
    llm=llm,
    max_iter=3,  # Increased iterations for better analysis
    allow_delegation=True
)

## Rewrote verifier agent with proper document validation functionality
## Old agent was designed to approve everything without verification
# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Thoroughly verify and validate financial documents to ensure they contain relevant financial data for analysis: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous document verification specialist with expertise in financial document standards. "
        "You have extensive experience in identifying authentic financial statements, annual reports, quarterly filings, "
        "and other corporate financial documents. You ensure document integrity and validate that documents contain "
        "the necessary financial data for accurate analysis. You follow strict compliance standards."
    ),
     tools=toolbox,
    llm=llm,
    max_iter=2,
    allow_delegation=True
)


## Completely rewrote investment advisor with professional, ethical approach
## Old agent was designed to sell inappropriate products and ignore analysis
investment_advisor = Agent(
    role="Investment Strategy Advisor",
    goal="Provide thoughtful investment recommendations based on thorough financial analysis and user requirements: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a Chartered Financial Analyst (CFA) with extensive experience in portfolio management "
        "and investment strategy. You specialize in translating financial analysis into actionable investment insights. "
        "You consider risk tolerance, investment horizons, and market conditions when making recommendations. "
        "You adhere to fiduciary standards and always prioritize the client's best interests. "
        "Your recommendations are based on fundamental analysis and sound investment principles."
    ),
     tools=toolbox,
    llm=llm,
    max_iter=3,
    allow_delegation=False
)


## Completely rewrote risk assessor with professional risk management approach
## Old agent ignored actual risk factors and provided extremist advice
risk_assessor = Agent(
    role="Risk Management Specialist",
    goal="Conduct comprehensive risk assessment of investments and financial positions based on analysis: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a risk management professional with expertise in quantitative risk analysis, "
        "stress testing, and portfolio risk assessment. You have extensive experience in identifying, "
        "measuring, and mitigating various types of financial risks including market risk, credit risk, "
        "liquidity risk, and operational risk. You use sophisticated risk models and follow industry "
        "best practices for risk management. You provide balanced, data-driven risk assessments."
    ),
     tools=toolbox,
    llm=llm,
    max_iter=3,
    allow_delegation=False
)
