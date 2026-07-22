from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMessageTermination, MaxMessageTermination

from agents.planner_node import PlannerAgentNode
from agents.database_agent import DatabaseAgent
from agents.backend_agent import BackendAgent
from agents.frontend_agent import FrontendAgent
from agents.reviewer_agent import ReviewerAgent

from scanners.convention_schema import ConventionSchema
from schemas.feature_plan import FeaturePlan

def create_team(conventions: ConventionSchema, plan: FeaturePlan) -> SelectorGroupChat:
    planner = PlannerAgentNode(conventions, plan)
    database = DatabaseAgent(conventions, plan)
    backend = BackendAgent(conventions, plan)
    frontend = FrontendAgent(conventions, plan)
    
    # Terminate when frontend finishes
    def term_func(msg) -> bool:
        return getattr(msg, "source", None) == "frontend"
        
    from autogen_agentchat.conditions import StopMessageTermination
    # We can just use MaxMessageTermination or a custom termination.
    # Actually, we can just let selector return None to terminate, but autogen-agentchat might require a termination condition.
    max_term = MaxMessageTermination(4) # planner, db, backend, frontend
    termination = max_term
    
    def custom_selector(messages) -> str | None:
        if not messages:
            return "planner"
            
        last_sender = messages[-1].source
        if last_sender == "planner":
            return "database"
        elif last_sender == "database":
            return "backend"
        elif last_sender == "backend":
            return "frontend"
        elif last_sender == "frontend":
            return None # Terminate
            
        return "planner"

    from orchestrator.gemini_client import GeminiClient
    import os
    
    group_client = GeminiClient(
        model_name=os.getenv("MODEL_NAME", "gemini-1.5-flash"),
        api_key=os.getenv("GEMINI_API_KEY")
    )
    
    team = SelectorGroupChat(
        participants=[planner, database, backend, frontend],
        model_client=group_client,
        termination_condition=termination,
        selector_func=custom_selector
    )
    
    return team
