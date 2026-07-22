"""Preflight checks for the Streamlit demo dashboard."""

from __future__ import annotations

import ast
import importlib.util
import py_compile
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "streamlit_app"
PAGES = DASHBOARD / "pages"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(DASHBOARD))

from streamlit_app.utils.dependency_checker import check_dependencies


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def main() -> int:
    page_files = sorted(PAGES.glob("*.py"))
    failures: list[str] = []
    route_names = [page.stem.replace("_", " ").casefold() for page in page_files]
    duplicates = sorted({name for name in route_names if route_names.count(name) > 1})
    if duplicates:
        failures.append(f"duplicate routes: {', '.join(duplicates)}")

    for path in [DASHBOARD / "app.py", DASHBOARD / "utils" / "api_client.py", *page_files]:
        try:
            py_compile.compile(str(path), doraise=True)
            missing = [name for name in imported_roots(path) if importlib.util.find_spec(name) is None]
            if missing:
                failures.append(f"{path.relative_to(ROOT)}: missing imports: {', '.join(sorted(missing))}")
        except (OSError, SyntaxError, py_compile.PyCompileError) as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")

    dependencies = check_dependencies()
    missing_dependencies = [name for name, available in dependencies.items() if not available]
    if missing_dependencies:
        failures.append(f"missing dependencies: {', '.join(missing_dependencies)}")

    print("Dashboard health report")
    print(f"Pages: {len(page_files)}")
    print(f"Duplicate routes: {len(duplicates)}")
    print("Dependencies: " + ", ".join(f"{name}={'ok' if ok else 'missing'}" for name, ok in dependencies.items()))
    if failures:
        print("Status: FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Status: HEALTHY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
