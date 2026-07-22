"""Realistic, deterministic fallback data for the engineering cockpit demo."""

from __future__ import annotations

import pandas as pd


ACCENT = "#7C3AED"
TEAL = "#14B8A6"
AMBER = "#F59E0B"
ROSE = "#F43F5E"
BLUE = "#38BDF8"


def dashboard() -> dict:
    return {
        "metrics": {"repositories": 24, "features": 186, "pass_rate": 96.8, "security": 92, "health": 99.95},
        "delivery": pd.DataFrame({"Week": ["Jun 24", "Jul 01", "Jul 08", "Jul 15", "This week"], "Features": [24, 31, 37, 42, 52], "Tests": [91, 93, 94, 96, 97]}),
        "activity": pd.DataFrame([
            {"Time": "09:42", "Event": "Release candidate verified", "Detail": "payments-api · 312 checks passed", "Status": "Complete"},
            {"Time": "09:18", "Event": "Convention extracted", "Detail": "web-console · 14 reusable patterns", "Status": "Indexed"},
            {"Time": "08:56", "Event": "Security review completed", "Detail": "auth-service · score improved to 94", "Status": "Secure"},
            {"Time": "08:31", "Event": "Planner created implementation plan", "Detail": "mobile-sdk · 8 tasks ready", "Status": "In progress"},
        ]),
        "repositories": pd.DataFrame({"Repository": ["payments-api", "web-console", "auth-service", "mobile-sdk"], "Health": [98, 96, 94, 91], "Change risk": ["Low", "Low", "Medium", "Medium"]}),
    }


def repository_intelligence() -> dict:
    return {
        "stats": {"repositories": 24, "files": 18_426, "symbols": 76_318, "coverage": 87.4},
        "graph": {"nodes": 76_318, "edges": 188_942, "communities": 41, "hotspots": 7},
        "languages": pd.DataFrame({"Language": ["TypeScript", "Python", "Go", "SQL", "Other"], "Files": [7_226, 4_931, 2_450, 1_148, 2_671]}),
        "conventions": pd.DataFrame([
            {"Convention": "API error envelope", "Confidence": 98, "Occurrences": 184, "Impact": "High"},
            {"Convention": "Feature flag guard", "Confidence": 95, "Occurrences": 112, "Impact": "High"},
            {"Convention": "Structured logging", "Confidence": 93, "Occurrences": 329, "Impact": "Medium"},
            {"Convention": "Repository test fixture", "Confidence": 89, "Occurrences": 78, "Impact": "Medium"},
        ]),
        "planner": pd.DataFrame([
            {"Plan": "Payments reconciliation", "Readiness": 96, "Tasks": 12, "Status": "Ready"},
            {"Plan": "Account recovery flow", "Readiness": 88, "Tasks": 9, "Status": "Review"},
            {"Plan": "Usage analytics export", "Readiness": 74, "Tasks": 7, "Status": "Mapping"},
        ]),
    }


def observability() -> dict:
    return {
        "metrics": {"cpu": 42, "memory": 68, "incidents": 2, "sla": 99.94, "error_rate": 0.18},
        "runtime": pd.DataFrame({"Time": ["09:00", "09:10", "09:20", "09:30", "09:40", "09:50", "10:00"], "CPU": [34, 38, 51, 46, 42, 39, 42], "Memory": [61, 63, 66, 67, 68, 67, 68], "Requests / min": [820, 936, 1180, 1094, 1016, 978, 1052]}),
        "deployments": pd.DataFrame([
            {"Service": "payments-api", "Version": "v2.14.0", "Environment": "Production", "Status": "Healthy", "Deployed": "34 min ago"},
            {"Service": "web-console", "Version": "v1.42.3", "Environment": "Production", "Status": "Healthy", "Deployed": "2 hr ago"},
            {"Service": "event-worker", "Version": "v3.7.1", "Environment": "Staging", "Status": "Monitoring", "Deployed": "18 min ago"},
        ]),
        "incidents": pd.DataFrame([
            {"Incident": "Elevated queue latency", "Severity": "Medium", "Owner": "Platform", "Status": "Mitigating"},
            {"Incident": "Webhook retries above baseline", "Severity": "Low", "Owner": "Integrations", "Status": "Investigating"},
        ]),
    }


def organization() -> dict:
    return {
        "metrics": {"sprint": 72, "velocity": 48, "burnout": 23, "headcount": 38},
        "teams": pd.DataFrame([
            {"Team": "Platform", "Lead": "Maya Chen", "Members": 9, "Focus": "Runtime reliability", "Health": "Strong"},
            {"Team": "Product Engineering", "Lead": "Ethan Cole", "Members": 14, "Focus": "Customer workflows", "Health": "Strong"},
            {"Team": "Data & Intelligence", "Lead": "Priya Shah", "Members": 8, "Focus": "Knowledge systems", "Health": "Watch"},
            {"Team": "Experience", "Lead": "Leo Martin", "Members": 7, "Focus": "Console and SDK", "Health": "Strong"},
        ]),
        "velocity_trend": pd.DataFrame({"Sprint": ["S19", "S20", "S21", "S22", "S23", "S24"], "Completed points": [39, 42, 44, 46, 43, 48], "Committed points": [44, 45, 46, 48, 47, 50]}),
        "hiring": pd.DataFrame([
            {"Role": "Senior SRE", "Why now": "Queue and deployment ownership exceeds capacity", "Priority": "High"},
            {"Role": "Staff Data Engineer", "Why now": "Knowledge graph roadmap is constrained", "Priority": "High"},
            {"Role": "Product Designer", "Why now": "Console discovery work begins next quarter", "Priority": "Planned"},
        ]),
    }


def laboratory() -> dict:
    return {
        "metrics": {"experiments": 12, "strategies": 8, "best_score": 94.6, "confidence": 91},
        "benchmarks": pd.DataFrame({"Strategy": ["Graph-guided repair", "Test-first planner", "Baseline agent", "Rule-based repair"], "Code quality": [94.6, 90.8, 82.4, 76.9], "Latency": [84, 88, 96, 72]}),
        "experiments": pd.DataFrame([
            {"Experiment": "Context-window routing", "Owner": "Nadia", "Progress": 85, "Result": "+11% task success", "Status": "Validating"},
            {"Experiment": "Semantic test selection", "Owner": "Owen", "Progress": 100, "Result": "-34% test time", "Status": "Promote"},
            {"Experiment": "Recovery policy v2", "Owner": "Iris", "Progress": 62, "Result": "Early signal positive", "Status": "Running"},
        ]),
        "recommendations": [
            ("Promote semantic test selection", "It reduced validation time by 34% while preserving a 98.1% defect catch rate."),
            ("Expand graph-guided repair", "It leads all strategies on quality and remains within the interactive latency budget."),
            ("Instrument recovery policy v2", "Current confidence is promising, but failure taxonomy needs one more experiment cycle."),
        ],
    }
