import pytest
from simulation.team_registry import TeamRegistry
from simulation.sprint_manager import SprintManager
from simulation.organization_memory import OrganizationMemory
from simulation.rfc_engine import RFCEngine
from simulation.conflict_resolver import ConflictResolver
from simulation.hiring_engine import HiringEngine
from simulation.velocity_engine import VelocityEngine
from simulation.backlog_manager import BacklogManager
from simulation.performance_engine import PerformanceEngine

def test_capacity_calculation():
    registry = TeamRegistry()
    registry.register_team("t1", {})
    registry.assign_member("t1", {"id": "m1", "story_points": 20})
    registry.assign_member("t1", {"id": "m2", "story_points": 20})
    
    assert registry.compute_capacity("t1") == 40
    
def test_sprint_assignment():
    registry = TeamRegistry()
    registry.register_team("t1", {})
    registry.assign_member("t1", {"id": "m1", "story_points": 40})
    
    manager = SprintManager(registry)
    sprint = manager.create_sprint("t1")
    
    backlog = [{"story_points": 20}, {"story_points": 30}]
    manager.assign_work(sprint["start_date"], backlog)
    
    # Capacity is 40, first task takes 20, leaving 20. Second task takes 30, so it shouldn't fit.
    assert len(manager.active_sprints[sprint["start_date"]]["tasks"]) == 1

def test_rfc_generation():
    memory = OrganizationMemory()
    engine = RFCEngine(memory)
    rfc = engine.generate_rfc("Sync", "Offline mode", ["Queue"], [], [])
    assert rfc["status"] == "Pending review"

def test_conflict_resolution():
    memory = OrganizationMemory()
    resolver = ConflictResolver(memory)
    # If options are provided, and conflict is detected, uses strategy
    resolution = resolver.resolve_conflict("DB Choice", ["PostgreSQL", "Kafka"], "cost optimization")
    assert resolution["decision"] == "Use PostgreSQL outbox."

def test_hiring_recommendation():
    memory = OrganizationMemory()
    registry = TeamRegistry()
    registry.register_team("t1", {})
    backlog = BacklogManager()
    for _ in range(10): backlog.add_item({"story_points": 10}) # 100 points
    
    # 0 members, capacity 0
    velocity = VelocityEngine(memory)
    hiring = HiringEngine(registry, backlog, velocity)
    
    # Need to fake velocity trend declining
    # ... mock out velocity.detect_slowdowns to return -0.1
    velocity.detect_slowdowns = lambda t: -0.1
    
    rec = hiring.recommend_hires("t1")
    assert rec is not None

def test_team_health():
    memory = OrganizationMemory()
    registry = TeamRegistry()
    registry.register_team("t1", {})
    velocity = VelocityEngine(memory)
    
    velocity.compute_velocity = lambda t: 50.0
    velocity.predict_burnout = lambda t: 0.1
    
    engine = PerformanceEngine(velocity, registry)
    health = engine.evaluate_team("t1")
    assert health > 0.5
