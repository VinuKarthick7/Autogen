"""Static, local repository analysis used by the repository intelligence API."""

from __future__ import annotations

import ast
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any


IGNORED_DIRECTORIES = {
    ".git", ".hg", ".svn", ".idea", ".vscode", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".tox", ".venv", "venv", "env", "node_modules",
    "dist", "build", "coverage", "htmlcov", "archive", "archives", "archived", "legacy",
}
LANGUAGES = {
    ".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript", ".js": "JavaScript",
    ".jsx": "JavaScript", ".go": "Go", ".java": "Java", ".cs": "C#", ".rb": "Ruby",
    ".php": "PHP", ".rs": "Rust", ".swift": "Swift", ".kt": "Kotlin", ".sql": "SQL",
    ".html": "HTML", ".css": "CSS", ".scss": "SCSS", ".vue": "Vue", ".yaml": "YAML",
    ".yml": "YAML", ".json": "JSON", ".toml": "TOML", ".md": "Markdown", ".sh": "Shell",
}
ROUTE_DECORATORS = {"get", "post", "put", "patch", "delete", "websocket"}
SOURCE_LANGUAGES = {"Python", "TypeScript", "JavaScript", "Java", "Go", "C#", "Ruby", "PHP", "Rust", "Swift", "Kotlin", "SQL"}


def _dotted_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _dotted_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return ""


def _is_model(class_node: ast.ClassDef) -> bool:
    base_names = {_dotted_name(base).split(".")[-1] for base in class_node.bases}
    return bool(base_names & {"Base", "DeclarativeBase", "SQLModel", "Model"})


class RepositoryScanner:
    """Analyzes repositories without executing their code.

    Completed scans are held in memory by resolved path. This keeps repeated demo
    scans responsive while allowing callers to request a fresh scan explicitly.
    """

    def __init__(self) -> None:
        self._cache: dict[str, dict[str, Any]] = {}
        self._lock = Lock()

    def analyze(self, repository_path: str, *, force: bool = False) -> dict[str, Any]:
        root = Path(repository_path).expanduser().resolve()
        if not root.exists():
            raise ValueError(f"Repository path does not exist: {root}")
        if not root.is_dir():
            raise ValueError(f"Repository path must be a directory: {root}")

        cache_key = str(root)
        with self._lock:
            if not force and cache_key in self._cache:
                return {**self._cache[cache_key], "cached": True}

        result = self._scan(root)
        with self._lock:
            self._cache[cache_key] = result
        return {**result, "cached": False}

    def _scan(self, root: Path) -> dict[str, Any]:
        languages: Counter[str] = Counter()
        imports: Counter[str] = Counter()
        functions = classes = api_endpoints = database_models = tests = python_modules = todos = 0
        directories = files = import_count = 0
        api_routes: list[dict[str, str]] = []
        models: list[dict[str, str]] = []
        dependency_edges: set[tuple[str, str, str]] = set()
        python_module_names: set[str] = set()
        directory_files: Counter[str] = Counter()
        module_metrics: list[dict[str, int | str]] = []
        started_at = datetime.now(timezone.utc)

        for directory, child_directories, filenames in os.walk(root, topdown=True, followlinks=False):
            child_directories[:] = [name for name in child_directories if name not in IGNORED_DIRECTORIES]
            directories += 1
            directory_path = Path(directory)
            for filename in filenames:
                path = directory_path / filename
                if path.is_symlink() or not path.is_file():
                    continue
                files += 1
                relative_path = path.relative_to(root)
                parent = relative_path.parent.as_posix()
                if parent != ".":
                    directory_files[parent] += 1
                suffix = path.suffix.lower()
                languages[LANGUAGES.get(suffix, suffix.lstrip(".").upper() or "Other")] += 1
                if suffix != ".py":
                    continue
                python_modules += 1
                module_name = str(relative_path.with_suffix("")).replace(os.sep, ".")
                python_module_names.add(module_name)
                source_kind = self._module_kind(path.relative_to(root))
                try:
                    source = path.read_text(encoding="utf-8", errors="ignore")
                    todos += source.lower().count("todo")
                    tree = ast.parse(source, filename=str(path))
                except (OSError, SyntaxError, UnicodeError):
                    continue
                module_functions = module_classes = 0
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        functions += 1
                        module_functions += 1
                        for decorator in node.decorator_list:
                            target = decorator.func if isinstance(decorator, ast.Call) else decorator
                            owner = _dotted_name(target.value).split(".")[-1] if isinstance(target, ast.Attribute) else ""
                            if isinstance(target, ast.Attribute) and target.attr in ROUTE_DECORATORS and (owner in {"app", "router"} or owner.endswith("_router")):
                                api_endpoints += 1
                                method = target.attr.upper().replace("API_ROUTE", "ROUTE")
                                route_path = ""
                                if isinstance(decorator, ast.Call) and decorator.args:
                                    first_argument = decorator.args[0]
                                    if isinstance(first_argument, ast.Constant) and isinstance(first_argument.value, str):
                                        route_path = first_argument.value
                                api_routes.append({"path": route_path or "(dynamic)", "method": method, "function": node.name, "module": module_name})
                    elif isinstance(node, ast.ClassDef):
                        classes += 1
                        module_classes += 1
                        if _is_model(node):
                            database_models += 1
                            models.append({"model": node.name, "module": module_name})
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            import_count += 1
                            dependency = alias.name
                            imports[dependency] += 1
                            dependency_edges.add((module_name, dependency, source_kind))
                    elif isinstance(node, ast.ImportFrom):
                        dependency = node.module or "."
                        import_count += len(node.names)
                        imports[dependency] += len(node.names)
                        dependency_edges.add((module_name, dependency, source_kind))
                if path.name.startswith("test_") or path.name.endswith("_test.py") or "tests" in path.parts:
                    tests += 1
                module_metrics.append({"file": relative_path.as_posix(), "lines": len(source.splitlines()), "functions": module_functions, "classes": module_classes})

        circular_import_details = self._circular_import_details(dependency_edges, python_module_names)
        circular_imports = len(circular_import_details)
        health_score, health_checks = self._health_score(root, tests, python_modules, api_endpoints, todos, circular_imports)
        return {
            "repository_name": root.name,
            "path": str(root),
            "files": files,
            "directories": max(directories - 1, 0),
            "languages": dict(languages.most_common()),
            "source_languages": {name: count for name, count in languages.most_common() if name in SOURCE_LANGUAGES},
            "supporting_files": {name: count for name, count in languages.most_common() if name not in SOURCE_LANGUAGES},
            "python_modules": python_modules,
            "api_endpoints": api_endpoints,
            "database_models": database_models,
            "tests": tests,
            "imports": import_count,
            "symbols": functions + classes,
            "functions": functions,
            "classes": classes,
            "health_score": health_score,
            "health_checks": health_checks,
            "todos": todos,
            "circular_imports": circular_imports,
            "circular_import_details": circular_import_details,
            "imports_by_category": self._categorize_imports(imports, python_module_names),
            "dependency_edges": [{"source": source, "target": target, "source_kind": source_kind} for source, target, source_kind in sorted(dependency_edges)[:100]],
            "directory_file_counts": [{"path": path, "files": count} for path, count in directory_files.most_common(10)],
            "module_metrics": sorted(module_metrics, key=lambda item: (int(item["lines"]), int(item["functions"]), int(item["classes"])), reverse=True)[:15],
            "api_routes": api_routes[:100],
            "models": models[:100],
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "scan_duration_ms": round((datetime.now(timezone.utc) - started_at).total_seconds() * 1000),
        }

    @staticmethod
    def _module_kind(path: Path) -> str:
        parts = {part.lower() for part in path.parts}
        if "archive" in parts or "archived" in parts:
            return "archived"
        if "tests" in parts or path.name.startswith("test_") or path.name.endswith("_test.py"):
            return "tests"
        if "api" in parts or "routes" in parts:
            return "api"
        if "services" in parts or "service" in parts:
            return "services"
        return "project"

    @staticmethod
    def _circular_import_details(edges: set[tuple[str, str, str]], modules: set[str]) -> list[list[str]]:
        graph = {module: set() for module in modules}
        for source, target, _ in edges:
            target_module = target.lstrip(".")
            if target_module in modules:
                graph[source].add(target_module)
        visited: set[str] = set()
        active: set[str] = set()
        cycles: list[list[str]] = []
        seen: set[tuple[str, ...]] = set()
        trail: list[str] = []

        def visit(module: str) -> None:
            visited.add(module)
            active.add(module)
            trail.append(module)
            for target in graph[module]:
                if target in active:
                    cycle = trail[trail.index(target):] + [target]
                    key = tuple(sorted(cycle[:-1]))
                    if key not in seen:
                        seen.add(key)
                        cycles.append(cycle)
                elif target not in visited:
                    visit(target)
            active.remove(module)
            trail.pop()

        for module in graph:
            if module not in visited:
                visit(module)
        return cycles[:10]

    @staticmethod
    def _categorize_imports(imports: Counter[str], modules: set[str]) -> dict[str, list[dict[str, int | str]]]:
        categories: dict[str, Counter[str]] = {"Standard library": Counter(), "Third-party packages": Counter(), "Internal project imports": Counter()}
        roots = {module.split(".")[0] for module in modules}
        stdlib = sys.stdlib_module_names
        for module, occurrences in imports.items():
            root = module.lstrip(".").split(".")[0]
            if module.startswith(".") or root in roots:
                category = "Internal project imports"
            elif root in stdlib:
                category = "Standard library"
            else:
                category = "Third-party packages"
            categories[category][module] += occurrences
        return {name: [{"module": module, "occurrences": count} for module, count in values.most_common(12)] for name, values in categories.items()}

    @staticmethod
    def _health_score(root: Path, tests: int, python_modules: int, api_endpoints: int, todos: int, circular_imports: int) -> tuple[int, list[dict[str, object]]]:
        readmes = [root / name for name in ("README.md", "README.rst", "README.txt")]
        readme_quality = any(path.exists() and path.stat().st_size >= 200 for path in readmes)
        package_config = any((root / name).exists() for name in ("pyproject.toml", "requirements.txt", "Pipfile", "package.json", "go.mod"))
        ci_config = (root / ".github" / "workflows").is_dir() or (root / ".gitlab-ci.yml").exists() or (root / "azure-pipelines.yml").exists()
        documentation = (root / "docs").is_dir() or sum(1 for path in root.glob("*.md") if path.stat().st_size >= 200) >= 2
        test_density = tests / python_modules if python_modules else 0
        score = 20 + (15 if readme_quality else 0) + (15 if package_config else 0) + (12 if tests else 0) + (10 if api_endpoints else 0) + (15 if ci_config else 0) + (10 if documentation else 0) + (10 if test_density >= 0.10 else 5 if test_density >= 0.03 else 0)
        score -= min(circular_imports * 6, 24)
        score -= min(max(todos - 10, 0), 20)
        checks = [
            {"Signal": "Meaningful README", "Status": "Pass" if readme_quality else "Missing", "Weight": 15},
            {"Signal": "Dependency configuration", "Status": "Pass" if package_config else "Missing", "Weight": 15},
            {"Signal": "Test files", "Status": "Pass" if tests else "Missing", "Weight": 12},
            {"Signal": "CI configuration", "Status": "Pass" if ci_config else "Missing", "Weight": 15},
            {"Signal": "Documentation", "Status": "Pass" if documentation else "Missing", "Weight": 10},
            {"Signal": "Circular imports", "Status": f"{circular_imports} detected", "Weight": -min(circular_imports * 6, 24)},
            {"Signal": "TODO markers", "Status": f"{todos} detected", "Weight": -min(max(todos - 10, 0), 20)},
        ]
        return max(min(score, 100), 0), checks


repository_scanner = RepositoryScanner()
