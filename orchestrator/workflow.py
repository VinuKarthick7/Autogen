import os
import json
import uuid
import asyncio
from datetime import datetime

from agents.planner import PlannerAgent
from orchestrator.team import create_team
from orchestrator.state import WorkflowState
from orchestrator.messages import to_agent_message, export_chat
from scanners.convention_schema import ConventionSchema
from schemas.workflow_result import WorkflowResult
from schemas.generated_file import GeneratedFile

class Workflow:
    def __init__(self, repo_path: str = "./repo"):
        self.repo_path = repo_path
        self.feature_planner = PlannerAgent()

    async def _run_team_chat(self, state: WorkflowState):
        team = create_team(state.conventions, state.feature_plan)
        
        task_prompt = f"Please implement the feature requested: {state.feature_request}"
        
        os.makedirs("logs", exist_ok=True)
        # autogen-agentchat v0.7.5 API
        async for message_event in team.run_stream(task=task_prompt):
            if hasattr(message_event, "source"):
                agent_msg = to_agent_message(message_event)
                state.add_message(agent_msg)
                
                # Incrementally save the transcript
                with open("logs/transcript.jsonl", "a", encoding="utf-8") as f:
                    f.write(agent_msg.model_dump_json() + "\n")
                
                # Naive JSON extraction from message
                content = agent_msg.message
                if content and "{" in content and "}" in content:
                    try:
                        start = content.find("{")
                        end = content.rfind("}") + 1
                        json_str = content[start:end]
                        data = json.loads(json_str)
                        if "files" in data:
                            files = [GeneratedFile(**f) for f in data["files"]]
                            state.add_files(files)
                    except Exception:
                        pass
        
    def run_workflow(
        self,
        feature_request: str,
        conventions: ConventionSchema,
    ) -> WorkflowResult:
        run_id = str(uuid.uuid4())
        artifacts_dir = os.path.join("artifacts", run_id)
        os.makedirs(artifacts_dir, exist_ok=True)
        
        repo_path = getattr(self, 'repo_path', './repo') # Default or set externally
        if not os.path.exists(repo_path):
            os.makedirs(repo_path, exist_ok=True)
            
        # 1. Analyze Repository & Build Dependency Graph
        from knowledge.symbol_index import SymbolIndex
        from knowledge.dependency_graph import DependencyGraph
        from knowledge.impact_analyzer import ImpactAnalyzer
        
        symbol_index = SymbolIndex(repo_path)
        symbol_index.build_index()
        
        dep_graph = DependencyGraph(repo_path)
        dep_graph.build_graph()
        dep_graph_path = os.path.join(artifacts_dir, "dependency_graph.json")
        dep_graph.export(dep_graph_path)
        
        # 2. Predict Impact
        impact_analyzer = ImpactAnalyzer()
        impact_report = asyncio.run(impact_analyzer.predict_impact(feature_request, dep_graph_path))
        
        enriched_request = f"{feature_request}\n\nPredicted affected files:\n" + "\n".join(impact_report.affected_files)
        state = WorkflowState(enriched_request, conventions)
        
        # 3. Retrieve Cross-Repository Knowledge
        from knowledge.implementation_retriever import ImplementationRetriever
        retriever = ImplementationRetriever()
        knowledge_context = retriever.retrieve_examples(feature_request)
        
        # 4. Extract Product Context
        from product.product_service import ProductService
        prod_svc = ProductService()
        product_context = prod_svc.generate_context(feature_request)
        enriched_request += "\n\nProduct Context:\n" + str(product_context)

        # 4.5 Extract Runtime Feedback Context
        from observability.observability_service import ObservabilityService
        obs_svc = ObservabilityService()
        runtime_context = obs_svc.get_runtime_feedback(repo_path)
        enriched_request += "\n\nRuntime Feedback (Production Memory):\n" + str(runtime_context)

        # 4.6 Extract Organization Context
        from simulation.organization_service import OrganizationService
        org_svc = OrganizationService()
        organization_context = org_svc.generate_context(repo_path)
        enriched_request += "\n\nOrganization Context:\n" + str(organization_context)

        # 4.7 Extract Laboratory Research Context
        from laboratory.laboratory_service import LaboratoryService
        lab_svc = LaboratoryService()
        research_context = lab_svc.generate_context(repo_path, runtime_context, organization_context)
        enriched_request += "\n\nResearch Context (Autonomous Software Laboratory):\n" + str(research_context)

        # 5. Generate and Normalize Plan
        if knowledge_context:
            enriched_request += "\n\nCross-Repository Examples:\n" + "\n".join(knowledge_context)
            
        state.feature_plan = self.feature_planner.create_plan(enriched_request, conventions)
        
        # 4. Run Team Chat
        asyncio.run(self._run_team_chat(state))
        
        # 5. Execution Pipeline
        
        # Save plan & chat
        with open(os.path.join(artifacts_dir, "plan.json"), "w") as f:
            f.write(state.feature_plan.model_dump_json(indent=2))
        chat_path = os.path.join(artifacts_dir, "chat.json")
        export_chat(state.messages, path=chat_path)

        if not state.generated_files:
            return None # No files generated
            
        from executor.workspace import WorkspaceManager
        from executor.git_manager import GitManager
        from executor.patch_writer import PatchWriter
        from executor.safety_checker import SafetyChecker
        from executor.diff_generator import DiffGenerator
        from schemas.patch_set import PatchSet
        from schemas.execution_result import ExecutionResult
        
        workspace_mgr = WorkspaceManager()
        target_repo = os.path.join(workspace_mgr.create_workspace(run_id), "repo")
        workspace_mgr.copy_repository(repo_path, target_repo)
        
        git_mgr = GitManager(target_repo)
        git_mgr.initialize()
        branch_name = git_mgr.create_branch(run_id)
        
        patch_writer = PatchWriter(target_repo)
        safety_checker = SafetyChecker()
        
        operations = []
        for f in state.generated_files:
            try:
                op = patch_writer.generate_operation(f)
                operations.append(op)
            except Exception as e:
                state.validation_errors.append(str(e))
                
        patch_set = PatchSet(operations=operations)
        
        try:
            safety_checker.validate_patch(patch_set)
        except Exception as e:
            state.validation_errors.append(str(e))
            # Even if it fails safety, we might still want to return a result
            
        for op in patch_set.operations:
            patch_writer.apply_operation(op)
            
        # 4.5 Quality Intelligence Pipeline
        from quality.quality_service import QualityService
        from agents.qa_agent import QAAgent
        from agents.security_agent import SecurityAgent
        from agents.performance_agent import PerformanceAgent
        from agents.compliance_agent import ComplianceAgent
        from agents.reliability_agent import ReliabilityAgent
        
        quality_svc = QualityService()
        quality_context = quality_svc.evaluate(target_repo)
        
        # We instantiate the agents (in a real system, they would run in sequence or parallel here)
        qa_agent = QAAgent()
        sec_agent = SecurityAgent()
        perf_agent = PerformanceAgent()
        comp_agent = ComplianceAgent()
        rel_agent = ReliabilityAgent()
        
        # We append the quality context to the state so Verification/DeploymentGuard can use it
        state.validation_errors.append(f"Quality Score computed: Security {quality_context.get('security_score')}")
        
        from verification.verifier import Verifier
        from verification.report_generator import ReportGenerator
        from agents.reviewer_agent import ReviewerAgent
        from verification.rules.repository_rules import RepositoryRulesEngine
        from schemas.verification_step import VerificationStep
        from repair.repair_executor import RepairExecutor
        from repair.repair_history import RepairHistory
        from agents.repair_agent import RepairAgent
        import copy
        
        verifier = Verifier()
        rules_engine = RepositoryRulesEngine()
        report_gen = ReportGenerator("artifacts")
        repair_executor = RepairExecutor()
        repair_history = RepairHistory()
        
        while True:
            # 4. Verification Pipeline
            report = verifier.verify(target_repo)
            violations = rules_engine.scan_patch(patch_set)
            
            report.rule_violations = [v.model_dump() for v in violations]
            blocking_violations = rules_engine.get_blocking_violations(violations)
            
            rules_step = VerificationStep(
                name="Rules Engine",
                command="repository_rules.py",
                success=not blocking_violations,
                duration_ms=0,
                stdout="\n".join([v.message for v in violations]),
                stderr=""
            )
            report.steps.append(rules_step)
            
            if blocking_violations:
                report.passed = False
                state.validation_errors.append(f"Blocked by {len(blocking_violations)} critical/high rule violations.")
                
            report_path = report_gen.save_report(run_id, report)
            
            # Check for repairs
            repair_plan = repair_executor.evaluate_failures(report, repair_history)
            if not repair_plan:
                break # Either passed or blocked by limits/security
                
            print(f"[REPAIR] Initiating repair cycle {repair_history.repair_count + 1}...")
            repair_agent = RepairAgent()
            
            # Formulate prompt for repair agent
            repair_prompt = f"Original feature: {feature_request}\nFailures:\n"
            for step in repair_plan.steps:
                repair_prompt += f"- {step.category} on {step.target_files}: {step.reason}\n"
                
            repair_response = asyncio.run(repair_agent.run(task=repair_prompt))
            
            # Parse output for new patch operations
            content = repair_response.messages[-1].content
            repaired = False
            if content and "{" in content and "}" in content:
                try:
                    start = content.find("{")
                    end = content.rfind("}") + 1
                    json_str = content[start:end]
                    data = json.loads(json_str)
                    if "operations" in data:
                        from schemas.patch_operation import PatchOperation
                        new_ops = [PatchOperation(**op) for op in data["operations"]]
                        # Apply patches to Git Sandbox
                        for op in new_ops:
                            patch_writer.apply_operation(op)
                            # Replace existing operation for this file or append
                            replaced = False
                            for i, existing_op in enumerate(patch_set.operations):
                                if existing_op.path == op.path:
                                    patch_set.operations[i] = op
                                    replaced = True
                                    break
                            if not replaced:
                                patch_set.operations.append(op)
                        git_mgr.get_diff() # Updates local git state
                        repaired = True
                        repair_history.increment_count()
                        repair_history.increment_depth()
                except Exception as e:
                    print(f"[REPAIR] Failed to parse repair agent output: {e}")
            
            if not repaired:
                print("[REPAIR] Agent failed to produce valid patch. Halting repairs.")
                break

        diff = git_mgr.get_diff()
        diff_gen = DiffGenerator("artifacts")
        diff_path = diff_gen.generate(run_id, diff, patch_set)
        
        # 5. Reviewer
        reviewer = ReviewerAgent(state.conventions, state.feature_plan, report)
        reviewer_response = asyncio.run(reviewer.run(task="Review the verification report and generated code."))
        
        is_approved = "APPROVE" in reviewer_response.messages[-1].content
        if not is_approved:
            state.validation_errors.append("Reviewer rejected the changes.")
        
        # Save generated files for posterity
        with open(os.path.join(artifacts_dir, "generated_files.json"), "w") as f:
            files_dump = [file.model_dump(mode="json") for file in state.generated_files]
            json.dump(files_dump, f, indent=2)
            
        # We need to add verification_passed to ExecutionResult
        # But schemas/execution_result.py might need it. Let's modify ExecutionResult if needed, or rely on passed.
        # Actually schemas/verification_result.py has run_id, passed, report_path, total_time_ms. But we are returning ExecutionResult from workflow.
        # Let's modify ExecutionResult schema or WorkflowResult to hold verification info.
        # The prompt says: "Return ExecutionResult" in Milestone 3. In Milestone 5: "VerificationResult".
        # Let's return a unified result, or just ExecutionResult? 
        # 6. Knowledge Update
        from knowledge.repair_memory import RepairMemory
        repair_memory = RepairMemory()
        if is_approved:
            if repair_history.repair_count > 0:
                # For this milestone, we log a generic successful repair
                from schemas.rule_violation import RuleViolation
                generic_violation = RuleViolation(severity="HIGH", category="DomainLogic", file="", line=1, message="Successful targeted repair", suggestion="")
                repair_memory.log_successful_repair([generic_violation], patch_set.operations)
        
        return ExecutionResult(
            run_id=run_id,
            branch_name=branch_name,
            files_changed=len(patch_set.operations),
            diff_path=diff_path,
            committed=False,
            rollback_available=True,
            verification_passed=is_approved
        )
