from datetime import datetime

class AuditLogger:
    def log_event(self, org_id: str, user_id: str, action: str, details: dict):
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "org_id": org_id,
            "user_id": user_id,
            "action": action,
            "details": details
        }
        # MOCKED: Write to DB or audit log stream
        print(f"[AUDIT] {event}")
