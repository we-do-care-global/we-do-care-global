"""
WDCG Compliance Engine — AI Governance & Regulatory Automation
We Do Care Global — Unified Ecosystem

Automates:
- EU AI Act compliance mapping
- NIST AI RMF integration
- Automated audit trail
- Per-action usage metering
- Agent Registry (A2A/MCP)
"""

import json
import hashlib
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from enum import Enum
from datetime import datetime


class RiskLevel(Enum):
    MINIMAL = "minimal"
    LIMITED = "limited"
    HIGH = "high"
    UNACCEPTABLE = "unacceptable"


class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PENDING = "pending"
    EXEMPT = "exempt"


class RegulationType(Enum):
    EU_AI_ACT = "eu_ai_act"
    NIST_AI_RMF = "nist_ai_rmf"
    ISO_42001 = "iso_42001"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    SOX = "sox"


@dataclass
class ComplianceRule:
    """Single compliance rule"""
    rule_id: str
    regulation: RegulationType
    category: str
    description: str
    risk_level: RiskLevel
    required_evidence: list
    automated_check: bool = True
    metadata: dict = field(default_factory=dict)


@dataclass
class AuditEvent:
    """Single audit event"""
    event_id: str
    timestamp: str
    agent_id: str
    action: str
    rule_id: str
    status: ComplianceStatus
    evidence: dict
    metadata: dict = field(default_factory=dict)


@dataclass
class UsageRecord:
    """Per-action usage metering"""
    record_id: str
    timestamp: str
    agent_id: str
    action: str
    tokens_used: int
    cost_usd: float
    duration_ms: float
    outcome: str  # success, failure, pending
    metadata: dict = field(default_factory=dict)


class ComplianceEngine:
    """WDCG Compliance Engine — Automated AI Governance"""

    # EU AI Act risk categories
    EU_AI_ACT_CATEGORIES = {
        "prohibited": RiskLevel.UNACCEPTABLE,
        "high_risk": RiskLevel.HIGH,
        "limited_risk": RiskLevel.LIMITED,
        "minimal_risk": RiskLevel.MINIMAL,
    }

    # NIST AI RMF functions
    NIST_RMF_FUNCTIONS = [
        "govern", "map", "measure", "manage"
    ]

    def __init__(self):
        self._rules: dict[str, ComplianceRule] = {}
        self._audit_log: list[AuditEvent] = []
        self._usage_records: list[UsageRecord] = []
        self._agent_registry: dict[str, dict] = {}
        self._initialize_default_rules()

    def _initialize_default_rules(self):
        """Initialize default compliance rules"""
        default_rules = [
            ComplianceRule(
                rule_id="EU-AI-ACT-001",
                regulation=RegulationType.EU_AI_ACT,
                category="prohibited",
                description="AI systems that manipulate human behavior",
                risk_level=RiskLevel.UNACCEPTABLE,
                required_evidence=["system_description", "intended_use", "risk_assessment"],
            ),
            ComplianceRule(
                rule_id="EU-AI-ACT-002",
                regulation=RegulationType.EU_AI_ACT,
                category="high_risk",
                description="AI systems in critical infrastructure",
                risk_level=RiskLevel.HIGH,
                required_evidence=["risk_assessment", "data_governance", "human_oversight"],
            ),
            ComplianceRule(
                rule_id="NIST-RMF-001",
                regulation=RegulationType.NIST_AI_RMF,
                category="govern",
                description="AI risk management framework",
                risk_level=RiskLevel.LIMITED,
                required_evidence=["governance_policy", "risk_tolerance"],
            ),
            ComplianceRule(
                rule_id="ISO-42001-001",
                regulation=RegulationType.ISO_42001,
                category="management",
                description="AI management system requirements",
                risk_level=RiskLevel.LIMITED,
                required_evidence=["management_policy", "continuous_improvement"],
            ),
        ]
        for rule in default_rules:
            self._rules[rule.rule_id] = rule

    def register_agent(
        self,
        agent_id: str,
        name: str,
        system: str,
        risk_category: str = "minimal_risk",
        capabilities: Optional[list] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Register an agent in the compliance registry"""
        if risk_category not in self.EU_AI_ACT_CATEGORIES:
            raise ValueError(f"Invalid risk category: {risk_category}")

        risk_level = self.EU_AI_ACT_CATEGORIES[risk_category]

        agent = {
            "agent_id": agent_id,
            "name": name,
            "system": system,
            "risk_category": risk_category,
            "risk_level": risk_level.value,
            "capabilities": capabilities or [],
            "metadata": metadata or {},
            "registered_at": datetime.utcnow().isoformat(),
            "compliance_status": ComplianceStatus.PENDING.value,
        }
        self._agent_registry[agent_id] = agent

        # Auto-assign compliance rules based on risk level
        assigned_rules = self._assign_rules(risk_level)

        return {
            "agent": agent,
            "assigned_rules": assigned_rules,
            "compliance_status": ComplianceStatus.PENDING.value,
        }

    def _assign_rules(self, risk_level: RiskLevel) -> list:
        """Assign compliance rules based on risk level"""
        rules = []
        for rule in self._rules.values():
            if risk_level == RiskLevel.UNACCEPTABLE:
                rules.append(rule.rule_id)
            elif risk_level == RiskLevel.HIGH and rule.risk_level in [RiskLevel.HIGH, RiskLevel.LIMITED]:
                rules.append(rule.rule_id)
            elif risk_level == RiskLevel.LIMITED and rule.risk_level == RiskLevel.LIMITED:
                rules.append(rule.rule_id)
        return rules

    def check_compliance(
        self,
        agent_id: str,
        action: str,
        evidence: Optional[dict] = None,
    ) -> dict:
        """Check if an action is compliant"""
        if agent_id not in self._agent_registry:
            raise ValueError(f"Agent not registered: {agent_id}")

        agent = self._agent_registry[agent_id]
        assigned_rules = self._assign_rules(RiskLevel(agent["risk_level"]))

        # Check each assigned rule
        results = []
        for rule_id in assigned_rules:
            rule = self._rules.get(rule_id)
            if not rule:
                continue

            # Automated check
            if rule.automated_check:
                check_result = self._automated_check(rule, evidence or {})
                results.append({
                    "rule_id": rule_id,
                    "status": check_result["status"],
                    "reason": check_result["reason"],
                })

        # Determine overall status
        if all(r["status"] == ComplianceStatus.COMPLIANT.value for r in results):
            overall_status = ComplianceStatus.COMPLIANT
        elif any(r["status"] == ComplianceStatus.NON_COMPLIANT.value for r in results):
            overall_status = ComplianceStatus.NON_COMPLIANT
        else:
            overall_status = ComplianceStatus.PENDING

        # Create audit event
        audit_event = AuditEvent(
            event_id=self._generate_id(),
            timestamp=datetime.utcnow().isoformat(),
            agent_id=agent_id,
            action=action,
            rule_id=",".join(assigned_rules),
            status=overall_status,
            evidence=evidence or {},
        )
        self._audit_log.append(audit_event)

        return {
            "agent_id": agent_id,
            "action": action,
            "status": overall_status.value,
            "checks": results,
            "audit_event_id": audit_event.event_id,
        }

    def _automated_check(self, rule: ComplianceRule, evidence: dict) -> dict:
        """Run automated compliance check"""
        # Check if all required evidence is present
        missing = [e for e in rule.required_evidence if e not in evidence]
        if missing:
            return {
                "status": ComplianceStatus.PENDING.value,
                "reason": f"Missing evidence: {', '.join(missing)}",
            }

        return {
            "status": ComplianceStatus.COMPLIANT.value,
            "reason": "All required evidence present",
        }

    def record_usage(
        self,
        agent_id: str,
        action: str,
        tokens_used: int = 0,
        cost_usd: float = 0.0,
        duration_ms: float = 0.0,
        outcome: str = "success",
        metadata: Optional[dict] = None,
    ) -> UsageRecord:
        """Record per-action usage for outcome-based pricing"""
        record = UsageRecord(
            record_id=self._generate_id(),
            timestamp=datetime.utcnow().isoformat(),
            agent_id=agent_id,
            action=action,
            tokens_used=tokens_used,
            cost_usd=cost_usd,
            duration_ms=duration_ms,
            outcome=outcome,
            metadata=metadata or {},
        )
        self._usage_records.append(record)
        return record

    def get_audit_trail(
        self,
        agent_id: Optional[str] = None,
        regulation: Optional[RegulationType] = None,
        limit: int = 100,
    ) -> list:
        """Get audit trail with optional filtering"""
        events = self._audit_log
        if agent_id:
            events = [e for e in events if e.agent_id == agent_id]
        if regulation:
            events = [e for e in events if any(
                self._rules.get(r.rule_id, ComplianceRule("", regulation, "", "", RiskLevel.MINIMAL, [])).regulation == regulation
                for r in [type("Rule", (), {"rule_id": rid}) for rid in e.rule_id.split(",")]
            )]
        return [asdict(e) for e in events[-limit:]]

    def get_usage_report(
        self,
        agent_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> dict:
        """Get usage report for outcome-based pricing"""
        records = self._usage_records
        if agent_id:
            records = [r for r in records if r.agent_id == agent_id]
        if start_time:
            records = [r for r in records if r.timestamp >= start_time]
        if end_time:
            records = [r for r in records if r.timestamp <= end_time]

        total_tokens = sum(r.tokens_used for r in records)
        total_cost = sum(r.cost_usd for r in records)
        total_duration = sum(r.duration_ms for r in records)
        success_count = sum(1 for r in records if r.outcome == "success")
        failure_count = sum(1 for r in records if r.outcome == "failure")

        return {
            "total_actions": len(records),
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 4),
            "total_duration_ms": round(total_duration, 2),
            "success_rate": round(success_count / max(len(records), 1), 4),
            "failure_count": failure_count,
            "records": [asdict(r) for r in records[-100:]],
        }

    def get_compliance_summary(self) -> dict:
        """Get compliance summary across all agents"""
        agents = list(self._agent_registry.values())
        total_agents = len(agents)
        compliant = sum(1 for a in agents if a["compliance_status"] == ComplianceStatus.COMPLIANT.value)
        non_compliant = sum(1 for a in agents if a["compliance_status"] == ComplianceStatus.NON_COMPLIANT.value)
        pending = sum(1 for a in agents if a["compliance_status"] == ComplianceStatus.PENDING.value)

        return {
            "total_agents": total_agents,
            "compliant": compliant,
            "non_compliant": non_compliant,
            "pending": pending,
            "compliance_rate": round(compliant / max(total_agents, 1), 4),
            "total_audit_events": len(self._audit_log),
            "total_usage_records": len(self._usage_records),
            "agents": agents,
        }

    def export_audit_report(self, format: str = "json") -> str:
        """Export audit report for regulatory submission"""
        summary = self.get_compliance_summary()
        audit_trail = self.get_audit_trail(limit=1000)
        usage_report = self.get_usage_report()

        report = {
            "report_id": self._generate_id(),
            "generated_at": datetime.utcnow().isoformat(),
            "compliance_summary": summary,
            "audit_trail": audit_trail,
            "usage_report": usage_report,
            "regulations": [r.value for r in RegulationType],
            "standards": ["EU AI Act", "NIST AI RMF", "ISO 42001"],
        }

        if format == "json":
            return json.dumps(report, indent=2)
        return str(report)

    @staticmethod
    def _generate_id() -> str:
        """Generate unique ID"""
        return hashlib.sha256(f"{time.time()}{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]


# Singleton instance
compliance_engine = ComplianceEngine()
