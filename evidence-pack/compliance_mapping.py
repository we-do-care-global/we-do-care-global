#!/usr/bin/env python3
"""
AgentProof Evidence Pack — Compliance Mapping Engine
=====================================================
Maps agentproof ExecutionBlock + Ed25519 Merkle chain to:
- SOC 2 Trust Services Criteria
- ISO 27001 Annex A controls
- EU AI Act requirements
- NIST AI RMF functions

Every execution block becomes a compliance evidence artifact.
"""

import json
import hashlib
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from enum import Enum
from datetime import datetime


class ComplianceFramework(Enum):
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    EU_AI_ACT = "eu_ai_act"
    NIST_AI_RMF = "nist_ai_rmf"


class ControlStatus(Enum):
    SATISFIED = "satisfied"
    PARTIAL = "partial"
    NOT_SATISFIED = "not_satisfied"
    NOT_APPLICABLE = "not_applicable"


# SOC 2 Trust Services Criteria mapping
SOC2_CONTROLS = {
    "CC6.1": {
        "title": "Logical and Physical Access Controls",
        "description": "The entity implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events.",
        "agentproof_mapping": "ExecutionBlock.agent_id + policy_context -> access control evidence",
        "evidence_fields": ["agent_id", "policy_context", "invocation"],
    },
    "CC6.2": {
        "title": "User Access Management",
        "description": "The entity restricts access to authorized users and devices.",
        "agentproof_mapping": "ExecutionBlock.invocation -> user action evidence",
        "evidence_fields": ["invocation", "telemetry"],
    },
    "CC6.3": {
        "title": "Access Removal",
        "description": "The entity removes access to protected information assets when no longer needed.",
        "agentproof_mapping": "Merkle chain integrity -> access lifecycle evidence",
        "evidence_fields": ["merkle_root", "prev_hash"],
    },
    "CC7.1": {
        "title": "Security Incident Detection",
        "description": "The entity detects and responds to security incidents.",
        "agentproof_mapping": "ExecutionBlock.telemetry -> anomaly detection evidence",
        "evidence_fields": ["telemetry", "execution_id"],
    },
    "CC7.2": {
        "title": "Incident Response",
        "description": "The entity responds to identified security incidents.",
        "agentproof_mapping": "Ed25519 signature -> non-repudiation evidence",
        "evidence_fields": ["signature", "timestamp_ns"],
    },
    "CC8.1": {
        "title": "Change Management",
        "description": "The entity authorizes, designs, develops, and changes infrastructure and software.",
        "agentproof_mapping": "ExecutionBlock.version -> change tracking evidence",
        "evidence_fields": ["version", "execution_id"],
    },
}

# ISO 27001 Annex A controls mapping
ISO27001_CONTROLS = {
    "A.8.1": {
        "title": "User Endpoint Devices",
        "description": "Information and information processing facilities shall be protected from unauthorized access.",
        "agentproof_mapping": "ExecutionBlock.agent_id -> device/agent identification",
        "evidence_fields": ["agent_id", "policy_context"],
    },
    "A.8.2": {
        "title": "Privileged Access Rights",
        "description": "The allocation and use of privileged access rights shall be restricted and controlled.",
        "agentproof_mapping": "ExecutionBlock.policy_context -> privilege evidence",
        "evidence_fields": ["policy_context", "invocation"],
    },
    "A.8.3": {
        "title": "Information Access Restriction",
        "description": "Access to information and application system functions shall be restricted in accordance with the established access control policy.",
        "agentproof_mapping": "Merkle chain -> access audit trail",
        "evidence_fields": ["merkle_root", "prev_hash"],
    },
    "A.8.4": {
        "title": "Access to Source Code",
        "description": "Access to source code shall be restricted to authorized personnel.",
        "agentproof_mapping": "Ed25519 signature -> code integrity evidence",
        "evidence_fields": ["signature", "timestamp_ns"],
    },
    "A.8.11": {
        "title": "Data Masking",
        "description": "Data masking shall be used in accordance with the established access control policy.",
        "agentproof_mapping": "ExecutionBlock.telemetry -> data handling evidence",
        "evidence_fields": ["telemetry"],
    },
    "A.8.12": {
        "title": "Data Leakage Prevention",
        "description": "Data leakage prevention measures shall be applied to systems, networks, and devices.",
        "agentproof_mapping": "Merkle chain integrity -> data flow evidence",
        "evidence_fields": ["merkle_root", "prev_hash"],
    },
}

# EU AI Act requirements mapping
EU_AI_ACT_CONTROLS = {
    "Article 9": {
        "title": "Risk Management System",
        "description": "A risk management system shall be established, implemented, documented and maintained.",
        "agentproof_mapping": "ExecutionBlock.policy_context -> risk assessment evidence",
        "evidence_fields": ["policy_context", "invocation"],
    },
    "Article 10": {
        "title": "Data Governance",
        "description": "Training, validation and testing data sets shall be relevant, representative, and respect data protection.",
        "agentproof_mapping": "ExecutionBlock.telemetry -> data lineage evidence",
        "evidence_fields": ["telemetry", "execution_id"],
    },
    "Article 11": {
        "title": "Technical Documentation",
        "description": "Technical documentation shall be kept up to date and made available to authorities.",
        "agentproof_mapping": "ExecutionBlock.version -> documentation version evidence",
        "evidence_fields": ["version", "execution_id"],
    },
    "Article 12": {
        "title": "Record Keeping",
        "description": "AI systems shall automatically record events (logs) over their lifetime.",
        "agentproof_mapping": "Merkle chain -> immutable audit log",
        "evidence_fields": ["merkle_root", "prev_hash", "timestamp_ns"],
    },
    "Article 13": {
        "title": "Transparency and Provision of Information",
        "description": "AI systems shall be designed to provide clear and meaningful information to users.",
        "agentproof_mapping": "ExecutionBlock.invocation -> user interaction evidence",
        "evidence_fields": ["invocation", "telemetry"],
    },
    "Article 14": {
        "title": "Human Oversight",
        "description": "AI systems shall be designed to allow effective human oversight.",
        "agentproof_mapping": "ExecutionBlock.policy_context -> oversight evidence",
        "evidence_fields": ["policy_context", "invocation"],
    },
    "Article 15": {
        "title": "Accuracy, Robustness and Cybersecurity",
        "description": "AI systems shall be accurate, robust and secure.",
        "agentproof_mapping": "Ed25519 signature -> integrity evidence",
        "evidence_fields": ["signature", "timestamp_ns"],
    },
}

# NIST AI RMF functions mapping
NIST_AI_RMF_CONTROLS = {
    "GOVERN": {
        "title": "Govern",
        "description": "Policies, procedures, and processes are in place to manage AI risk.",
        "agentproof_mapping": "ExecutionBlock.policy_context -> governance evidence",
        "evidence_fields": ["policy_context", "invocation"],
    },
    "MAP": {
        "title": "Map",
        "description": "Context and impacts of AI systems are identified and documented.",
        "agentproof_mapping": "ExecutionBlock.telemetry -> context evidence",
        "evidence_fields": ["telemetry", "execution_id"],
    },
    "MEASURE": {
        "title": "Measure",
        "description": "AI risks are assessed and measured.",
        "agentproof_mapping": "Merkle chain -> measurement evidence",
        "evidence_fields": ["merkle_root", "prev_hash"],
    },
    "MANAGE": {
        "title": "Manage",
        "description": "AI risks are managed and monitored.",
        "agentproof_mapping": "Ed25519 signature -> management evidence",
        "evidence_fields": ["signature", "timestamp_ns"],
    },
}


@dataclass
class ComplianceEvidence:
    """Single compliance evidence item"""
    evidence_id: str
    framework: ComplianceFramework
    control_id: str
    control_title: str
    status: ControlStatus
    agentproof_field: str
    evidence_value: str
    timestamp: str
    metadata: dict = field(default_factory=dict)


class ComplianceMapper:
    """Maps agentproof ExecutionBlock to compliance controls"""

    FRAMEWORK_CONTROLS = {
        ComplianceFramework.SOC2: SOC2_CONTROLS,
        ComplianceFramework.ISO27001: ISO27001_CONTROLS,
        ComplianceFramework.EU_AI_ACT: EU_AI_ACT_CONTROLS,
        ComplianceFramework.NIST_AI_RMF: NIST_AI_RMF_CONTROLS,
    }

    def __init__(self):
        self.evidence: list[ComplianceEvidence] = []

    def map_execution_block(self, block: dict) -> list[ComplianceEvidence]:
        """Map a single ExecutionBlock to all compliance frameworks"""
        results = []
        for framework, controls in self.FRAMEWORK_CONTROLS.items():
            for control_id, control in controls.items():
                evidence = self._create_evidence(framework, control_id, control, block)
                results.append(evidence)
        return results

    def _create_evidence(
        self,
        framework: ComplianceFramework,
        control_id: str,
        control: dict,
        block: dict,
    ) -> ComplianceEvidence:
        """Create compliance evidence from ExecutionBlock"""
        # Extract relevant fields from block
        evidence_values = []
        for field_name in control["evidence_fields"]:
            value = block.get(field_name, "N/A")
            evidence_values.append(f"{field_name}={value}")

        evidence_value = "; ".join(evidence_values)

        # Determine status based on field presence
        status = ControlStatus.SATISFIED
        for field_name in control["evidence_fields"]:
            if field_name not in block or block[field_name] == "N/A":
                status = ControlStatus.PARTIAL
                break

        return ComplianceEvidence(
            evidence_id=f"{framework.value}:{control_id}",
            framework=framework,
            control_id=control_id,
            control_title=control["title"],
            status=status,
            agentproof_field=", ".join(control["evidence_fields"]),
            evidence_value=evidence_value,
            timestamp=datetime.utcnow().isoformat() + "Z",
            metadata={
                "mapping": control["agentproof_mapping"],
                "description": control["description"],
            },
        )

    def generate_evidence_pack(self, blocks: list) -> dict:
        """Generate full evidence pack from multiple ExecutionBlocks"""
        all_evidence = []
        for block in blocks:
            all_evidence.extend(self.map_execution_block(block))

        # Group by framework
        by_framework = {}
        for framework in ComplianceFramework:
            framework_evidence = [e for e in all_evidence if e.framework == framework]
            by_framework[framework.value] = {
                "total_controls": len(framework_evidence),
                "satisfied": len([e for e in framework_evidence if e.status == ControlStatus.SATISFIED]),
                "partial": len([e for e in framework_evidence if e.status == ControlStatus.PARTIAL]),
                "not_satisfied": len([e for e in framework_evidence if e.status == ControlStatus.NOT_SATISFIED]),
                "evidence": [asdict(e) for e in framework_evidence],
            }

        # Convert enums to strings for JSON serialization
        serializable_frameworks = {}
        for fw_name, fw_data in by_framework.items():
            serializable_frameworks[fw_name] = {
                **fw_data,
                "evidence": [
                    {
                        **asdict(e),
                        "framework": e.framework.value,
                        "status": e.status.value,
                    }
                    for e in fw_data["evidence"]
                ],
            }

        return {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "total_blocks": len(blocks),
            "total_evidence_items": len(all_evidence),
            "frameworks": serializable_frameworks,
        }


def main():
    """Demo: map sample ExecutionBlock to compliance evidence"""
    sample_block = {
        "version": "1.0",
        "execution_id": "exec-001",
        "prev_hash": "abc123",
        "timestamp_ns": "1696156800000000000",
        "agent_id": "agentguard-01",
        "policy_context": {"risk_level": "high", "oversight": "required"},
        "invocation": {"tool": "file_read", "path": "/data/file.txt"},
        "telemetry": {"tokens": 150, "duration_ms": 250},
        "merkle_root": "def456",
        "signature": "ed25519-sig-xyz",
    }

    mapper = ComplianceMapper()
    evidence_pack = mapper.generate_evidence_pack([sample_block])

    print(json.dumps(evidence_pack, indent=2))


if __name__ == "__main__":
    main()
