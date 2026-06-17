import json
from backend.services.gemini_service import analyze_document_with_gemini
from backend.services.gemini_service import DocumentAnalysis

# We'll import the internal parser via function name lookup
from importlib import import_module
mod = import_module('backend.services.gemini_service')
_parse = getattr(mod, '_parse_structured_response')

class MockRespJSON:
    def __init__(self, data):
        self._data = data
    def json(self):
        return self._data

class MockRespText:
    def __init__(self, text):
        self.text = text

def sample_payload():
    return {
        "document_type": "Notice",
        "parties": [{"name": "Alice", "role": "plaintiff"}],
        "dates": [{"type": "notice_date", "value": "2024-12-31"}],
        "sections": ["Section 1"],
        "clauses": ["Clause A"],
        "summary": "Short summary.",
        "risk_level": "Low",
        "urgency": "Normal",
        "consequences": ["None"],
        "recommended_timeline": "Respond within 7 days",
        "actions": [{"priority": "high", "action": "Do X", "why": "Because", "timeline": "ASAP"}]
    }

def test_parse_from_json_method():
    data = sample_payload()
    resp = MockRespJSON(data)
    parsed = _parse(resp)
    assert parsed == data

def test_parse_from_fenced_text():
    data = sample_payload()
    txt = "Here is the analysis:\n```json\n" + json.dumps(data) + "\n```"
    resp = MockRespText(txt)
    parsed = _parse(resp)
    assert parsed == data

def test_parse_from_embedded_text():
    data = sample_payload()
    txt = "Intro text..." + json.dumps(data) + "...trailer"
    resp = MockRespText(txt)
    parsed = _parse(resp)
    assert parsed == data


def sample_diff_payload():
    return {
        "diff_stats": {
            "lines_added": 12,
            "lines_removed": 4
        },
        "analysis": {
            "overall_risk_level": "medium",
            "summary": "This is a summary of the differences.",
            "added_obligations": [
                {"clause": "Clause 1", "severity": "medium", "detail": "Details of the obligation"}
            ],
            "increased_penalties": [
                {"clause": "Clause 2", "old_value": "$100", "new_value": "$500", "detail": "Details of penalty"}
            ],
            "reduced_employee_rights": [
                {"clause": "Clause 3", "severity": "low", "detail": "Details of right"}
            ],
            "hidden_modifications": [
                {"clause": "Clause 4", "risk": "medium", "detail": "Details of modification"}
            ],
            "new_legal_exposure": [
                {"clause": "Clause 5", "severity": "medium", "detail": "Details of exposure"}
            ],
            "recommended_actions": ["Review carefully", "Verify limits"]
        }
    }


def test_parse_diff_from_json_method():
    data = sample_diff_payload()
    resp = MockRespJSON(data)
    parsed = _parse(resp)
    assert parsed == data


def test_parse_diff_from_fenced_text():
    data = sample_diff_payload()
    txt = "Here is the diff analysis:\n```json\n" + json.dumps(data) + "\n```"
    resp = MockRespText(txt)
    parsed = _parse(resp)
    assert parsed == data

