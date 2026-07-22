import os
from schemas.evaluation_report import EvaluationReport

class ReportGenerator:
    @staticmethod
    def generate_report(report: EvaluationReport, out_dir: str):
        os.makedirs(out_dir, exist_ok=True)
        md_content = f"""# Benchmark Evaluation Report

## Summary
- **Total Runs**: {report.total_runs}
- **Passed**: {report.passed_runs}
- **Failed**: {report.failed_runs}
- **Average Score**: {report.average_score:.2f}

## Efficiency
- **Average Tokens**: {report.average_tokens:.0f}
- **Average Cost**: ${report.average_cost:.4f}
- **Average Repair Depth**: {report.average_repair_depth:.2f}

## Results Breakdown
"""
        for r in report.benchmark_results:
            md_content += f"- **{r.benchmark_id}**: {'✅ Passed' if r.passed else '❌ Failed'} (Cost: ${r.estimated_cost_usd:.4f})\n"

        md_path = os.path.join(out_dir, "benchmark_report.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # Simple HTML
        html_path = os.path.join(out_dir, "benchmark_report.html")
        import markdown
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(f"<html><body>{markdown.markdown(md_content)}</body></html>")
