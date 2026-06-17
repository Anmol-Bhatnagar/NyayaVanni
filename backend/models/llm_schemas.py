from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date


# Define Pydantic models for structured data
class Party(BaseModel):
    name: str
    role: str

class DateEntry(BaseModel):
    # Using Literal to restrict the type to specific choices
    type: Literal["notice_date", "response_deadline"]
    # Pydantic will automatically validate strings like "2024-12-31" into date objects
    value: date 

class ActionItem(BaseModel):
    priority: Literal["high", "medium", "low"]
    action: str = Field(description="What to do next")
    why: str = Field(description="Reason for the action")
    timeline: str = Field(description="When to do it")

class DocumentAnalysis(BaseModel):
    document_type: str = Field(
        description="Type of document (e.g., FIR, Notice, Contract, etc.)"
    )
    parties: List[Party]
    dates: List[DateEntry]
    sections: List[str] = Field(
        description="Extract explicit legal sections/laws from Document, or apply from Relevant Laws"
    )
    clauses: List[str] = Field(
        description="Extract key clauses/obligations from Document"
    )
    summary: str = Field(
        description="A clear 2-3 sentence explanation of the document."
    )
    risk_level: Literal["Low", "Medium", "High"]
    urgency: Literal["Immediate", "Soon", "Normal"]
    consequences: List[str] = Field(
        description="List of potential outcomes"
    )
    recommended_timeline: str = Field(
        description="e.g., Respond within X days"
    )
    actions: List[ActionItem]


class DiffStats(BaseModel):
    lines_added: int
    lines_removed: int


class AddedObligation(BaseModel):
    clause: str
    severity: Literal["low", "medium", "high", "critical"]
    detail: str


class IncreasedPenalty(BaseModel):
    clause: str
    old_value: str
    new_value: str
    detail: str


class ReducedEmployeeRight(BaseModel):
    clause: str
    severity: Literal["low", "medium", "high", "critical"]
    detail: str


class HiddenModification(BaseModel):
    clause: str
    risk: Literal["low", "medium", "high", "critical"]
    detail: str


class NewLegalExposure(BaseModel):
    clause: str
    severity: Literal["low", "medium", "high", "critical"]
    detail: str


class DiffAnalysisResult(BaseModel):
    overall_risk_level: Literal["low", "medium", "high", "critical"]
    summary: str
    added_obligations: List[AddedObligation]
    increased_penalties: List[IncreasedPenalty]
    reduced_employee_rights: List[ReducedEmployeeRight]
    hidden_modifications: List[HiddenModification]
    new_legal_exposure: List[NewLegalExposure]
    recommended_actions: List[str]


class DiffAnalysisResponse(BaseModel):
    diff_stats: DiffStats
    analysis: DiffAnalysisResult

