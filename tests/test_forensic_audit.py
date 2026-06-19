import pytest
from fastapi.testclient import TestClient

from backend.services.forensic_audit_service import run_forensic_audit_pipeline, compiled_graph

@pytest.mark.asyncio
async def test_run_forensic_audit_pipeline(monkeypatch):
    """Test that the run_forensic_audit_pipeline compiles and returns correctly mapped results."""
    mock_response = {
        "synthesis": {
            "document_type": "Contract",
            "parties": [{"name": "Company A", "role": "Discloser"}],
            "dates": [],
            "sections": [],
            "clauses": [],
            "summary": "This is a mock synthesis summary.",
            "risk_level": "High",
            "urgency": "Normal",
            "consequences": [],
            "recommended_timeline": "No deadline",
            "actions": [],
            "forensic_audit": {
                "asymmetric_clauses": [
                    {
                        "clause_name": "Indemnity Limit",
                        "quoted_text": "Indemnity shall be unlimited.",
                        "bias_direction": "disclosing_party",
                        "severity": "critical",
                        "analysis": "Unbalanced indemnity requirement."
                    }
                ],
                "compliance_breaches": [],
                "loopholes": [],
                "executive_summary": "Overall high risk document."
            }
        }
    }
    
    async def mock_invoke(state):
        return mock_response

    monkeypatch.setattr(compiled_graph, "ainvoke", mock_invoke)

    res = await run_forensic_audit_pipeline("Mock text", [])
    assert res["document_type"] == "Contract"
    assert res["risk_level"] == "High"
    assert len(res["forensic_audit"]["asymmetric_clauses"]) == 1
    assert res["forensic_audit"]["asymmetric_clauses"][0]["clause_name"] == "Indemnity Limit"


def test_analyze_endpoint_returns_forensic_audit(test_client, monkeypatch):
    """Test that the /api/analyze route executes the forensic pipeline and returns the payload."""
    async def mock_run_pipeline(*args, **kwargs):
        return {
            "document_type": "Notice",
            "parties": [],
            "dates": [],
            "sections": [],
            "clauses": [],
            "summary": "Mock summary",
            "risk_level": "Low",
            "urgency": "Normal",
            "consequences": [],
            "recommended_timeline": "",
            "actions": [],
            "forensic_audit": {
                "asymmetric_clauses": [],
                "compliance_breaches": [],
                "loopholes": [],
                "executive_summary": "Mock summary"
            }
        }
    
    monkeypatch.setattr(
        "backend.api.routes.run_forensic_audit_pipeline",
        mock_run_pipeline
    )
    
    monkeypatch.setattr("backend.api.routes.require_session_id", lambda request: "mock_session")
    monkeypatch.setattr("backend.api.routes.require_document_owner", lambda doc_id, session_id: {
        "document_id": doc_id,
        "session_id": session_id,
        "filename": "test.pdf",
        "local_path": "test.pdf"
    })
    monkeypatch.setattr("backend.api.routes.get_document_record", lambda doc_id: {
        "document_id": doc_id,
        "filename": "test.pdf",
        "local_path": "test.pdf"
    })
    
    # Mock open and reading file
    import builtins
    original_open = builtins.open
    def mock_open(file, mode='r', *args, **kwargs):
        if "test.pdf" in str(file):
            import io
            return io.BytesIO(b"Dummy PDF content")
        return original_open(file, mode, *args, **kwargs)
    monkeypatch.setattr(builtins, "open", mock_open)
    
    # Mock extract_document and index_document
    monkeypatch.setattr("backend.api.routes.extract_document", lambda *args, **kwargs: "Mock extracted text")
    monkeypatch.setattr("backend.api.routes.index_document", lambda *args: None)
    monkeypatch.setattr("backend.api.routes.retrieve_relevant_laws", lambda *args, **kwargs: [])
    monkeypatch.setattr("backend.api.routes.classify_document", lambda *args: {"predicted_type": "Other / Unknown", "confidence": 0.9, "alternatives": []})
    
    response = test_client.post("/api/analyze/test-doc-id")
    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data
    assert "forensic_audit" in data["analysis"]
