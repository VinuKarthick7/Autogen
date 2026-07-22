import os
import json
from schemas.symbol import Symbol

class GlobalSymbolIndex:
    def __init__(self, index_file="knowledge/symbols/global_index.json"):
        self.index_file = index_file
        os.makedirs(os.path.dirname(self.index_file), exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(self.index_file):
            with open(self.index_file, "r") as f:
                self.index = json.load(f)
        else:
            self.index = []

    def _save(self):
        with open(self.index_file, "w") as f:
            json.dump(self.index, f, indent=4)

    def index_repository(self, repo_id: str, symbols: list[dict]):
        # Remove old symbols for this repo
        self.index = [s for s in self.index if s.get("repository") != repo_id]
        # Add new symbols
        for sym in symbols:
            sym["repository"] = repo_id
            self.index.append(sym)
        self._save()

    def find_symbol(self, repo_id: str, symbol_name: str):
        for s in self.index:
            if s.get("repository") == repo_id and s.get("symbol") == symbol_name:
                return s
        return None

    def search(self, query: str) -> list[dict]:
        results = []
        q = query.lower()
        for s in self.index:
            if q in str(s.get("symbol", "")).lower():
                results.append(s)
        return results

    def find_related_symbols(self, query: str) -> list[dict]:
        # For now just use search
        return self.search(query)
