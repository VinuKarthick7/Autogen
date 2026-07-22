PLANS = {
    "Free": {"runs": 100, "price": 0},
    "Pro": {"runs": 2000, "price": 499},
    "Enterprise": {"runs": float('inf'), "price": 5000}
}

class SubscriptionService:
    def get_plan(self, plan_name: str):
        return PLANS.get(plan_name, PLANS["Free"])
