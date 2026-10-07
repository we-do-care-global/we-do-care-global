"""
WDCG Ecosystem — Integration Test
Tests all modules: ecosystem, compliance, registry, agent_eval
"""

import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ecosystem import WDCEcosystem, SystemStatus
from compliance import ComplianceEngine, RegulationType, RiskLevel, ComplianceStatus
from registry import AgentRegistry, ProtocolType, AgentStatus
from agent_eval import AgentEval, ToolDecision, ErrorClass


def test_ecosystem():
    """Test ecosystem integration"""
    print("=" * 60)
    print("TEST: Ecosystem Integration")
    print("=" * 60)
    
    eco = WDCEcosystem()
    
    # Register agents
    eco.register_agent("agent-001", "Research Agent", "foundation", ["web_search", "analysis"])
    eco.register_agent("agent-002", "Security Agent", "agentguard", ["policy_check", "audit"])
    
    # Check system status
    status = eco.get_system_status()
    print(f"✓ Systems: {len(status)}")
    
    # Route tool call
    result = eco.route_tool_call("agent-001", "web_search")
    print(f"✓ Tool call routed: {result['decision']}")
    
    # Summary
    summary = eco.summary()
    print(f"✓ Summary: {summary['registered_agents']} agents, {summary['audit_events']} events")
    print()


def test_compliance():
    """Test compliance engine"""
    print("=" * 60)
    print("TEST: Compliance Engine")
    print("=" * 60)
    
    comp = ComplianceEngine()
    
    # Register agent
    agent = comp.register_agent("agent-001", "Test Agent", "foundation", "limited_risk")
    print(f"✓ Agent registered: {agent['agent']['agent_id']}")
    print(f"  Risk level: {agent['agent']['risk_level']}")
    print(f"  Assigned rules: {len(agent['assigned_rules'])}")
    
    # Check compliance
    result = comp.check_compliance("agent-001", "web_search", {
        "system_description": "Test system",
        "intended_use": "Research",
        "risk_assessment": "Low risk",
    })
    print(f"✓ Compliance check: {result['status']}")
    
    # Record usage
    comp.record_usage("agent-001", "web_search", tokens_used=1000, cost_usd=0.05, duration_ms=150)
    print(f"✓ Usage recorded")
    
    # Summary
    summary = comp.get_compliance_summary()
    print(f"✓ Summary: {summary['total_agents']} agents, {summary['total_audit_events']} events")
    print()


def test_registry():
    """Test agent registry"""
    print("=" * 60)
    print("TEST: Agent Registry")
    print("=" * 60)
    
    reg = AgentRegistry()
    
    # Register agents
    reg.register(
        "agent-001",
        "Research Agent",
        "Performs web research",
        "https://agent1.example.com",
        "both",
        ["web_search", "analysis"],
        tags=["research", "external"],
    )
    reg.register(
        "agent-002",
        "Security Agent",
        "Checks security policies",
        "https://agent2.example.com",
        "mcp",
        ["policy_check", "audit"],
        tags=["security", "internal"],
    )
    print(f"✓ Registered 2 agents")
    
    # Discover
    agents = reg.discover(capability="web_search")
    print(f"✓ Discovery: {len(agents)} agents with web_search")
    
    # Route
    best = reg.route("web_search")
    print(f"✓ Routing: {best['name'] if best else 'None'}")
    
    # Stats
    stats = reg.get_stats()
    print(f"✓ Stats: {stats['total_agents']} agents, {stats['capabilities']} capabilities")
    print()


def test_agent_eval():
    """Test agent evaluation"""
    print("=" * 60)
    print("TEST: Agent Evaluation")
    print("=" * 60)
    
    eval = AgentEval()
    
    # Record tool calls
    eval.record_tool_call("web_search", "agent-001", 150, ToolDecision.ALLOWED)
    eval.record_tool_call("file_write", "agent-001", 50, ToolDecision.ALLOWED)
    eval.record_tool_call("send_email", "agent-001", 0, ToolDecision.DENIED, error=ErrorClass.POLICY_VIOLATION)
    print(f"✓ Recorded 3 tool calls")
    
    # Get metrics
    metrics = eval.get_metrics("agent-001")
    print(f"✓ Metrics: {metrics['total_calls']} calls, {metrics['success_rate']:.0%} success")
    
    # Summary
    summary = eval.summary()
    print(f"✓ Summary: {summary['total_calls']} calls, {summary['overall_success_rate']:.0%} success")
    print()


def test_full_integration():
    """Test full ecosystem integration"""
    print("=" * 60)
    print("TEST: Full Integration")
    print("=" * 60)
    
    eco = WDCEcosystem()
    comp = ComplianceEngine()
    reg = AgentRegistry()
    eval = AgentEval()
    
    # Register agent in all systems
    eco.register_agent("agent-001", "Full Test Agent", "foundation", ["web_search", "analysis"])
    comp.register_agent("agent-001", "Full Test Agent", "foundation", "limited_risk")
    reg.register("agent-001", "Full Test Agent", "Test agent", "https://agent.example.com", "both", ["web_search"])
    
    print("✓ Agent registered in all systems")
    
    # Route tool call through ecosystem
    result = eco.route_tool_call("agent-001", "web_search")
    print(f"✓ Ecosystem routing: {result['decision']}")
    
    # Check compliance
    comp_result = comp.check_compliance("agent-001", "web_search", {
        "system_description": "Test",
        "intended_use": "Research",
        "risk_assessment": "Low",
    })
    print(f"✓ Compliance: {comp_result['status']}")
    
    # Record in eval
    eval.record_tool_call("web_search", "agent-001", 150, ToolDecision.ALLOWED)
    print(f"✓ Eval recorded")
    
    # Record usage
    comp.record_usage("agent-001", "web_search", 1000, 0.05, 150)
    print(f"✓ Usage recorded")
    
    print()
    print("=" * 60)
    print("ALL TESTS PASSED ✓")
    print("=" * 60)


if __name__ == "__main__":
    test_ecosystem()
    test_compliance()
    test_registry()
    test_agent_eval()
    test_full_integration()
