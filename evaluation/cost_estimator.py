class CostEstimator:
    # Approximate pricing per 1M tokens (Input/Output average for simplicity)
    # USD Pricing
    PRICING = {
        "gemini-1.5-flash": 0.50, # Blended assumption
        "gemini-1.5-pro": 3.50,
        "gpt-4o": 10.0,
        "claude-3-5-sonnet": 3.0
    }

    @staticmethod
    def estimate_cost(tokens_used: int, model_name: str = "gemini-1.5-flash") -> float:
        rate_per_million = CostEstimator.PRICING.get(model_name, 0.50)
        return (tokens_used / 1_000_000) * rate_per_million

    @staticmethod
    def estimate_monthly_cost(avg_tokens_per_run: int, runs_per_month: int, model_name: str = "gemini-1.5-flash") -> float:
        return CostEstimator.estimate_cost(avg_tokens_per_run * runs_per_month, model_name)
