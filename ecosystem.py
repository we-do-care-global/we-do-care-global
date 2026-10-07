"""
WDCG Ecosystem — Unified Integration Layer
We Do Care Global — All 6 Systems Connected

Provides a single API to:
- Register agents across all systems
- Route tool calls through AgentGuard policies
- Store knowledge in Enterprise Hybrid-RAG
- Monitor via Agent Eval
- Manage secrets via AgentVault
- Orchestrate via FoundationCentar
"""

import os
import json
import hashlib
import requests
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from enum import Enum
from datetime import datetime


class SystemStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


@dataclass
class SystemInfo:
    """Info about a WDCG system"""
    name: str
    url: str
    status: SystemStatus = SystemStatus.UNKNOWN
    version: str = "unknown"
    last_check: str = ""
    capabilities: list = field(default_factory=list)


@dataclass
class AgentRegistration:
    """Agent registered in the ecosystem"""
    agent_id: str
    name: str
    system: str  # Which system owns this agent
    capabilities: list = field(default_factory=list)
    policy: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: dict = field(default_factory=dict)


class WDCEcosystem:
    """Unified WDCG Ecosystem Manager"""

    SYSTEMS = {
        "foundation": {
            "name": "FoundationCentar",
            "url": "https://foundationcentar-demo-rkwero.v2.appdeploy.ai",
            "capabilities": ["orchestration", "multi-agent", "governance"],
        },
        "agentguard": {
            "name": "AgentGuard",
            "url": "https://command-center-agentguard-wallet-os-lz1sg2.v2.appdeploy.ai",
            "capabilities": ["security", "policy", "audit", "kill-switch"],
        },
        "hybrid-rag": {
            "name": "Enterprise Hybrid-RAG",
            "url": "https://we-do-care-global.github.io/enterprise-hybrid-rag/",
            "capabilities": ["retrieval", "embeddings", "evaluation"],
        },
        "agent-eval": {
            "name": "Agent Eval",
            "url": "https://we-do-care-global.github.io/agent-eval/",
            "capabilities": ["metrics", "tracing", "benchmarks"],
        },
        "agentvault": {
            "name": "AgentVault",
            "url": "https://we-do-care-global.github.io/agentvault/",
            "capabilities": ["secrets", "encryption", "zero-trust"],
        },
        "pharma": {
            "name": "Pharma Intelligence OS",
            "url": "https://we-do-care-global.github.io/pharma-intelligence-os/",
            "capabilities": ["pharmacovigilance", "regulatory", "fda"],
        },
    }

    def __init__(self):
        self._agents: dict[str, AgentRegistration] = {}
        self._system_status: dict[str, SystemInfo] = {}
        self._audit_log: list[dict] = []

    def register_agent(
        self,
        agent_id: str,
        name: str,
        system: str,
        capabilities: Optional[list] = None,
        policy: Optional[dict] = None,
        metadata: Optional[dict] = None,
    ) -> AgentRegistration:
        """Register an agent in the ecosystem"""
        if system not in self.SYSTEMS:
            raise ValueError(f"Unknown system: {system}. Available: {list(self.SYSTEMS.keys())}")

        agent = AgentRegistration(
            agent_id=agent_id,
            name=name,
            system=system,
            capabilities=capabilities or [],
            policy=policy or {},
            metadata=metadata or {},
        )
        self._agents[agent_id] = agent

        self._audit_log.append({
            "event": "agent.registered",
            "agent_id": agent_id,
            "system": system,
            "timestamp": datetime.utcnow().isoformat(),
        })

        return agent

    def route_tool_call(
        self,
        agent_id: str,
        tool_name: str,
        input_data: Any = None,
        require_approval: bool = False,
    ) -> dict:
        """Route a tool call through the ecosystem"""
        if agent_id not in self._agents:
            raise ValueError(f"Agent not registered: {agent_id}")

        agent = self._agents[agent_id]

        # Check AgentGuard policy
        policy_check = self._check_policy(agent, tool_name)

        # Log to Agent Eval
        eval_record = {
            "agent_id": agent_id,
            "tool_name": tool_name,
            "system": agent.system,
            "policy_check": policy_check,
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Audit log
        self._audit_log.append({
            "event": "tool_call",
            "agent_id": agent_id,
            "tool_name": tool_name,
            "decision": policy_check["decision"],
            "timestamp": datetime.utcnow().isoformat(),
        })

        return {
            "allowed": policy_check["allowed"],
            "decision": policy_check["decision"],
            "reason": policy_check["reason"],
            "agent": asdict(agent),
            "eval_record": eval_record,
        }

    def _check_policy(self, agent: AgentRegistration, tool_name: str) -> dict:
        """Check if tool call is allowed by policy"""
        policy = agent.policy

        # Check denied tools
        denied = policy.get("denied_tools", [])
        if tool_name in denied:
            return {
                "allowed": False,
                "decision": "denied",
                "reason": f"Tool '{tool_name}' is in denied list",
            }

        # Check allowed tools
        allowed = policy.get("allowed_tools", [])
        if allowed and tool_name not in allowed:
            return {
                "allowed": False,
                "decision": "denied",
                "reason": f"Tool '{tool_name}' is not in allowed list",
            }

        # Check if approval required
        approval_required = policy.get("require_approval", False)
        if approval_required:
            return {
                "allowed": True,
                "decision": "approval",
                "reason": "Human approval required",
            }

        return {
            "allowed": True,
            "decision": "allowed",
            "reason": "Tool allowed by policy",
        }

    def get_system_status(self, system: Optional[str] = None) -> dict:
        """Get status of one or all systems"""
        if system:
            if system not in self.SYSTEMS:
                raise ValueError(f"Unknown system: {system}")
            info = self.SYSTEMS[system]
            return {
                "name": info["name"],
                "url": info["url"],
                "capabilities": info["capabilities"],
                "status": "online",  # Would be checked via health endpoint
            }
        return {
            name: {
                "name": info["name"],
                "url": info["url"],
                "capabilities": info["capabilities"],
                "status": "online",
            }
            for name, info in self.SYSTEMS.items()
        }

    def get_agents(self, system: Optional[str] = None) -> list:
        """Get registered agents, optionally filtered by system"""
        agents = list(self._agents.values())
        if system:
            agents = [a for a in agents if a.system == system]
        return [asdict(a) for a in agents]

    def get_audit_log(self, limit: int = 100) -> list:
        """Get audit log"""
        return self._audit_log[-limit:]

    def summary(self) -> dict:
        """Get ecosystem summary"""
        return {
            "systems": len(self.SYSTEMS),
            "registered_agents": len(self._agents),
            "audit_events": len(self._audit_log),
            "system_status": self.get_system_status(),
            "agents": self.get_agents(),
        }


# Singleton instance
ecosystem = WDCEcosystem()
