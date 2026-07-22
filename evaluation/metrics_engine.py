from typing import List

class MetricsEngine:
    @staticmethod
    def compute_planner_accuracy(expected_files: List[str], generated_files: List[str]) -> float:
        if not expected_files and not generated_files:
            return 1.0
        if not expected_files or not generated_files:
            return 0.0
            
        expected = set(expected_files)
        generated = set(generated_files)
        intersection = expected.intersection(generated)
        union = expected.union(generated)
        
        return len(intersection) / len(union)

    @staticmethod
    def compute_dependency_accuracy(expected_deps: List[str], generated_deps: List[str]) -> float:
        return MetricsEngine.compute_planner_accuracy(expected_deps, generated_deps)

    @staticmethod
    def compute_repair_score(repair_attempts: int, repair_success: bool, max_depth: int) -> float:
        if repair_attempts == 0 and repair_success:
            return 1.0 # No repairs needed = perfect
        if not repair_success:
            return 0.0
        # If success, penalize based on attempts vs max depth
        # 1 attempt = high score, close to max_depth = low score
        if max_depth == 0: 
            return 0.0
        penalty = repair_attempts / (max_depth + 1)
        return max(0.0, 1.0 - penalty)

    @staticmethod
    def compute_verification_score(passed: bool, lint_passed: bool, tests_passed: bool) -> float:
        score = 0.0
        if passed:
            score += 0.5
        if lint_passed:
            score += 0.25
        if tests_passed:
            score += 0.25
        return score
