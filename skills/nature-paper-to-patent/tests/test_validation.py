import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_patent_draft", ROOT / "scripts" / "validate_patent_draft.py"
)
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


def valid_draft():
    return {
        "title": "\u4e00\u79cd\u5de5\u4e1a\u56fe\u50cf\u7f3a\u9677\u68c0\u6d4b\u65b9\u6cd5",
        "metadata": {"draft_status": "\u4f9b\u590d\u6838"},
        "source_analysis": {
            "contains_core_formulas": True,
            "contains_methodology_figures": False,
        },
        "source_map": [
            {"id": "P001", "type": "paper-text", "locator": "\u7b2c3\u9875", "summary": "\u6d41\u7a0b"},
            {"id": "E001", "type": "equation", "locator": "\u7b2c4\u9875\u516c\u5f0f1", "summary": "\u878d\u5408"},
        ],
        "terminology_ledger": [
            {
                "concept": "\u878d\u5408\u7279\u5f81",
                "canonical_zh": "\u878d\u5408\u7279\u5f81",
                "source_terms": ["fused feature"],
                "forbidden_aliases": [],
            }
        ],
        "formula_inventory": [
            {
                "source_id": "E001",
                "source_number": "(1)",
                "technical_role": "\u878d\u5408\u4e0d\u540c\u5c3a\u5ea6\u7279\u5f81",
                "disposition": "specification-equation-1",
            }
        ],
        "figure_inventory": [
            {
                "source_id": "P001",
                "source_number": "\u65b9\u6cd5\u7ae0\u8282",
                "type": "flowchart",
                "disposition": "redraw-as-figure-1",
            }
        ],
        "evidence_ledger": [
            {
                "id": "EV1",
                "feature": "\u591a\u5c3a\u5ea6\u7279\u5f81\u878d\u5408",
                "source_ids": ["P001", "E001"],
                "support_status": "explicit",
            }
        ],
        "claims": [
            {
                "number": 1,
                "text": "\u4e00\u79cd\u5de5\u4e1a\u56fe\u50cf\u7f3a\u9677\u68c0\u6d4b\u65b9\u6cd5，\u5176\u7279\u5f81\u5728\u4e8e，\u5305\u62ec：S1，\u83b7\u53d6\u5de5\u4e1a\u56fe\u50cf；S2，\u5bf9\u5de5\u4e1a\u56fe\u50cf\u8fdb\u884c\u591a\u5c3a\u5ea6\u7279\u5f81\u878d\u5408；S3，\u6839\u636e\u878d\u5408\u7279\u5f81\u8f93\u51fa\u7f3a\u9677\u68c0\u6d4b\u7ed3\u679c。",
            }
        ],
        "claim_feature_map": [
            {"claim_number": 1, "feature": "\u591a\u5c3a\u5ea6\u7279\u5f81\u878d\u5408", "evidence_ids": ["EV1"]}
        ],
        "abstract_figure_number": 1,
        "figures": [
            {
                "number": 1,
                "title": "\u65b9\u6cd5\u6d41\u7a0b\u56fe",
                "type": "flowchart",
                "orientation": "vertical",
                "claim_number": 1,
                "complete_claim_flow": True,
                "source_ids": ["P001"],
                "nodes": [
                    {"id": "S1", "label": "S1：\u83b7\u53d6\u5de5\u4e1a\u56fe\u50cf", "claim_step": "S1"},
                    {
                        "id": "S2",
                        "label": "S2：\u8fdb\u884c\u591a\u5c3a\u5ea6\u7279\u5f81\u878d\u5408",
                        "claim_step": "S2",
                    },
                    {
                        "id": "S3",
                        "label": "S3：\u8f93\u51fa\u7f3a\u9677\u68c0\u6d4b\u7ed3\u679c",
                        "claim_step": "S3",
                    },
                ],
                "edges": [{"from": "S1", "to": "S2"}, {"from": "S2", "to": "S3"}],
            }
        ],
        "specification": {
            "technical_field": ["\u672c\u53d1\u660e\u6d89\u53ca\u5de5\u4e1a\u89c6\u89c9\u68c0\u6d4b\u9886\u57df。"],
            "background": ["\u73b0\u6709\u65b9\u6cd5\u5bf9\u5c0f\u7f3a\u9677\u8868\u5f81\u4e0d\u8db3。"],
            "invention_content": {
                "problem": ["\u63d0\u9ad8\u5c0f\u7f3a\u9677\u68c0\u6d4b\u80fd\u529b。"],
                "solution": ["\u91c7\u7528\u591a\u5c3a\u5ea6\u7279\u5f81\u878d\u5408。"],
                "beneficial_effects": ["\u4fdd\u7559\u4e0d\u540c\u5c3a\u5ea6\u7684\u7f3a\u9677\u4fe1\u606f。"],
            },
            "figure_descriptions": ["\u56fe1\u4e3a\u65b9\u6cd5\u6d41\u7a0b\u56fe。"],
            "equations": [
                {
                    "number": 1,
                    "source_ids": ["E001"],
                    "latex": "F=F_1+F_2",
                    "expression": "F=F1+F2",
                    "symbols": [
                        {"symbol": "F", "meaning": "\u878d\u5408\u7279\u5f81"},
                        {"symbol": "F_1", "meaning": "\u7b2c\u4e00\u5c3a\u5ea6\u7279\u5f81"},
                    ],
                    "technical_role": "\u878d\u5408\u4e0d\u540c\u5c3a\u5ea6\u7279\u5f81",
                    "description": "\u5176\u4e2d，F\u8868\u793a\u878d\u5408\u7279\u5f81，F1\u548cF2\u8868\u793a\u4e0d\u540c\u5c3a\u5ea6\u7279\u5f81。",
                }
            ],
            "embodiments": [{"heading": "\u5b9e\u65bd\u4f8b1", "paragraphs": ["\u6267\u884c\u4e0a\u8ff0\u6b65\u9aa4。"]}],
        },
        "abstract": "\u672c\u53d1\u660e\u516c\u5f00\u4e00\u79cd\u5de5\u4e1a\u56fe\u50cf\u7f3a\u9677\u68c0\u6d4b\u65b9\u6cd5，\u901a\u8fc7\u591a\u5c3a\u5ea6\u7279\u5f81\u878d\u5408\u8f93\u51fa\u7f3a\u9677\u68c0\u6d4b\u7ed3\u679c。",
        "quality_assessment": {
            "status": "review-draft",
            "scores": {
                "evidence_support": {"score": 4, "evidence": "\u7279\u5f81\u5747\u6709\u6765\u6e90。"},
                "claim_architecture": {"score": 4, "evidence": "\u6280\u672f\u94fe\u95ed\u5408。"},
                "terminology_consistency": {"score": 4, "evidence": "\u672f\u8bed\u4e00\u81f4。"},
                "enablement_detail": {"score": 3, "evidence": "\u5df2\u8bf4\u660e\u4e3b\u8981\u6b65\u9aa4。"},
                "technical_effect_reasoning": {"score": 3, "evidence": "\u6548\u679c\u5173\u8054\u624b\u6bb5。"},
                "formula_coverage": {"score": 4, "evidence": "\u6838\u5fc3\u516c\u5f0f\u5df2\u6536\u5f55。"},
                "figure_alignment": {"score": 4, "evidence": "\u9644\u56fe\u4e0e\u6b65\u9aa4\u4e00\u81f4。"},
            }
        },
    }


class DraftValidationTests(unittest.TestCase):
    def test_valid_draft_passes(self):
        self.assertEqual([], VALIDATOR.validate(valid_draft()))

    def test_unmapped_claim_fails(self):
        draft = valid_draft()
        draft["claim_feature_map"] = []
        codes = {item.code for item in VALIDATOR.validate(draft)}
        self.assertIn("CLAIM_NOT_MAPPED", codes)

    def test_missing_core_equation_fails(self):
        draft = valid_draft()
        draft["specification"]["equations"] = []
        codes = {item.code for item in VALIDATOR.validate(draft)}
        self.assertIn("MISSING_CORE_EQUATIONS", codes)


if __name__ == "__main__":
    unittest.main()
