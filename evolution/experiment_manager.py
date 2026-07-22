class ExperimentManager:
    def get_experiments(self):
        # mock experiments list
        return [
            {
                "experiment_id": "exp-001",
                "name": "Planner V12 vs V13",
                "control_variant": "v12",
                "treatment_variant": "v13",
                "metric": "benchmark_score",
                "status": "running"
            }
        ]
