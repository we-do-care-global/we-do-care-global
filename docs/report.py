"""
WDCG Report Generator — Regulatory Audit Report Generator
We Do Care Global — Compliance Engine

Generates audit-ready reports for:
- EU AI Act compliance
- NIST AI RMF alignment
- ISO 42001 certification
- Internal governance reviews
"""

import json
import hashlib
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from datetime import datetime


@dataclass
class ReportSection:
    """Single report section"""
    title: str
    content: str
    status: str  # pass, fail, warning, info
    evidence: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)


@dataclass
class AuditReport:
    """Complete audit report"""
    report_id: str
    agent_id: str
    regulation: str
    generated_at: str
    overall_score: float
    overall_status: str
    sections: list
    summary: dict
    recommendations: list
    metadata: dict = field(default_factory=dict)


class ReportGenerator:
    """Generate regulatory audit reports"""

    def __init__(self):
        self._reports: dict[str, AuditReport] = {}

    def generate(
        self,
        agent_id: str,
        regulation: str,
        compliance_result: dict,
        evidence_result: dict,
        usage_result: Optional[dict] = None,
    ) -> AuditReport:
        """Generate complete audit report"""
        sections = []

        # Section 1: Executive Summary
        sections.append(self._exec_summary(agent_id, regulation, compliance_result, evidence_result))

        # Section 2: Compliance Status
        sections.append(self._compliance_section(compliance_result))

        # Section 3: Evidence Status
        sections.append(self._evidence_section(evidence_result))

        # Section 4: Usage & Cost
        if usage_result:
            sections.append(self._usage_section(usage_result))

        # Section 5: Recommendations
        recommendations = self._generate_recommendations(compliance_result, evidence_result)
        sections.append(self._recommendations_section(recommendations))

        # Calculate overall score
        score = self._calculate_score(sections)
        status = self._determine_status(score)

        report = AuditReport(
            report_id=self._generate_id(),
            agent_id=agent_id,
            regulation=regulation,
            generated_at=datetime.utcnow().isoformat(),
            overall_score=score,
            overall_status=status,
            sections=[asdict(s) for s in sections],
            summary={
                "total_sections": len(sections),
                "passed": sum(1 for s in sections if s.status == "pass"),
                "failed": sum(1 for s in sections if s.status == "fail"),
                "warnings": sum(1 for s in sections if s.status == "warning"),
            },
            recommendations=recommendations,
        )

        self._reports[report.report_id] = report
        return report

    def _exec_summary(self, agent_id, regulation, compliance, evidence) -> ReportSection:
        """Executive summary section"""
        score = evidence.get("summary", {}).get("completeness_pct", 0)
        status = "pass" if score >= 80 else "warning" if score >= 50 else "fail"

        content = f"""Agent: {agent_id}
Regulation: {regulation}
Generated: {datetime.utcnow().isoformat()}
Evidence Completeness: {score}%
Compliance Status: {compliance.get("status", "unknown")}
"""

        return ReportSection(
            title="Executive Summary",
            content=content,
            status=status,
            evidence=evidence.get("evidence", []),
        )

    def _compliance_section(self, compliance) -> ReportSection:
        """Compliance status section"""
        checks = compliance.get("checks", [])
        passed = sum(1 for c in checks if c.get("status") == "compliant")
        total = len(checks)

        status = "pass" if passed == total else "warning" if passed > 0 else "fail"

        content = f"""Compliance Checks: {passed}/{total} passed
Overall Status: {compliance.get("status", "unknown")}
"""

        return ReportSection(
            title="Compliance Status",
            content=content,
            status=status,
            evidence=checks,
        )

    def _evidence_section(self, evidence) -> ReportSection:
        """Evidence status section"""
        summary = evidence.get("summary", {})
        completeness = summary.get("completeness_pct", 0)
        status = "pass" if completeness >= 80 else "warning" if completeness >= 50 else "fail"

        content = f"""Evidence Completeness: {completeness}%
Present: {summary.get("present", 0)}
Missing: {summary.get("missing", 0)}
Incomplete: {summary.get("incomplete", 0)}
Ready for Audit: {summary.get("ready_for_audit", False)}
"""

        return ReportSection(
            title="Evidence Status",
            content=content,
            status=status,
            evidence=evidence.get("evidence", []),
        )

    def _usage_section(self, usage) -> ReportSection:
        """Usage and cost section"""
        content = f"""Total Actions: {usage.get("total_actions", 0)}
Total Tokens: {usage.get("total_tokens", 0)}
Total Cost: ${usage.get("total_cost_usd", 0):.4f}
Success Rate: {usage.get("success_rate", 0):.0%}
"""

        return ReportSection(
            title="Usage & Cost",
            content=content,
            status="info",
        )

    def _recommendations_section(self, recommendations) -> ReportSection:
        """Recommendations section"""
        content = "\n".join(f"- {r}" for r in recommendations) if recommendations else "No recommendations."

        return ReportSection(
            title="Recommendations",
            content=content,
            status="info",
            recommendations=recommendations,
        )

    def _generate_recommendations(self, compliance, evidence) -> list:
        """Generate recommendations based on results"""
        recs = []

        # Evidence recommendations
        summary = evidence.get("summary", {})
        if summary.get("missing", 0) > 0:
            recs.append(f"Provide {summary['missing']} missing evidence items")
        if summary.get("incomplete", 0) > 0:
            recs.append(f"Complete {summary['incomplete']} incomplete evidence items")

        # Compliance recommendations
        checks = compliance.get("checks", [])
        for check in checks:
            if check.get("status") != "compliant":
                recs.append(f"Address compliance issue: {check.get('reason', 'Unknown')}")

        return recs

    def _calculate_score(self, sections) -> float:
        """Calculate overall score"""
        weights = {"pass": 100, "warning": 50, "fail": 0, "info": 100}
        total = sum(weights.get(s.status, 0) for s in sections)
        return round(total / max(len(sections), 1), 1)

    def _determine_status(self, score) -> str:
        """Determine overall status"""
        if score >= 80:
            return "compliant"
        elif score >= 50:
            return "pending"
        else:
            return "non_compliant"

    def export_json(self, report_id: str) -> str:
        """Export report as JSON"""
        report = self._reports.get(report_id)
        if not report:
            raise ValueError(f"Report not found: {report_id}")
        return json.dumps(asdict(report), indent=2)

    def export_markdown(self, report_id: str) -> str:
        """Export report as Markdown"""
        report = self._reports.get(report_id)
        if not report:
            raise ValueError(f"Report not found: {report_id}")

        md = f"""# WDCG Audit Report

**Report ID:** {report.report_id}
**Agent:** {report.agent_id}
**Regulation:** {report.regulation}
**Generated:** {report.generated_at}
**Overall Score:** {report.overall_score}/100
**Status:** {report.overall_status}

---

"""

        for section in report.sections:
            icon = "✅" if section.status == "pass" else "⚠️" if section.status == "warning" else "❌" if section.status == "fail" else "ℹ️"
            md += f"## {icon} {section.title}\n\n{section.content}\n\n"

        if report.recommendations:
            md += "## Recommendations\n\n"
            for rec in report.recommendations:
                md += f"- {rec}\n"
            md += "\n"

        md += f"""---

*Generated by WDCG Compliance Engine*
*We Do Care Global — Sarajevo, Bosnia and Herzegovina*
*ORCID: 0009-0009-8515-2727*
"""

        return md

    def get_report(self, report_id: str) -> Optional[dict]:
        """Get report by ID"""
        report = self._reports.get(report_id)
        return asdict(report) if report else None

    def list_reports(self) -> list:
        """List all reports"""
        return [asdict(r) for r in self._reports.values()]

    @staticmethod
    def _generate_id() -> str:
        """Generate unique ID"""
        return hashlib.sha256(f"{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]


# Singleton instance
report_generator = ReportGenerator()
