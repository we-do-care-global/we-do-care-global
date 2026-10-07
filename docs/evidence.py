"""
WDCG Evidence Collector — Automated Audit Evidence Gathering
We Do Care Global — Compliance Engine

Automatically collects and validates evidence required for:
- EU AI Act compliance
- NIST AI RMF alignment
- ISO 42001 certification
- Internal governance audits
"""

import json
import hashlib
import os
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from enum import Enum
from datetime import datetime


class EvidenceType(Enum):
    SYSTEM_DESCRIPTION = "system_description"
    INTENDED_USE = "intended_use"
    RISK_ASSESSMENT = "risk_assessment"
    DATA_GOVERNANCE = "data_governance"
    HUMAN_OVERSIGHT = "human_oversight"
    TECHNICAL_DOCUMENTATION = "technical_documentation"
    TEST_RESULTS = "test_results"
    AUDIT_LOG = "audit_log"
    TRAINING_DATA = "training_data"
    MODEL_CARD = "model_card"


class EvidenceStatus(Enum):
    PRESENT = "present"
    MISSING = "missing"
    INCOMPLETE = "incomplete"
    EXPIRED = "expired"


@dataclass
class EvidenceItem:
    """Single evidence item"""
    evidence_id: str
    evidence_type: EvidenceType
    title: str
    description: str
    status: EvidenceStatus
    source: str  # file path, URL, or system
    collected_at: str
    expires_at: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    validation_result: Optional[dict] = None


class EvidenceCollector:
    """Automated evidence collection for compliance audits"""

    # Required evidence by regulation
    REQUIRED_EVIDENCE = {
        "eu_ai_act": {
            "minimal_risk": [
                EvidenceType.SYSTEM_DESCRIPTION,
                EvidenceType.INTENDED_USE,
            ],
            "limited_risk": [
                EvidenceType.SYSTEM_DESCRIPTION,
                EvidenceType.INTENDED_USE,
                EvidenceType.RISK_ASSESSMENT,
                EvidenceType.DATA_GOVERNANCE,
            ],
            "high_risk": [
                EvidenceType.SYSTEM_DESCRIPTION,
                EvidenceType.INTENDED_USE,
                EvidenceType.RISK_ASSESSMENT,
                EvidenceType.DATA_GOVERNANCE,
                EvidenceType.HUMAN_OVERSIGHT,
                EvidenceType.TECHNICAL_DOCUMENTATION,
                EvidenceType.TEST_RESULTS,
                EvidenceType.AUDIT_LOG,
            ],
        },
        "nist_ai_rmf": [
            EvidenceType.SYSTEM_DESCRIPTION,
            EvidenceType.RISK_ASSESSMENT,
            EvidenceType.DATA_GOVERNANCE,
            EvidenceType.HUMAN_OVERSIGHT,
            EvidenceType.AUDIT_LOG,
        ],
        "iso_42001": [
            EvidenceType.SYSTEM_DESCRIPTION,
            EvidenceType.TECHNICAL_DOCUMENTATION,
            EvidenceType.TEST_RESULTS,
            EvidenceType.AUDIT_LOG,
            EvidenceType.TRAINING_DATA,
        ],
    }

    def __init__(self):
        self._evidence: dict[str, EvidenceItem] = {}
        self._collection_log: list[dict] = []

    def collect(
        self,
        agent_id: str,
        regulation: str,
        risk_level: str,
        evidence_sources: Optional[dict] = None,
    ) -> dict:
        """Collect all required evidence for an agent"""
        if regulation not in self.REQUIRED_EVIDENCE:
            raise ValueError(f"Unknown regulation: {regulation}")

        required = self.REQUIRED_EVIDENCE[regulation].get(risk_level, [])
        evidence_sources = evidence_sources or {}

        results = []
        for ev_type in required:
            source = evidence_sources.get(ev_type.value, "")
            item = self._collect_single(agent_id, ev_type, source)
            results.append(item)

        # Log collection
        self._collection_log.append({
            "agent_id": agent_id,
            "regulation": regulation,
            "risk_level": risk_level,
            "collected_at": datetime.utcnow().isoformat(),
            "items": len(results),
        })

        return {
            "agent_id": agent_id,
            "regulation": regulation,
            "risk_level": risk_level,
            "evidence": [asdict(r) for r in results],
            "summary": self._summarize(results),
        }

    def _collect_single(
        self,
        agent_id: str,
        evidence_type: EvidenceType,
        source: str,
    ) -> EvidenceItem:
        """Collect single evidence item"""
        # Check if source exists
        status = EvidenceStatus.MISSING
        if source:
            if source.startswith("http://") or source.startswith("https://"):
                status = EvidenceStatus.PRESENT  # Would validate URL
            elif os.path.exists(source):
                status = EvidenceStatus.PRESENT
            else:
                status = EvidenceStatus.INCOMPLETE

        return EvidenceItem(
            evidence_id=self._generate_id(),
            evidence_type=evidence_type,
            title=evidence_type.value.replace("_", " ").title(),
            description=f"Evidence for {evidence_type.value}",
            status=status,
            source=source or "not provided",
            collected_at=datetime.utcnow().isoformat(),
        )

    def _summarize(self, results: list) -> dict:
        """Summarize evidence collection results"""
        total = len(results)
        present = sum(1 for r in results if r.status == EvidenceStatus.PRESENT)
        missing = sum(1 for r in results if r.status == EvidenceStatus.MISSING)
        incomplete = sum(1 for r in results if r.status == EvidenceStatus.INCOMPLETE)

        return {
            "total_required": total,
            "present": present,
            "missing": missing,
            "incomplete": incomplete,
            "completeness_pct": round(present / max(total, 1) * 100, 1),
            "ready_for_audit": missing == 0 and incomplete == 0,
        }

    def get_evidence(self, evidence_id: str) -> Optional[dict]:
        """Get evidence by ID"""
        item = self._evidence.get(evidence_id)
        return asdict(item) if item else None

    def list_evidence(self, agent_id: Optional[str] = None) -> list:
        """List all evidence"""
        items = list(self._evidence.values())
        return [asdict(i) for i in items]

    def validate_evidence(self, evidence_id: str) -> dict:
        """Validate evidence item"""
        item = self._evidence.get(evidence_id)
        if not item:
            return {"valid": False, "reason": "Evidence not found"}

        # Basic validation
        issues = []
        if item.status == EvidenceStatus.MISSING:
            issues.append("Evidence is missing")
        if item.status == EvidenceStatus.INCOMPLETE:
            issues.append("Evidence is incomplete")
        if item.expires_at and item.expires_at < datetime.utcnow().isoformat():
            issues.append("Evidence has expired")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "evidence_id": evidence_id,
        }

    def export_evidence_package(self, agent_id: str, regulation: str) -> dict:
        """Export complete evidence package for regulatory submission"""
        evidence = [e for e in self._evidence.values() if e.metadata.get("agent_id") == agent_id]

        return {
            "package_id": self._generate_id(),
            "agent_id": agent_id,
            "regulation": regulation,
            "generated_at": datetime.utcnow().isoformat(),
            "evidence_count": len(evidence),
            "evidence": [asdict(e) for e in evidence],
            "manifest": {
                "total_items": len(evidence),
                "valid_items": sum(1 for e in evidence if e.status == EvidenceStatus.PRESENT),
                "regulations": [regulation],
            },
        }

    @staticmethod
    def _generate_id() -> str:
        """Generate unique ID"""
        return hashlib.sha256(f"{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]


# Singleton instance
evidence_collector = EvidenceCollector()
