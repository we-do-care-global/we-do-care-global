"""
WDCG Agent Registry — A2A/MCP Interoperability
We Do Care Global — Unified Ecosystem

Provides:
- Agent discovery and registration
- A2A (Agent-to-Agent) protocol support
- MCP (Model Context Protocol) integration
- Workload balancing across agents
- Capability-based routing
"""

import json
import hashlib
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
from enum import Enum
from datetime import datetime


class AgentStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BUSY = "busy"
    ERROR = "error"


class ProtocolType(Enum):
    A2A = "a2a"
    MCP = "mcp"
    BOTH = "both"


@dataclass
class AgentCapability:
    """Single agent capability"""
    name: str
    description: str
    input_schema: dict = field(default_factory=dict)
    output_schema: dict = field(default_factory=dict)
    examples: list = field(default_factory=list)


@dataclass
class AgentEndpoint:
    """Agent endpoint info"""
    url: str
    protocol: ProtocolType
    auth_type: str = "none"  # none, api_key, oauth
    rate_limit: int = 100  # requests per minute
    timeout_ms: int = 30000


@dataclass
class RegisteredAgent:
    """Agent registered in the registry"""
    agent_id: str
    name: str
    description: str
    endpoint: AgentEndpoint
    capabilities: list
    status: AgentStatus = AgentStatus.ACTIVE
    registered_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_heartbeat: str = ""
    metadata: dict = field(default_factory=dict)
    tags: list = field(default_factory=list)


class AgentRegistry:
    """WDCG Agent Registry — A2A/MCP Interoperability"""

    def __init__(self):
        self._agents: dict[str, RegisteredAgent] = {}
        self._capability_index: dict[str, list[str]] = {}  # capability -> [agent_ids]
        self._protocol_index: dict[str, list[str]] = {}  # protocol -> [agent_ids]

    def register(
        self,
        agent_id: str,
        name: str,
        description: str,
        url: str,
        protocol: str = "both",
        capabilities: Optional[list] = None,
        auth_type: str = "none",
        rate_limit: int = 100,
        timeout_ms: int = 30000,
        tags: Optional[list] = None,
        metadata: Optional[dict] = None,
    ) -> RegisteredAgent:
        """Register a new agent"""
        if agent_id in self._agents:
            raise ValueError(f"Agent already registered: {agent_id}")

        try:
            protocol_type = ProtocolType(protocol)
        except ValueError:
            raise ValueError(f"Invalid protocol: {protocol}. Use: a2a, mcp, both")

        endpoint = AgentEndpoint(
            url=url,
            protocol=protocol_type,
            auth_type=auth_type,
            rate_limit=rate_limit,
            timeout_ms=timeout_ms,
        )

        agent = RegisteredAgent(
            agent_id=agent_id,
            name=name,
            description=description,
            endpoint=endpoint,
            capabilities=capabilities or [],
            tags=tags or [],
            metadata=metadata or {},
        )

        self._agents[agent_id] = agent

        # Update indexes
        for cap in agent.capabilities:
            if cap not in self._capability_index:
                self._capability_index[cap] = []
            self._capability_index[cap].append(agent_id)

        if protocol_type.value not in self._protocol_index:
            self._protocol_index[protocol_type.value] = []
        self._protocol_index[protocol_type.value].append(agent_id)

        return agent

    def discover(
        self,
        capability: Optional[str] = None,
        protocol: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[list] = None,
    ) -> list:
        """Discover agents by capability, protocol, status, or tags"""
        agents = list(self._agents.values())

        if capability:
            agent_ids = self._capability_index.get(capability, [])
            agents = [self._agents[aid] for aid in agent_ids if aid in self._agents]

        if protocol:
            agent_ids = self._protocol_index.get(protocol, [])
            agents = [a for a in agents if a.agent_id in agent_ids]

        if status:
            agents = [a for a in agents if a.status.value == status]

        if tags:
            agents = [a for a in agents if any(t in a.tags for t in tags)]

        return [asdict(a) for a in agents]

    def route(
        self,
        capability: str,
        protocol: Optional[str] = None,
        exclude_agents: Optional[list] = None,
    ) -> Optional[dict]:
        """Route a request to the best agent for a capability"""
        candidates = self.discover(capability=capability, protocol=protocol, status="active")

        if exclude_agents:
            candidates = [c for c in candidates if c["agent_id"] not in exclude_agents]

        if not candidates:
            return None

        # Simple round-robin (could be enhanced with load balancing)
        # For now, return first available
        return candidates[0]

    def heartbeat(self, agent_id: str, status: str = "active") -> dict:
        """Update agent heartbeat"""
        if agent_id not in self._agents:
            raise ValueError(f"Agent not found: {agent_id}")

        agent = self._agents[agent_id]
        agent.last_heartbeat = datetime.utcnow().isoformat()
        agent.status = AgentStatus(status)

        return asdict(agent)

    def get_agent(self, agent_id: str) -> Optional[dict]:
        """Get agent by ID"""
        agent = self._agents.get(agent_id)
        return asdict(agent) if agent else None

    def list_agents(self) -> list:
        """List all registered agents"""
        return [asdict(a) for a in self._agents.values()]

    def get_stats(self) -> dict:
        """Get registry statistics"""
        agents = list(self._agents.values())
        return {
            "total_agents": len(agents),
            "active": sum(1 for a in agents if a.status == AgentStatus.ACTIVE),
            "inactive": sum(1 for a in agents if a.status == AgentStatus.INACTIVE),
            "busy": sum(1 for a in agents if a.status == AgentStatus.BUSY),
            "error": sum(1 for a in agents if a.status == AgentStatus.ERROR),
            "capabilities": len(self._capability_index),
            "protocols": list(self._protocol_index.keys()),
        }


# Singleton instance
agent_registry = AgentRegistry()
