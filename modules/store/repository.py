"""Repositorio de apps: carga y filtra desde apps.json."""
import json
import os
from typing import List, Optional
from .models import App


class StoreRepository:
    def __init__(self, json_path: str):
        self.json_path = json_path
        self.apps: List[App] = []
        self.categories: List[str] = []
        self.load()

    def load(self):
        if not os.path.exists(self.json_path):
            print(f"[StoreRepo] No existe: {self.json_path}")
            self.apps = []
            self.categories = []
            return
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.apps = [App.from_dict(d) for d in data.get("apps", [])]
        cats = sorted({a.category for a in self.apps})
        self.categories = ["Todas"] + cats
        print(f"[StoreRepo] {len(self.apps)} apps cargadas, {len(cats)} categorias")

    def all(self) -> List[App]:
        return self.apps

    def by_id(self, app_id: str) -> Optional[App]:
        for a in self.apps:
            if a.id == app_id:
                return a
        return None

    def filter(self, category: str = "Todas", query: str = "") -> List[App]:
        q = query.strip().lower()
        result = []
        for a in self.apps:
            if category != "Todas" and a.category != category:
                continue
            if q:
                haystack = f"{a.name} {a.short_desc} {a.category}".lower()
                if q not in haystack:
                    continue
            result.append(a)
        return result
