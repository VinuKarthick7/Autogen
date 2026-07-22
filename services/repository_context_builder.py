"""Build a compact, evidence-only scanner context for repository review agents."""

from __future__ import annotations

from collections import Counter
from typing import Any


LAYER_NAMES = ("routes", "services", "repositories", "models", "schemas", "utils")


class RepositoryContextBuilder:
    """Converts one scanner result into a capped context of fewer than ~1200 tokens."""

    def build(self, result: dict[str, Any]) -> dict[str, Any]:
        imports = result.get("imports_by_category", {})
        architecture = self._architecture(result, imports)
        return {
            "repository": {"name": result["repository_name"], "path": result["path"], "tech_stack": self._tech_stack(imports), "languages": list(result.get("source_languages", {}))[:12], "health_score": result["health_score"]},
            "structure": {"total_files": result["files"], "api_routes": result["api_endpoints"], "database_models": result["database_models"]},
            "quality": {"test_files": result["tests"], "todo_count": result.get("todos", 0), "documentation_score": self._documentation_score(result), "circular_imports": result.get("circular_import_details", []), "circular_import_count": result.get("circular_imports", 0)},
            "dependencies": {"internal_imports": imports.get("Internal project imports", [])[:12], "external_imports": imports.get("Third-party packages", [])[:8]},
            "architecture": architecture,
        }

    def _architecture(self, result: dict[str, Any], imports: dict[str, Any]) -> dict[str, Any]:
        edges = result.get("dependency_edges", [])[:100]
        fan_in: Counter[str] = Counter(edge["target"] for edge in edges)
        fan_out: Counter[str] = Counter(edge["source"] for edge in edges)
        internal_names = {str(item["module"]).lstrip(".") for item in imports.get("Internal project imports", [])}
        hotspot_names = {name for name in (set(fan_in) | set(fan_out)) if name in fan_out or name.lstrip(".") in internal_names}
        hotspots = [{"module": name, "fan_in": fan_in[name], "fan_out": fan_out[name]} for name in hotspot_names if fan_in[name] or fan_out[name]]
        hotspots.sort(key=lambda item: (item["fan_in"] + item["fan_out"], item["fan_in"]), reverse=True)
        api_groups: Counter[str] = Counter()
        for route in result.get("api_routes", [])[:100]:
            path = route.get("path", "")
            if path.startswith("/"):
                parts = path.split("/")
                api_groups["/" + parts[1] if len(parts) > 1 and parts[1] else "/"] += 1
        layer_counts: Counter[str] = Counter()
        for module in result.get("module_metrics", []):
            parts = set(str(module["file"]).lower().split("/"))
            for layer in LAYER_NAMES:
                if layer in parts or layer.rstrip("s") in parts:
                    layer_counts[layer] += 1
        return {
            "largest_directories": result.get("directory_file_counts", [])[:10],
            "largest_modules": result.get("module_metrics", [])[:15],
            "most_imported_modules": imports.get("Internal project imports", [])[:15],
            "dependency_hotspots": hotspots[:10],
            "api_groups": [{"prefix": prefix, "routes": count} for prefix, count in api_groups.most_common(10)],
            "service_boundaries": [{"layer": layer, "files": count} for layer, count in layer_counts.most_common()],
            "circular_imports": result.get("circular_import_details", [])[:10],
            "internal_import_count": sum(int(item["occurrences"]) for item in imports.get("Internal project imports", [])),
            "route_to_module_ratio": round(result["api_endpoints"] / max(result["python_modules"], 1), 2),
        }

    @staticmethod
    def _tech_stack(imports: dict[str, Any]) -> list[str]:
        packages = [item["module"].split(".")[0] for item in imports.get("Third-party packages", [])]
        return list(dict.fromkeys(packages))[:12]

    @staticmethod
    def _documentation_score(result: dict[str, Any]) -> int:
        checks = {item["Signal"]: item["Status"] for item in result.get("health_checks", [])}
        return 100 if checks.get("Documentation") == "Pass" and checks.get("Meaningful README") == "Pass" else 50 if checks.get("Meaningful README") == "Pass" else 0
