from schemas.scorecard_result import ScorecardResult

class Scorecard:
    @staticmethod
    def generate_scorecard(
        planner_acc: float,
        repair_score: float,
        verification_score: float,
        dependency_acc: float,
        safety_score: float = 1.0
    ) -> ScorecardResult:
        
        total = (
            (planner_acc * 0.25) +
            (repair_score * 0.25) +
            (verification_score * 0.20) +
            (dependency_acc * 0.15) +
            (safety_score * 0.15)
        ) * 100.0

        if total >= 90: grade = "A+"
        elif total >= 80: grade = "A"
        elif total >= 70: grade = "B"
        elif total >= 60: grade = "C"
        else: grade = "F"

        return ScorecardResult(
            planner_score=planner_acc * 100,
            repair_score=repair_score * 100,
            verification_score=verification_score * 100,
            dependency_score=dependency_acc * 100,
            safety_score=safety_score * 100,
            total_score=total,
            grade=grade
        )
