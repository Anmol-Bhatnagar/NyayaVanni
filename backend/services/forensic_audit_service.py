import os
import logging
from typing import TypedDict, List, Dict, Any, Optional
from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

from ..models.llm_schemas import (
    DocumentAnalysis,
    AsymmetricClause,
    LawBreach,
    AdversarialLoophole,
    ForensicReport
)

logger = logging.getLogger(__name__)

# Define LangGraph AuditState
class AuditState(TypedDict):
    document_text: str
    relevant_laws: List[str]
    language: str
    asymmetric_clauses: List[Dict[str, Any]]
    compliance_breaches: List[Dict[str, Any]]
    loopholes: List[Dict[str, Any]]
    synthesis: Optional[Dict[str, Any]]

# Define Structured Output Schemas for intermediate agent states
class ExtractedAsymmetricClauses(BaseModel):
    asymmetric_clauses: List[AsymmetricClause] = Field(
        description="List of sneaky, asymmetric, or unbalanced clauses identified in the document."
    )

class ComplianceBreaches(BaseModel):
    compliance_breaches: List[LawBreach] = Field(
        description="List of legal compliance issues, violations, or voidable clauses identified under Indian Law."
    )

class AdversarialLoopholes(BaseModel):
    loopholes: List[AdversarialLoophole] = Field(
        description="List of legal loopholes, wording ambiguities, or liability exposures that can be exploited by an opposing party."
    )

# Node 1: Forensic Clause Extractor
async def extractor_node(state: AuditState) -> Dict[str, Any]:
    logger.info("Executing Agent 1: Forensic Clause Extractor")
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.1,
            google_api_key=api_key
        )
        structured_llm = llm.with_structured_output(ExtractedAsymmetricClauses)
        
        lang_instruction = ""
        if state["language"] == "hi":
            lang_instruction = "IMPORTANT: You MUST write the 'analysis' descriptions in Hindi (हिन्दी). Provide the values in Hindi, but keep the JSON keys strictly in English."

        prompt = f"""
        You are a forensic legal contract auditor specializing in identifying asymmetric, sneaky, or unfair clauses.
        Analyze the following document text and extract any clauses that are heavily biased, containing hidden liabilities, unilateral termination rights, unbalanced indemnity, or auto-renewals with penalty conditions.
        
        {lang_instruction}

        Document Content:
        {state["document_text"][:10000]}
        """
        
        result = await structured_llm.ainvoke(prompt)
        clauses_dict = [clause.dict() for clause in result.asymmetric_clauses]
        return {"asymmetric_clauses": clauses_dict}
        
    except Exception as e:
        logger.error(f"Extractor Agent failed: {e}")
        return {"asymmetric_clauses": []}

# Node 2: Indian Law Compliance Auditor
async def compliance_auditor_node(state: AuditState) -> Dict[str, Any]:
    logger.info("Executing Agent 2: Indian Law Compliance Auditor")
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")
            
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.1,
            google_api_key=api_key
        )
        structured_llm = llm.with_structured_output(ComplianceBreaches)
        
        context = "\n".join(state["relevant_laws"])
        asymmetric_clauses_str = "\n".join([
            f"- {c['clause_name']}: {c['quoted_text']}\n  Analysis: {c['analysis']}" 
            for c in state["asymmetric_clauses"]
        ])
        
        lang_instruction = ""
        if state["language"] == "hi":
            lang_instruction = "IMPORTANT: You MUST write the 'reasoning' and descriptions in Hindi (हिन्दी). Provide the values in Hindi, but keep the JSON keys strictly in English."

        prompt = f"""
        You are an Indian Legal Compliance Auditor. 
        Your task is to take the asymmetric clauses identified by the Extractor agent and audit them against the provided Indian Law references.
        Verify if any of these clauses violate or are void/voidable under Indian laws (e.g., Section 27 of the Indian Contract Act for restrictive non-compete clauses, local rent control laws, consumer protection, etc.).
        
        {lang_instruction}

        Asymmetric Clauses:
        {asymmetric_clauses_str}

        Relevant Law Context:
        {context}
        """
        
        result = await structured_llm.ainvoke(prompt)
        breaches_dict = [breach.dict() for breach in result.compliance_breaches]
        return {"compliance_breaches": breaches_dict}
        
    except Exception as e:
        logger.error(f"Compliance Auditor Agent failed: {e}")
        return {"compliance_breaches": []}

# Node 3: Adversarial Risk Modeler
async def adversarial_modeler_node(state: AuditState) -> Dict[str, Any]:
    logger.info("Executing Agent 3: Adversarial Risk Modeler")
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")
            
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.2,
            google_api_key=api_key
        )
        structured_llm = llm.with_structured_output(AdversarialLoopholes)
        
        asymmetric_clauses_str = "\n".join([
            f"- {c['clause_name']}: {c['quoted_text']}" 
            for c in state["asymmetric_clauses"]
        ])
        
        lang_instruction = ""
        if state["language"] == "hi":
            lang_instruction = "IMPORTANT: You MUST write the 'exploit_scenario' and 'remediation' in Hindi (हिन्दी). Provide the values in Hindi, but keep the JSON keys strictly in English."

        prompt = f"""
        You are an aggressive opposing counsel trying to exploit loopholes or ambiguities in the document.
        Analyze the document text and the flagged asymmetric clauses to identify wording ambiguities, lack of remedy clauses, or liability traps that could be exploited in court.
        Provide remediation recommendations on how to rewrite the clause to protect the user.
        
        {lang_instruction}

        Asymmetric Clauses:
        {asymmetric_clauses_str}

        Document Content:
        {state["document_text"][:10000]}
        """
        
        result = await structured_llm.ainvoke(prompt)
        loopholes_dict = [lh.dict() for lh in result.loopholes]
        return {"loopholes": loopholes_dict}
        
    except Exception as e:
        logger.error(f"Adversarial Modeler Agent failed: {e}")
        return {"loopholes": []}

# Node 4: Chief Synthesizer
async def synthesizer_node(state: AuditState) -> Dict[str, Any]:
    logger.info("Executing Agent 4: Chief Synthesizer")
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")
            
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.1,
            google_api_key=api_key
        )
        structured_llm = llm.with_structured_output(DocumentAnalysis)
        
        # Prepare summaries of inputs
        clauses_str = "\n".join([f"- {c['clause_name']}: {c['quoted_text']} ({c['severity']})" for c in state["asymmetric_clauses"]])
        breaches_str = "\n".join([f"- {b['clause_affected']} violates {b['indian_law_citation']}: {b['reasoning']}" for b in state["compliance_breaches"]])
        loopholes_str = "\n".join([f"- {l['title']}: {l['exploit_scenario']}. Fix: {l['remediation']} ({l['exposure_level']})" for l in state["loopholes"]])
        
        lang_instruction = ""
        if state["language"] == "hi":
            lang_instruction = "IMPORTANT: You MUST write the summary, action points, and all textual explanations in Hindi (हिन्दी). Keep JSON keys strictly in English."

        prompt = f"""
        You are the Chief Legal Synthesizer. Your job is to compile the reports from all sub-agents and generate the final structured DocumentAnalysis payload.
        Make sure the legacy fields (document_type, parties, dates, sections, clauses, summary, risk_level, urgency, consequences, recommended_timeline, actions) are populated accurately.
        Additionally, populate the `forensic_audit` field with the consolidated list of asymmetric_clauses, compliance_breaches, loopholes, and an executive_summary.
        
        {lang_instruction}

        Document Content:
        {state["document_text"][:8000]}

        1. Flagged Asymmetric Clauses:
        {clauses_str}

        2. Compliance Breaches:
        {breaches_str}

        3. Adversarial Loopholes:
        {loopholes_str}
        """
        
        result = await structured_llm.ainvoke(prompt)
        return {"synthesis": result.dict()}
        
    except Exception as e:
        logger.error(f"Synthesizer Agent failed: {e}")
        return {"synthesis": None}

# Compile the StateGraph workflow
def build_forensic_audit_graph() -> StateGraph:
    workflow = StateGraph(AuditState)
    
    # Add nodes
    workflow.add_node("extractor", extractor_node)
    workflow.add_node("compliance_auditor", compliance_auditor_node)
    workflow.add_node("adversarial_modeler", adversarial_modeler_node)
    workflow.add_node("synthesizer", synthesizer_node)
    
    # Add edges
    workflow.add_edge(START, "extractor")
    # Parallel split from extractor to compliance auditor & adversarial modeler
    workflow.add_edge("extractor", "compliance_auditor")
    workflow.add_edge("extractor", "adversarial_modeler")
    # Join parallel branches in synthesizer
    workflow.add_edge("compliance_auditor", "synthesizer")
    workflow.add_edge("adversarial_modeler", "synthesizer")
    workflow.add_edge("synthesizer", END)
    
    return workflow.compile()

# Global compiled application instance
compiled_graph = build_forensic_audit_graph()

async def run_forensic_audit_pipeline(
    document_text: str,
    relevant_laws: List[str],
    language: str = "en"
) -> Dict[str, Any]:
    """
    Runs the multi-agent legal audit workflow on the document text.
    """
    initial_state: AuditState = {
        "document_text": document_text,
        "relevant_laws": relevant_laws,
        "language": language,
        "asymmetric_clauses": [],
        "compliance_breaches": [],
        "loopholes": [],
        "synthesis": None
    }
    
    # Run graph execution asynchronously
    final_output = await compiled_graph.ainvoke(initial_state)
    synthesis = final_output.get("synthesis")
    
    if not synthesis:
        raise ValueError("Multi-agent synthesis returned empty result")
        
    return synthesis
