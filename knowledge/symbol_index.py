import os
import ast
from typing import List
from schemas.symbol import Symbol

class SymbolIndex:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.symbols: List[Symbol] = []

    def build_index(self):
        self.symbols = []
        for root, _, files in os.walk(self.repo_path):
            if '.git' in root or '__pycache__' in root or '.pytest_cache' in root:
                continue
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self._parse_file(file_path)

    def _parse_file(self, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            tree = ast.parse(content)
        except Exception:
            return

        rel_path = os.path.relpath(file_path, self.repo_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                sym_type = "class"
                if "Router" in node.name or "router" in node.name.lower():
                    sym_type = "router"
                elif "Model" in node.name or "Entity" in node.name:
                    sym_type = "model"
                elif "Service" in node.name:
                    sym_type = "service"
                elif "Schema" in node.name:
                    sym_type = "schema"
                self.symbols.append(Symbol(name=node.name, type=sym_type, file_path=rel_path))
            elif isinstance(node, ast.FunctionDef):
                if node.name.startswith('_'):
                    continue
                # simplistic: if the function is a top-level function in a router file
                sym_type = "function"
                if "router" in rel_path.lower():
                    sym_type = "router"
                self.symbols.append(Symbol(name=node.name, type=sym_type, file_path=rel_path))

    def get_symbol(self, name: str) -> Symbol:
        for sym in self.symbols:
            if sym.name == name:
                return sym
        return None
