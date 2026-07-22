class RepairHistory:
    def __init__(self):
        self.repair_count = 0
        self.repair_depth = 0

    def increment_count(self):
        self.repair_count += 1
        
    def increment_depth(self):
        self.repair_depth += 1
        
    def can_repair(self, max_attempts: int = 3, max_depth: int = 2) -> bool:
        return self.repair_count < max_attempts and self.repair_depth < max_depth
