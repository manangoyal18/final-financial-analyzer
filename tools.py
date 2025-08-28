## Fixed imports and added missing PDF processing libraries
## Old code was missing crucial PDF processing imports
## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

## Updated PDF processing imports to match optimized installation
## Added pypdf as primary library with PyPDF2 as fallback
# PDF processing imports
try:
    from pypdf import PdfReader  # Primary PDF library
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False
    
try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Type
from pydantic import BaseModel, Field


## from crewai_tools import BaseTool
from crewai.tools import BaseTool  # << moved from crewai_tools to crewai.tools
## from crewai_tools.tools.serper_dev_tool import SerperDevTool

from crewai_tools import SerperDevTool

## Creating search tool
search_tool = SerperDevTool()

class ReadPDFInput(BaseModel):
    path: str = Field(default="data/sample.pdf", description="Path to the PDF file")


## Completely rewrote PDF reader tool with proper implementation
## Old code used undefined 'Pdf' class and had async method without @staticmethod
## Creating custom pdf reader tool
class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = "Tool to read and extract financial data from PDF documents"
    args_schema: Type[BaseModel] = ReadPDFInput


    @staticmethod
    def read_data_tool(path: str = 'data/sample.pdf') -> str:
        # """Tool to read data from a pdf file from a path

        # Args:
        #     path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

        # Returns:
        #     str: Full Financial Document content
        # """
        try:
            if not os.path.exists(path):
                return f"Error: File {path} not found."
                
            full_report = ""
            
            # Try multiple PDF processing approaches in order of preference
            pdf_processed = False
            
            # 1. Try pdfplumber first (best for financial documents)
            if PDFPLUMBER_AVAILABLE and not pdf_processed:
                try:
                    with pdfplumber.open(path) as pdf:
                        for page_num, page in enumerate(pdf.pages):
                            text = page.extract_text()
                            if text:
                                # Clean and format the financial document data
                                content = text.strip()
                                # Remove excessive whitespaces and format properly
                                while "\n\n\n" in content:
                                    content = content.replace("\n\n\n", "\n\n")
                                
                                full_report += f"\n--- Page {page_num + 1} ---\n{content}\n"
                    pdf_processed = True
                except Exception as pdfplumber_error:
                    pass  # Try next method
            
            # 2. Try pypdf as secondary option
            if PYPDF_AVAILABLE and not pdf_processed:
                try:
                    with open(path, 'rb') as file:
                        pdf_reader = PdfReader(file)
                        for page_num, page in enumerate(pdf_reader.pages):
                            text = page.extract_text()
                            if text:
                                content = text.strip()
                                while "\n\n\n" in content:
                                    content = content.replace("\n\n\n", "\n\n")
                                full_report += f"\n--- Page {page_num + 1} ---\n{content}\n"
                    pdf_processed = True
                except Exception as pypdf_error:
                    pass  # Try next method
            
            # 3. Fallback to PyPDF2 if other methods fail
            if PYPDF2_AVAILABLE and not pdf_processed:
                try:
                    with open(path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        for page_num, page in enumerate(pdf_reader.pages):
                            text = page.extract_text()
                            if text:
                                content = text.strip()
                                while "\n\n\n" in content:
                                    content = content.replace("\n\n\n", "\n\n")
                                full_report += f"\n--- Page {page_num + 1} ---\n{content}\n"
                    pdf_processed = True
                except Exception as pypdf2_error:
                    pass  # All methods failed
            
            if not pdf_processed:
                return f"Error: No PDF processing libraries available or all methods failed"
                            
            return full_report if full_report else "Error: Could not extract text from PDF"
            
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"
    
    def _run(self, path: str = 'data/sample.pdf') -> str:
        return self.read_data_tool(path)

class InvestmentInput(BaseModel):
    financial_document_data: str = Field(..., description="Raw text extracted from a financial PDF")

## Implemented comprehensive Investment Analysis Tool
## Old code was just a stub with TODO comment
## Creating Investment Analysis Tool
class InvestmentTool(BaseTool):
    name: str = "Investment Analysis Tool"
    description: str = "Analyzes financial documents and provides investment insights"
    
    @staticmethod
    def analyze_investment_tool(financial_document_data: str) -> Dict[str, Any]:
        # """Analyze financial document data for investment opportunities
        
        # Args:
        #     financial_document_data (str): Raw financial document text
            
        # Returns:
        #     Dict[str, Any]: Investment analysis results
        # """
        try:
            if not financial_document_data or financial_document_data.strip() == "":
                return {"error": "No financial data provided for analysis"}
            
            # Clean up the data format
            processed_data = financial_document_data
            while "  " in processed_data:  # Remove double spaces
                processed_data = processed_data.replace("  ", " ")
            
            # Basic financial metrics extraction (simplified)
            analysis_results = {
                "document_length": len(processed_data),
                "key_financial_terms": [],
                "potential_metrics": [],
                "investment_indicators": [],
                "analysis_summary": ""
            }
            
            # Look for common financial terms
            financial_terms = [
                "revenue", "profit", "loss", "ebitda", "margin", "growth", 
                "cash flow", "debt", "equity", "assets", "liabilities",
                "earnings", "dividend", "market cap", "p/e ratio", "roi"
            ]
            
            text_lower = processed_data.lower()
            found_terms = [term for term in financial_terms if term in text_lower]
            analysis_results["key_financial_terms"] = found_terms[:10]  # Limit to top 10
            
            # Simple investment indicators
            if "growth" in text_lower and "revenue" in text_lower:
                analysis_results["investment_indicators"].append("Potential Growth Company")
            if "dividend" in text_lower:
                analysis_results["investment_indicators"].append("Dividend-Paying Stock")
            if "debt" in text_lower and "low" in text_lower:
                analysis_results["investment_indicators"].append("Low Debt Profile")
                
            analysis_results["analysis_summary"] = f"Found {len(found_terms)} key financial terms in document"
            
            return analysis_results
            
        except Exception as e:
            return {"error": f"Investment analysis failed: {str(e)}"}
    
    def _run(self, financial_document_data: str) -> Dict[str, Any]:
        return self.analyze_investment_tool(financial_document_data)

class RiskInput(BaseModel):
    financial_document_data: str = Field(..., description="Raw text extracted from a financial PDF")

## Implemented comprehensive Risk Assessment Tool
## Old code was just a stub with TODO comment
## Creating Risk Assessment Tool
class RiskTool(BaseTool):
    name: str = "Risk Assessment Tool"
    description: str = "Assesses financial risks based on document analysis"
    
    @staticmethod
    def create_risk_assessment_tool(financial_document_data: str) -> Dict[str, Any]:
        # """Create comprehensive risk assessment from financial document
        
        # Args:
        #     financial_document_data (str): Raw financial document text
            
        # Returns:
        #     Dict[str, Any]: Risk assessment results
        # """
        try:
            if not financial_document_data or financial_document_data.strip() == "":
                return {"error": "No financial data provided for risk assessment"}
            
            text_lower = financial_document_data.lower()
            
            risk_assessment = {
                "overall_risk_level": "Medium",  # Default
                "identified_risks": [],
                "risk_factors": [],
                "mitigation_suggestions": [],
                "risk_score": 5,  # Scale of 1-10
                "assessment_summary": ""
            }
            
            # Risk indicators
            high_risk_terms = ["loss", "decline", "bankruptcy", "litigation", "regulatory", "volatile"]
            moderate_risk_terms = ["uncertainty", "competition", "market conditions", "economic"]
            low_risk_terms = ["stable", "consistent", "diversified", "strong position"]
            
            # Count risk indicators
            high_risk_count = sum(1 for term in high_risk_terms if term in text_lower)
            moderate_risk_count = sum(1 for term in moderate_risk_terms if term in text_lower)
            low_risk_count = sum(1 for term in low_risk_terms if term in text_lower)
            
            # Calculate risk score
            risk_score = 5  # Base score
            risk_score += high_risk_count * 1.5
            risk_score += moderate_risk_count * 0.5
            risk_score -= low_risk_count * 0.5
            risk_score = max(1, min(10, risk_score))  # Clamp between 1-10
            
            # Determine overall risk level
            if risk_score <= 3:
                risk_level = "Low"
            elif risk_score <= 7:
                risk_level = "Medium"
            else:
                risk_level = "High"
                
            # Identify specific risks
            identified_risks = []
            if "debt" in text_lower:
                identified_risks.append("Debt levels may impact financial flexibility")
            if "competition" in text_lower:
                identified_risks.append("Competitive market pressures identified")
            if "regulatory" in text_lower:
                identified_risks.append("Regulatory compliance risks present")
                
            risk_assessment.update({
                "overall_risk_level": risk_level,
                "risk_score": round(risk_score, 1),
                "identified_risks": identified_risks[:5],  # Limit to top 5
                "risk_factors": [f"High-risk terms: {high_risk_count}", f"Moderate-risk terms: {moderate_risk_count}"],
                "mitigation_suggestions": [
                    "Diversify investment portfolio",
                    "Monitor financial metrics regularly",
                    "Consider position sizing based on risk level"
                ],
                "assessment_summary": f"Risk level: {risk_level} (Score: {round(risk_score, 1)}/10)"
            })
            
            return risk_assessment
            
        except Exception as e:
            return {"error": f"Risk assessment failed: {str(e)}"}
    
    def _run(self, financial_document_data: str) -> Dict[str, Any]:
        return self.create_risk_assessment_tool(financial_document_data)

financial_document_tool = FinancialDocumentTool()
investment_tool = InvestmentTool()
risk_tool = RiskTool()