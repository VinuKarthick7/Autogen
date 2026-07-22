class UsageMeter:
    def record_run(self, org_id: str):
        # MOCKED: increment run count in DB/Redis
        pass
        
    def record_tokens(self, org_id: str, tokens: int):
        pass
