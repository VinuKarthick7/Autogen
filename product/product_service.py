class ProductService:
    def generate_context(self, prd_content: str) -> dict:
        # returns product context for the planner
        return {
            "prd": prd_content,
            "epics": [],
            "roadmaps": []
        }
