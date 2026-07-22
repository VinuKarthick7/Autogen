from core_platform.billing.subscriptions import SubscriptionService

class QuotaService:
    def __init__(self):
        self.sub_svc = SubscriptionService()
        self.usage = {"org_1": 15}

    def check_quota(self, org_id: str, plan_name: str) -> bool:
        plan = self.sub_svc.get_plan(plan_name)
        current = self.usage.get(org_id, 0)
        return current < plan["runs"]
